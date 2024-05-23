import re
import xml.dom.minidom
####
def notag(text):
    # Define regex pattern to match text outside <> tags
    pattern = r'(?<=>)([^<]*)(?=<)'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # Concatenate the matches into a single string
    result = ''.join(matches)

    return result 

def compile_class(text, index, lst, cpy):
    # insert opening tag @ index
    cpy.insert(index, '<class>\n')
    print('compile_class')

# def compile_class_var_dec(cur_loc):
# def compile_subroutine():
# def comile_var_dec():

def triage(text, index, lst, cpy):
    # compile_class
    if text == 'class':
        print('class detected')
        compile_class(text, index, lst, cpy)
    # compile_class_var_dec
    #if (text == 'static' or text == 'field'):
        #compile_class_var_dec(text, index, lst)
    # compile_subroutine
    #if text == ('constructor' or text == 'function' or text == 'method'):
        #compile_subroutine(text, index, lst)
    # compile_var_dec
    #if text == 'var':
        #compile_var_dec(text, index, lst)
  
def compile(lst):
    cpy = lst.copy()
    for index, line in enumerate(lst):
        #print(f"Index: {index}, Value: {line}")
        triage(notag(line), index, lst, cpy)

    print('\n'.join(cpy))

    return cpy

# def token_type():
# def content():

# def compile_parameter_list():
# def compile_statements():
# def compile_do():
# def compile_let():
# def compile_while():
# def compile_return():
# def compile_if():
# def compile_expression():
# def compile_term():
# def compile_expression_list():

