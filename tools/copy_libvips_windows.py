#!/usr/bin/env python3
"""
Download and extract libvips pre-built binaries for Windows.

This script downloads the official pre-built libvips binaries from GitHub
and extracts them to an output directory.

Usage:
    python3 copy_libvips_windows.py --output C:\\path\\to\\output --arch x64 --build-type web
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

# Configure logging for GitHub Actions output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# libvips GitHub releases URL
LIBVIPS_RELEASES_API = "https://api.github.com/repos/libvips/build-win64-mxe/releases/latest"
LIBVIPS_RELEASES_PAGE = "https://github.com/libvips/build-win64-mxe/releases"

# Architecture mappings
ARCH_MAP = {
    "x64": "w64",
    "x86_64": "w64",
    "amd64": "w64",
    "arm64": "arm64",
    "aarch64": "arm64",
}


def run_command(cmd: list[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command and log it."""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True, shell=(os.name == 'nt'))
    if result.returncode != 0:
        logger.error(f"Command failed with code {result.returncode}")
        if result.stderr:
            logger.error(f"stderr: {result.stderr}")
    return result


def get_latest_release_info() -> dict:
    """Get the latest release information from GitHub API."""
    import json
    
    logger.info("Fetching latest release information from GitHub...")
    
    try:
        req = urllib.request.Request(
            LIBVIPS_RELEASES_API,
            headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "libvips-precompile-mobile"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        logger.error(f"Failed to fetch release info: {e}")
        raise


def find_asset_for_arch(release_info: dict, arch: str, build_type: str = "web") -> tuple[str, str] | None:
    """Find the download URL for the specified architecture and build type.
    
    Args:
        release_info: GitHub release information
        arch: Architecture (x64 or arm64)
        build_type: Build type ("web" or "all")
    
    Returns:
        Tuple of (download_url, filename) or None if not found
    """
    arch_suffix = ARCH_MAP.get(arch, arch)
    
    logger.info(f"Looking for architecture: {arch} (suffix: {arch_suffix}), build type: {build_type}")
    
    # Look for the asset with specific build type
    for asset in release_info.get("assets", []):
        name = asset["name"]
        # Pattern: vips-dev-w64-web-X.Y.Z-static.zip or vips-dev-w64-all-X.Y.Z.zip
        # Prefer non-ffi versions for simplicity
        if arch_suffix in name and build_type in name and name.endswith(".zip"):
            # Prefer non-ffi versions
            if "ffi" not in name:
                logger.info(f"Found asset: {name}")
                return asset["browser_download_url"], name
    
    # Fallback: look for any matching zip with build type
    for asset in release_info.get("assets", []):
        name = asset["name"]
        if arch_suffix in name and build_type in name and name.endswith(".zip"):
            logger.info(f"Found fallback asset: {name}")
            return asset["browser_download_url"], name
    
    return None


def download_file(url: str, dest_path: Path) -> None:
    """Download a file with progress indication."""
    logger.info(f"Downloading: {url}")
    logger.info(f"Destination: {dest_path}")
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "libvips-precompile-mobile"})
        with urllib.request.urlopen(req, timeout=300) as response:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            block_size = 8192
            
            with open(dest_path, 'wb') as f:
                while True:
                    block = response.read(block_size)
                    if not block:
                        break
                    f.write(block)
                    downloaded += len(block)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        if downloaded % (block_size * 100) == 0 or downloaded == total_size:
                            logger.info(f"  Progress: {downloaded:,} / {total_size:,} bytes ({percent:.1f}%)")
        
        logger.info(f"Download complete: {dest_path.stat().st_size:,} bytes")
    except urllib.error.URLError as e:
        logger.error(f"Download failed: {e}")
        raise


def extract_zip(zip_path: Path, extract_dir: Path) -> Path:
    """Extract a zip file and return the extracted directory."""
    logger.info(f"Extracting: {zip_path}")
    logger.info(f"To: {extract_dir}")
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # List contents
        names = zf.namelist()
        logger.info(f"  Archive contains {len(names)} entries")
        
        # Extract
        zf.extractall(extract_dir)
    
    # Find the extracted directory (usually the first level)
    extracted_dirs = [d for d in extract_dir.iterdir() if d.is_dir()]
    if extracted_dirs:
        logger.info(f"  Extracted to: {extracted_dirs[0]}")
        return extracted_dirs[0]
    
    return extract_dir


def copy_libraries(source_dir: Path, output_dir: Path, include_headers: bool = True) -> list[str]:
    """Copy DLL files and optionally headers to the output directory.
    
    This function extracts only the minimal files needed for FFI bindings:
    - DLL files (dynamic libraries for runtime loading)
    - Headers (optional, for FFI code generation)
    
    This is consistent with other platforms:
    - macOS: .dylib files + headers
    - Linux: .so files + headers
    - iOS: .xcframework (static)
    - Android: .so files in jniLibs + headers
    """
    copied_files = []
    
    # Copy DLL files to lib directory (consistent with macOS/Linux which use lib/)
    bin_src = source_dir / "bin"
    lib_dst = output_dir / "lib"
    
    if bin_src.exists():
        logger.info(f"Copying DLL files from {bin_src}")
        lib_dst.mkdir(parents=True, exist_ok=True)
        
        for dll in bin_src.glob("*.dll"):
            shutil.copy2(dll, lib_dst)
            copied_files.append(dll.name)
            logger.info(f"  Copied: {dll.name}")
    else:
        logger.warning(f"Bin directory not found: {bin_src}")
    
    # Copy include directory (headers) - needed for FFI code generation
    if include_headers:
        include_src = source_dir / "include"
        include_dst = output_dir / "include"
        
        if include_src.exists():
            logger.info(f"Copying headers from {include_src}")
            shutil.copytree(include_src, include_dst, dirs_exist_ok=True)
            
            header_count = sum(1 for _ in include_dst.rglob("*.h"))
            logger.info(f"  Copied {header_count} header files")
        else:
            logger.debug(f"Include directory not found: {include_src}")
    
    # Copy pkg-config files (useful for build systems)
    pkgconfig_src = source_dir / "lib" / "pkgconfig"
    pkgconfig_dst = output_dir / "lib" / "pkgconfig"
    
    if pkgconfig_src.exists():
        logger.info(f"Copying pkg-config files from {pkgconfig_src}")
        pkgconfig_dst.mkdir(parents=True, exist_ok=True)
        
        for pc_file in pkgconfig_src.glob("*.pc"):
            shutil.copy2(pc_file, pkgconfig_dst)
            logger.info(f"  Copied: {pc_file.name}")
    else:
        logger.debug(f"No pkg-config directory found: {pkgconfig_src}")
    
    return copied_files


def get_version_from_filename(filename: str) -> str:
    """Extract version from the download filename."""
    # Pattern: vips-dev-w64-web-8.17.0-static.zip
    parts = filename.replace(".zip", "").split("-")
    for part in parts:
        if part[0].isdigit():
            return part
    return "unknown"


def main():
    parser = argparse.ArgumentParser(
        description="Download and extract libvips pre-built binaries for Windows"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output directory for extracted libraries"
    )
    parser.add_argument(
        "--arch", "-a",
        type=str,
        choices=["x64", "arm64"],
        default="x64",
        help="Target architecture (default: x64)"
    )
    parser.add_argument(
        "--build-type", "-b",
        type=str,
        choices=["web", "all"],
        default="web",
        help="Build type: web (common formats) or all (all formats) (default: web)"
    )
    parser.add_argument(
        "--version", "-V",
        type=str,
        default="latest",
        help="libvips version to download (default: latest)"
    )
    parser.add_argument(
        "--include-headers",
        action="store_true",
        help="Also copy header files"
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
    logger.info("libvips Windows Binary Downloader")
    logger.info("=" * 60)
    logger.info(f"Target architecture: {args.arch}")
    logger.info(f"Build type: {args.build_type}")
    logger.info(f"Target version: {args.version}")
    logger.info(f"Output directory: {args.output}")
    
    # Get latest release info
    release_info = get_latest_release_info()
    release_tag = release_info.get("tag_name", "unknown")
    logger.info(f"Latest release: {release_tag}")
    
    # Find the appropriate asset
    asset = find_asset_for_arch(release_info, args.arch, args.build_type)
    if not asset:
        logger.error(f"Could not find a download for architecture: {args.arch}, build type: {args.build_type}")
        logger.error(f"Available assets:")
        for a in release_info.get("assets", []):
            logger.error(f"  - {a['name']}")
        sys.exit(1)
    
    download_url, filename = asset
    version = get_version_from_filename(filename)
    logger.info(f"Download URL: {download_url}")
    logger.info(f"Filename: {filename}")
    logger.info(f"Version: {version}")
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Download to temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / filename
        
        logger.info("")
        logger.info("Downloading pre-built binaries...")
        logger.info("-" * 40)
        download_file(download_url, zip_path)
        
        logger.info("")
        logger.info("Extracting archive...")
        logger.info("-" * 40)
        extracted_dir = extract_zip(zip_path, temp_path)
        
        logger.info("")
        logger.info("Copying libraries...")
        logger.info("-" * 40)
        copied_files = copy_libraries(extracted_dir, args.output, args.include_headers)
    
    # Create version info file
    version_file = args.output / "VERSION.txt"
    with open(version_file, "w") as f:
        f.write(f"libvips version: {version}\n")
        f.write(f"Release tag: {release_tag}\n")
        f.write(f"Architecture: {args.arch}\n")
        f.write(f"Build type: {args.build_type}\n")
        f.write(f"Source: {LIBVIPS_RELEASES_PAGE}\n")
        f.write(f"Download URL: {download_url}\n")
        f.write(f"Filename: {filename}\n")
        f.write(f"\nDLLs copied: {len([f for f in copied_files if f.endswith('.dll')])}\n")
        f.write(f"\nLibraries:\n")
        for file in sorted(copied_files):
            f.write(f"  - {file}\n")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    logger.info(f"libvips version: {version}")
    logger.info(f"Release tag: {release_tag}")
    logger.info(f"Architecture: {args.arch}")
    logger.info(f"Build type: {args.build_type}")
    logger.info(f"DLLs copied: {len([f for f in copied_files if f.endswith('.dll')])}")
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
