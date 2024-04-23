import sys
import os
import glob

def load_file(directory_path):
    files = glob.glob(os.path.join(directory_path, f'*.vm'))
    lines = []
    for file_path in files:
        lines.append('~' + os.path.basename(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    if not line.startswith('/'):
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
        'direct': 0
    }

    return switcher.get(segment)
