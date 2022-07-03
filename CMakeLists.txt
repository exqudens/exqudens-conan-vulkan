cmake_minimum_required(VERSION 3.21 FATAL_ERROR)
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.txt" INFO)
string(REPLACE ":" ";" INFO_LIST "${INFO}")
list(GET INFO_LIST 0 RAW_NAME)
list(GET INFO_LIST 1 RAW_VERSION)
string(STRIP "${RAW_NAME}" NAME)
string(STRIP "${RAW_VERSION}" VERSION)
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message("project: '${PROJECT_NAME}-${PROJECT_VERSION}'")

find_program(CONAN_COMMAND NAMES "conan.exe" "conan" REQUIRED)

if(NOT EXISTS "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}-Installer.exe")
    file(DOWNLOAD
        #"https://sdk.lunarg.com/sdk/download/${PROJECT_VERSION}/windows/VulkanSDK-${PROJECT_VERSION}-Installer.exe"
        "file:///C:/install/VulkanSDK-${PROJECT_VERSION}-Installer.exe"
        "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}-Installer.exe"
        EXPECTED_MD5 "13464d539a0a30392637fc30011aae41"
    )
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}")
    file(MAKE_DIRECTORY "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}")
    if("Windows" STREQUAL "${CMAKE_HOST_SYSTEM_NAME}")
        find_program(7Z_COMMAND NAMES "7z.exe" "7z" REQUIRED)
        execute_process(
            COMMAND "${7Z_COMMAND}" "x" "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}-Installer.exe"
            WORKING_DIRECTORY "${PROJECT_BINARY_DIR}/VulkanSDK-${PROJECT_VERSION}"
            COMMAND_ECHO "STDOUT"
            ENCODING "UTF-8"
            COMMAND_ERROR_IS_FATAL ANY
        )
    endif()
endif()

execute_process(
    COMMAND "${CONAN_COMMAND}" "search" "${PROJECT_NAME}/${PROJECT_VERSION}"
    OUTPUT_VARIABLE "CONAN_SEARCH_RESULT"
    COMMAND_ECHO "STDOUT"
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ENCODING "UTF-8"
    COMMAND_ERROR_IS_FATAL ANY
)

if("${CONAN_SEARCH_RESULT}" MATCHES "Existing package recipes.+")
    string(REPLACE ":" ";" CONAN_SEARCH_RESULT "${CONAN_SEARCH_RESULT}")
    list(GET CONAN_SEARCH_RESULT 1 CONAN_SEARCH_RESULT)
    string(STRIP ${CONAN_SEARCH_RESULT} CONAN_SEARCH_RESULT)
    message("Existing package recipes: ${CONAN_SEARCH_RESULT}")
    return()
endif()

execute_process(
    COMMAND "${CONAN_COMMAND}"
            export
            "conanfile.py"
            #${CONAN_PACKAGE_USER_CHANNEL}
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
)

foreach(arch "x86" "x86_64")
    foreach(os "Windows")
        foreach(compiler "Visual Studio")
            foreach(build_type "Release")
                foreach(shared "True")
                    if("Visual Studio" STREQUAL "${compiler}")
                        foreach(compiler_version "16")
                            set(type "shared")
                            set(compiler_runtime "MD")
                            if("False" STREQUAL "${shared}")
                                set(type "static")
                                set(compiler_runtime "MT")
                            endif()
                            string(JOIN " AND " CONAN_REMOVE_QUERY
                                "arch=${arch}"
                                "os=Windows"
                                "compiler=\"Visual Studio\""
                                "compiler.version=${compiler_version}"
                                "compiler.runtime=${compiler_runtime}"
                                "build_type=Release"
                                "shared=${shared}"
                            )
                            execute_process(
                                COMMAND "${CONAN_COMMAND}" remove --force "${PROJECT_NAME}/${PROJECT_VERSION}@" --query "${CONAN_REMOVE_QUERY}"
                                WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                            )
                            set(CONAN_EXPORT_ARGS
                                "-s" "arch=${arch}"
                                "-s" "os=Windows"
                                "-s" "compiler=Visual Studio"
                                "-s" "compiler.version=${compiler_version}"
                                "-s" "compiler.runtime=${compiler_runtime}"
                                "-s" "build_type=Release"
                                "-o" "shared=${shared}"
                            )
                            execute_process(
                                COMMAND "${CONAN_COMMAND}"
                                        export-pkg
                                        "conanfile.py"
                                        #${CONAN_PACKAGE_USER_CHANNEL}
                                        ${CONAN_EXPORT_ARGS}
                                WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                            )
                        endforeach()
                    endif()
                endforeach()
            endforeach()
        endforeach()
    endforeach()
endforeach()

execute_process(
    COMMAND "${CMAKE_COMMAND}" -E echo "BUILD_SUCCESSFUL"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
)
