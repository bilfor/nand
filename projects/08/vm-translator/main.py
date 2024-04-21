import os
import sys
import re
import parser as p
import codewriter as cw
import time

start_time = time.time()

file_path = os.path.abspath(sys.argv[1])
dir_name = os.path.basename(file_path)
file_name = os.path.splitext(os.path.basename(file_path))[0]
front = file_path[:-3]
prog = p.load_file(file_path)
bootstrap_vm = ['call Sys.init 0']
prog = bootstrap_vm + prog 

asm = cw.generate_bootstrap_asm()
# asm = []
stack = []
local = [0] * 10
argument = [0] * 10
this = [0] * 10
that = [0] * 10
pointer = [0] * 10
static = [0] * 10
temp = [0] * 10
sp = 256 

call_counter = 1
eq_counter = 1
gt_counter = 1
lt_counter = 1

for line in prog:
    print(line)
    print('\n')
    clean = line.split('/')[0]
    parts = clean.split()
    asm.append('// ' + clean)
    if parts == []:
        continue
    if len(parts) > 0:
        command = parts[0]
    if len(parts) > 1:
        segment = parts[1]
    if len(parts) > 2: 
        index = int(parts[2])

    if command == 'call':
        # Xxx.foo$ret.i
        # Xxx.foo = segment
        # ret = ret
        # i = call_counter
        ret_addr = segment + '$ret.' + str(call_counter)
        print('ret_addr: ' + ret_addr)

        #
        #
        #

        code = cw.generate_call_asm(segment, index, ret_addr)
        asm.extend(code)

        call_counter += 1

    if command == 'function':
        code = cw.generate_function_asm(segment, index)
        asm.extend(code)

    if command == 'label':
        code = cw.generate_label_asm(segment)
        asm.extend(code)

    if command == 'if-goto':
        code = cw.generate_ifgoto_asm(segment)
        asm.extend(code)

    if command == 'goto':
        code = cw.generate_goto_asm(segment)
        asm.extend(code)

    if command == 'return':
        code = cw.generate_return_asm()
        asm.extend(code)

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

        if segment == 'temp':
            stack.append(temp[index])
            code = cw.generate_push_asm(sp, 'temp', index)

        if segment == 'pointer':
            stack.append(pointer[index])
            code = cw.generate_push_asm(sp, 'pointer', index)

        if segment == 'static':
            stack.append(static[index])
            code = cw.generate_push_asm(file_name, 'static', index)

        asm.extend(code)

    if command == 'pop':
        try:
            op1 = stack.pop()
        except IndexError:
            print('emptypop')
        
        if segment == 'local':
            local[index] = op1

        if segment == 'argument':
            argument[index] = op1

        if segment == 'this':
            this[index] = op1

        if segment == 'that':
            that[index] = op1

        if segment == 'temp':
            temp[index] = op1

        if segment == 'pointer':
            pointer[index] = op1

        if segment == 'static':
            static[index] = op1

        code = cw.generate_pop_asm(file_name, segment, index)

        asm.extend(code)

    if command == 'add':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_add_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op1)+int(op2))

    if command == 'sub':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_sub_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op2)-int(op1))

    if command == 'neg':
        op1 = stack.pop()
        code = cw.generate_neg_asm(sp, op1)
        asm.extend(code)
        stack.append(-op1)

    if command == 'eq':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_eq_asm(eq_counter)
        eq_counter += 1
        asm.extend(code)
        stack.append(op1==op2)

    if command == 'lt':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_lt_asm(lt_counter)
        lt_counter += 1
        asm.extend(code)
        stack.append(op2<op1)

    if command == 'gt':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_gt_asm(gt_counter)
        gt_counter += 1
        asm.extend(code)
        stack.append(op2>op1)

    if command == 'and':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_and_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(int(op2)&op1)

    if command == 'or':
        op1 = stack.pop()
        op2 = stack.pop()
        code = cw.generate_or_asm(sp, op1, op2)
        asm.extend(code)
        stack.append(op2|int(op1))

    if command == 'not':
        op1 = stack.pop()
        code = cw.generate_not_asm(sp, op1)
        asm.extend(code)
        stack.append(~op1)

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
    print('TEMP:', end = ' ')
    print(temp)
    print('POINTER:', end = ' ')
    print(pointer)
    print('STATIC:', end = ' ')
    print(static)
    print(' ')

print(asm)

out_name = file_path + '/' + dir_name + '.asm'
print(out_name)
with open(out_name, 'w') as file:
    for line in asm:
        file.write(f"{line}\n") 

#print(time.time() - start_time)
