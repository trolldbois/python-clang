cmake_minimum_required(VERSION 3.15)
project(clang NONE)

include(ExternalProject)

include(llvm_version.cmake)

# Set the URL and local paths
set(CLANG_TARBALL_URL "https://github.com/llvm/llvm-project/releases/download/llvmorg-${LLVM_VERSION}/clang-${LLVM_VERSION}.src.tar.xz")
set(CLANG_TARBALL "${CMAKE_BINARY_DIR}/clang-${LLVM_VERSION}.src.tar.xz")
set(CLANG_SOURCE_DIR "${CMAKE_BINARY_DIR}/clang-src")
set(PYTHON_BINDINGS_OUTPUT "${CLANG_SOURCE_DIR}/bindings/python/clang/")

# Download the tarball using ExternalProject_Add
ExternalProject_Add(clang
    URL ${CLANG_TARBALL_URL}
    URL_HASH SHA256=${LLVM_SHA256}
    DOWNLOAD_DIR ${CMAKE_BINARY_DIR}
    SOURCE_DIR ${CLANG_SOURCE_DIR}
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    LOG_DOWNLOAD OFF
    DOWNLOAD_EXTRACT_TIMESTAMP ON
)

# Define installation so that scikit-build packages the python files into the wheel
install(DIRECTORY ${PYTHON_BINDINGS_OUTPUT} DESTINATION clang USE_SOURCE_PERMISSIONS)