import os
import sys
import re
import parser as p
import codewriter as cw
import time

start_time = time.time()

file_path = sys.argv[1]
prog = p.load_file(file_path)

asm = ['@256', 'D=A', '@SP', 'M=D']
stack = []
local = [0] * 10
argument = [0] * 10
this = [0] * 10
that = [0] * 10
pointer = [0] * 10
temp = [0] * 10
sp = 256 

for line in prog:
    parts = re.split(r'\s+', line)
    command = parts[0]
    if len(parts) > 1:
        segment = parts[1]
    if len(parts) > 2: 
        index = int(parts[2])

    if command == 'push':

        if segment == 'constant':
            stack.append(index)
            code = cw.generate_push_asm(sp, 'constant', index)

        if segment == 'local':
            stack.append(local[index])
            code = cw.generate_push_asm(sp, 'local', index)

        if segment == 'argument':
            stack.append(argument[index])
            code = cw.generate_push_asm(sp, 'argument', index)

        if segment == 'this':
            stack.append(this[index])
            code = cw.generate_push_asm(sp, 'this', index)

        if segment == 'that':
            stack.append(that[index])
            code = cw.generate_push_asm(sp, 'that', index)

        print('LINE:', end = ' ')
        print(parts)
        print('STACK:', end = ' ')
        print(stack)
        print('LOCAL:', end = ' ')
        print(local)
        print('ARGUMENT:', end = ' ')
        print(argument)
        print('THIS:', end = ' ')
        print(this)
        print('THAT:', end = ' ')
        print(that)
        print(' ')

        asm.extend(code)

    elif command == 'pop':
        op1 = stack.pop()
        
        if segment == 'local':
            local[index] = op1

        if segment == 'argument':
            argument[index] = op1

        if segment == 'this':
            this[index] = op1

        if segment == 'that':
            that[index] = op1

        code = cw.generate_pop_asm(sp, segment, index)
        asm.extend(code)

        print('LINE:', end = ' ')
        print(parts)
        print('STACK:', end = ' ')
        print(stack)
        print('LOCAL:', end = ' ')
        print(local)
        print('ARGUMENT:', end = ' ')
        print(argument)
        print('THIS:', end = ' ')
        print(this)
        print('THAT:', end = ' ')
        print(that)
        print(' ')

    elif parts[0] == 'add':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_add_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op1)+int(op2))

    elif parts[0] == 'sub':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_sub_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op2)-int(op1))

    elif parts[0] == 'neg':
        op1 = stack.pop()
        code = cw.generate_neg_asm(sp, op1)
        asm.extend(code)
        stack.append(-op1)

    elif parts[0] == 'eq':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_eq_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(op1==op2)

    elif parts[0] == 'lt':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_lt_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(op2<op1)

    elif parts[0] == 'gt':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_gt_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(op2>op1)

    elif parts[0] == 'and':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_and_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op2)&op1)

    elif parts[0] == 'or':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_or_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(op2|int(op1))

    elif parts[0] == 'not':
        op1 = stack.pop()
        code = cw.generate_not_asm(sp, op1)
        asm.extend(code)
        stack.append(~op1)

front = file_path[:-3]
out_name = front + '.asm'
with open(out_name, 'w') as file:
    for line in asm:
        file.write(f"{line}\n") 

print(time.time() - start_time)