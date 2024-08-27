import re
import os

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

def string_tokenize(s):
    words_and_chars = []
    word = ''
    inside_quotes = False

    for char in s:
        if char == '"':
            if inside_quotes:
                if word:
                    words_and_chars.append('"' + word + '"')
                    word = ''
                inside_quotes = False
            else:
                if word:
                    words_and_chars.append('"' + word + '"')
                    word = ''
                inside_quotes = True
        elif inside_quotes:
            word += char
        elif char.isalnum():
            word += char
        else:
            if word:
                words_and_chars.append(word)
                word = ''
            if char != ' ':
                words_and_chars.append(char)
    
    if word:
        words_and_chars.append(word)

    return words_and_chars

def simple_tokenize(s):
    words_and_chars = []
    word = ''
    for char in s:
        if char.isalpha():
            word += char
        else:
            if word:
                words_and_chars.append(word)
                word = ''
            if char != ' ':
                words_and_chars.append(char)
    if word:
        words_and_chars.append(word)
    
    return words_and_chars

def merge_entries_with_quotes(lst):
    merged_list = []
    merge_flag = False
    merged_entry = ''

    for entry in lst:
        if entry == '"':
            if merge_flag:
                merged_list.append(merged_entry)
                merged_entry = ''
                merge_flag = False
            else:
                merge_flag = True
        elif merge_flag:
            if merged_entry:
                merged_entry += ' '
            merged_entry += entry
        else:
            merged_list.append(entry)

    return merged_list

def tokenize(nc_nnl_code):
    simple = string_tokenize(nc_nnl_code) 
    simple_nw = [item for item in simple if item != "\n"] 
    simple_nw_nt = [item for item in simple_nw if item != "\t"] 
    merged = merge_entries_with_quotes(simple_nw_nt)
    return merged

def main(directory):
    # keywords
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
                'this', 'let', 'do', 'if', 'else', 'while', 'return']
    # symbols
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', 
               '&', '|', '<', '>', '=', '~']

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
            tokens = tokenize(no_whitespace_code)

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

if __name__ == "__main__":
    main()
