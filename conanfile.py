#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
import shutil

class LibmodbusConan(ConanFile):
    name = "libmodbus"
    version = "3.1.6"
    license = "LGPL-2.1"
    url = "https://github.com/joakimono/conan-libmodbus"
    homepage = "http://libmodbus.org"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    description = "libmodbus is a free software library to send/receive data with a device which respects the Modbus protocol."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports_sources = ["extra/*" , "CMakeLists.txt"]
    source_subfolder = "libmodbus"
    build_subfolder = "build_subfolder"

    def source(self):

        self.run("git clone --depth 1 -b v{0} https://github.com/stephane/libmodbus.git".format(self.version))
        #self.run("git clone https://github.com/stephane/libmodbus.git")
        #self.run("cd {} && git checkout df7d633fd98a1cfaf698d41af50ddd095e64d053".format(self.source_subfolder))

    def build(self):
        if self.settings.compiler == "Visual Studio":
            shutil.move(self.source_folder + "/CMakeLists.txt",
                        self.source_folder + "/{}/CMakeLists.txt".format(self.source_subfolder))
            shutil.move(self.source_folder + "/extra/win_config.h",
                        self.source_folder + "/{}/config.h".format(self.source_subfolder))
            shutil.move(self.source_folder + "/extra/project-config.cmake.in",
                        self.source_folder + "/{}/project-config.cmake.in".format(self.source_subfolder))
            tools.patch(patch_file = self.source_folder + "/extra/modbus.patch",
                        base_path=self.source_subfolder)
            cmake = CMake(self)
            cmake.configure(source_folder=self.source_subfolder, build_folder = self.build_subfolder)
            cmake.build()
            cmake.install()
        else:
            if self.options.shared:
                shared_static = "--enable-host-shared --prefix "
            else:
                shared_static = "--enable-static --disable-shared --prefix "
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True
            with tools.environment_append(env_build.vars):
                self.run("cd {} && ./autogen.sh".format(self.source_subfolder))
                self.run("cd {} && ./configure {}{}".format(self.source_subfolder,
                                                            shared_static,
                                                            self.package_folder))
                self.run("cd {} && make".format(self.source_subfolder))
                self.run("cd {} && make install".format(self.source_subfolder))

    def package(self):
        self.copy("COPYING.LESSER", dst="licenses", src=self.source_subfolder,
                  ignore_case=True, keep_path=False)

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            if self.options.shared == True:
                self.cpp_info.libs = ["modbus"]
            else:
                self.cpp_info.libs = ["libmodbus", "ws2_32"]
                self.cpp_info.defines = ["LIBMODBUS_STATICBUILD"]
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += '_d'
        else:
            self.cpp_info.libs = ["modbus"]
        self.cpp_info.includedirs = ["include"]

    def configure(self):
        del self.settings.compiler.libcxx
