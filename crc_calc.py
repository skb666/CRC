#!/usr/bin/python
"""Generic CRC calculate implementation.
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
import array


class CRC_CALC(object):
    """Generic CRC model implemented with lookup tables.
    The model parameter can are the constructor parameters.
    Args:
        width (int): Number of bits of the polynomial
        polynomial (int): CRC polynomial
        initial_value (int): Initial value of the checksum
        final_xor_value (int): Value that will be XOR-ed with final checksum
        input_reflected (bool): True, if each input byte should be reflected
        result_reflected (bool): True, if the result should be reflected before the final XOR is applied
    """

    def __init__(self, width, polynomial, initial_value, final_xor_value, input_reflected, result_reflected):
        assert 8 <= width <= 64
        assert width % 8 == 0

        self._width = width
        self._polynomial = polynomial
        self._initial_value = initial_value
        self._final_xor_value = final_xor_value
        self._input_reflected = input_reflected
        self._result_reflected = result_reflected
        self.__accumulate = initial_value

        # Initialize casting mask to keep the correct width for dynamic Python
        # integers
        self._cast_mask = int('1' * self._width, base=2)

        # Mask that can be applied to get the Most Significant Bit (MSB) if the
        # number with given width
        self._msb_mask = 0x01 << (self._width - 1)

        # The lookup tables get initialized lazzily. This ensures that only
        # tables are calculated that are actually needed.
        self.__table = None
        self.__reflected_table = None

    def __reflect(self, num, width):
        """Reverts bit order of the given number
        Args:
            num (int): Number that should be reflected
            width (int): Size of the number in bits
        """
        reflected = 0

        for i in range(width):
            if (num >> i) & 1 != 0:
                reflected |= 1 << (width - 1 - i)

        return reflected

    def __make_table(self, width):
        """Create static sized CRC lookup table and initialize it with ``0``.
        For 8, 16, 32, and 64 bit width :class:`array.array` instances are used. For
        all other widths it falls back to a generic Python :class:`list`.
        Args:
            width (int): Size of elements in bits
        """
        initializer = (0 for _ in range(256))

        if width <= 8:
            return array.array('B', initializer)
        elif width <= 16:
            return array.array('H', initializer)
        elif width <= 32:
            return array.array('L', initializer)
        elif width <= 64:
            return array.array('Q', initializer)
        else:
            # Fallback to a generic list
            return list(initializer)

    def __calculate_crc_table(self):
        table = self.__make_table(self._width)

        for divident in range(256):
            cur_byte = (divident << (self._width - 8)) & self._cast_mask

            for bit in range(8):
                if (cur_byte & self._msb_mask) != 0:
                    cur_byte <<= 1
                    cur_byte ^= self._polynomial
                else:
                    cur_byte <<= 1

            table[divident] = cur_byte & self._cast_mask

        return table

    def __calculate_crc_table_reflected(self):
        table = self.__make_table(self._width)

        for divident in range(256):
            reflected_divident = self.__reflect(divident, 8)
            cur_byte = (reflected_divident << (
                self._width - 8)) & self._cast_mask

            for bit in range(8):
                if (cur_byte & self._msb_mask) != 0:
                    cur_byte <<= 1
                    cur_byte ^= self._polynomial
                else:
                    cur_byte <<= 1

            cur_byte = self.__reflect(cur_byte, self._width)

            table[divident] = (cur_byte & self._cast_mask)

        return table

    def __repr__(self):
        if self._input_reflected and self._result_reflected:
            if self.__reflected_table is None:
                self.__reflected_table = self.__calculate_crc_table_reflected()
            table = self.__reflected_table
        else:
            if self.__table is None:
                self.__table = self.__calculate_crc_table()
            table = self.__table

        table = [table[i:i+8] for i in range(0, len(table), 8)]
        table_str = [', '.join(
            ["0x{:0{}X}".format(i, self._width // 4) for i in t]
        ) for t in table]
        return ',\n'.join(table_str) + ','

    def __fast_reflected(self, value):
        """If the input data and the result checksum are both reflected in the
        current model, an optimized algorithm can be used that reflects the
        looup table rather then the input data. This saves the reflection
        operation of the input data.
        """
        if not self._input_reflected or not self._result_reflected:
            raise ValueError("Input and result must be reflected")

        # Lazy initialization of the lookup table
        if self.__reflected_table is None:
            self.__reflected_table = self.__calculate_crc_table_reflected()

        crc = self._initial_value

        for cur_byte in value:
            # The LSB of the XOR-red remainder and the next byte is the index
            # into the lookup table
            index = (crc & 0xff) ^ cur_byte

            # Shift out the index
            crc = (crc >> 8) & self._cast_mask

            # XOR-ing remainder from the loopup table
            crc = crc ^ self.__reflected_table[index]

        # Final XBOR
        return crc ^ self._final_xor_value

    def __call__(self, value):
        """Compute the CRC checksum with respect to the model parameters by using
        a looup table algorithm.
        Args:
            value (bytes): Input bytes that should be checked
        Returns:
            int - CRC checksum
        """
        # Use the reflection optimization if applicable
        if self._input_reflected and self._result_reflected:
            return self.__fast_reflected(value)

        # Lazy initialization of the lookup table
        if self.__table is None:
            self.__table = self.__calculate_crc_table()

        crc = self._initial_value

        for cur_byte in value:
            if self._input_reflected:
                cur_byte = self.__reflect(cur_byte, 8)

            # Update the MSB of the CRC value with the next input byte
            crc = (crc ^ (cur_byte << (self._width - 8))) & self._cast_mask

            # This MSB byte value is the index into the lookup table
            index = (crc >> (self._width - 8)) & 0xff

            # Shift out the index
            crc = (crc << 8) & self._cast_mask

            # XOR-ing crc from the lookup table using the calculated index
            crc = crc ^ self.__table[index]

        if self._result_reflected:
            crc = self.__reflect(crc, self._width)

        # Final XBOR
        return crc ^ self._final_xor_value

    def __fast_reflected_acc(self, value):
        if not self._input_reflected or not self._result_reflected:
            raise ValueError("Input and result must be reflected")

        # Lazy initialization of the lookup table
        if self.__reflected_table is None:
            self.__reflected_table = self.__calculate_crc_table_reflected()

        for cur_byte in value:
            # The LSB of the XOR-red remainder and the next byte is the index
            # into the lookup table
            index = (self.__accumulate & 0xff) ^ cur_byte

            # Shift out the index
            self.__accumulate = (self.__accumulate >> 8) & self._cast_mask

            # XOR-ing remainder from the loopup table
            self.__accumulate = self.__accumulate ^ self.__reflected_table[index]

        # Final XBOR
        return self.__accumulate ^ self._final_xor_value

    def accumulate(self, value):
        # Use the reflection optimization if applicable
        if self._input_reflected and self._result_reflected:
            return self.__fast_reflected_acc(value)

        # Lazy initialization of the lookup table
        if self.__table is None:
            self.__table = self.__calculate_crc_table()

        for cur_byte in value:
            if self._input_reflected:
                cur_byte = self.__reflect(cur_byte, 8)

            # Update the MSB of the CRC value with the next input byte
            self.__accumulate = (self.__accumulate ^ (
                cur_byte << (self._width - 8))) & self._cast_mask

            # This MSB byte value is the index into the lookup table
            index = (self.__accumulate >> (self._width - 8)) & 0xff

            # Shift out the index
            self.__accumulate = (self.__accumulate << 8) & self._cast_mask

            # XOR-ing crc from the lookup table using the calculated index
            self.__accumulate = self.__accumulate ^ self.__table[index]

        if self._result_reflected:
            self.__accumulate = self.__reflect(self.__accumulate, self._width)

        # Final XBOR
        return self.__accumulate ^ self._final_xor_value

    def reset(self):
        self.__accumulate = self._initial_value

    def get(self):
        crc = self.__accumulate
        # self.reset()
        return crc ^ self._final_xor_value


if __name__ == '__main__':
    # 自定义 CRC 参数模型
    crc32 = CRC_CALC(32, 0x04c11db7, 0xffffffff, 0xffffffff, True, True)

    data1 = b'hello '
    data2 = b'world'
    data3 = b'!!!'

    # 单次校验
    val_a1 = crc32(data1)
    val_a2 = crc32(data2)
    val_a3 = crc32(data3)
    crc1 = crc32(data1 + data2 + data3)

    # 分次校验
    crc32.reset()
    val_b1 = crc32.accumulate(data1)
    val_b2 = crc32.accumulate(data2)
    val_b3 = crc32.accumulate(data3)
    crc2 = crc32.get()

    assert crc1 == crc2
    print(hex(val_a1), hex(val_a2), hex(val_a3), hex(crc1))
    print(hex(val_b1), hex(val_b2), hex(val_b3), hex(crc2))
