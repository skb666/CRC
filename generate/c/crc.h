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
#ifndef __CRC_H__
#define __CRC_H__

#include <stdint.h>
#include <stdlib.h>

#include "crc_conf.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t width;
    uint8_t input_reflected;
    uint8_t result_reflected;
    // data
    CRC_NUM_TYPE polynomial;
    CRC_NUM_TYPE initial_value;
    CRC_NUM_TYPE final_xor_value;
    CRC_NUM_TYPE accumulate;
} CRC_DATA;

void crc_init(CRC_DATA *crc);
CRC_NUM_TYPE crc_calc(CRC_DATA *crc, void *data, size_t length);
CRC_NUM_TYPE crc_accum(CRC_DATA *crc, void *data, size_t length);
void crc_reset(CRC_DATA *crc);
CRC_NUM_TYPE crc_get(CRC_DATA *crc);

#ifdef __cplusplus
}
#endif

#endif
