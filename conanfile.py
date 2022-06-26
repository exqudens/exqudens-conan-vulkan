from os import path
from traceback import format_exc
from logging import error
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class ConanConfiguration(ConanFile):
    settings = {
        "arch": ["x86_64", "x86"],
        "os": ["Windows"],
        "compiler": {
            "Visual Studio": {
                "version": ["15", "16", "17"],
                "runtime": ["MD"]
            }
        },
        "build_type": ["Release"]
    }
    options = {"shared": [True, False]}
    default_options = {"shared": True}

    def set_name(self):
        try:
            self.name = tools.load(path.join(path.dirname(path.abspath(__file__)), "name-version.txt")).split(':')[0].strip()
        except Exception as e:
            error(format_exc())
            raise e

    def set_version(self):
        try:
            self.version = tools.load(path.join(path.dirname(path.abspath(__file__)), "name-version.txt")).split(':')[1].strip()
        except Exception as e:
            error(format_exc())
            raise e

    def package(self):
        try:
            if (
                self.settings.arch == "x86"
                and self.settings.os == "Windows"
                and self.settings.compiler == "Visual Studio"
                and self.settings.compiler.version == 16
                and self.settings.compiler.runtime == "MD"
                and self.settings.build_type == "Release"
                and self.options.shared
            ):
                self.copy(src="build/VulkanSDK-{}/Include".format(self.version), pattern="*.*", dst="include")
                self.copy(src="build/VulkanSDK-{}/Lib32".format(self.version), pattern="*.*", dst="lib")
                self.copy(src="build/VulkanSDK-{}/Bin32".format(self.version), pattern="*.*", dst="bin")
                self.copy(src="build/VulkanSDK-{}/Config".format(self.version), pattern="*.*", dst="config")
                self.copy(src="build/VulkanSDK-{}/Tools32".format(self.version), pattern="*.*", dst="tools")
            elif (
                self.settings.arch == "x86_64"
                and self.settings.os == "Windows"
                and self.settings.compiler == "Visual Studio"
                and self.settings.compiler.version == 16
                and self.settings.compiler.runtime == "MD"
                and self.settings.build_type == "Release"
                and self.options.shared
            ):
                self.copy(src="build/VulkanSDK-{}/Include".format(self.version), pattern="*.*", dst="include")
                self.copy(src="build/VulkanSDK-{}/Lib".format(self.version), pattern="*.*", dst="lib")
                self.copy(src="build/VulkanSDK-{}/Bin".format(self.version), pattern="*.*", dst="bin")
                self.copy(src="build/VulkanSDK-{}/Config".format(self.version), pattern="*.*", dst="config")
                self.copy(src="build/VulkanSDK-{}/Tools".format(self.version), pattern="*.*", dst="tools")
            else:
                raise ConanInvalidConfiguration(
                    "Unsupported"
                    + " 'self.settings.arch' = '" + str(self.settings.arch) + "'"
                    + " 'self.settings.os' = '" + str(self.settings.os) + "'"
                    + " 'self.settings.compiler' = '" + str(self.settings.compiler) + "'"
                    + " 'self.settings.compiler.version' = '" + str(self.settings.compiler.version) + "'"
                    + " 'self.settings.compiler.runtime' = '" + str(self.settings.compiler.runtime) + "'"
                    + " 'self.settings.build_type' = '" + str(self.settings.build_type) + "'"
                    + " 'self.options.shared' = '" + str(self.options.shared) + "'"
                )
        except Exception as e:
            error(format_exc())
            raise e

    def package_info(self):
        try:
            self.cpp_info.names["cmake_find_package"] = "Vulkan"
            self.cpp_info.libs = ["vulkan-1.lib"]
        except Exception as e:
            error(format_exc())
            raise e


if __name__ == "__main__":
    pass
