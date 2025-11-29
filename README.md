# Build libvips for Mobile Platforms

This repository contains precompiled libvips libraries for mobile platforms (iOS and Android).

[![Build iOS libvips](https://github.com/CaiJingLong/libvips_precompile_mobile/actions/workflows/build-ios-libvips.yml/badge.svg)](https://github.com/CaiJingLong/libvips_precompile_mobile/actions/workflows/build-ios-libvips.yml)
[![Build Android libvips](https://github.com/CaiJingLong/libvips_precompile_mobile/actions/workflows/build-android-libvips.yml/badge.svg)](https://github.com/CaiJingLong/libvips_precompile_mobile/actions/workflows/build-android-libvips.yml)

## Quick Download

Pre-built libraries are available on the [Releases](https://github.com/CaiJingLong/libvips_precompile_mobile/releases) page.

| Platform | Download |
|----------|----------|
| iOS | `libvips-ios-*.tar.xz` |
| Android | `libvips-android-*.tar.xz` |

## Platform Documentation

For detailed build instructions and integration guides, see the platform-specific documentation:

| Platform | Documentation |
|----------|---------------|
| iOS | [English](ios/README.md) \| [中文](ios/README_CN.md) |
| Android | [English](android/README.md) \| [中文](android/README_CN.md) |

---

## iOS Build Overview

The iOS build uses [MobiPkg/Compile](https://github.com/MobiPkg/Compile) to cross-compile libvips for iOS platforms.

### Supported Architectures

- `arm64` - iOS devices (iPhone/iPad)
- `arm64-simulator` - iOS Simulator on Apple Silicon Macs

### Dependencies

| Library | Description |
|---------|-------------|
| zlib | Compression library |
| libffi | Foreign function interface library |
| pcre2 | Perl Compatible Regular Expressions |
| expat | XML parser library |
| glib | Core application building blocks |
| libjpeg-turbo | JPEG image codec |
| libpng | PNG image codec |
| libwebp | WebP image codec |
| libvips | Image processing library |

---

## Android Build Overview

The Android build uses Conan package manager to cross-compile libvips for Android platforms.

### Supported Architectures

| Architecture | Android ABI |
|-------------|-------------|
| armv8 | arm64-v8a |
| armv7 | armeabi-v7a |
| x86 | x86 |
| x86_64 | x86_64 |

### Quick Setup

```bash
# Install Conan
pip install conan

# Set Android NDK path
export ANDROID_NDK=/path/to/ndk

# Run the build script
python build_android.py
```

### Dependencies

| Library | Description |
|---------|-------------|
| glib | Core application building blocks |
| libgettext | Internationalization library |
| libvips | Image processing library |
| libjpeg-turbo | JPEG image codec |
| libpng | PNG image codec |
| libwebp | WebP image codec |
| libtiff | TIFF image codec |
| zlib | Compression library |
| libffi | Foreign function interface library |
| pcre2 | Perl Compatible Regular Expressions |
| expat | XML parser library |
| fftw | Fast Fourier Transform library |
| lcms2 | Little CMS color management library |
| libdeflate | Fast compression library |
| zstd | Zstandard compression |
| bzip2 | Compression library |

---

## Release Information

Each release includes:
- **Build artifacts** (compressed as `.tar.xz`)
- **Build environment information** (macOS/Linux version, tool versions)
- **Source references** (commit SHA, workflow file links)
- **Dependency installation instructions** (reproducible builds)

For iOS releases, the exact MobiPkg/Compile commit used is included for full build reproducibility.

---

## License

See the [LICENSE](LICENSE) file for details.

[Releases]: https://github.com/CaiJingLong/libvips_precompile_mobile/releases
