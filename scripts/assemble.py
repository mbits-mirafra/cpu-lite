# Script which takes assembly file and generates machine code

# read command line for input and output files
import sys
import re
import os

instructions = {"LOAD" :          {"args": ["R", "ADDR"]},
                "LOAD_INDIRECT" : {"args": ["R", "ADDR"]},
                "LOAD_IMM" :      {"args": ["R", "IMM"]},
                "STORE" :         {"args": ["R", "ADDR"]},
                "STORE_INDIRECT" : {"args": ["R", "ADDR"]},
                "ADD" :           {"args": ["R", "R", "R"]},
                "SUB" :           {"args": ["R", "R", "R"]},
                "MUL" :           {"args": ["R", "R", "R"]},
                "AND" :           {"args": ["R", "R", "R"]},
                "OR" :            {"args": ["R", "R", "R"]},
                "NOT" :           {"args": ["R", "R"]},
                "CMP" :           {"args": ["R", "R", "R"]},
                "EQ" :            {"args": ["R", "R", "R"]},
                "JMP" :           {"args": ["ADDR"]},
                "JMP_IF" :        {"args": ["R", "ADDR"]},
                "HALT" :          {"args": []}
                }

instruction_opcode_map = {}
instruction_names = list(instructions.keys())
# opcodes start from 1
for i in range(len(instruction_names)):
    instruction_opcode_map[instruction_names[i]] = i + 1

def get_machine_code(instruction, tokens):
    opcode = instruction_opcode_map[instruction]
    machine_code = 0
    # opcode is 6 bits
    machine_code = opcode << 26
    
    # reg is 4 bits
    # addr is 14 bits
    # imm is 14 bits

    bits_used = 6
    args = instructions[instruction]["args"]
    for i in range(len(args)):
        if args[i] == "R":
            reg = int(tokens[i+1][1:])
            machine_code |= reg << (32 - (bits_used + 4))
            bits_used += 4
        elif args[i] == "ADDR" or args[i] == "IMM":
            # addr or imm always in low order 16 bits
            value = int(tokens[i+1], 16)
            machine_code |= value

    return machine_code

def check_args(instruction, tokens, line_num):
    # check for correct number of arguments
    if len(tokens) != len(instructions[instruction]["args"]) + 1:
        print("Error: invalid number of arguments for instruction \"" + instruction + "\"" + " on line " + str(line_num))
        sys.exit()

    # check for valid arguments
    args = instructions[instruction]["args"]
    for i in range(len(args)):
        if args[i] == "R":
            if not re.match(r"R[0-9]+", tokens[i+1]):
                print("Error: invalid argument \"" + tokens[i+1] + "\"" + " on line " + str(line_num))
                sys.exit()
        elif args[i] == "ADDR":
            # match a hex number
            if not re.match(r"0x[0-9|a-f|A-F]+", tokens[i+1]):
                print("Error: invalid argument \"" + tokens[i+1] + "\"" + " on line " + str(line_num))
                sys.exit()
        elif args[i] == "IMM":
            if not re.match(r"0x[0-9|a-f|A-F]+", tokens[i+1]):
                print("Error: invalid argument \"" + tokens[i+1] + "\"" + " on line " + str(line_num))
                sys.exit()

def tokenise(line):
    tokens = []
    # Everything after # is a commnt
    line = line.split("#")[0]
    # remove leading and trailing whitespace
    line = line.strip()
    # split line into tokens
    tokens = line.split()
    return tokens
 

labels = {}
def collect_labels(lines):
    line_num = 0
    for line in lines:
        tokens = tokenise(line)
        if len(tokens) == 0:
            continue

        # check for label
        if tokens[0][-1] == ":":
            label = tokens[0][:-1]
            if label in labels:
                print("Error: duplicate label \"" + label + "\"" + " on line " + str(line_num))
                sys.exit()
            labels[label] = line_num
        line_num += 1

def replace_labels(lines):
    line_num = 0
    for line in lines:
        tokens = tokenise(line)
        if len(tokens) > 0:
            # Remove label from before instruction
            if tokens[0][-1] == ":":
                tokens = tokens[1:]

            # check for label in arguments
            for i in range(len(tokens)):
                if tokens[i] in labels:
                    tokens[i] = hex(labels[tokens[i]])
            line = " ".join(tokens)
            lines[line_num] = line
        line_num += 1

def generate_code(lines, outfile):
    line_num = 0
    for line in lines:
        print("Processing line: " + line)
        tokens = tokenise(line)
        if len(tokens) == 0:
            continue
    
        # Remove label from before instruction
        if tokens[0][-1] == ":":
            tokens = tokens[1:]
    
        # check for instruction
        instruction = tokens[0]
        if instruction not in instruction_names:
            print("Error: invalid instruction \"" + instruction + "\"" + " on line " + str(line_num))
            sys.exit()
    
        line_num += 1
    
        check_args(instruction, tokens, line_num)
        # Create machine code from instruction
        code = get_machine_code(instruction, tokens)
        # write instruction opcode to output file in hex of width 8
        outfile.write('0x'+hex(code)[2:].zfill(8))
        outfile.write('  #'+bin(code)[2:].zfill(32))
        outfile.write("\n")
    
# check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python assemble.py <input file> <output file>")
    sys.exit()

# open input file
try:
   infile = open(sys.argv[1], "r")
except:
    print("Error: could not open input file")
    sys.exit()

# open output file
try:
    outfile = open(sys.argv[2], "w")
except:
    print("Error: could not open output file")
    sys.exit()

# read input file into list of lines
lines = infile.readlines()
line_num = 0

collect_labels(lines)

replace_labels(lines)

generate_code(lines, outfile)


