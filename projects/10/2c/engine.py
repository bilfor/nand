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

def add_indentation(output):
    indented_output = []
    indent_level = 0

    for line in output:
        if line.startswith("</"):  # Closing tag decreases indentation
            indent_level -= 1

        indented_output.append("  " * indent_level + line)

        if line.startswith("<") and not line.startswith("</") and not line.endswith("/>"):  # Opening tag increases indentation
            indent_level += 1

    return indented_output

def constructor(directory):
    for file_path in glob.glob(os.path.join(directory, '*T.xml')):
        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file]
            tokens = tokens[1:-1]
            output = compile_class(tokens)
            indented = add_indentation(output)

            output_fp = file_path[:-5] + 'C.xml'
            with open(output_fp, 'w') as file:
                for item in output:
                    file.write(item + '\n')

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
        print('***************************************')
        print(f"********** CLASS: {content} **********")
        print('***************************************')
        output.append(token)
        index, token, content, tag = advance(tokens, index)

    # third token will always be '{'
    if content == '{':
        output.append(token)
        index, token, content, tag = advance(tokens, index)

    while content != '}':
        #print(f"Processing token: {token}")

        if content in {"static", "field"}:
            index = compile_class_var_dec(tokens, index, output)

        elif content in {"constructor", "function", "method"}:
            index = compile_subroutine(tokens, index, output)

        #else:
            #print(f"Unexpected token: {tokens[index]}")

        index, token, content, tag = advance(tokens, index)

    if tokens[index] == "}":
        output.append("<symbol> } </symbol>")
        output.append("</class>")
       
    print('\n\n')
    print_list(output)
    print('\n\n')

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
    index = compile_parameter_list(tokens, index, output) # always a parameter list

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # )

    index, token, content, tag = advance(tokens, index)
    index = compile_subroutine_body(tokens, index, output) # always a SRB

    output.append('</subroutineDec>')

    return index

def compile_parameter_list(tokens, index, output):
    output.append('<parameterList>')

    token, content, tag = get_token_data(tokens, index)
    
    if content == ')':
        output.append("</parameterList>")
        # output.append(token) # )
        return index # empty parameterList

    while True:
        output.append(token) # type, if not empty list

        index, token, content, tag = advance(tokens, index)
        output.append(token) # varName
    
        index, token, content, tag = advance(tokens, index)

        if content != ',':
            break # no more

        output.append(token) # ,
        index, token, content, tag = advance(tokens, index)

    output.append("</parameterList>")
    # output.append(token) # )

    return index

def compile_subroutine_body(tokens, index, output):
    statements = ['let', 'if', 'while', 'do', 'return']

    output.append('<subroutineBody>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # {

    index, token, content, tag = advance(tokens, index)

    if content == 'var':
        # token, content, tag = get_token_data(tokens, index)
        index = compile_var_dec(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)

    if content in statements:
        index = compile_statements(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # }

    output.append('</subroutineBody>')

    return index

def compile_var_dec(tokens, index, output):
    output.append('<varDec>')

    token, content, tag = get_token_data(tokens, index)

    while True:
        output.append(token) # var

        index, token, content, tag = advance(tokens, index)
        output.append(token) # type
    
        index, token, content, tag = advance(tokens, index)
        output.append(token) # varName

        index, token, content, tag = advance(tokens, index)

        if content == ';':
            break # no more

        output.append(token) # ,
        index, token, content, tag = advance(tokens, index)

    output.append(token) # ;
    index, token, content, tag = advance(tokens, index)
    output.append('</varDec>')

    return index

def compile_statements(tokens, index, output):
    statements = ['let', 'if', 'while', 'do', 'return']

    output.append('<statements>')

    token, content, tag = get_token_data(tokens, index)

    while content in statements:

        if content == 'let':
            index = compile_let(tokens, index, output)

        if content == 'if':
            index = compile_if(tokens, index, output)

        if content == 'while':
            index = compile_while(tokens, index, output)

        if content == 'do':
            index = compile_do(tokens, index, output)

        if content == 'return':
            index = compile_return(tokens, index, output)

        index, token, content, tag = advance(tokens, index)

        print(content)

    output.append('</statements>')
    return index

def compile_let(tokens, index, output):
    output.append('<letStatement>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # let 
    
    index, token, content, tag = advance(tokens, index)
    output.append(token) # varName

    index, token, content, tag = advance(tokens, index)

    if content == '[':
        output.append(token) # [
        index = compile_expression(tokens, index, output)
        token, content, tag = get_token_data(tokens, index)

    if content == '=':
        output.append(token) # =

    index, token, content, tag = advance(tokens, index)
    index = compile_expression(tokens, index, output)
        
    token, content, tag = get_token_data(tokens, index)
    output.append(token) # ;

    output.append('</letStatement>')
    return index

def compile_if(tokens, index, output):
    output.append('<ifStatement>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # if

    index, token, content, tag = advance(tokens, index)
    output.append(token) # (

    index, token, content, tag = advance(tokens, index)
    index = compile_expression(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # )

    index, token, content, tag = advance(tokens, index)
    output.append(token) # {

    index, token, content, tag = advance(tokens, index)
    index = compile_statements(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # }

    index, token, content, tag = advance(tokens, index)
    
    if content == 'else':
        output.append(token) # else
    
        index, token, content, tag = advance(tokens, index)
        output.append(token) # {

        index, token, content, tag = advance(tokens, index)
        index = compile_statements(tokens, index, output)

        token, content, tag = get_token_data(tokens, index)
        output.append(token) # }

        index, token, content, tag = advance(tokens, index)

    index -= 1

    output.append('</ifStatement>')
    return index

def compile_while(tokens, index, output):
    return index

def compile_do(tokens, index, output):
    output.append('<doStatement>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # do 
    
    index, token, content, tag = advance(tokens, index)
    index = compile_subroutine_call(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # ; 

    # index, token, content, tag = advance(tokens, index)

    output.append('</doStatement>')
    return index

def compile_return(tokens, index, output):
    output.append('<returnStatement>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # return

    index, token, content, tag = advance(tokens, index)

    if content != ';':
        index = compile_expression(tokens, index, output)
        token, content, tag = get_token_data(tokens, index)

    output.append(token) # ;

    # index, token, content, tag = advance(tokens, index)
    output.append('</returnStatement>')
    return index

def compile_expression(tokens, index, output):
    output.append('<expression>')
    output.append('<term>')

    token, content, tag = get_token_data(tokens, index)
    output.append(token)
    index, token, content, tag = advance(tokens, index)

    output.append('</term>')
    output.append('</expression>')
    return index

def compile_subroutine_call(tokens, index, output):
    token, content, tag = get_token_data(tokens, index)
    output.append(token) # subroutineName

    index, token, content, tag = advance(tokens, index)

    if content == '.':
        output.append(token) # .

        index, token, content, tag = advance(tokens, index)
        output.append(token) # subroutineName

        index, token, content, tag = advance(tokens, index)
 
    output.append(token) # (

    index, token, content, tag = advance(tokens, index)
    index = compile_expression_list(tokens, index, output)

    token, content, tag = get_token_data(tokens, index)
    output.append(token) # )

    index, token, content, tag = advance(tokens, index)

    return index

def compile_expression_list(tokens, index, output):
    output.append('<expressionList>')

    token, content, tag = get_token_data(tokens, index)
    
    if content != ')':
        index = compile_expression(tokens, index, output)

    output.append('</expressionList>')

    return index
