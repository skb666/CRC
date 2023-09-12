# crc
file(GLOB_RECURSE CRC_SRCS "*.c")
add_library(crc STATIC ${CRC_SRCS})
target_include_directories(crc PUBLIC .)
