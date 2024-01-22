# cpu-lite
CPU Lite is a small CPU designed for instruction purposes.

Directories

iss: Instruction set simulator. Takes a file produced by the assembler
scripts: Contains the assembler
examples: Some basic examples

To compile the ISS:

> cd iss
> gcc -o iss iss.c

Flow:

- Write an assembly file
- Run the assembler:
  > assemble.py example.asm example.out
- Run the instruction set simulator
  > iss example.out
