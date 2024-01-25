# Simple loop which adds numbers 1 to 10
LOAD_IMM R0 0x1    # R0 is the loop increment
LOAD_IMM R1 0xa    # R1 is the loop limit 
LOAD_IMM R2 0x1    # R2 is the counter
LOAD_IMM R3 0x0    # R3 is the sum
LOOP: CMP R4 R2 R1     # R4 = R2 > R1
JMP_IF R4 END_OF_LOOP
ADD R3 R3 R2     # R3 = R3 + R2
ADD R2 R2 R0     # R2 = R2 + 1
JMP LOOP
END_OF_LOOP: HALT

