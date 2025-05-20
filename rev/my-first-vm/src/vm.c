#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Program idea:
 * Read input 64 hex bytes
 * Hex string to byte array of len 32
 * Perform some operations
 * Check password
 */

// --------------------- OPCODES ---------------------
#define READ_INPUT  0x00
#define LOADA       0x02
#define LOADB       0x03
#define STORE       0x04
#define MODULO      0x05
#define ADDA        0x06
#define ADDB        0x07
#define ADD         0x08
#define XOR         0x09
#define INC         0x0a
#define LOOP        0x0b
#define CHECK       0x0c
#define COMPUTE_SWAP       0x0d
#define PRINT       0x0e
#define REGXORA     0x10
#define REGXORB     0x11

#define EXIT        0xff

#define PROGRAM_START     0
#define INPUT_ADDR      118
#define KEY_ADDR        251
#define INPUTLEN         64
#define ROUNDS            8
#define VARS            248
#define RESULT_ADDR     183
#define KEYLEN            5








static unsigned char tape[] = {
    READ_INPUT,
    STORE,
    VARS,
    0,
    LOADA,
    VARS,
    ADDA,
    INPUT_ADDR,
    LOADB,
    VARS,
    MODULO,
    KEYLEN,
    ADDB,
    KEY_ADDR,
    XOR,
    INC,
    VARS,
    LOOP,
    VARS,
    INPUTLEN,
    4,
    STORE,
    VARS,
    0,
    STORE,
    VARS + 1,
    0,
    LOADA,
    VARS,
    LOADB,
    VARS + 1,
    COMPUTE_SWAP,
    XOR,
    REGXORA,
    REGXORB,
    REGXORA,
    XOR,
    REGXORA,
    REGXORB,
    REGXORA,
    XOR,
    INC,
    VARS + 1,
    LOOP,
    VARS + 1,
    (ROUNDS / 2),
    27,
    INC,
    VARS,
    LOOP,
    VARS,
    ROUNDS,
    24,
    STORE,
    VARS,
    0,
    STORE,
    VARS + 2,
    0x0f,
    STORE,
    VARS + 1,
    VARS + 2,
    LOADB,
    VARS + 1,
    LOADA,
    VARS,
    ADDA,
    INPUT_ADDR,
    XOR,
    INC,
    VARS,
    LOOP,
    VARS,
    INPUTLEN,
    59,
    CHECK,
    EXIT,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0xF8,
    0xD9,
    0xBF,
    0x19,
    0x8A,
    0xDE,
    0xD0,
    0x85,
    0xBE,
    0x0,
    0xBF,
    0xD4,
    0xC9,
    0xB8,
    0x14,
    0xBF,
    0x81,
    0xD2,
    0xFD,
    0xA4,
    0x17,
    0x99,
    0xEE,
    0xD0,
    0xD5,
    0x8E,
    0x8,
    0x81,
    0xC6,
    0xD1,
    0x8E,
    0x16,
    0xF,
    0xBF,
    0xC5,
    0xCB,
    0x8E,
    0x10,
    0x94,
    0xD8,
    0xC5,
    0xFD,
    0xA5,
    0xD,
    0x8F,
    0xD9,
    0xD6,
    0xB8,
    0xA8,
    0xA,
    0x81,
    0xC3,
    0xCD,
    0xA1,
    0x15,
    0x85,
    0x9D,
    0xC8,
    0xD0,
    0xBE,
    0x15,
    0x85,
    0xDC,
    0xFD,
    0,
    0,
    0,
    0,
    0xde,
    0xad,
    0xbe,
    0xef,
    0x77,
};

int main(int argc, char *argv[]) {
    unsigned char instruction_pointer = PROGRAM_START;
    unsigned char regA = 0x00;
    unsigned char regB = 0x00;
    unsigned char addr = 0x00;
    while (1)
    {
        unsigned char opcode = tape[instruction_pointer];

        // printf("opcode: %d\n", opcode);

        switch (opcode)
        {
        case READ_INPUT:
            // TODO: read from actual input
            if (argc != 2) {
                printf("usage: ./vm FLAG");
                return 1;
            }
            if (strlen(argv[1]) != INPUTLEN) {
                printf("Incorrect flag length");
                return 1;
            }
            
            memcpy(&tape[INPUT_ADDR], argv[1], INPUTLEN);
            ++instruction_pointer;
            break;
        case LOADA:
            addr = tape[++instruction_pointer];
            regA = tape[addr];
            // printf("regA = %d\n", regA);
            ++instruction_pointer;
            break;
        case LOADB:
            addr = tape[++instruction_pointer];
            regB = tape[addr];
            // printf("regB = %d\n", regB);
            ++instruction_pointer;
            break;
        case INC:
            // INC ADDR
            // Increment tape[ADDR]
            addr = tape[++instruction_pointer];
            tape[addr]++;
            ++instruction_pointer;
            // printf("index = %d \n ", tape[addr]);
            break;
        case LOOP:
            // LOOP ADDR VALUE JUMPADDR
            addr = tape[++instruction_pointer];
            if (tape[addr] != tape[++instruction_pointer]) {
                instruction_pointer = tape[++instruction_pointer];
                // printf("jumping to %d \n", instruction_pointer);
                break;
            }
            ++instruction_pointer;
            ++instruction_pointer;
            break;
        case STORE:
            // STORE ADDR VALUE
            // Stores value into tape[ADDR]
            addr = tape[++instruction_pointer];
            tape[addr] = tape[++instruction_pointer];
            ++instruction_pointer;
            break;
        case ADDA:
            // ADDA VALUE
            // Adds value to regA
            regA += tape[++instruction_pointer];
            ++instruction_pointer;
            break;
        case ADDB:
            // ADDB VALUE
            // Adds value to regB
            regB += tape[++instruction_pointer];
            ++instruction_pointer;
            break;
        case XOR:
            // TODO: what about multiple variants of this?
            // XOR ADDR ADDRB
            // addra ^= addrb
            tape[regA] = tape[regA] ^ tape[regB];
            // printf("xorred %d with %d\n", regA, regB);
            ++instruction_pointer;
            break;
        case COMPUTE_SWAP:
            // COMPUTE_SWAP 
            // COMPUTE_SWAP compute correct indices
            int a = INPUT_ADDR + 8 * regA + regB;
            int b = INPUT_ADDR + 8 * (regA + 1) - (regB + 1);
            regA = a;
            regB = b;
            ++instruction_pointer;
            break;
        case CHECK:
            // Check the value against the known password "hash"
            for (int i = 0; i < INPUTLEN; ++i){
                if (tape[INPUT_ADDR + i] != tape[RESULT_ADDR + i]) {
                    printf("Flag is wrong at index %d\n", i);
                    return 1;
                }
            }
            printf("Correct flag! Well done :)\n");
            ++instruction_pointer;
            break;
        case MODULO:
            // MODULO VALUE
            // regB gets moduloed by value
            regB = regB % tape[++instruction_pointer];
            ++instruction_pointer;
            break;
        case REGXORA:
            regA ^= regB;
            ++instruction_pointer;
            break;
        case REGXORB:
            regB ^= regA;
            ++instruction_pointer;
            break;
        case PRINT:
            for (int i = 0; i < INPUTLEN; i++) {
                printf("0x%X, ",tape[INPUT_ADDR + i]);
            }
            printf("\n");
            ++instruction_pointer;
            break;
        case EXIT:
            printf("Done!\n");
            return 0;
        default:
            printf("program ended unexpectedly!\n");
            return 1;
        }
    }
}

