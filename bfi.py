#!/usr/bin/env python3

import sys
import getch

class Bfm:
    def __init__(self, code='', mem_size=32768, input_func=None, output_func=None):
        self.cycle = 0
        self.mem_size = mem_size
        self.word_size = 256
        self.mem = [0]*mem_size
        self.mp = 0
        self.code = ''.join(c for c in code if c in '.,[]<>+-')  # clean code!
        self.ip = 0
        self.stack = []
        self.input_func = input_func if input_func else lambda: ord(getch.getch())
        self.output_func = output_func if output_func else lambda c: sys.stdout.write(c)

    def exec(self):
        """
        Returns:
            True if running and no output
            False if end of program
        """
        # get current instruction 
        if self.ip < len(self.code):
            instruction = self.code[self.ip]
        else:
            return False    # no more instructions

        # instructions:  + - < > [ ] . ,
        if instruction=='+':
            self.mem[self.mp] = (self.mem[self.mp] + 1) % self.word_size

        elif instruction=='-':
            self.mem[self.mp] = (self.mem[self.mp] - 1) % self.word_size

        elif instruction=='<':
            self.mp = 0 if self.mp <= 0 else self.mp - 1

        elif instruction=='>':
            self.mp = self.mp + 1
            if self.mp >= self.mem_size:
                raise IndexError("ERROR: Memory pointer out of bounds")

        elif instruction==',':
            self.mem[self.mp] = self.input_func()  # use supplied input function

        elif instruction=='.':
            self.output_func(chr(self.mem[self.mp]))    # use supplied output function

        elif instruction=='[':
            # if mem[mp] == 0, skip to matching ']' 
            if self.mem[self.mp] == 0:
                depth = 1
                self.ip += 1  # start w/ next instuction
                while self.ip < len(self.code):
                    if self.code[self.ip] == '[':
                        depth += 1
                    elif self.code[self.ip] == ']':
                        depth -= 1
                        if depth == 0:
                            break
                    self.ip += 1
                if depth > 0:
                    raise SyntaxError('ERROR: Unmatched [ in code')

            # enter loop, push address
            else:
                self.stack.append(self.ip)  

        elif instruction==']':
            if self.mem[self.mp] == 0:   # exit loop
                if not self.stack:
                    raise SyntaxError('ERROR: Unmatched ] in code')
                _ = self.stack.pop()  # discard '[' address
            else:
                self.ip = self.stack[-1]  # get '[' from TOS (don't pop)

        else:  # no-op; do nothing and increment
            pass

        self.ip +=1     # increment instruction pointer
        self.cycle += 1 # increment cycle count
        return True

    def __str__(self):
        # Visualization code directly embedded here
        row_size = 16

        # Show only the row containing the pointer
        pointer_row = self.mp // row_size
        start_idx = pointer_row * row_size
        end_idx = min(len(self.mem), start_idx + row_size)
        row_bytes = self.mem[start_idx:end_idx]

        # Address (leftmost element), show as 4-digit hex
        addr_str = f'{start_idx:04X}:'

        # Hex bytes as two groups of 8 separated by two spaces
        first_half = ' '.join(f'{b:02X}' for b in row_bytes[:8])
        second_half = ' '.join(f'{b:02X}' for b in row_bytes[8:])

        if second_half:
            hex_str = f'{first_half}  {second_half}'
        else:
            hex_str = first_half

        # ASCII characters (printable) or '.'
        ascii_chars = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in row_bytes)

        # Compose the full line
        line = f'{addr_str} {hex_str:<39} |  {ascii_chars}'

        # Pointer indicator line with two carets ^^
        byte_pos_in_row = self.mp % row_size
        if byte_pos_in_row < 8:
            caret_pos = len(addr_str) + 1 + (byte_pos_in_row * 3)
        else:
            caret_pos = len(addr_str) + 1 + (8 * 3 - 1) + 2 + ((byte_pos_in_row - 8) * 3)

        pointer_line = ' ' * caret_pos + '^^'

        # Code snippet visualization
        code_window = 54
        code_start = max(0, self.ip - code_window // 2)
        code_end = min(len(self.code), code_start + code_window)
        code_snippet = self.code[code_start:code_end]
        instr_indicator = ' ' * (self.ip - code_start) + '^'
        stack_str = ' '.join(f'{addr:04X}' for addr in self.stack)

        result = []
        result.append("\nMemory:")
        result.append(line)
        result.append(pointer_line)
        result.append("Code:")
        result.append(code_snippet)
        result.append(instr_indicator)
        result.append(f"Stack (bottom->top): [{stack_str}]")
        result.append(f"\nMem  mp: {self.mp:04X} | Instr ip: {self.ip:04X} | Cycle: {self.cycle}\n")

        return '\n'.join(result)


def main():
    # Parse command-line arguments for -v
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="brainf--- source file")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode: show memory/code before, after run`")
    args = parser.parse_args()

    filename = args.filename
    with open(filename, 'r') as f:
        code = f.read()

    u1 = Bfm(code)

    # exec loop
    running = True
    while running == True:
        running = u1.exec()

    if args.verbose: print(u1)

if __name__ == "__main__":
    main()