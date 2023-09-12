/**
 * Copyright (c) 2023-present SKB(skb666@qq.com)
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "crc.h"

#include <stdio.h>
#include <string.h>

const static CRC_DATA crc_default = {
#include CRC_DEFAULT_DATA
};

const static CRC_NUM_TYPE crc_table[] = {
#include CRC_TABLE_DATA
};

static CRC_NUM_TYPE reverse_bits(CRC_NUM_TYPE data, uint8_t width) {
    CRC_NUM_TYPE result = 0;

    for (uint8_t i = 0; i < width; ++i) {
        result <<= 1;
        result |= data & 1;
        data >>= 1;
    }

    return result;
}

void crc_init(CRC_DATA *crc) {
    memcpy(crc, &crc_default, sizeof(CRC_DATA));
}

static CRC_NUM_TYPE crc_calc_reflect(CRC_DATA *crc, void *data, size_t length) {
    uint8_t *value, index;
    CRC_NUM_TYPE crc_val;

    value = (uint8_t *)data;
    crc_val = crc->initial_value;

    for (size_t i = 0; i < length; ++value, ++i) {
        index = (crc_val & 0xFF) ^ (*value);
        crc_val >>= 8;
        crc_val ^= crc_table[index];
    }

    return crc_val ^ crc->final_xor_value;
}

CRC_NUM_TYPE crc_calc(CRC_DATA *crc, void *data, size_t length) {
    uint8_t *value, index;
    CRC_NUM_TYPE crc_val, data_xor;

    if (crc->input_reflected && crc->result_reflected) {
        return crc_calc_reflect(crc, data, length);
    }

    value = (uint8_t *)data;
    crc_val = crc->initial_value;

    for (size_t i = 0; i < length; ++value, ++i) {
        if (crc->input_reflected) {
            data_xor = reverse_bits(*value, 8) & 0xFF;
        } else {
            data_xor = *value;
        }

        crc_val ^= data_xor << (crc->width - 8);
        index = (uint8_t)((crc_val >> (crc->width - 8)) & 0xFF);
        crc_val <<= 8;
        crc_val ^= crc_table[index];
    }

    if (crc->result_reflected) {
        crc_val = reverse_bits(crc_val, crc->width);
    }

    return crc_val ^ crc->final_xor_value;
}

static CRC_NUM_TYPE crc_accum_reflect(CRC_DATA *crc, void *data, size_t length) {
    uint8_t *value, index;

    value = (uint8_t *)data;

    for (size_t i = 0; i < length; ++value, ++i) {
        index = (crc->accumulate & 0xFF) ^ (*value);
        crc->accumulate >>= 8;
        crc->accumulate ^= crc_table[index];
    }

    return crc->accumulate ^ crc->final_xor_value;
}

CRC_NUM_TYPE crc_accum(CRC_DATA *crc, void *data, size_t length) {
    uint8_t *value, index;
    CRC_NUM_TYPE data_xor;

    if (crc->input_reflected && crc->result_reflected) {
        return crc_accum_reflect(crc, data, length);
    }

    value = (uint8_t *)data;

    for (size_t i = 0; i < length; ++value, ++i) {
        if (crc->input_reflected) {
            data_xor = reverse_bits(*value, 8) & 0xFF;
        } else {
            data_xor = *value;
        }

        crc->accumulate ^= data_xor << (crc->width - 8);
        index = (uint8_t)((crc->accumulate >> (crc->width - 8)) & 0xFF);
        crc->accumulate <<= 8;
        crc->accumulate ^= crc_table[index];
    }

    if (crc->result_reflected) {
        crc->accumulate = reverse_bits(crc->accumulate, crc->width);
    }

    return crc->accumulate ^ crc->final_xor_value;
}

void crc_reset(CRC_DATA *crc) {
    crc->accumulate = crc->initial_value;
}

CRC_NUM_TYPE crc_get(CRC_DATA *crc) {
    CRC_NUM_TYPE crc_val;

    crc_val = crc->accumulate;
    crc_reset(crc);

    return crc_val;
}
