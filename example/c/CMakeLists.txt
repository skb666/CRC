cmake_minimum_required(VERSION 3.10)

set(CMAKE_SYSTEM_NAME Generic)

# 选择编译版本（可以通过 vscode 指定）
set(CMAKE_BUILD_TYPE Release)
# set(CMAKE_BUILD_TYPE Debug)

# 交叉编译器（可以通过 vscode 指定）
# set(CMAKE_C_COMPILER "gcc")
# set(CMAKE_CXX_COMPILER "g++")

set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-fPIC")
set(CMAKE_C_FLAGS_DEBUG "-O2 -g -D DEBUG")
set(CMAKE_C_FLAGS_RELEASE "-Os")

project(example LANGUAGES C CXX)

# 更详细的编译信息
# set(CMAKE_VERBOSE_MAKEFILE on)

# 存放可执行软件的目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
# 默认存放静态库的文件夹位置
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
# 默认存放动态库的文件夹位置
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})

# 添加编译参数
add_compile_options(-Wall -fdata-sections -ffunction-sections)

# 递归调用子文件的 CMakeLists.txt
add_subdirectory(crc)

# example
add_executable(example example.c)
target_link_libraries(example crc)

# 编译后执行
add_custom_command(
    TARGET example POST_BUILD
    COMMAND ./example
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)
