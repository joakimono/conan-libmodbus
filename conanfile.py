from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
import shutil

class LibmodbusConan(ConanFile):
    name = "libmodbus"
    version = "3.1.4p1"
    license = "LGPL-2.1"
    url = "https://github.com/joakimono/conan-libmodbus"
    homepage = "http://libmodbus.org"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    description = "libmodbus is a free software library to send/receive data with a device which respects the Modbus protocol."
    settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports_sources = "extra/*" , "CMakeLists.txt"

    def source(self):
    
        # Using a patched 3.1.4p1, which is similar to 3.1.4, but with some more commits (bug fixes.)
        #self.run("git clone --depth 1 -b v{0} https://github.com/stephane/libmodbus.git".format(self.version))
        self.run("git clone https://github.com/stephane/libmodbus.git")
        self.run("cd libmodbus && git checkout df7d633fd98a1cfaf698d41af50ddd095e64d053") 
        
    def build(self):
        if self.settings.os == "Windows":
            shutil.move(self.source_folder + "/CMakeLists.txt", 
                        self.source_folder + "/libmodbus/CMakeLists.txt")
            shutil.move(self.source_folder + "/extra/win_config.h", 
                        self.source_folder + "/libmodbus/config.h")
            shutil.move(self.source_folder + "/extra/project-config.cmake.in",
                        self.source_folder + "/libmodbus/project-config.cmake.in")
            tools.patch(patch_file = self.source_folder + "/extra/modbus.patch", 
                        base_path="libmodbus")
            cmake = CMake(self)
            cmake.configure(source_folder=self.source_folder + "/libmodbus")
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
                self.run("cd libmodbus && ./autogen.sh")
                self.run("cd libmodbus && ./configure {}{}".format(shared_static, self.package_folder))
                self.run("cd libmodbus && make")
                self.run("cd libmodbus && make install") 

    def package(self):
        self.copy("COPYING.LESSER", dst="licenses", src="libmodbus",
                  ignore_case=True, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared == True:
                self.cpp_info.libs = ["modbus"]
            else:
                self.cpp_info.libs = ["libmodbus", "ws2_32"]
                self.cpp_info.defines = ["LIBMODBUS_STATICBUILD"]
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += '_d'
        else:
            self.cpp_info.libs = ["modbus"]
        self.cpp_info.includedirs =["include/modbus"]

    def configure(self):
        del self.settings.compiler.libcxx
