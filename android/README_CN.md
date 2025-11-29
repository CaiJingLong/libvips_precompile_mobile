# Android 构建 - libvips

本目录包含为 Android 平台构建 libvips 的脚本和文档。

## 支持的架构

| 架构 | Android ABI | 说明 |
|------|-------------|------|
| `armv8` | `arm64-v8a` | 64位 ARM 设备 |
| `armv7` | `armeabi-v7a` | 32位 ARM 设备 |
| `x86` | `x86` | 32位 x86 模拟器 |
| `x86_64` | `x86_64` | 64位 x86 模拟器 |

## 构建环境要求

此构建脚本已在以下环境中测试：

- **操作系统**：macOS / Linux
- **NDK 版本**：NDK 25
- **Conan 版本**：2.0.14+
- **Python 版本**：3.11.6+

## 依赖库

Android 构建包含以下依赖项（由 Conan 管理）：

| 库 | 说明 |
|----|------|
| glib | 核心应用程序构建块 |
| libgettext | 国际化库 |
| libvips | 图像处理库 |
| libjpeg-turbo | JPEG 图像编解码器 |
| libpng | PNG 图像编解码器 |
| libwebp | WebP 图像编解码器 |
| libtiff | TIFF 图像编解码器 |
| zlib | 压缩库 |
| libffi | 外部函数接口库 |
| pcre2 | Perl 兼容正则表达式 |
| expat | XML 解析库 |
| fftw | 快速傅里叶变换库 |
| lcms2 | Little CMS 颜色管理库 |
| libdeflate | 快速压缩库 |
| zstd | Zstandard 压缩 |
| bzip2 | 压缩库 |

## 环境配置

### 1. 安装 Python 和 Conan

```bash
# 安装 Python 3.11+
# macOS:
brew install python@3.11

# Linux (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# 安装 Conan
pip install conan
```

### 2. 配置 Android NDK

下载并安装 Android NDK，然后设置环境变量：

```bash
export ANDROID_NDK=/path/to/your/android-ndk
```

### 3. 安装构建工具

```bash
# macOS:
brew install ninja meson

# Linux (Ubuntu/Debian):
sudo apt-get install ninja-build meson
```

## 构建

从仓库根目录运行构建脚本：

```bash
# 使用 Python
python build_android.py

# 或者
python3 build_android.py

# 或者使其可执行
chmod +x build_android.py
./build_android.py
```

交互式菜单将引导您：
1. 选择目标架构
2. 配置构建选项
3. 生成 jniLibs 文件夹结构

## 构建输出

构建完成后，库文件将组织在 `output/android/jniLibs/` 目录中：

```
output/android/jniLibs/
├── arm64-v8a/
│   ├── libvips.so
│   ├── libvips-cpp.so
│   └── ... (其他 .so 文件)
├── armeabi-v7a/
│   └── ...
├── x86/
│   └── ...
├── x86_64/
│   └── ...
└── include/
    └── vips/
        └── ... (头文件)
```

## 下载预编译库

如果您只想下载预编译库而不自行构建：

1. 前往 [Releases](https://github.com/CaiJingLong/libvips_precompile_mobile/releases) 页面
2. 下载最新的 `libvips-android-*.tar.xz` 文件
3. 解压：

```bash
tar -xvf libvips-android-*.tar.xz
```

## 集成到 Android 项目

1. 将 `jniLibs` 文件夹复制到您 Android 项目的 `app/src/main/` 目录
2. 如果需要 C/C++ 头文件，请复制 `include` 文件夹
3. 如有必要，更新您的 `build.gradle`

## 故障排除

### 找不到 NDK

确保正确设置了 `ANDROID_NDK` 环境变量：

```bash
echo $ANDROID_NDK
# 应该输出您的 NDK 安装路径
```

### Conan 构建失败

尝试清除 Conan 缓存并重新构建：

```bash
conan remove "*" -c
python build_android.py
```

## 许可证

详见 [LICENSE](../LICENSE) 文件。
