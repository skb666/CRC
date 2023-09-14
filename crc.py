#!/usr/bin/python
"""Generic CRC implementation with many pre-defined CRC models.
    Copyright (c) 2023-present SKB(skb666@qq.com)

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os
import shutil
from crc_calc import CRC_CALC


"""Known CRC algorihtms table
    struct:
        "algorihtms name": (width, polynomial, initial_value, final_xor_value, input_reflected, result_reflected)
    description:
        width (int): Number of bits of the polynomial
        polynomial (int): CRC polynomial
        initial_value (int): Initial value of the checksum
        final_xor_value (int): Value that will be XOR-ed with final checksum
        input_reflected (bool): True, if each input byte should be reflected
        result_reflected (bool): True, if the result should be reflected before the final XOR is applied
"""
crc_alg_table = {
    # CRC8
    "crc8": (8, 0x07, 0x00, 0x00, False, False),
    "crc8_sae_j1850": (8, 0x1d, 0xff, 0xff, False, False),
    "crc8_sae_j1850_zero": (8, 0x1d, 0x00, 0x00, False, False),
    "crc8_8h2f": (8, 0x2f, 0xff, 0xff, False, False),
    "crc8_cdma2000": (8, 0x9b, 0xff, 0x00, False, False),
    "crc8_darc": (8, 0x39, 0x00, 0x00, True, True),
    "crc8_dvb_s2": (8, 0xd5, 0x00, 0x00, False, False),
    "crc8_ebu": (8, 0x1d, 0xff, 0x00, True, True),
    "crc8_icode": (8, 0x1d, 0xfd, 0x00, False, False),
    "crc8_itu": (8, 0x07, 0x00, 0x55, False, False),
    "crc8_maxim": (8, 0x31, 0x00, 0x00, True, True),
    "crc8_rohc": (8, 0x07, 0xff, 0x00, True, True),
    "crc8_wcdma": (8, 0x9b, 0x00, 0x00, True, True),
    # CRC16
    "crc16_ccit_zero": (16, 0x1021, 0x0000, 0x0000, False, False),
    "crc16_arc": (16, 0x8005, 0x0000, 0x0000, True, True),
    "crc16_aug_ccitt": (16, 0x1021, 0x1d0f, 0x0000, False, False),
    "crc16_buypass": (16, 0x8005, 0x0000, 0x0000, False, False),
    "crc16_ccitt_false": (16, 0x1021, 0xffff, 0x0000, False, False),
    "crc16_cdma2000": (16, 0xc867, 0xffff, 0x0000, False, False),
    "crc16_dds_110": (16, 0x8005, 0x800d, 0x0000, False, False),
    "crc16_dect_r": (16, 0x0589, 0x0000, 0x0001, False, False),
    "crc16_dect_x": (16, 0x0589, 0x0000, 0x0000, False, False),
    "crc16_dnp": (16, 0x3d65, 0x0000, 0xffff, True, True),
    "crc16_en_13757": (16, 0x3d65, 0x0000, 0xffff, False, False),
    "crc16_genibus": (16, 0x1021, 0xffff, 0xffff, False, False),
    "crc16_ibm": (16, 0x8005, 0x0000, 0x0000, True, True),
    "crc16_maxim": (16, 0x8005, 0x0000, 0xffff, True, True),
    "crc16_mcrf4xx": (16, 0x1021, 0xffff, 0x0000, True, True),
    "crc16_riello": (16, 0x1021, 0xb2aa, 0x0000, True, True),
    "crc16_t10_dif": (16, 0x8bb7, 0x0000, 0x0000, False, False),
    "crc16_teledisk": (16, 0xa097, 0x0000, 0x0000, False, False),
    "crc16_tms37157": (16, 0x1021, 0x89ec, 0x0000, True, True),
    "crc16_usb": (16, 0x8005, 0xffff, 0xffff, True, True),
    "crc16_a": (16, 0x1021, 0xc6c6, 0x0000, True, True),
    "crc16_kermit": (16, 0x1021, 0x0000, 0x0000, True, True),
    "crc16_modbus": (16, 0x8005, 0xffff, 0x0000, True, True),
    "crc16_x25": (16, 0x1021, 0xffff, 0xffff, True, True),
    "crc16_xmodem": (16, 0x1021, 0x0000, 0x0000, False, False),
    # CRC24
    "crc24_openpgp": (24, 0x864cfb, 0xb704ce, 0x000000, False, False),
    "crc24_flexray_a": (24, 0x5d6dcb, 0xfedcba, 0x000000, False, False),
    "crc24_flexray_b": (24, 0x5d6dcb, 0xabcdef, 0x000000, False, False),
    # CRC32
    "crc32": (32, 0x04c11db7, 0xffffffff, 0xffffffff, True, True),
    "crc32_bzip2": (32, 0x04c11db7, 0xffffffff, 0xffffffff, False, False),
    "crc32_c": (32, 0x1edc6f41, 0xffffffff, 0xffffffff, True, True),
    "crc32_d": (32, 0xa833982b, 0xffffffff, 0xffffffff, True, True),
    "crc32_mpeg2": (32, 0x04c11db7, 0xffffffff, 0x00000000, False, False),
    "crc32_posix": (32, 0x04c11db7, 0x00000000, 0xffffffff, False, False),
    "crc32_q": (32, 0x814141ab, 0x00000000, 0x00000000, False, False),
    "crc32_jamcrc": (32, 0x04c11db7, 0xffffffff, 0x00000000, True, True),
    "crc32_xfer": (32, 0x000000af, 0x00000000, 0x00000000, False, False),
    # CRC64
    "crc64_ecma_182": (64, 0x42f0e1eba9ea3693, 0x0000000000000000, 0x0000000000000000, False, False),
    "crc64_go_iso": (64, 0x000000000000001b, 0xffffffffffffffff, 0xffffffffffffffff, True, True),
    "crc64_we": (64, 0x42f0e1eba9ea3693, 0xffffffffffffffff, 0xffffffffffffffff, False, False),
    "crc64_xz": (64, 0x42f0e1eba9ea3693, 0xffffffffffffffff, 0xffffffffffffffff, True, True),
}


class CRC(CRC_CALC):
    def __init__(self, alg_name):
        if not alg_name in crc_alg_table.keys():
            raise ValueError("Unknown CRC algorihtm")
        else:
            super().__init__(*crc_alg_table[alg_name])
            self._algorithm = alg_name
            if self._width <= 8:
                self._data_width = 8
            elif self._width <= 16:
                self._data_width = 16
            elif self._width <= 32:
                self._data_width = 32
            elif self._width <= 64:
                self._data_width = 64
            else:
                raise ValueError("CRC parameter error")

    def __check_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path, mode=0o755, exist_ok=True)

    def generate_for_c(self, path="./generate/c/"):
        script_path = os.path.realpath(__file__)
        template_path = os.path.dirname(script_path) + "/template/c"
        crc_path = path + "libcrc/{alg_name}/crc/".format(alg_name=self._algorithm)

        crc_table = str(self)

        with open(template_path + "/crc/crc.default", "r") as f_obj:
            crc_default = f_obj.read().format(
                display_width=self._width // 4,
                width=self._width,
                input_reflected=self._input_reflected,
                result_reflected=self._result_reflected,
                polynomial=self._polynomial,
                initial_value=self._initial_value,
                final_xor_value=self._final_xor_value,
                cast_mask=self._cast_mask,
            )

        with open(template_path + "/crc/crc.h", "r") as f_obj:
            crc_h = f_obj.read().format(
                algorithm=self._algorithm,
                algorithm_upper=self._algorithm.upper(),
                display_width=self._width // 4,
                data_width=self._data_width,
                width=self._width,
            )

        with open(template_path + "/crc/crc.c", "r") as f_obj:
            crc_c = f_obj.read().format(
                algorithm=self._algorithm,
                algorithm_upper=self._algorithm.upper(),
            )

        with open(template_path + "/crc/CMakeLists.txt", "r") as f_obj:
            crc_cmake = f_obj.read().format(
                algorithm=self._algorithm,
            )

        with open(template_path + "/test/test.c", "r") as f_obj:
            crc_test = f_obj.read().format(
                algorithm=self._algorithm,
                algorithm_upper=self._algorithm.upper(),
            )

        with open(template_path + "/test/CMakeLists.txt", "r") as f_obj:
            crc_test_cmake = f_obj.read().format(
                algorithm=self._algorithm,
            )

        self.__check_path(crc_path)
        shutil.copyfile(template_path + "/CMakeLists.txt",
                        path + "CMakeLists.txt")
        shutil.copyfile(template_path + "/toolchain.cmake",
                        path + "toolchain.cmake")
        shutil.copyfile(template_path + "/libcrc.cmake",
                        path + "libcrc/libcrc.cmake")

        with open(crc_path + "{alg_name}.table".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_table)

        with open(crc_path + "{alg_name}.default".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_default)

        with open(crc_path + "{alg_name}.h".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_h)

        with open(crc_path + "{alg_name}.c".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_c)

        with open(crc_path + "CMakeLists.txt", "w") as f_obj:
            f_obj.write(crc_cmake)

        with open(path + "libcrc/{alg_name}/test_{alg_name}.c".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_test)

        with open(path + "libcrc/{alg_name}/CMakeLists.txt".format(alg_name=self._algorithm), "w") as f_obj:
            f_obj.write(crc_test_cmake)


if __name__ == '__main__':
    # 实例化一个 CRC，参数模型使用 crc32_mpeg2
    crc32_mpeg2 = CRC("crc32_mpeg2")

    data1 = b'hello '
    data2 = b'world'
    data3 = b'!!!'

    # 单次校验
    val_a1 = crc32_mpeg2(data1)
    val_a2 = crc32_mpeg2(data2)
    val_a3 = crc32_mpeg2(data3)
    crc1 = crc32_mpeg2(data1 + data2 + data3)

    # 分次校验
    crc32_mpeg2.reset()
    val_b1 = crc32_mpeg2.accumulate(data1)
    val_b2 = crc32_mpeg2.accumulate(data2)
    val_b3 = crc32_mpeg2.accumulate(data3)
    crc2 = crc32_mpeg2.get()

    assert crc1 == crc2
    print(hex(val_a1), hex(val_a2), hex(val_a3), hex(crc1))
    print(hex(val_b1), hex(val_b2), hex(val_b3), hex(crc2))

    # 生成 C 语言代码
    for alg in crc_alg_table.keys():
        CRC(alg).generate_for_c()
