import re

def notag(text):
    # Define regex pattern to match text outside <> tags
    pattern = r'(?<=>)([^<]*)(?=<)'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # Concatenate the matches into a single string
    result = ''.join(matches)

    return result 

def compile_class(text, index, lst):
    # insert opening tag @ index
    lst.insert(index, '<class>\n')
    # insert closing tag after last instance of }
    last_element = None
    for item in reversed(lst):
        if '}' in item:
            last_index = len(lst) - index - 1
            break
    lst.insert(last_index+1, '</class>\n')
# def compile_class_var_dec(cur_loc):
# def compile_subroutine():
# def comile_var_dec():

def triage(text, index, lst):
    # compile_class
    if text == 'class':
        compile_class(text, index, lst)
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
    for index, line in enumerate(lst):
        triage(notag(line), index, lst)

    print(lst)

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

