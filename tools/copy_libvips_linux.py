#!/usr/bin/env python3
"""
Copy libvips dynamic libraries from Homebrew installation on Linux.

This script extracts libvips and its dependencies from Homebrew (Linuxbrew),
copies them to an output directory, and fixes the library paths
for redistribution.

Usage:
    python3 copy_libvips_linux.py --output /path/to/output
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging for GitHub Actions output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def run_command(cmd: list[str], capture_output: bool = True, env=None) -> subprocess.CompletedProcess:
    """Run a command and log it."""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True, env=env)
    if result.returncode != 0:
        logger.error(f"Command failed with code {result.returncode}")
        if result.stderr:
            logger.error(f"stderr: {result.stderr}")
    return result


def get_homebrew_prefix() -> Path:
    """Get the Homebrew prefix path."""
    result = run_command(["brew", "--prefix"])
    if result.returncode != 0:
        raise RuntimeError("Failed to get Homebrew prefix")
    return Path(result.stdout.strip())


def get_package_prefix(package: str) -> Path:
    """Get the prefix path for a specific Homebrew package."""
    result = run_command(["brew", "--prefix", package])
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get prefix for {package}")
    return Path(result.stdout.strip())


def get_package_version(package: str) -> str:
    """Get the version of a Homebrew package."""
    result = run_command(["brew", "info", "--json=v2", package])
    if result.returncode != 0:
        return "unknown"
    import json
    try:
        data = json.loads(result.stdout)
        if data.get("formulae"):
            return data["formulae"][0].get("versions", {}).get("stable", "unknown")
    except (json.JSONDecodeError, KeyError, IndexError):
        pass
    return "unknown"


def get_so_deps(so_path: Path) -> list[str]:
    """Get the list of shared library dependencies using ldd or readelf."""
    # Try ldd first
    result = run_command(["ldd", str(so_path)])
    if result.returncode == 0:
        deps = []
        for line in result.stdout.splitlines():
            line = line.strip()
            # Format: libname.so => /path/to/lib (0x...)
            if "=>" in line:
                parts = line.split("=>")
                if len(parts) >= 2:
                    path = parts[1].strip().split()[0]
                    if path and path != "not" and not path.startswith("("):
                        deps.append(path)
            # Format: /path/to/lib (0x...) - for ld-linux
            elif line.startswith("/"):
                path = line.split()[0]
                deps.append(path)
        return deps
    
    # Fallback to readelf
    result = run_command(["readelf", "-d", str(so_path)])
    if result.returncode == 0:
        deps = []
        for line in result.stdout.splitlines():
            if "NEEDED" in line:
                # Format: 0x... (NEEDED) Shared library: [libname.so]
                start = line.find("[")
                end = line.find("]")
                if start != -1 and end != -1:
                    deps.append(line[start+1:end])
        return deps
    
    return []


def find_library(lib_name: str, search_paths: list[Path]) -> Path | None:
    """Find a library in the given search paths."""
    for search_path in search_paths:
        lib_path = search_path / lib_name
        if lib_path.exists():
            return lib_path
        # Also check for versioned libraries
        for lib in search_path.glob(f"{lib_name}*"):
            if lib.is_file():
                return lib
    return None


def copy_shared_libs_recursive(
    lib_path: Path,
    output_dir: Path,
    copied: set[str],
    homebrew_prefix: Path,
    search_paths: list[Path]
) -> None:
    """Recursively copy a shared library and its dependencies."""
    lib_name = lib_path.name
    
    # Skip if already copied
    if lib_name in copied:
        return
    
    # Skip system libraries
    system_prefixes = ["/lib", "/lib64", "/usr/lib", "/usr/lib64"]
    if any(str(lib_path).startswith(prefix) for prefix in system_prefixes):
        # But include if it's a commonly needed library that might not be on target systems
        essential_libs = ["libstdc++", "libgcc_s"]
        if not any(essential in lib_name for essential in essential_libs):
            logger.debug(f"Skipping system library: {lib_path}")
            return
    
    if not lib_path.exists():
        logger.warning(f"Library not found: {lib_path}")
        return
    
    logger.info(f"Copying: {lib_path}")
    
    # Resolve symlinks to get the actual file
    real_path = lib_path.resolve()
    
    # Copy the file
    dest_path = output_dir / lib_name
    shutil.copy2(real_path, dest_path)
    copied.add(lib_name)
    
    # Also copy symlinks if the original was a symlink
    if lib_path.is_symlink():
        symlink_name = lib_path.name
        if symlink_name != real_path.name:
            logger.info(f"  (resolved from symlink: {symlink_name} -> {real_path.name})")
    
    logger.info(f"  -> {dest_path}")
    
    # Get dependencies and copy them too
    deps = get_so_deps(dest_path)
    for dep in deps:
        dep_path = Path(dep)
        
        # Only copy Homebrew dependencies or find them
        if str(dep_path).startswith(str(homebrew_prefix)):
            copy_shared_libs_recursive(dep_path, output_dir, copied, homebrew_prefix, search_paths)
        elif not dep_path.is_absolute():
            # Try to find the library
            found = find_library(dep, search_paths)
            if found and str(found).startswith(str(homebrew_prefix)):
                copy_shared_libs_recursive(found, output_dir, copied, homebrew_prefix, search_paths)


def fix_library_rpath(output_dir: Path) -> None:
    """Fix library RPATH for redistribution using patchelf."""
    logger.info("Fixing library RPATH for redistribution...")
    
    # Check if patchelf is available
    result = run_command(["which", "patchelf"])
    if result.returncode != 0:
        logger.warning("patchelf not found, skipping RPATH fixing")
        logger.warning("Install patchelf with: sudo apt-get install patchelf")
        return
    
    so_files = list(output_dir.glob("*.so*"))
    
    for so_file in so_files:
        logger.info(f"Fixing: {so_file.name}")
        
        # Set RPATH to $ORIGIN so libraries find each other
        run_command(["patchelf", "--set-rpath", "$ORIGIN", str(so_file)])


def copy_headers(package_prefix: Path, output_dir: Path) -> None:
    """Copy header files from the package."""
    include_src = package_prefix / "include"
    include_dst = output_dir / "include"
    
    if include_src.exists():
        logger.info(f"Copying headers from {include_src}")
        shutil.copytree(include_src, include_dst, dirs_exist_ok=True)
        
        # Count header files
        header_count = sum(1 for _ in include_dst.rglob("*.h"))
        logger.info(f"  Copied {header_count} header files")
    else:
        logger.warning(f"Include directory not found: {include_src}")


def copy_pkgconfig(package_prefix: Path, output_dir: Path) -> None:
    """Copy pkg-config files from the package."""
    pkgconfig_src = package_prefix / "lib" / "pkgconfig"
    pkgconfig_dst = output_dir / "lib" / "pkgconfig"
    
    if pkgconfig_src.exists():
        logger.info(f"Copying pkg-config files from {pkgconfig_src}")
        pkgconfig_dst.mkdir(parents=True, exist_ok=True)
        
        for pc_file in pkgconfig_src.glob("*.pc"):
            shutil.copy2(pc_file, pkgconfig_dst)
            logger.info(f"  Copied: {pc_file.name}")
    else:
        logger.debug(f"No pkg-config directory found: {pkgconfig_src}")


def get_arch() -> str:
    """Get the current architecture."""
    import platform
    machine = platform.machine()
    if machine in ["x86_64", "amd64"]:
        return "x86_64"
    elif machine in ["aarch64", "arm64"]:
        return "arm64"
    return machine


def main():
    parser = argparse.ArgumentParser(
        description="Copy libvips dynamic libraries from Homebrew (Linux)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output directory for copied libraries"
    )
    parser.add_argument(
        "--include-headers",
        action="store_true",
        help="Also copy header files"
    )
    parser.add_argument(
        "--fix-rpath",
        action="store_true",
        default=True,
        help="Fix library RPATH for redistribution (default: True)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("libvips Linux Library Copier (Homebrew)")
    logger.info("=" * 60)
    
    # Get Homebrew prefix
    homebrew_prefix = get_homebrew_prefix()
    logger.info(f"Homebrew prefix: {homebrew_prefix}")
    
    # Get libvips prefix and version
    vips_prefix = get_package_prefix("vips")
    vips_version = get_package_version("vips")
    logger.info(f"libvips prefix: {vips_prefix}")
    logger.info(f"libvips version: {vips_version}")
    
    # Get architecture
    arch = get_arch()
    logger.info(f"Architecture: {arch}")
    
    # Create output directory
    lib_output_dir = args.output / "lib"
    lib_output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {lib_output_dir}")
    
    # Build search paths for libraries
    search_paths = [
        vips_prefix / "lib",
        homebrew_prefix / "lib",
    ]
    
    # Find the main libvips shared library
    vips_lib_dir = vips_prefix / "lib"
    main_lib = None
    
    for pattern in ["libvips.so", "libvips.so.*"]:
        libs = list(vips_lib_dir.glob(pattern))
        if libs:
            main_lib = libs[0]
            break
    
    if not main_lib:
        logger.error(f"Could not find libvips.so in {vips_lib_dir}")
        sys.exit(1)
    
    logger.info(f"Main library: {main_lib}")
    
    # Copy libraries recursively
    logger.info("")
    logger.info("Copying shared libraries...")
    logger.info("-" * 40)
    
    copied = set()
    copy_shared_libs_recursive(main_lib, lib_output_dir, copied, homebrew_prefix, search_paths)
    
    # Also explicitly look for versioned libraries
    for lib in vips_lib_dir.glob("libvips*.so*"):
        if lib.name not in copied:
            copy_shared_libs_recursive(lib, lib_output_dir, copied, homebrew_prefix, search_paths)
    
    logger.info("-" * 40)
    logger.info(f"Total libraries copied: {len(copied)}")
    
    # Fix RPATH
    if args.fix_rpath:
        logger.info("")
        fix_library_rpath(lib_output_dir)
    
    # Copy headers if requested
    if args.include_headers:
        logger.info("")
        copy_headers(vips_prefix, args.output)
        
        # Also copy glib headers which are commonly needed
        try:
            glib_prefix = get_package_prefix("glib")
            copy_headers(glib_prefix, args.output)
        except RuntimeError:
            logger.warning("Could not find glib headers")
    
    # Copy pkg-config files
    copy_pkgconfig(vips_prefix, args.output)
    
    # Create version info file
    version_file = args.output / "VERSION.txt"
    with open(version_file, "w") as f:
        f.write(f"libvips version: {vips_version}\n")
        f.write(f"Homebrew prefix: {homebrew_prefix}\n")
        f.write(f"Architecture: {arch}\n")
        f.write(f"Libraries copied: {len(copied)}\n")
        f.write(f"\nLibraries:\n")
        for lib in sorted(copied):
            f.write(f"  - {lib}\n")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    logger.info(f"libvips version: {vips_version}")
    logger.info(f"Architecture: {arch}")
    logger.info(f"Libraries copied: {len(copied)}")
    logger.info(f"Output directory: {args.output}")
    
    # List all copied files
    logger.info("")
    logger.info("Files in output directory:")
    for item in sorted(args.output.rglob("*")):
        if item.is_file():
            size = item.stat().st_size
            logger.info(f"  {item.relative_to(args.output)} ({size:,} bytes)")
    
    logger.info("")
    logger.info("Done!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
