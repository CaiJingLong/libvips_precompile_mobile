#!/usr/bin/env python3
"""
Copy libvips dynamic libraries from Homebrew installation on macOS.

This script extracts libvips and its dependencies from Homebrew,
copies them to an output directory, and fixes the library paths
for redistribution.

Usage:
    python3 copy_libvips_macos.py --output /path/to/output
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


def run_command(cmd: list[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command and log it."""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True)
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


def get_dylib_deps(dylib_path: Path) -> list[str]:
    """Get the list of dynamic library dependencies using otool."""
    result = run_command(["otool", "-L", str(dylib_path)])
    if result.returncode != 0:
        return []
    
    deps = []
    for line in result.stdout.splitlines()[1:]:  # Skip first line (the library itself)
        line = line.strip()
        if line:
            # Extract the path (before " (compatibility version")
            path = line.split(" (")[0].strip()
            deps.append(path)
    return deps


def copy_dylibs_recursive(
    lib_path: Path,
    output_dir: Path,
    copied: set[str],
    homebrew_prefix: Path
) -> None:
    """Recursively copy a dylib and its dependencies."""
    lib_name = lib_path.name
    
    # Skip if already copied
    if lib_name in copied:
        return
    
    # Skip system libraries
    if str(lib_path).startswith("/usr/lib") or str(lib_path).startswith("/System"):
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
        # Create the symlink in output as well
        symlink_name = lib_path.name
        if symlink_name != real_path.name:
            logger.info(f"  (resolved from symlink: {symlink_name} -> {real_path.name})")
    
    logger.info(f"  -> {dest_path}")
    
    # Get dependencies and copy them too
    deps = get_dylib_deps(dest_path)
    for dep in deps:
        dep_path = Path(dep)
        # Only copy Homebrew dependencies
        if str(dep_path).startswith(str(homebrew_prefix)):
            copy_dylibs_recursive(dep_path, output_dir, copied, homebrew_prefix)


def fix_library_paths(output_dir: Path) -> None:
    """Fix library paths using install_name_tool for redistribution."""
    logger.info("Fixing library paths for redistribution...")
    
    dylibs = list(output_dir.glob("*.dylib"))
    
    for dylib in dylibs:
        logger.info(f"Fixing: {dylib.name}")
        
        # Change the install name to use @rpath
        new_id = f"@rpath/{dylib.name}"
        run_command(["install_name_tool", "-id", new_id, str(dylib)])
        
        # Fix dependencies to use @rpath
        deps = get_dylib_deps(dylib)
        for dep in deps:
            dep_path = Path(dep)
            dep_name = dep_path.name
            
            # Check if this dependency exists in our output directory
            if (output_dir / dep_name).exists():
                new_dep = f"@rpath/{dep_name}"
                run_command([
                    "install_name_tool", "-change", dep, new_dep, str(dylib)
                ])
                logger.info(f"  Changed: {dep} -> {new_dep}")


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


def main():
    parser = argparse.ArgumentParser(
        description="Copy libvips dynamic libraries from Homebrew"
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
        "--fix-paths",
        action="store_true",
        default=True,
        help="Fix library paths for redistribution (default: True)"
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
    logger.info("libvips macOS Library Copier")
    logger.info("=" * 60)
    
    # Get Homebrew prefix
    homebrew_prefix = get_homebrew_prefix()
    logger.info(f"Homebrew prefix: {homebrew_prefix}")
    
    # Get libvips prefix and version
    vips_prefix = get_package_prefix("vips")
    vips_version = get_package_version("vips")
    logger.info(f"libvips prefix: {vips_prefix}")
    logger.info(f"libvips version: {vips_version}")
    
    # Create output directory
    lib_output_dir = args.output / "lib"
    lib_output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {lib_output_dir}")
    
    # Find the main libvips dylib
    vips_lib_dir = vips_prefix / "lib"
    main_lib = None
    
    for pattern in ["libvips.dylib", "libvips.*.dylib"]:
        libs = list(vips_lib_dir.glob(pattern))
        if libs:
            main_lib = libs[0]
            break
    
    if not main_lib:
        logger.error(f"Could not find libvips.dylib in {vips_lib_dir}")
        sys.exit(1)
    
    logger.info(f"Main library: {main_lib}")
    
    # Copy libraries recursively
    logger.info("")
    logger.info("Copying dynamic libraries...")
    logger.info("-" * 40)
    
    copied = set()
    copy_dylibs_recursive(main_lib, lib_output_dir, copied, homebrew_prefix)
    
    # Also explicitly look for versioned libraries
    for lib in vips_lib_dir.glob("libvips*.dylib"):
        if lib.name not in copied:
            copy_dylibs_recursive(lib, lib_output_dir, copied, homebrew_prefix)
    
    logger.info("-" * 40)
    logger.info(f"Total libraries copied: {len(copied)}")
    
    # Fix library paths
    if args.fix_paths:
        logger.info("")
        fix_library_paths(lib_output_dir)
    
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
        f.write(f"Architecture: {os.uname().machine}\n")
        f.write(f"Libraries copied: {len(copied)}\n")
        f.write(f"\nLibraries:\n")
        for lib in sorted(copied):
            f.write(f"  - {lib}\n")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    logger.info(f"libvips version: {vips_version}")
    logger.info(f"Architecture: {os.uname().machine}")
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
