# iOS 构建 - libvips

本目录包含为 iOS 平台构建 libvips 的文档。

## 支持的架构

| 架构 | 平台 | 说明 |
|------|------|------|
| `arm64` | `ios` | iOS 设备（iPhone/iPad）|
| `arm64` | `ios-simulator` | Apple Silicon Mac 上的 iOS 模拟器 |

## 构建系统

iOS 构建使用 [MobiPkg/Compile](https://github.com/MobiPkg/Compile) 构建系统，这是一个基于 Dart 的跨平台编译工具。

### 构建脚本来源

- **仓库**：[MobiPkg/Compile](https://github.com/MobiPkg/Compile)
- **构建脚本**：[build-ios-with-workspace.sh](https://github.com/MobiPkg/Compile/blob/main/example/libvips/build-ios-with-workspace.sh)
- **工作区配置**：[workspace.yaml](https://github.com/MobiPkg/Compile/blob/main/example/libvips/workspace.yaml)
- **libvips 配置**：[lib.yaml](https://github.com/MobiPkg/Compile/blob/main/example/libvips/libvips/lib.yaml)

## 构建环境要求

- **操作系统**：macOS 14+（推荐 Apple Silicon）
- **Xcode**：最新稳定版本
- **Dart SDK**：稳定版本

### 构建工具

以下工具是必需的，在 GitHub Actions 构建期间会自动安装：

| 工具 | 用途 |
|------|------|
| meson | 构建系统 |
| ninja | 构建工具 |
| automake | 构建配置 |
| autoconf | 构建配置 |
| libtool | 库管理 |
| pkg-config | 包配置 |
| nasm | 汇编器（用于 libjpeg-turbo）|
| cmake | 构建系统 |

## 依赖库

iOS 构建编译以下依赖项（在 workspace.yaml 中定义）：

| 库 | 说明 |
|----|------|
| zlib | 压缩库 |
| libffi | 外部函数接口库 |
| pcre2 | Perl 兼容正则表达式 |
| expat | XML 解析库 |
| glib | 核心应用程序构建块 |
| libjpeg-turbo | JPEG 图像编解码器 |
| libpng | PNG 图像编解码器 |
| libwebp | WebP 图像编解码器 |
| libvips | 图像处理库 |

## 本地构建

### 1. 安装先决条件

```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装构建依赖
brew install meson ninja automake autoconf libtool pkg-config nasm cmake

# 安装 Dart SDK
brew tap dart-lang/dart
brew install dart
```

### 2. 克隆 MobiPkg/Compile

```bash
git clone https://github.com/MobiPkg/Compile.git /tmp/Compile
cd /tmp/Compile
dart pub get
```

### 3. 运行构建

```bash
cd /tmp/Compile

INSTALL_PREFIX="/tmp/Compile/example/libvips/install"
mkdir -p "$INSTALL_PREFIX"

# 构建所有依赖和 libvips
dart run bin/compile.dart workspace -C example/libvips \
  --ios --no-android \
  --install-prefix "$INSTALL_PREFIX" \
  --dependency-prefix "$INSTALL_PREFIX" \
  --target libvips
```

### 4. 创建 XCFramework

```bash
cd /tmp/Compile

dart run bin/compile.dart package xcframework -C example/libvips \
  -p "$INSTALL_PREFIX" \
  -t libvips \
  -o libvips
```

## 构建输出

构建完成后，您将得到：

```
output/
└── libvips.xcframework/
    ├── Info.plist
    ├── ios-arm64/
    │   └── libvips.a
    └── ios-arm64-simulator/
        └── libvips.a
```

## 下载预编译库

如果您只想下载预编译库而不自行构建：

1. 前往 [Releases](https://github.com/CaiJingLong/libvips_precompile_mobile/releases) 页面
2. 下载最新的 `libvips-ios-*.tar.xz` 文件
3. 解压：

```bash
tar -xvf libvips-ios-*.tar.xz
```

## 集成到 iOS/macOS 项目

### 使用 XCFramework

1. 将 `libvips.xcframework` 拖入您的 Xcode 项目
2. 确保它已添加到目标的"Frameworks, Libraries, and Embedded Content"中
3. 将嵌入选项设置为"Do Not Embed"（静态库）

### 使用 CocoaPods

您可以创建 podspec 来分发预编译框架：

```ruby
Pod::Spec.new do |s|
  s.name         = 'libvips'
  s.version      = '8.16.0'
  s.summary      = 'libvips 图像处理库'
  s.homepage     = 'https://github.com/libvips/libvips'
  s.license      = { :type => 'LGPL-2.1' }
  s.author       = 'libvips'
  s.platform     = :ios, '13.0'
  s.source       = { :http => 'https://github.com/CaiJingLong/libvips_precompile_mobile/releases/download/...' }
  s.vendored_frameworks = 'libvips.xcframework'
end
```

## 故障排除

### 找不到 Xcode 命令行工具

```bash
xcode-select --install
```

### 架构不匹配

确保您在 Apple Silicon Mac（M1/M2/M3）上构建以支持 arm64-simulator。Intel Mac 无法构建 arm64 模拟器二进制文件。

### 缺少构建依赖

重新安装所有依赖：

```bash
brew reinstall meson ninja automake autoconf libtool pkg-config nasm cmake
```

## 许可证

详见 [LICENSE](../LICENSE) 文件。
