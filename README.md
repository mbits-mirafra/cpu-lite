# cpu-lite
CPU Lite is a small CPU designed for instruction purposes. The spec of the CPU is [here](https://docs.google.com/document/d/1FdNK_6NyDhWIm0i9qcjZsOt_JWX7oAX46fh0V3FiX8I/edit?usp=sharing).

Directories

iss: Instruction set simulator. Takes a file produced by the assembler

scripts: Contains the assembler

examples: Some basic examples

To compile the ISS:

```
> cd iss 
> gcc -o iss iss.c
```

Flow:

- Write an assembly file
- Run the assembler:
  ```
  > assemble.py example.asm example.out
  ```
- Run the instruction set simulator
  ```
  > iss example.out
  ```
