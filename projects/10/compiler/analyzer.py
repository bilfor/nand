import os
import sys
import tokenizer as t
import engine as e

# Specify the directory you want to work with as a cmd line arg
directory = sys.argv[1]

# keywords
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
            'this', 'let', 'do', 'if', 'else', 'while', 'return']
# symbols
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', 
           '&', '|', '<', '>', '=', '~']

def remove_comments(code):
    lines = code.split('\n')
    cleaned_code = []
    inside_block_comment = False
    for line in lines:
        # Check for /* and */ comments
        if '/*' in line and '*/' in line:
            line = line.split('/*')[0] + line.split('*/')[1]
        elif '/*' in line:
            inside_block_comment = True
            line = line.split('/*')[0]
        elif '*/' in line:
            inside_block_comment = False
            line = line.split('*/')[1]
        elif inside_block_comment:
            line = ''

        # Check for /** and */ comments
        if '/**' in line and '*/' in line:
            line = line.split('/**')[0] + line.split('*/')[1]
        elif '/**' in line:
            inside_block_comment = True
            line = line.split('/**')[0]
        elif '*/' in line:
            inside_block_comment = False
            line = line.split('*/')[1]
        elif inside_block_comment:
            line = ''

        # Remove comments starting with //
        line = line.split('//')[0].rstrip()

        cleaned_code.append(line)
    return '\n'.join(cleaned_code)

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if the file is a .jack file
    if filename.endswith('.jack'):

        jack_file_path = os.path.join(directory, filename)

        xml_file_path = os.path.join(directory, filename.replace('.jack', 'T.xml'))
        
        with open(jack_file_path, 'r') as jack_file:
            code = jack_file.read()

        no_comments_code = remove_comments(code)
        no_whitespace_code = no_comments_code.strip() 
        tokens = t.tokenize(no_whitespace_code)

        # Open the .xml file in write mode
        with open(xml_file_path, 'w') as xml_file:
            # Write arbitrary text to the .xml file
            xml_file.write('<tokens>\n')
            for token in tokens:
                if token in symbols:
                    tag = 'symbol'
                    if token == '<':
                        token = '&lt;'
                    if token == '>':
                        token = '&gt;'
                    if token == '"':
                        token = '&quot;'
                    if token == '&':
                        token = '&amp;'
                elif token in keywords:
                    tag = 'keyword'
                elif token[0].isdigit():
                    tag = 'integerConstant'
                elif '"' in token:
                    tag = 'stringConstant'
                    token = token.replace('"', '')
                else:
                    tag = 'identifier'


                xml_file.write('<' + tag + '>' + token + '</' + tag + '>' + '\n')
            xml_file.write('</tokens>')

        print(f'Processed {jack_file_path} and wrote to {xml_file_path}')

