# Brainf--- interpreter in Python

## Usage
### From command line

    ```python
    from bfi import Bfm
    # Hello World!\n
    code = '>++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+.'
    u1 = Bfm(code)

    # exec loop
    running = True
    while running == True:
        running = u1.exec()
    ```

### With debug monitor

    ```python
    output_buffer = []
    def debug_output_func(c): output_buffer.append(c)
    u1 = Bfm(code, output_func=debug_output_func)
    print(u1)

    # exec loop
    running = True
    while running != False:
        # next_step = input('> ')
        running = u1.exec()
        print(u1)
        print(''.join(output_buffer), end='')
        print()
    ```

### Options
- `mem_size=32768`: Alternate memory size can be specified.  Incrementing past `mem_size` raises an error.
- `output_func=None`: Alternate stdout handler (useful for grabbing output when using debug monitor)
- `input_func=None`: Alternate stdin handler

### Error conditions checked
- `SyntaxError('ERROR: Unmatched [ in code')`
- `SyntaxError('ERROR: Unmatched ] in code')`
- `IndexError("ERROR: Memory pointer out of bounds")`
- * Decrementing `mp` below `00` is silently ignored
 

## Setting up the development environment

1. Create a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows, use .venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```