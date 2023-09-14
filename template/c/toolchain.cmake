set(CMAKE_SYSTEM_NAME Generic)

# 选择编译版本（可以通过 vscode 指定）
set(CMAKE_BUILD_TYPE Release)
# set(CMAKE_BUILD_TYPE Debug)

# 交叉编译器（可以通过 vscode 指定）
set(CMAKE_C_COMPILER "gcc")
# set(CMAKE_CXX_COMPILER "g++")

set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-fPIC")
set(CMAKE_C_FLAGS_DEBUG "-O2 -g -D DEBUG")
set(CMAKE_C_FLAGS_RELEASE "-Os")

# set(CMAKE_EXE_LINKER_FLAGS "--specs=nosys.specs")

# 存放可执行软件的目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
# 默认存放静态库的文件夹位置
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
# 默认存放动态库的文件夹位置
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
