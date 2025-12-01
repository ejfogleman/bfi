from bfi import Bfm
import time

# initialization
# the complete "Hello World!\n" string (print and leave in memory)
code = '>+++++++++[<++++++++>-]<.> >>+++++[<+++++>-]<[<++++>-]<+.> >>+++++++++[<++++>-]<[<+++>-]<.> >>+++++++++[<++++>-]<[<+++>-]<.> >>+++++++[<++++>-]<[<++++>-]<-.> >++++++++[<++++>-]<.> >>+++++++++[<+++++>-]<[<++>-]<---.> >>+++++++[<++++>-]<[<++++>-]<-.> >>+++++++[<++++>-]<[<++++>-]<++.> >>+++++++++[<++++>-]<[<+++>-]<.> >>+++++[<+++++>-]<[<++++>-]<.> >++++++++[<++++>-]<+.> ++++++++++.'

# https://en.wikipedia.org/wiki/Brainf---
# https://esolangs.org/wiki/Brainf---
# another hello world: | passes
code = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
# another (2) | passes
code = '+++++++++++[>++++++>+++++++++>++++++++>++++>+++>+<<<<<<-]>++++++.>++.+++++++..+++.>>.>-.<<-.<.+++.------.--------.>>>+.>-.'
# another (3) | passes
code = '>++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+.'

# test unmatched [
# code = '[[[]]'
# test unmatched ]
# code = '[[]]]'
# test memory out of bounds error
# code = '>>>>>>>>>'

output_buffer = []
def debug_output_func(c): output_buffer.append(c)
u1 = Bfm(code, mem_size=32768, output_func=debug_output_func)
print(u1)

# exec loop
running = True
while running != False:
    # next_step = input('> ')
    running = u1.exec()
    print(u1)
    print(''.join(output_buffer), end='')
    print()
    time.sleep(0.01)
