/** Genetrate from template/crc/crc.h
 * @param algorithm: {algorithm}
 * @param algorithm_upper: {algorithm_upper}
 * @param display_width: {display_width}
 * @param width: {width}
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
#ifndef __{algorithm_upper}_H__
#define __{algorithm_upper}_H__

#include <inttypes.h>
#include <stdint.h>
#include <stdlib.h>

#define {algorithm_upper}_NUM_WIDTH "{display_width}"
#define {algorithm_upper}_NUM_PRIx PRIx{width}
#define {algorithm_upper}_NUM_PRIX PRIX{width}

#define {algorithm_upper}_NUM_TYPE uint{width}_t
#define {algorithm_upper}_DEFAULT_DATA "{algorithm}.default"
#define {algorithm_upper}_TABLE_DATA "{algorithm}.table"

#ifdef __cplusplus
extern "C" {{
#endif

typedef struct {{
    uint8_t width;
    uint8_t input_reflected;
    uint8_t result_reflected;
    // data
    {algorithm_upper}_NUM_TYPE polynomial;
    {algorithm_upper}_NUM_TYPE initial_value;
    {algorithm_upper}_NUM_TYPE final_xor_value;
    {algorithm_upper}_NUM_TYPE accumulate;
}} {algorithm_upper}_DATA;

void {algorithm}_init({algorithm_upper}_DATA *crc);
{algorithm_upper}_NUM_TYPE {algorithm}_calc({algorithm_upper}_DATA *crc, void *data, size_t length);
{algorithm_upper}_NUM_TYPE {algorithm}_accum({algorithm_upper}_DATA *crc, void *data, size_t length);
void {algorithm}_reset({algorithm_upper}_DATA *crc);
{algorithm_upper}_NUM_TYPE {algorithm}_get({algorithm_upper}_DATA *crc);

#ifdef __cplusplus
}}
#endif

#endif
