#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <openssl/hmac.h>//HOTP
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <unistd.h>

#define KEY_FILE "ft_otp.key"
#define DIGITS 6

void print_usage() {
    printf("Usage:\n");
    printf("  ft_otp -g <keyfile>    Store the key securely\n");
    printf("  ft_otp -k <keyfile>    Generate a 6-digit OTP\n");
}

//2 hex = 1 byte ff = 255
int hex_to_bytes(const char *hex, uint8_t *out, size_t len) {
    for (size_t i = 0; i < len; i++) {
        if (sscanf(hex + 2 * i, "%2hhx", &out[i]) != 1) {
            return 0;
        }
    }
    return 1;
}


int encrypt_and_store_key(const char *hexfile) {
    FILE *f = fopen(hexfile, "r");
    if (!f) {
        perror("Error opening hex file");
        return 1;
    }

    char hex[65];
    if (!fgets(hex, sizeof(hex), f)) {
        perror("Error reading key");
        fclose(f);
        return 1;
    }
    fclose(f);

    if (strlen(hex) != 64) {
        fprintf(stderr, "Error: key must be 64 hexadecimal characters.\n");
        return 1;
    }

    uint8_t key[32], rand_key[32], encrypted[32];
    if (!hex_to_bytes(hex, key, 32)) {
        fprintf(stderr, "Invalid hex characters.\n");
        return 1;
    }

    if (!RAND_bytes(rand_key, 32)) {
        fprintf(stderr, "Error generating random encryption key.\n");
        return 1;
    }

    for (int i = 0; i < 32; i++) {
        encrypted[i] = key[i] ^ rand_key[i];
    }

    FILE *out = fopen(KEY_FILE, "wb");
    if (!out) {
        perror("Error opening output key file");
        return 1;
    }

    fwrite(rand_key, 1, 32, out);
    fwrite(encrypted, 1, 32, out);
    fclose(out);
    printf("Key was successfully saved in %s.\n", KEY_FILE);
    return 0;
}


//geenerate a 6 digit
uint32_t generate_hotp(uint8_t *key, uint64_t counter) {
    uint8_t counter_bytes[8];
    for (int i = 7; i >= 0; i--) {
        counter_bytes[i] = counter & 0xFF;
        counter >>= 8;
    }

    unsigned char *hmac_result;
    unsigned int len;
    hmac_result = HMAC(EVP_sha1(), key, 32, counter_bytes, 8, NULL, &len);

    int offset = hmac_result[19] & 0x0F;
    uint32_t code = (hmac_result[offset] & 0x7f) << 24 |
                    (hmac_result[offset + 1] & 0xff) << 16 |
                    (hmac_result[offset + 2] & 0xff) << 8 |
                    (hmac_result[offset + 3] & 0xff);

    return code % 1000000;
}

//decryption
int load_key_and_generate_otp(const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        perror("Error opening key file");
        return 1;
    }

    uint8_t rand_key[32], encrypted[32], key[32];
    fread(rand_key, 1, 32, f);
    fread(encrypted, 1, 32, f);
    fclose(f);

    for (int i = 0; i < 32; i++) {
        key[i] = encrypted[i] ^ rand_key[i];
    }

    time_t now = time(NULL);
    uint64_t counter = now / 60;

    uint32_t otp = generate_hotp(key, counter);
    printf("%06u\n", otp);

    return 0;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        print_usage();
        return 1;
    }

    if (strcmp(argv[1], "-g") == 0) {
        return encrypt_and_store_key(argv[2]);
    } else if (strcmp(argv[1], "-k") == 0) {
        return load_key_and_generate_otp(argv[2]);
    } else {
        print_usage();
        return 1;
    }
}
