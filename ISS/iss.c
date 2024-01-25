#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void initialize_registers();
void parse_file(FILE* assembly_file);
void print_instructions();
void simulate();
void print_registers();

int instructions[1000];
int num_instructions = 0;

int main(int argc, char* argv[]) {
    char *assembly_filename;
    FILE* assembly_file;
    if (argc < 2) {
        printf("Usage: iss <assembly_filename>\n");
        exit(1);
    }
    printf("Welcome to Mini ISS\n");
    assembly_filename = argv[1]; 
    printf("Assembly file: %s\n", assembly_filename);
    assembly_file = fopen(assembly_filename, "r");
    if (assembly_file == NULL) {
        printf("Error: Unable to open file %s\n", assembly_filename);
        exit(1);
    }

    initialize_registers();
    parse_file(assembly_file);
    print_instructions();
    simulate();
    print_registers();
    return 0;
}

void parse_file(FILE* assembly_file) {
    int line_number = 1;
    while(1) {
        char line[256];
        unsigned int instruction;
        if (fgets(line, sizeof(line), assembly_file) == NULL) {
            break;
        }
        instruction = strtol(line, NULL, 0);
        if (instruction == 0) {
            printf("Error: Invalid instruction %s at line %d\n", line, line_number);
            exit(1);
        }
        instructions[num_instructions] = instruction;
        num_instructions++;
        line_number++;
    }
}

#define NUM_REGISTERS 16
unsigned int registers[NUM_REGISTERS];
unsigned int memory[65536];

char* instruction_names[] = {
    "NA",
    "LOAD",
    "LOAD_INDIRECT",
    "LOAD_IMM",
    "STORE",
    "STORE_INDIRECT",
    "ADD",
    "SUB",
    "MUL",
    "AND",
    "OR",
    "NOT",
    "CMP",
    "EQ",
    "JMP",
    "JMP_IF",
    "HALT"
};


void simulate() {
    int i;
    unsigned int program_counter = 0;
    while (1) {
        unsigned int instruction = instructions[program_counter];
        unsigned int opcode = instruction >> 26;
        unsigned int out = (instruction >> 22) & 0xf;
        unsigned int in1 = (instruction >> 18) & 0xf;
        unsigned int in2 = (instruction >> 14) & 0xf;
        unsigned int imm = instruction & 0x3fff;
        unsigned int addr = instruction & 0xffff;
        unsigned int data;
        printf("Instruction: %x\n", instruction);
        printf("Opcode: %x\n", opcode);
        switch(opcode) {
            case 1: // LOAD
                data = memory[addr];
                registers[out] = data;
                break;
            case 2: // LOAD_INDIRECT
                data = memory[registers[in1]];
                registers[out] = data;
                break;
            case 3: // LOAD_IMM
                registers[out] = imm;
                break;
            case 4: // STORE
                memory[addr] = registers[out];
                break;
            case 5: // STORE_INDIRECT
                memory[registers[in1]] = registers[out];
                break;
            case 6: // ADD
                registers[out] = registers[in1] + registers[in2];
                break;
            case 7: // SUB
                registers[out] = registers[in1] - registers[in2];
                break;
            case 8: // MUL
                registers[out] = registers[in1] * registers[in2];
                break;
            case 9: // AND
                registers[out] = registers[in1] & registers[in2];
                break;
            case 10: // OR
                registers[out] = registers[in1] | registers[in2];
                break;
            case 11: // NOT
                registers[out] = ~registers[in1];
                break;
            case 12: // CMP
                registers[out] = (registers[in1] > registers[in2]);
                break;
            case 13: // EQ
                registers[out] = registers[in1] == registers[in2];
                break;
            case 14: // JMP
                program_counter = addr;
                continue;
            case 15: // JMP_IF
                if (registers[out]) {
                    program_counter = addr;
                    continue;
                }
                break;
            case 16: // HALT
                return;
            default:
                printf("Error: Invalid opcode %x\n", opcode);
                exit(1);
        }
        program_counter++;
    }
}

void print_instructions() {
    int i;
    for (i = 0; i < num_instructions; i++) {
        unsigned int instruction = instructions[i];
        unsigned int opcode = instruction >> 26;
        unsigned int out = (instruction >> 22) & 0xf;
        unsigned int in1 = (instruction >> 18) & 0xf;
        unsigned int in2 = (instruction >> 14) & 0xf;
        unsigned int imm = instruction & 0x3fff;
        unsigned int addr = instruction & 0x3ffff;
        printf("%s R%d, R%d, R%d, %x, %x\n", instruction_names[opcode], out, in1, in2, imm, addr);
    }
}

void initialize_registers() {
    int i;
    for (i = 0; i < NUM_REGISTERS; i++) {
        registers[i] = 0;
    }
}

void print_register(int i) {
    printf("R%d: %x\n", i, registers[i]);
}

void print_registers() {
    int i;
    for (i = 0; i < NUM_REGISTERS; i++) {
        print_register(i);
    }
}
