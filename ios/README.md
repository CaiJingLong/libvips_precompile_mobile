# iOS Build - libvips

This directory contains documentation for building libvips for iOS platforms.

## Supported Architectures

| Architecture | Platform | Description |
|-------------|----------|-------------|
| `arm64` | `ios` | iOS devices (iPhone/iPad) |
| `arm64` | `ios-simulator` | iOS Simulator on Apple Silicon Macs |

## Build System

The iOS build uses the [MobiPkg/Compile](https://github.com/MobiPkg/Compile) build system, which is a Dart-based tool for cross-compiling libraries to mobile platforms.

### Build Script Source

- **Repository**: [MobiPkg/Compile](https://github.com/MobiPkg/Compile)
- **Build Script**: [build-ios-with-workspace.sh](https://github.com/MobiPkg/Compile/blob/main/example/libvips/build-ios-with-workspace.sh)
- **Workspace Configuration**: [workspace.yaml](https://github.com/MobiPkg/Compile/blob/main/example/libvips/workspace.yaml)
- **libvips Configuration**: [lib.yaml](https://github.com/MobiPkg/Compile/blob/main/example/libvips/libvips/lib.yaml)

## Build Environment Requirements

- **Operating System**: macOS 14+ (Apple Silicon recommended)
- **Xcode**: Latest stable version
- **Dart SDK**: Stable channel

### Build Tools

The following tools are required and will be installed automatically during the GitHub Actions build:

| Tool | Purpose |
|------|---------|
| meson | Build system |
| ninja | Build tool |
| automake | Build configuration |
| autoconf | Build configuration |
| libtool | Library management |
| pkg-config | Package configuration |
| nasm | Assembler (for libjpeg-turbo) |
| cmake | Build system |

## Dependencies

The iOS build compiles the following dependencies (as defined in workspace.yaml):

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

## Building Locally

### 1. Install Prerequisites

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install build dependencies
brew install meson ninja automake autoconf libtool pkg-config nasm cmake

# Install Dart SDK
brew tap dart-lang/dart
brew install dart
```

### 2. Clone MobiPkg/Compile

```bash
git clone https://github.com/MobiPkg/Compile.git /tmp/Compile
cd /tmp/Compile
dart pub get
```

### 3. Run the Build

```bash
cd /tmp/Compile

INSTALL_PREFIX="/tmp/Compile/example/libvips/install"
mkdir -p "$INSTALL_PREFIX"

# Build all dependencies and libvips
dart run bin/compile.dart workspace -C example/libvips \
  --ios --no-android \
  --install-prefix "$INSTALL_PREFIX" \
  --dependency-prefix "$INSTALL_PREFIX" \
  --target libvips
```

### 4. Create XCFramework

```bash
cd /tmp/Compile

dart run bin/compile.dart package xcframework -C example/libvips \
  -p "$INSTALL_PREFIX" \
  -t libvips \
  -o libvips
```

## Build Output

After building, you'll have:

```
output/
└── libvips.xcframework/
    ├── Info.plist
    ├── ios-arm64/
    │   └── libvips.a
    └── ios-arm64-simulator/
        └── libvips.a
```

## Downloading Pre-built Libraries

If you just want to download pre-built libraries without building:

1. Go to the [Releases](https://github.com/CaiJingLong/libvips_precompile_mobile/releases) page
2. Download the latest `libvips-ios-*.tar.xz` file
3. Extract:

```bash
tar -xvf libvips-ios-*.tar.xz
```

## Integration with iOS/macOS Project

### Using XCFramework

1. Drag the `libvips.xcframework` into your Xcode project
2. Ensure it's added to your target's "Frameworks, Libraries, and Embedded Content"
3. Set the embedding option to "Do Not Embed" (static library)

### Using CocoaPods

You can create a podspec to distribute the pre-built framework:

```ruby
Pod::Spec.new do |s|
  s.name         = 'libvips'
  s.version      = '8.16.0'
  s.summary      = 'libvips image processing library'
  s.homepage     = 'https://github.com/libvips/libvips'
  s.license      = { :type => 'LGPL-2.1' }
  s.author       = 'libvips'
  s.platform     = :ios, '13.0'
  s.source       = { :http => 'https://github.com/CaiJingLong/libvips_precompile_mobile/releases/download/...' }
  s.vendored_frameworks = 'libvips.xcframework'
end
```

## Troubleshooting

### Xcode Command Line Tools Not Found

```bash
xcode-select --install
```

### Architecture Mismatch

Make sure you're building on an Apple Silicon Mac (M1/M2/M3) for arm64-simulator support. Intel Macs cannot build arm64 simulator binaries.

### Build Dependencies Missing

Reinstall all dependencies:

```bash
brew reinstall meson ninja automake autoconf libtool pkg-config nasm cmake
```

## License

See the [LICENSE](../LICENSE) file for details.
