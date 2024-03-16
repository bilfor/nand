import sys

def load_file(file_path):
    lines=[]
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                if '/' not in line:
                    lines.append(line.strip())
        return lines

def dest(line):
    index = line.find('=')

    if index != -1:
        dest = line[0:index]
    else:
        dest = ''

    return dest 

def comp(line):
    eq_index = line.find('=')
    semi_index = line.find(';')

    if eq_index != -1:
        if semi_index == -1:
            comp = line[eq_index+1:]
        else:
            comp = line[eq_index+1:semi_index]
    else:
        if semi_index == -1:
            comp = line[:]
        else:
            comp = line[:semi_index] 
    
    return comp

def jump(line):
    index = line.find(';')
    if index != -1:
        jump = line[index+1:]
    else:
        jump = 'null'
    
    return jump 
