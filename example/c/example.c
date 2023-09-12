#include <stdio.h>
#include <string.h>

#include "crc.h"

int main() {
    CRC_DATA crc;
    CRC_NUM_TYPE crc_val, crc1, crc2;

    char *data[] = {
        "hello ",
        "world",
        "!!!",
    };

    crc_init(&crc);

    printf("\nCRC Test Start\n\n");

    for (int i = 0; i < sizeof(data) / sizeof(data[0]); ++i) {
        crc_val = crc_calc(&crc, data[i], strlen(data[i]));
        printf("0x%0" CRC_NUM_WIDTH CRC_NUM_PRIx " ", crc_val);
    }
    crc1 = crc_calc(&crc, "hello world!!!", 14);
    printf("0x%0" CRC_NUM_WIDTH CRC_NUM_PRIx "\n", crc1);

    for (int i = 0; i < sizeof(data) / sizeof(data[0]); ++i) {
        crc_val = crc_accum(&crc, data[i], strlen(data[i]));
        printf("0x%0" CRC_NUM_WIDTH CRC_NUM_PRIx " ", crc_val);
    }
    crc2 = crc_get(&crc);
    printf("0x%0" CRC_NUM_WIDTH CRC_NUM_PRIx "\n", crc2);

    if (crc1 == crc2) {
        printf("\nTest succeeded!!!\n\n");
    } else {
        printf("\nTest failed!!!\n\n");
    }

    return 0;
}
