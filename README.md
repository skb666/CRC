# CRC

+ 支持 CRC8、CRC16、CRC32、CRC64
+ 支持单次计算、分次计算
+ 支持自定义参数模型
+ 支持代码生成（C/C++）

## 使用方法

### 已知参数模型

```python
from crc import CRC

# 实例化一个 CRC，参数模型使用 crc32_mpeg2
crc32_mpeg2 = CRC("crc32_mpeg2")

data1 = b'hello '
data2 = b'world'
data3 = b'!!!'

# 单次校验
crc1 = crc32_mpeg2(data1 + data2 + data3)

# 分步校验
val1 = crc32_mpeg2.accumulate(data1)
val2 = crc32_mpeg2.accumulate(data2)
val3 = crc32_mpeg2.accumulate(data3)
crc2 = crc32_mpeg2.get()

print(hex(crc1), hex(crc2))
```

### 自定义参数模型

```python
from crc_calc import CRC_CALC

data1 = b'hello '
data2 = b'world'
data3 = b'!!!'

crc32 = CRC_CALC(32, 0x04c11db7, 0xffffffff, 0xffffffff, True, True)

# 单次校验
crc1 = mycrc(data1 + data2 + data3)

# 分步校验
val1 = crc32.accumulate(data1)
val2 = crc32.accumulate(data2)
val3 = crc32.accumulate(data3)
crc2 = crc32.get()

print(hex(crc1), hex(crc2))
```

### 代码生成

**生成 C/C++ 代码**

```python
from crc import CRC

CRC("crc32_mpeg2").generate_for_c()
```

**编译测试工程**

```bash
cd generate/c/
cmake -S. -Bbuild
# 构建所有目标
cmake --build build --target all -- -j${nproc}
# 执行单元测试
cmake --build build --target test
```

## 已知的 CRC 参数模型

| 算法名称            | 宽度  | 多项式             | 初始值             | 结果异或值         | 输入反转 | 输出反转 |
| :------------------ | :---: | :----------------- | :----------------- | :----------------- | -------: | -------: |
| crc8                |   8   | 0x07               | 0x00               | 0x00               |    False |    False |
| crc8_sae_j1850      |   8   | 0x1D               | 0xFF               | 0xFF               |    False |    False |
| crc8_sae_j1850_zero |   8   | 0x1D               | 0x00               | 0x00               |    False |    False |
| crc8_8h2f           |   8   | 0x2F               | 0xFF               | 0xFF               |    False |    False |
| crc8_cdma2000       |   8   | 0x9B               | 0xFF               | 0x00               |    False |    False |
| crc8_darc           |   8   | 0x39               | 0x00               | 0x00               |     True |     True |
| crc8_dvb_s2         |   8   | 0xD5               | 0x00               | 0x00               |    False |    False |
| crc8_ebu            |   8   | 0x1D               | 0xFF               | 0x00               |     True |     True |
| crc8_icode          |   8   | 0x1D               | 0xFD               | 0x00               |    False |    False |
| crc8_itu            |   8   | 0x07               | 0x00               | 0x55               |    False |    False |
| crc8_maxim          |   8   | 0x31               | 0x00               | 0x00               |     True |     True |
| crc8_rohc           |   8   | 0x07               | 0xFF               | 0x00               |     True |     True |
| crc8_wcdma          |   8   | 0x9B               | 0x00               | 0x00               |     True |     True |
| crc16_ccit_zero     |  16   | 0x1021             | 0x0000             | 0x0000             |    False |    False |
| crc16_arc           |  16   | 0x8005             | 0x0000             | 0x0000             |     True |     True |
| crc16_aug_ccitt     |  16   | 0x1021             | 0x1D0F             | 0x0000             |    False |    False |
| crc16_buypass       |  16   | 0x8005             | 0x0000             | 0x0000             |    False |    False |
| crc16_ccitt_false   |  16   | 0x1021             | 0xFFFF             | 0x0000             |    False |    False |
| crc16_cdma2000      |  16   | 0xC867             | 0xFFFF             | 0x0000             |    False |    False |
| crc16_dds_110       |  16   | 0x8005             | 0x800D             | 0x0000             |    False |    False |
| crc16_dect_r        |  16   | 0x0589             | 0x0000             | 0x0001             |    False |    False |
| crc16_dect_x        |  16   | 0x0589             | 0x0000             | 0x0000             |    False |    False |
| crc16_dnp           |  16   | 0x3D65             | 0x0000             | 0xFFFF             |     True |     True |
| crc16_en_13757      |  16   | 0x3D65             | 0x0000             | 0xFFFF             |    False |    False |
| crc16_genibus       |  16   | 0x1021             | 0xFFFF             | 0xFFFF             |    False |    False |
| crc16_ibm           |  16   | 0x8005             | 0x0000             | 0x0000             |     True |     True |
| crc16_maxim         |  16   | 0x8005             | 0x0000             | 0xFFFF             |     True |     True |
| crc16_mcrf4xx       |  16   | 0x1021             | 0xFFFF             | 0x0000             |     True |     True |
| crc16_riello        |  16   | 0x1021             | 0xB2AA             | 0x0000             |     True |     True |
| crc16_t10_dif       |  16   | 0x8BB7             | 0x0000             | 0x0000             |    False |    False |
| crc16_teledisk      |  16   | 0xA097             | 0x0000             | 0x0000             |    False |    False |
| crc16_tms37157      |  16   | 0x1021             | 0x89EC             | 0x0000             |     True |     True |
| crc16_usb           |  16   | 0x8005             | 0xFFFF             | 0xFFFF             |     True |     True |
| crc16_a             |  16   | 0x1021             | 0xC6C6             | 0x0000             |     True |     True |
| crc16_kermit        |  16   | 0x1021             | 0x0000             | 0x0000             |     True |     True |
| crc16_modbus        |  16   | 0x8005             | 0xFFFF             | 0x0000             |     True |     True |
| crc16_x25           |  16   | 0x1021             | 0xFFFF             | 0xFFFF             |     True |     True |
| crc16_xmodem        |  16   | 0x1021             | 0x0000             | 0x0000             |    False |    False |
| crc32               |  32   | 0x04C11DB7         | 0xFFFFFFFF         | 0xFFFFFFFF         |     True |     True |
| crc32_bzip2         |  32   | 0x04C11DB7         | 0xFFFFFFFF         | 0xFFFFFFFF         |    False |    False |
| crc32_c             |  32   | 0x1EDC6F41         | 0xFFFFFFFF         | 0xFFFFFFFF         |     True |     True |
| crc32_d             |  32   | 0xA833982B         | 0xFFFFFFFF         | 0xFFFFFFFF         |     True |     True |
| crc32_mpeg2         |  32   | 0x04C11DB7         | 0xFFFFFFFF         | 0x00000000         |    False |    False |
| crc32_posix         |  32   | 0x04C11DB7         | 0x00000000         | 0xFFFFFFFF         |    False |    False |
| crc32_q             |  32   | 0x814141AB         | 0x00000000         | 0x00000000         |    False |    False |
| crc32_jamcrc        |  32   | 0x04C11DB7         | 0xFFFFFFFF         | 0x00000000         |     True |     True |
| crc32_xfer          |  32   | 0x000000AF         | 0x00000000         | 0x00000000         |    False |    False |
| crc64_ecma_182      |  64   | 0x42F0E1EBA9EA3693 | 0x0000000000000000 | 0x0000000000000000 |    False |    False |
| crc64_go_iso        |  64   | 0x000000000000001B | 0xFFFFFFFFFFFFFFFF | 0xFFFFFFFFFFFFFFFF |     True |     True |
| crc64_we            |  64   | 0x42F0E1EBA9EA3693 | 0xFFFFFFFFFFFFFFFF | 0xFFFFFFFFFFFFFFFF |    False |    False |
| crc64_xz            |  64   | 0x42F0E1EBA9EA3693 | 0xFFFFFFFFFFFFFFFF | 0xFFFFFFFFFFFFFFFF |     True |     True |

## 在线验证平台

1. [CRC（循环冗余校验）在线计算](http://www.ip33.com/crc.html)
2. [CRC Calculator (Javascript)](http://www.sunshine2k.de/coding/javascript/crc/crc_js.html)
