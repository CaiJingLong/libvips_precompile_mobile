from conan import ConanFile


class DepLibVips(ConanFile):
    name = "hello"
    version = "1.0"

    def requirements(self):
        # self.build_requires('make/4.4')
        # self.requires('libiconv/1.17')
        self.requires('libgettext/0.22')
        # self.requires('pcre2/10.42')
        self.requires('glib/2.78.3')
        self.requires('libvips/8.14.2')
        # self.requires('libtiff/4.6.0')
        # self.requires("libiconv/1.17")
        # self.requires('giflib/5.2.1')
        # self.requires('ffmpeg/5.1')
