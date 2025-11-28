# Build libvips for Mobile Platforms

This repository contains precompiled libvips libraries for mobile platforms.

## iOS Build (libvips-8.16.0-ios)

The iOS build of libvips-8.16.0 is compiled using the build scripts from the [MobiPkg/Compile](https://github.com/MobiPkg/Compile) repository.

### Build Script Source

The iOS compilation is based on:
- **Repository**: [MobiPkg/Compile](https://github.com/MobiPkg/Compile)
- **Build Script**: [build-ios-with-workspace.sh](https://github.com/MobiPkg/Compile/blob/main/example/libvips/build-ios-with-workspace.sh)

The build script uses the Dart-based Compile tool to orchestrate the compilation of libvips and its dependencies for iOS platforms.

### Dependencies Compiled

The iOS build includes the following dependencies (as defined in [workspace.yaml](https://github.com/MobiPkg/Compile/blob/main/example/libvips/workspace.yaml)):

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

### Supported Architectures

- `arm64` - iOS devices (iPhone/iPad)
- `arm64-simulator` - iOS Simulator on Apple Silicon Macs

---

## Android Build (libvips)

This packaging script is only tested in the following environments:

1. macOS
2. NDK 25
3. conan 2.0.14
4. python 3.11.6

## Setup

- Install conan

```bash
pip install conan
```

- Add ANDROID_NDK to environment variables

```bash
export ANDROID_NDK=/path/to/ndk
```

- run the script

```bash
python build_android.py
python3 build_android.py

chmod +x build_android.py
./build_android.py
```

## Download libraries

If you just want to download lib files

You just to [release][] page and download the latest release.

Just download `jniLibs.tar.xz` file and extract it.

```sh
tar -xvf jniLibs.tar.xz
```

<details>

<summary>libs for libvips</summary>

```sh
android/jniLibs
├── arm64-v8a
│   ├── libbz2.so
│   ├── libcharset.so
│   ├── libcpufeatures-webp.a
│   ├── libdeflate.so
│   ├── libelf.a
│   ├── libexpat.so
│   ├── libffi.so
│   ├── libfftw3.so
│   ├── libgio-2.0.so
│   ├── libglib-2.0.so
│   ├── libgmodule-2.0.so
│   ├── libgnuintl.a
│   ├── libgobject-2.0.so
│   ├── libgthread-2.0.so
│   ├── libiconv.so
│   ├── libjbig.so
│   ├── libjpeg.so
│   ├── liblcms2.so
│   ├── liblzma.so
│   ├── libpcre2-16.so
│   ├── libpcre2-32.so
│   ├── libpcre2-8.so
│   ├── libpcre2-posix.so
│   ├── libsharpyuv.so
│   ├── libspng.so
│   ├── libtiff.so
│   ├── libtiffxx.so
│   ├── libvips-cpp.so
│   ├── libvips.so
│   ├── libwebp.so
│   ├── libwebpdecoder.so
│   ├── libwebpdemux.so
│   ├── libwebpmux.so
│   ├── libz.so
│   └── libzstd.so
├── armeabi-v7a
│   ├── libbz2.so
│   ├── libcharset.so
│   ├── libcpufeatures-webp.a
│   ├── libdeflate.so
│   ├── libelf.a
│   ├── libexpat.so
│   ├── libffi.so
│   ├── libfftw3.so
│   ├── libgio-2.0.so
│   ├── libglib-2.0.so
│   ├── libgmodule-2.0.so
│   ├── libgnuintl.a
│   ├── libgobject-2.0.so
│   ├── libgthread-2.0.so
│   ├── libiconv.so
│   ├── libjbig.so
│   ├── libjpeg.so
│   ├── liblcms2.so
│   ├── liblzma.so
│   ├── libpcre2-16.so
│   ├── libpcre2-32.so
│   ├── libpcre2-8.so
│   ├── libpcre2-posix.so
│   ├── libsharpyuv.so
│   ├── libspng.so
│   ├── libtiff.so
│   ├── libtiffxx.so
│   ├── libvips-cpp.so
│   ├── libvips.so
│   ├── libwebp.so
│   ├── libwebpdecoder.so
│   ├── libwebpdemux.so
│   ├── libwebpmux.so
│   ├── libz.so
│   └── libzstd.so
├── include
│   ├── bzlib.h
│   ├── expat.h
│   ├── expat_config.h
│   ├── expat_external.h
│   ├── ffi.h
│   ├── ffitarget.h
│   ├── fftw3.f
│   ├── fftw3.f03
│   ├── fftw3.h
│   ├── fftw3l.f03
│   ├── fftw3q.f03
│   ├── gelf.h
│   ├── gio-unix-2.0
│   │   └── gio
│   │       ├── gdesktopappinfo.h
│   │       ├── gfiledescriptorbased.h
│   │       ├── gunixfdmessage.h
│   │       ├── gunixinputstream.h
│   │       ├── gunixmounts.h
│   │       └── gunixoutputstream.h
│   ├── glib-2.0
│   │   ├── gio
│   │   │   ├── gaction.h
│   │   │   ├── gactiongroup.h
│   │   │   ├── gactiongroupexporter.h
│   │   │   ├── gactionmap.h
│   │   │   ├── gappinfo.h
│   │   │   ├── gapplication.h
│   │   │   ├── gapplicationcommandline.h
│   │   │   ├── gasyncinitable.h
│   │   │   ├── gasyncresult.h
│   │   │   ├── gbufferedinputstream.h
│   │   │   ├── gbufferedoutputstream.h
│   │   │   ├── gbytesicon.h
│   │   │   ├── gcancellable.h
│   │   │   ├── gcharsetconverter.h
│   │   │   ├── gcontenttype.h
│   │   │   ├── gconverter.h
│   │   │   ├── gconverterinputstream.h
│   │   │   ├── gconverteroutputstream.h
│   │   │   ├── gcredentials.h
│   │   │   ├── gdatagrambased.h
│   │   │   ├── gdatainputstream.h
│   │   │   ├── gdataoutputstream.h
│   │   │   ├── gdbusactiongroup.h
│   │   │   ├── gdbusaddress.h
│   │   │   ├── gdbusauthobserver.h
│   │   │   ├── gdbusconnection.h
│   │   │   ├── gdbuserror.h
│   │   │   ├── gdbusinterface.h
│   │   │   ├── gdbusinterfaceskeleton.h
│   │   │   ├── gdbusintrospection.h
│   │   │   ├── gdbusmenumodel.h
│   │   │   ├── gdbusmessage.h
│   │   │   ├── gdbusmethodinvocation.h
│   │   │   ├── gdbusnameowning.h
│   │   │   ├── gdbusnamewatching.h
│   │   │   ├── gdbusobject.h
│   │   │   ├── gdbusobjectmanager.h
│   │   │   ├── gdbusobjectmanagerclient.h
│   │   │   ├── gdbusobjectmanagerserver.h
│   │   │   ├── gdbusobjectproxy.h
│   │   │   ├── gdbusobjectskeleton.h
│   │   │   ├── gdbusproxy.h
│   │   │   ├── gdbusserver.h
│   │   │   ├── gdbusutils.h
│   │   │   ├── gdebugcontroller.h
│   │   │   ├── gdebugcontrollerdbus.h
│   │   │   ├── gdrive.h
│   │   │   ├── gdtlsclientconnection.h
│   │   │   ├── gdtlsconnection.h
│   │   │   ├── gdtlsserverconnection.h
│   │   │   ├── gemblem.h
│   │   │   ├── gemblemedicon.h
│   │   │   ├── gfile.h
│   │   │   ├── gfileattribute.h
│   │   │   ├── gfileenumerator.h
│   │   │   ├── gfileicon.h
│   │   │   ├── gfileinfo.h
│   │   │   ├── gfileinputstream.h
│   │   │   ├── gfileiostream.h
│   │   │   ├── gfilemonitor.h
│   │   │   ├── gfilenamecompleter.h
│   │   │   ├── gfileoutputstream.h
│   │   │   ├── gfilterinputstream.h
│   │   │   ├── gfilteroutputstream.h
│   │   │   ├── gicon.h
│   │   │   ├── ginetaddress.h
│   │   │   ├── ginetaddressmask.h
│   │   │   ├── ginetsocketaddress.h
│   │   │   ├── ginitable.h
│   │   │   ├── ginputstream.h
│   │   │   ├── gio-autocleanups.h
│   │   │   ├── gio-visibility.h
│   │   │   ├── gio.h
│   │   │   ├── gioenums.h
│   │   │   ├── gioenumtypes.h
│   │   │   ├── gioerror.h
│   │   │   ├── giomodule.h
│   │   │   ├── gioscheduler.h
│   │   │   ├── giostream.h
│   │   │   ├── giotypes.h
│   │   │   ├── glistmodel.h
│   │   │   ├── gliststore.h
│   │   │   ├── gloadableicon.h
│   │   │   ├── gmemoryinputstream.h
│   │   │   ├── gmemorymonitor.h
│   │   │   ├── gmemoryoutputstream.h
│   │   │   ├── gmenu.h
│   │   │   ├── gmenuexporter.h
│   │   │   ├── gmenumodel.h
│   │   │   ├── gmount.h
│   │   │   ├── gmountoperation.h
│   │   │   ├── gnativesocketaddress.h
│   │   │   ├── gnativevolumemonitor.h
│   │   │   ├── gnetworkaddress.h
│   │   │   ├── gnetworking.h
│   │   │   ├── gnetworkmonitor.h
│   │   │   ├── gnetworkservice.h
│   │   │   ├── gnotification.h
│   │   │   ├── goutputstream.h
│   │   │   ├── gpermission.h
│   │   │   ├── gpollableinputstream.h
│   │   │   ├── gpollableoutputstream.h
│   │   │   ├── gpollableutils.h
│   │   │   ├── gpowerprofilemonitor.h
│   │   │   ├── gpropertyaction.h
│   │   │   ├── gproxy.h
│   │   │   ├── gproxyaddress.h
│   │   │   ├── gproxyaddressenumerator.h
│   │   │   ├── gproxyresolver.h
│   │   │   ├── gremoteactiongroup.h
│   │   │   ├── gresolver.h
│   │   │   ├── gresource.h
│   │   │   ├── gseekable.h
│   │   │   ├── gsettings.h
│   │   │   ├── gsettingsbackend.h
│   │   │   ├── gsettingsschema.h
│   │   │   ├── gsimpleaction.h
│   │   │   ├── gsimpleactiongroup.h
│   │   │   ├── gsimpleasyncresult.h
│   │   │   ├── gsimpleiostream.h
│   │   │   ├── gsimplepermission.h
│   │   │   ├── gsimpleproxyresolver.h
│   │   │   ├── gsocket.h
│   │   │   ├── gsocketaddress.h
│   │   │   ├── gsocketaddressenumerator.h
│   │   │   ├── gsocketclient.h
│   │   │   ├── gsocketconnectable.h
│   │   │   ├── gsocketconnection.h
│   │   │   ├── gsocketcontrolmessage.h
│   │   │   ├── gsocketlistener.h
│   │   │   ├── gsocketservice.h
│   │   │   ├── gsrvtarget.h
│   │   │   ├── gsubprocess.h
│   │   │   ├── gsubprocesslauncher.h
│   │   │   ├── gtask.h
│   │   │   ├── gtcpconnection.h
│   │   │   ├── gtcpwrapperconnection.h
│   │   │   ├── gtestdbus.h
│   │   │   ├── gthemedicon.h
│   │   │   ├── gthreadedsocketservice.h
│   │   │   ├── gtlsbackend.h
│   │   │   ├── gtlscertificate.h
│   │   │   ├── gtlsclientconnection.h
│   │   │   ├── gtlsconnection.h
│   │   │   ├── gtlsdatabase.h
│   │   │   ├── gtlsfiledatabase.h
│   │   │   ├── gtlsinteraction.h
│   │   │   ├── gtlspassword.h
│   │   │   ├── gtlsserverconnection.h
│   │   │   ├── gunixconnection.h
│   │   │   ├── gunixcredentialsmessage.h
│   │   │   ├── gunixfdlist.h
│   │   │   ├── gunixsocketaddress.h
│   │   │   ├── gvfs.h
│   │   │   ├── gvolume.h
│   │   │   ├── gvolumemonitor.h
│   │   │   ├── gzlibcompressor.h
│   │   │   └── gzlibdecompressor.h
│   │   ├── glib
│   │   │   ├── deprecated
│   │   │   │   ├── gallocator.h
│   │   │   │   ├── gcache.h
│   │   │   │   ├── gcompletion.h
│   │   │   │   ├── gmain.h
│   │   │   │   ├── grel.h
│   │   │   │   └── gthread.h
│   │   │   ├── galloca.h
│   │   │   ├── garray.h
│   │   │   ├── gasyncqueue.h
│   │   │   ├── gatomic.h
│   │   │   ├── gbacktrace.h
│   │   │   ├── gbase64.h
│   │   │   ├── gbitlock.h
│   │   │   ├── gbookmarkfile.h
│   │   │   ├── gbytes.h
│   │   │   ├── gcharset.h
│   │   │   ├── gchecksum.h
│   │   │   ├── gconvert.h
│   │   │   ├── gdataset.h
│   │   │   ├── gdate.h
│   │   │   ├── gdatetime.h
│   │   │   ├── gdir.h
│   │   │   ├── genviron.h
│   │   │   ├── gerror.h
│   │   │   ├── gfileutils.h
│   │   │   ├── ggettext.h
│   │   │   ├── ghash.h
│   │   │   ├── ghmac.h
│   │   │   ├── ghook.h
│   │   │   ├── ghostutils.h
│   │   │   ├── gi18n-lib.h
│   │   │   ├── gi18n.h
│   │   │   ├── giochannel.h
│   │   │   ├── gkeyfile.h
│   │   │   ├── glib-autocleanups.h
│   │   │   ├── glib-typeof.h
│   │   │   ├── glib-visibility.h
│   │   │   ├── glist.h
│   │   │   ├── gmacros.h
│   │   │   ├── gmain.h
│   │   │   ├── gmappedfile.h
│   │   │   ├── gmarkup.h
│   │   │   ├── gmem.h
│   │   │   ├── gmessages.h
│   │   │   ├── gnode.h
│   │   │   ├── goption.h
│   │   │   ├── gpathbuf.h
│   │   │   ├── gpattern.h
│   │   │   ├── gpoll.h
│   │   │   ├── gprimes.h
│   │   │   ├── gprintf.h
│   │   │   ├── gqsort.h
│   │   │   ├── gquark.h
│   │   │   ├── gqueue.h
│   │   │   ├── grand.h
│   │   │   ├── grcbox.h
│   │   │   ├── grefcount.h
│   │   │   ├── grefstring.h
│   │   │   ├── gregex.h
│   │   │   ├── gscanner.h
│   │   │   ├── gsequence.h
│   │   │   ├── gshell.h
│   │   │   ├── gslice.h
│   │   │   ├── gslist.h
│   │   │   ├── gspawn.h
│   │   │   ├── gstdio.h
│   │   │   ├── gstrfuncs.h
│   │   │   ├── gstring.h
│   │   │   ├── gstringchunk.h
│   │   │   ├── gstrvbuilder.h
│   │   │   ├── gtestutils.h
│   │   │   ├── gthread.h
│   │   │   ├── gthreadpool.h
│   │   │   ├── gtimer.h
│   │   │   ├── gtimezone.h
│   │   │   ├── gtrashstack.h
│   │   │   ├── gtree.h
│   │   │   ├── gtypes.h
│   │   │   ├── gunicode.h
│   │   │   ├── guri.h
│   │   │   ├── gutils.h
│   │   │   ├── guuid.h
│   │   │   ├── gvariant.h
│   │   │   ├── gvarianttype.h
│   │   │   ├── gversion.h
│   │   │   ├── gversionmacros.h
│   │   │   └── gwin32.h
│   │   ├── glib-object.h
│   │   ├── glib-unix.h
│   │   ├── glib.h
│   │   ├── gmodule
│   │   │   └── gmodule-visibility.h
│   │   ├── gmodule.h
│   │   └── gobject
│   │       ├── gbinding.h
│   │       ├── gbindinggroup.h
│   │       ├── gboxed.h
│   │       ├── gclosure.h
│   │       ├── genums.h
│   │       ├── glib-enumtypes.h
│   │       ├── glib-types.h
│   │       ├── gmarshal.h
│   │       ├── gobject-autocleanups.h
│   │       ├── gobject-visibility.h
│   │       ├── gobject.h
│   │       ├── gobjectnotifyqueue.c
│   │       ├── gparam.h
│   │       ├── gparamspecs.h
│   │       ├── gsignal.h
│   │       ├── gsignalgroup.h
│   │       ├── gsourceclosure.h
│   │       ├── gtype.h
│   │       ├── gtypemodule.h
│   │       ├── gtypeplugin.h
│   │       ├── gvalue.h
│   │       ├── gvaluearray.h
│   │       ├── gvaluecollector.h
│   │       └── gvaluetypes.h
│   ├── iconv.h
│   ├── jbig.h
│   ├── jconfig.h
│   ├── jerror.h
│   ├── jmorecfg.h
│   ├── jpegint.h
│   ├── jpeglib.h
│   ├── lcms2.h
│   ├── lcms2_plugin.h
│   ├── libcharset.h
│   ├── libdeflate.h
│   ├── libelf
│   │   ├── elf_repl.h
│   │   ├── gelf.h
│   │   ├── libelf.h
│   │   ├── nlist.h
│   │   └── sys_elf.h
│   ├── libelf.h
│   ├── libintl.h
│   ├── localcharset.h
│   ├── lzma
│   │   ├── base.h
│   │   ├── bcj.h
│   │   ├── block.h
│   │   ├── check.h
│   │   ├── container.h
│   │   ├── delta.h
│   │   ├── filter.h
│   │   ├── hardware.h
│   │   ├── index.h
│   │   ├── index_hash.h
│   │   ├── lzma12.h
│   │   ├── stream_flags.h
│   │   ├── version.h
│   │   └── vli.h
│   ├── lzma.h
│   ├── nlist.h
│   ├── pcre2.h
│   ├── pcre2posix.h
│   ├── spng.h
│   ├── tiff.h
│   ├── tiffconf.h
│   ├── tiffio.h
│   ├── tiffio.hxx
│   ├── tiffvers.h
│   ├── transupp.h
│   ├── vips
│   │   ├── VConnection8.h
│   │   ├── VError8.h
│   │   ├── VImage8.h
│   │   ├── VInterpolate8.h
│   │   ├── VRegion8.h
│   │   ├── almostdeprecated.h
│   │   ├── arithmetic.h
│   │   ├── basic.h
│   │   ├── buf.h
│   │   ├── colour.h
│   │   ├── connection.h
│   │   ├── conversion.h
│   │   ├── convolution.h
│   │   ├── create.h
│   │   ├── dbuf.h
│   │   ├── debug.h
│   │   ├── deprecated.h
│   │   ├── dispatch.h
│   │   ├── draw.h
│   │   ├── enumtypes.h
│   │   ├── error.h
│   │   ├── foreign.h
│   │   ├── format.h
│   │   ├── freqfilt.h
│   │   ├── gate.h
│   │   ├── generate.h
│   │   ├── header.h
│   │   ├── histogram.h
│   │   ├── image.h
│   │   ├── interpolate.h
│   │   ├── intl.h
│   │   ├── mask.h
│   │   ├── memory.h
│   │   ├── morphology.h
│   │   ├── mosaicing.h
│   │   ├── object.h
│   │   ├── operation.h
│   │   ├── private.h
│   │   ├── rect.h
│   │   ├── region.h
│   │   ├── resample.h
│   │   ├── sbuf.h
│   │   ├── semaphore.h
│   │   ├── thread.h
│   │   ├── threadpool.h
│   │   ├── transform.h
│   │   ├── type.h
│   │   ├── util.h
│   │   ├── vector.h
│   │   ├── version.h
│   │   ├── video.h
│   │   ├── vips.h
│   │   ├── vips7compat.h
│   │   └── vips8
│   ├── webp
│   │   ├── decode.h
│   │   ├── demux.h
│   │   ├── encode.h
│   │   ├── mux.h
│   │   ├── mux_types.h
│   │   ├── sharpyuv
│   │   │   ├── sharpyuv.h
│   │   │   └── sharpyuv_csp.h
│   │   └── types.h
│   ├── zconf.h
│   ├── zdict.h
│   ├── zlib.h
│   ├── zstd.h
│   └── zstd_errors.h
├── x86
│   ├── libbz2.so
│   ├── libcharset.so
│   ├── libcpufeatures-webp.a
│   ├── libdeflate.so
│   ├── libelf.a
│   ├── libexpat.so
│   ├── libffi.so
│   ├── libfftw3.so
│   ├── libgio-2.0.so
│   ├── libglib-2.0.so
│   ├── libgmodule-2.0.so
│   ├── libgnuintl.a
│   ├── libgobject-2.0.so
│   ├── libgthread-2.0.so
│   ├── libiconv.so
│   ├── libjbig.so
│   ├── libjpeg.so
│   ├── liblcms2.so
│   ├── liblzma.so
│   ├── libpcre2-16.so
│   ├── libpcre2-32.so
│   ├── libpcre2-8.so
│   ├── libpcre2-posix.so
│   ├── libsharpyuv.so
│   ├── libspng.so
│   ├── libtiff.so
│   ├── libtiffxx.so
│   ├── libvips-cpp.so
│   ├── libvips.so
│   ├── libwebp.so
│   ├── libwebpdecoder.so
│   ├── libwebpdemux.so
│   ├── libwebpmux.so
│   ├── libz.so
│   └── libzstd.so
└── x86_64
    ├── libbz2.so
    ├── libcharset.so
    ├── libcpufeatures-webp.a
    ├── libdeflate.so
    ├── libelf.a
    ├── libexpat.so
    ├── libffi.so
    ├── libfftw3.so
    ├── libgio-2.0.so
    ├── libglib-2.0.so
    ├── libgmodule-2.0.so
    ├── libgnuintl.a
    ├── libgobject-2.0.so
    ├── libgthread-2.0.so
    ├── libiconv.so
    ├── libjbig.so
    ├── libjpeg.so
    ├── liblcms2.so
    ├── liblzma.so
    ├── libpcre2-16.so
    ├── libpcre2-32.so
    ├── libpcre2-8.so
    ├── libpcre2-posix.so
    ├── libsharpyuv.so
    ├── libspng.so
    ├── libtiff.so
    ├── libtiffxx.so
    ├── libvips-cpp.so
    ├── libvips.so
    ├── libwebp.so
    ├── libwebpdecoder.so
    ├── libwebpdemux.so
    ├── libwebpmux.so
    ├── libz.so
    └── libzstd.so

19 directories, 543 files

```

</details>

[release]: https://github.com/CaiJingLong/libvips_android_script/releases
