import os
import glob

def print_list(input_list):
    for item in input_list:
        print(item)

def advance(tokens, index):
    index = index + 1
    token, content, tag = get_token_data(tokens, index)
    return index, token, content, tag

def current_token(tokens, index):
    return tokens[index]

def get_tag(token):
    start_tag_start = token.find("<") + 1
    start_tag_end = token.find(">", start_tag_start)
    return token[start_tag_start:start_tag_end]

def get_content(token):
    start_tag_end = token.find(">") + 1
    end_tag_start = token.rfind("<")
    return token[start_tag_end:end_tag_start]

def get_token_data(tokens, index):
    token = current_token(tokens, index)
    content = get_content(token)
    tag = get_tag(token)
    return token, content, tag 

def constructor(directory):
    for file_path in glob.glob(os.path.join(directory, '*T.xml')):
        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file]
            tokens = tokens[1:-1]
            compile_class(tokens)

def compile_class(tokens):
    index = 0
    output = []

    token, content, tag = get_token_data(tokens, index)

    # first token will always be class
    if content == 'class':
        output.append('<class>')
        output.append(token)
        index, token, content, tag = advance(tokens, index)
        
    # second token will always be class name
    if tag == 'identifier':
        output.append(token)
        index, token, content, tag = advance(tokens, index)

    # third token will always be '{'
    if content == '{':
        output.append(token)
        index, token, content, tag = advance(tokens, index)

    while content != '}':
        print(f"Processing token: {token}")

        if content in {"static", "field"}:
            index = compile_class_var_dec(tokens, index, output)

        elif content in {"constructor", "function", "method"}:
            index = compile_subroutine(tokens, index, output)

        else:
            print(f"Unexpected token: {tokens[index]}")

        index, token, content, tag = advance(tokens, index)

    if tokens[index] == "}":
        output.append("<symbol> } </symbol>")
        output.append("</class>")
       
    print('\n\n\n\n\n\n\n\n\n')
    print_list(output)
    print('\n\n\n\n\n\n\n\n\n')
    return output 

def compile_class_var_dec(tokens, index, output):
    output.append('<classVarDec>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # either field or static

    index, token, content, tag = advance(tokens, index)
    output.append(token) # type

    index, token, content, tag = advance(tokens, index)
    output.append(token) # varName

    index, token, content, tag = advance(tokens, index)

    # handle additional varNames
    while content == ",":
        output.append(token) # comma
        index, token, content, tag = advance(tokens, index)
        output.append(token) # varName
        index, token, content, tag = advance(tokens, index)

    # end of classVarDec
    if content == ";":
        output.append(token)
    
    output.append("</classVarDec>")

    return index

def compile_subroutine(tokens, index, output):
    output.append('<subroutineDec>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # constructor, function, or method

    index, token, content, tag = advance(tokens, index)
    output.append(token) # void or type

    index, token, content, tag = advance(tokens, index)
    output.append(token) # subroutineName 

    index, token, content, tag = advance(tokens, index)
    output.append(token) # (

    index, token, content, tag = advance(tokens, index)
    compile_parameter_list(token, index, output) # always a parameter list

    index, token, content, tag = advance(tokens, index)
    output.append(token) # )

    index, token, content, tag = advance(tokens, index)
    compile_subroutine_body(token, index, output) # always a SRB

    return index
