import os
import glob

def constructor(directory):
    for file_path in glob.glob(os.path.join(directory, '*T.xml')):
        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file]
            tokens = tokens[1:-1]
            compile_class(tokens)

def compile_class(tokens):
    print(tokens)
