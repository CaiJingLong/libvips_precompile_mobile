# Android Build - libvips

This directory contains scripts and documentation for building libvips for Android platforms.

## Supported Architectures

| Architecture | Android ABI | Description |
|-------------|-------------|-------------|
| `armv8` | `arm64-v8a` | 64-bit ARM devices |
| `armv7` | `armeabi-v7a` | 32-bit ARM devices |
| `x86` | `x86` | 32-bit x86 emulator |
| `x86_64` | `x86_64` | 64-bit x86 emulator |

## Build Environment Requirements

This build script has been tested with the following environment:

- **Operating System**: macOS / Linux
- **NDK Version**: NDK 25
- **Conan Version**: 2.0.14+
- **Python Version**: 3.11.6+

## Dependencies

The Android build includes the following dependencies (managed by Conan):

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

## Setup

### 1. Install Python and Conan

```bash
# Install Python 3.11+
# On macOS:
brew install python@3.11

# On Linux (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# Install Conan
pip install conan
```

### 2. Set up Android NDK

Download and install Android NDK, then set the environment variable:

```bash
export ANDROID_NDK=/path/to/your/android-ndk
```

### 3. Install Build Tools

```bash
# On macOS:
brew install ninja meson

# On Linux (Ubuntu/Debian):
sudo apt-get install ninja-build meson
```

## Building

Run the build script from the repository root:

```bash
# Using Python
python build_android.py

# Or
python3 build_android.py

# Or make it executable
chmod +x build_android.py
./build_android.py
```

The interactive menu will guide you through:
1. Select the target architecture
2. Configure build options
3. Generate jniLibs folder structure

## Build Output

After building, the libraries will be organized in the `output/android/jniLibs/` directory:

```
output/android/jniLibs/
├── arm64-v8a/
│   ├── libvips.so
│   ├── libvips-cpp.so
│   └── ... (other .so files)
├── armeabi-v7a/
│   └── ...
├── x86/
│   └── ...
├── x86_64/
│   └── ...
└── include/
    └── vips/
        └── ... (header files)
```

## Downloading Pre-built Libraries

If you just want to download pre-built libraries without building:

1. Go to the [Releases](https://github.com/CaiJingLong/libvips_precompile_mobile/releases) page
2. Download the latest `libvips-android-*.tar.xz` file
3. Extract:

```bash
tar -xvf libvips-android-*.tar.xz
```

## Integration with Android Project

1. Copy the `jniLibs` folder to your Android project's `app/src/main/` directory
2. Copy the `include` folder if you need C/C++ headers
3. Update your `build.gradle` if necessary

## Troubleshooting

### NDK Not Found

Make sure `ANDROID_NDK` environment variable is set correctly:

```bash
echo $ANDROID_NDK
# Should output the path to your NDK installation
```

### Conan Build Fails

Try clearing Conan cache and rebuilding:

```bash
conan remove "*" -c
python build_android.py
```

## License

See the [LICENSE](../LICENSE) file for details.
