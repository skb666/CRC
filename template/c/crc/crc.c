/** Genetrate from template/crc/crc.c
 * @param algorithm: {algorithm}
 * @param algorithm_upper: {algorithm_upper}
 * 
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
#include "{algorithm}.h"

#include <stdio.h>
#include <string.h>

const static {algorithm_upper}_DATA {algorithm}_default = {{
#include {algorithm_upper}_DEFAULT_DATA
}};

const static {algorithm_upper}_NUM_TYPE {algorithm}_table[] = {{
#include {algorithm_upper}_TABLE_DATA
}};

static {algorithm_upper}_NUM_TYPE {algorithm}_reverse_bits({algorithm_upper}_NUM_TYPE data, uint8_t width) {{
    {algorithm_upper}_NUM_TYPE result = 0;

    for (uint8_t i = 0; i < width; ++i) {{
        result <<= 1;
        result |= data & 1;
        data >>= 1;
    }}

    return result;
}}

void {algorithm}_init({algorithm_upper}_DATA *crc) {{
    memcpy(crc, &{algorithm}_default, sizeof({algorithm_upper}_DATA));
}}

static {algorithm_upper}_NUM_TYPE {algorithm}_calc_reflect({algorithm_upper}_DATA *crc, void *data, size_t length) {{
    uint8_t *value, index;
    {algorithm_upper}_NUM_TYPE crc_val;

    value = (uint8_t *)data;
    crc_val = crc->initial_value;

    for (size_t i = 0; i < length; ++value, ++i) {{
        index = (crc_val & 0xFF) ^ (*value);
        crc_val >>= 8;
        crc_val ^= {algorithm}_table[index];
    }}

    return crc_val ^ crc->final_xor_value;
}}

{algorithm_upper}_NUM_TYPE {algorithm}_calc({algorithm_upper}_DATA *crc, void *data, size_t length) {{
    uint8_t *value, index;
    {algorithm_upper}_NUM_TYPE crc_val, data_xor;

    if (crc->input_reflected && crc->result_reflected) {{
        return {algorithm}_calc_reflect(crc, data, length);
    }}

    value = (uint8_t *)data;
    crc_val = crc->initial_value;

    for (size_t i = 0; i < length; ++value, ++i) {{
        if (crc->input_reflected) {{
            data_xor = {algorithm}_reverse_bits(*value, 8) & 0xFF;
        }} else {{
            data_xor = *value;
        }}

        crc_val ^= data_xor << (crc->width - 8);
        index = (uint8_t)((crc_val >> (crc->width - 8)) & 0xFF);
        crc_val <<= 8;
        crc_val ^= {algorithm}_table[index];
    }}

    if (crc->result_reflected) {{
        crc_val = {algorithm}_reverse_bits(crc_val, crc->width);
    }}

    return crc_val ^ crc->final_xor_value;
}}

static {algorithm_upper}_NUM_TYPE {algorithm}_accum_reflect({algorithm_upper}_DATA *crc, void *data, size_t length) {{
    uint8_t *value, index;

    value = (uint8_t *)data;

    for (size_t i = 0; i < length; ++value, ++i) {{
        index = (crc->accumulate & 0xFF) ^ (*value);
        crc->accumulate >>= 8;
        crc->accumulate ^= {algorithm}_table[index];
    }}

    return crc->accumulate ^ crc->final_xor_value;
}}

{algorithm_upper}_NUM_TYPE {algorithm}_accum({algorithm_upper}_DATA *crc, void *data, size_t length) {{
    uint8_t *value, index;
    {algorithm_upper}_NUM_TYPE data_xor;

    if (crc->input_reflected && crc->result_reflected) {{
        return {algorithm}_accum_reflect(crc, data, length);
    }}

    value = (uint8_t *)data;

    for (size_t i = 0; i < length; ++value, ++i) {{
        if (crc->input_reflected) {{
            data_xor = {algorithm}_reverse_bits(*value, 8) & 0xFF;
        }} else {{
            data_xor = *value;
        }}

        crc->accumulate ^= data_xor << (crc->width - 8);
        index = (uint8_t)((crc->accumulate >> (crc->width - 8)) & 0xFF);
        crc->accumulate <<= 8;
        crc->accumulate ^= {algorithm}_table[index];
    }}

    if (crc->result_reflected) {{
        crc->accumulate = {algorithm}_reverse_bits(crc->accumulate, crc->width);
    }}

    return crc->accumulate ^ crc->final_xor_value;
}}

void {algorithm}_reset({algorithm_upper}_DATA *crc) {{
    crc->accumulate = crc->initial_value;
}}

{algorithm_upper}_NUM_TYPE {algorithm}_get({algorithm_upper}_DATA *crc) {{
    {algorithm_upper}_NUM_TYPE crc_val;

    crc_val = crc->accumulate;
    {algorithm}_reset(crc);

    return crc_val ^ crc->final_xor_value;
}}
