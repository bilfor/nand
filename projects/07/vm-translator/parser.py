import sys

def load_file(file_path):
    lines=[]
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                if '/' not in line:
                    lines.append(line.strip())
        return lines

def switcher(segment):
    switcher = {
        'local': 1,
        'argument': 2,
        'this': 3,
        'that': 4,
        'temp': 5,
        'gpr': 13,
        'pointer': 3,
        'static': 16,
    }

    return switcher.get(segment)
