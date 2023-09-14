# 递归调用子文件的 CMakeLists.txt
add_subdirectory(crc)

# test
file(GLOB test_{algorithm}_srcs "*.c")
add_executable(test_{algorithm} ${{test_{algorithm}_srcs}})
target_link_libraries(test_{algorithm} PRIVATE {algorithm})
add_dependencies(test_{algorithm} {algorithm})

# 单元测试
add_test(
    NAME test_{algorithm}
    COMMAND ./test_{algorithm}
    WORKING_DIRECTORY ${{PROJECT_SOURCE_DIR}}/bin
)
