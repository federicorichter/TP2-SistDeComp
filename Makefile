# Compiler flags
CFLAGS = -Wall -Wextra -std=c11

# Linker flags
LDFLAGS =

# Target executable
TARGET = calculator

# Source files
C_SOURCES = calculator.c
ASM_SOURCES = float_to_int.asm

# Object files
C_OBJECTS = $(C_SOURCES:.c=.o)
ASM_OBJECTS = $(ASM_SOURCES:.asm=.o)

all: $(TARGET)

# Rule to compile C files
%.o: %.c
	gcc $(CFLAGS) -c $< -o $@

# Rule to compile assembly files
%.o: %.asm
	nasm -f elf64 $< -o $@

# Linking rule
$(TARGET): $(C_OBJECTS) $(ASM_OBJECTS)
	gcc $(C_OBJECTS) $(ASM_OBJECTS) $(LDFLAGS) -g -o $(TARGET)

clean:
	rm -f $(TARGET) $(C_OBJECTS) $(ASM_OBJECTS)
