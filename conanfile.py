from conans import ConanFile, tools
import os


class BoostIostreamsConan(ConanFile):
    name = "Boost.Iostreams"
    version = "1.64.0"
    generators = "boost" 
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-iostreams"
    description = "Please visit http://www.boost.org/doc/libs/1_64_0/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["iostreams"]
    options = {"shared": [True, False], 'use_zlib': [True, False], 'use_bzip2': [True, False]}
    default_options = "shared=False", "use_zlib=True", "use_bzip2=True"
    build_requires = "Boost.Generator/1.64.0@bincrafters/stable"
    requires =  "Boost.Assert/1.64.0@bincrafters/stable", \
                      "Boost.Bind/1.64.0@bincrafters/stable", \
                      "Boost.Config/1.64.0@bincrafters/stable", \
                      "Boost.Core/1.64.0@bincrafters/stable", \
                      "Boost.Detail/1.64.0@bincrafters/stable", \
                      "Boost.Function/1.64.0@bincrafters/stable", \
                      "Boost.Integer/1.64.0@bincrafters/stable", \
                      "Boost.Mpl/1.64.0@bincrafters/stable", \
                      "Boost.Preprocessor/1.64.0@bincrafters/stable", \
                      "Boost.Random/1.64.0@bincrafters/stable", \
                      "Boost.Range/1.64.0@bincrafters/stable", \
                      "Boost.Regex/1.64.0@bincrafters/stable", \
                      "Boost.Smart_Ptr/1.64.0@bincrafters/stable", \
                      "Boost.Static_Assert/1.64.0@bincrafters/stable", \
                      "Boost.Throw_Exception/1.64.0@bincrafters/stable", \
                      "Boost.Type_Traits/1.64.0@bincrafters/stable", \
                      "Boost.Utility/1.64.0@bincrafters/stable"

                      #assert1 bind3 config0 core2 detail5 function5 integer3 mpl5 preprocessor0 random9 range7 regex6 smart_ptr4 static_assert1 throw_exception2 type_traits3 utility5
                      
    def requirements(self):
        if not self.options.shared:
            if self.options.use_bzip2:
                self.requires("bzip2/1.0.6@conan/stable")
            if self.options.use_zlib:
                self.requires("zlib/1.2.11@conan/stable")

    def configure(self):
        if self.options.use_bzip2:
            self.options["bzip"].shared = False
        if self.options.use_zlib:
            self.options["zlib"].shared = False

    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version
        for lib_short_name in self.lib_short_names:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command)
        
    def package(self):
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)		

        self.copy(pattern="*", dst="lib", src="stage/lib")

    def package_info(self):
        self.user_info.lib_short_names = (",").join(self.lib_short_names)
        self.cpp_info.libs = tools.collect_libs(self)

