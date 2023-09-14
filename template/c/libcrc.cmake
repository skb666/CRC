function(append_srcs_dir out_var)
    set(listVar ${${out_var}})
    foreach(f ${ARGN})
        aux_source_directory(${f} tmp)
        list(APPEND listVar ${tmp})
    endforeach(f)
    set(${out_var} "${listVar}" PARENT_SCOPE)
endfunction()

# 获取目录下的子目录名
# subdirnamelist 子目录名称列表，输出变量，调用处定义，填充时不能加${}
# targetdir      目标路径，为全路径
macro(SUBDIRNAMELIST_MACRO subdirnamelist targetdir)
    # message(STATUS "macro subdirnamelist = ${subdirnamelist}")
    # message(STATUS "macro targetdir = ${targetdir}")
    file(GLOB children ${targetdir}/*) # 获取目标路径下的内容，深度为1
    # message(STATUS "macro children = ${children}")
    set(dirlist "")
    foreach(child ${children})
        file(RELATIVE_PATH child_name ${targetdir} ${child}) # 通过相对路径计算获取名称
        # message(STATUS "macro child = ${child_name}")
        # message(STATUS "targetdir/child = ${targetdir}/${child_name}")
        if(IS_DIRECTORY ${targetdir}/${child_name})
            # message(STATUS "yes dir : targetdir/child = ${targetdir}/${child_name}")
            list(APPEND dirlist ${child_name})
        endif()
    endforeach()
    list(APPEND ${subdirnamelist} ${dirlist})
    # message(STATUS "macro dirlist = ${dirlist}")
    # message(STATUS "macro subdirnamelist = ${subdirnamelist}")
endmacro()
 
# 获取目录下是否有CMakeLists
# hascmakelist 是否含有CMakeLists.txt，输出变量，调用处定义，填充时不能加${}
# targetdir    目标路径，为全路径
macro(CHECK_DIR_HAS_CMAKELIST hascmakelist targetdir)
    # message(STATUS "macro check has cmakelist targetdir = ${targetdir}")
    set(${hascmakelist} FALSE)
    if(IS_DIRECTORY ${targetdir})
        # message(STATUS "macro check has cmakelist is dir, targetdir = ${targetdir}")
        if(EXISTS ${targetdir}/CMakeLists.txt)
            set(${hascmakelist} TRUE)
        endif()
    else()
        message(FATAL_ERROR "Invalid dir para: targetdir = ${targetdir}")
    endif()
endmacro()
 
# 为含有CMakeList的子目录添加add_subdirectory调用
# 自动识别调用处所在目录有哪些子目录，并为还有CMakeLists.txt的子目录添加add_sundirectory调用
macro(CRC_ALG_COLLECT crc_dir crc_alg_name crc_source crc_include)
    set(subdirnamelisttemp "")
    SUBDIRNAMELIST_MACRO(subdirnamelisttemp ${crc_dir})
    set(${crc_alg_name} ${subdirnamelisttemp})
    # message(STATUS "macro add_subdir subdirnamelisttemp = ${subdirnamelisttemp}")
    foreach(subdir ${subdirnamelisttemp})
        # message(STATUS "macro add_subdir subdir = ${subdir}")
        set(hascmakelisttemp FALSE)
        CHECK_DIR_HAS_CMAKELIST(hascmakelisttemp ${crc_dir}/${subdir})
        # message(STATUS "macro add_subdir hascmakelisttemp = ${hascmakelisttemp}")
        if(${hascmakelisttemp})
            # message(STATUS "macro add_subdir go to add_subdir = ${subdir}")
            add_subdirectory(${crc_dir}/${subdir})
            append_srcs_dir(ADD_SRCS ${crc_dir}/${subdir}/crc)
            list(APPEND ADD_INCLUDE ${crc_dir}/${subdir}/crc)
        endif()
    endforeach()
    set(${crc_source} ${ADD_SRCS})
    set(${crc_include} ${ADD_INCLUDE})
endmacro()

if(LIBCRC_DIR)
    CRC_ALG_COLLECT(${CMAKE_CURRENT_SOURCE_DIR}/${LIBCRC_DIR} crc_alg crc_src crc_inc)
else()
    CRC_ALG_COLLECT(${CMAKE_CURRENT_SOURCE_DIR} crc_alg crc_src crc_inc)
endif()

add_library(crc_all INTERFACE)
target_link_libraries(crc_all INTERFACE ${crc_alg})

add_library(crc STATIC ${crc_src})
target_include_directories(crc PUBLIC ${crc_inc})
