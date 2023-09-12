# {algorithm}
file(GLOB {algorithm}_srcs "*.c")
add_library({algorithm} STATIC ${{{algorithm}_srcs}})
target_include_directories({algorithm} PUBLIC .)
