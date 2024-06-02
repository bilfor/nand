from lxml import etree
import re

def print_elements(element):
    #print(etree.tostring(element, pretty_print=True).decode())
    for child in element:
        print_elements(child)

def rename_root_element(tree, new_root_tag):
    # Get the current root element
    root = tree.getroot()

    # Create a new root element with the desired tag
    new_root = etree.Element(new_root_tag)

    # Copy attributes from the original root to the new root
    for key, value in root.attrib.items():
        new_root.set(key, value)

    # Copy children from the original root to the new root
    for child in root:
        new_root.append(child)

    # Set the new root as the root of the tree
    tree._setroot(new_root)  # Use _setroot() to set the root without triggering validation errors

def find_next(tree, symbol, start):
    index = start
    for item in tree[start:]:
        if get_text(item) == symbol:
            return index + 1
        else:
            index += 1

# def compile_subroutine():
# def comile_var_dec():

def triage(text, index, tree):
    insertion = False

    parent = find_one_higher_parent(tree, index)
    print('PARENT: ' + parent)

    # compile_class_var_dec
    if (text == ' static ' or text == ' field '):
        tree.insert(index, '<classVarDec>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</classVarDec>')
        insertion = 'before'

    if (text == ' constructor ' or text == ' function ' or text == ' method' ):
        tree.insert(index, '<subroutineDec>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</subroutineDec>')
        insertion = 'before'

    if (text == ' ( '):
        tree.insert(index + 1, '<parameterList>')
        final_element_index = find_next(tree, ' ) ', index)
        tree.insert(final_element_index - 1, '</parameterList>')
        insertion = 'after'

    if (parent == 'subroutineDec' and text == ' { '):
        tree.insert(index, '<subroutineBody>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</subroutineBody>')
        insertion = 'before'

    return insertion
        # print('final_element_index: ' + str(final_element_index))
        # print('post insert index: ' + str(index))
        # print('text: ' + text + '\n')
        # print('pre insert index: ' + str(index))
    # compile_subroutine
    #if text == ('constructor' or text == 'function' or text == 'method'):
        #compile_subroutine(text, index, lst)
    # compile_var_dec
    #if text == 'var':
        #compile_var_dec(text, index, lst)

def get_text(input_string):
    # Define a regular expression pattern to match the text between <tag> and </tag>
    pattern = r'<[^>]+>([^<]+)</[^>]+>'
    
    # Search for the pattern in the input string
    match = re.search(pattern, input_string)
    
    # If a match is found, return the text, otherwise return None
    if match:
        return match.group(1)
    else:
        return None
  
# def find_closing(symbol, start) 

def replace_first_and_last(lst, x, y):
    if len(lst) >= 1:
        lst[0] = x
    if len(lst) >= 2:
        lst[-1] = y
    return lst

def compile(tree):
    tree = replace_first_and_last(tree, '<class>', '</class>')

    index = 0
    insertion = 'none'

    for element in tree:
        if insertion == 'before':
            index += 1
            insertion = 'none'
            continue
        if insertion == 'after':
            index += 1
            insertion = 'before'
            continue

        print(element)
        # print('\n' + element + '\n')
        text = get_text(element)
        insertion = triage(text, index, tree)
        index += 1
        print('INDEX: ' + str(index))

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

