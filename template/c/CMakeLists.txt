cmake_minimum_required(VERSION 3.10)

set(TOOLCHAIN_FILE "toolchain.cmake")

if(CMAKE_TOOLCHAIN_FILE)
    message(STATUS "Using toolchain file: ${CMAKE_TOOLCHAIN_FILE}.")
elseif(EXISTS ${TOOLCHAIN_FILE})
    set(CMAKE_TOOLCHAIN_FILE ${TOOLCHAIN_FILE})
    message(STATUS "Using default toolchain file.")
endif()

project(example LANGUAGES C CXX)

# 更详细的编译信息
# set(CMAKE_VERBOSE_MAKEFILE on)

# 添加编译参数
add_compile_options(-Wall -fdata-sections -ffunction-sections)

# 开启测试功能
enable_testing()

set(LIBCRC_DIR libcrc)
include(${LIBCRC_DIR}/libcrc.cmake)
