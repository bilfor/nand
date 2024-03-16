import os
import sys
import re
import parser as p
import code as c
import symbol_table as st
import time

start_time = time.time()

file_path = sys.argv[1]
prog = p.load_file(file_path)

#print(prog)

hack = []

symbol_table = st.constructor()
#print(prog)

st.first_pass(prog,symbol_table) 
print(symbol_table)

free_mem = 16

for line in prog:
    if line[0] == '@':
        if line[1].isdigit():
            addr = int(line[1:])
        else:
            key = line[1:]
            #print(key)
            if key not in symbol_table:
                symbol_table[key] = free_mem
                free_mem += 1
            val = symbol_table[key]
            addr = int(val)
        bin_addr = bin(addr)[2:]
        full_bin_addr = bin_addr.zfill(16)
        #print(full_bin_addr)
        hack.append(full_bin_addr) 
        #print("A INSTRUCTION: " + full_bin_addr) 
    
    elif '(' not in line:
        dest = p.dest(line)
        comp = p.comp(line)
        #print(comp)
        jump = p.jump(line)
        dcode = c.dest(dest)
        ccode = c.comp(comp)
        jcode = c.jump(jump)
        #print(jcode)
        full_c_instr = "111" + ccode + dcode + jcode 
        #print("C INSTRUCTION: " + full_c_instr) 
        hack.append(full_c_instr) 
 
#print(hack)

dot = file_path.find('.')
front = file_path[:dot]
out_name = front + '-w' + '.hack'
#print(out_name)
with open(out_name, 'w') as file:
    for line in hack:
        file.write(f"{line}\n") 

print(time.time() - start_time)
