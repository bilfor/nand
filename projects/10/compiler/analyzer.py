import os
import sys
import re
import tokenizer as t
import engine as e
import xml.dom.minidom

def pretty_print_xml_elements(xml_elements):
    """
    Pretty print a list of XML elements with indentation.

    Args:
    xml_elements (list of str): List of XML element strings to be formatted and printed.
    """
    # Wrap the individual XML elements in a root element
    wrapped_xml = f"<root>{''.join(xml_elements)}</root>"
    
    # Parse the wrapped XML string into a DOM object
    dom = xml.dom.minidom.parseString(wrapped_xml)
    
    # Pretty print the DOM object with tabs for indentation
    pretty_xml_as_string = dom.toprettyxml(indent="\t")
    
    # Remove the added root element and the first line (XML declaration)
    pretty_xml_body = '\n'.join(pretty_xml_as_string.split('\n')[2:])
    
    # Print the formatted XML string
    print(pretty_xml_body)

# Specify the directory you want to work with as a cmd line arg
directory = sys.argv[1]

# keywords
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
            'this', 'let', 'do', 'if', 'else', 'while', 'return']
# symbols
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', 
           '&', '|', '<', '>', '=', '~']

def read_file_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        # Strip newline characters from each line and create a list
        lines = [line.strip() for line in lines]
    return lines

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

        print(f'Processed {jack_file_path} and wrote to {xml_file_path}\n\n')

xml_tokens = read_file_lines(xml_file_path)
#print(xml)
print('Compiling...\n\n')
compiled_xml_list = e.compile(xml_tokens)

pretty_print_xml_elements(compiled_xml_list)
