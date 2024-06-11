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

def get_parent(tree, index):
    i = 0
    stack = []
    for element in tree:
        if element.count('<') == 1 and element.count('/') == 1:
            popped = stack.pop()
            # print('popping: ' + popped)
        if element.count('<') == 1 and element.count('/') == 0:
            stack.append(element)
            # print('appending: ' + element)
        if index == i:
            if stack:
                # print(stack[-1])
                return stack.pop()
            else:
                return 'class'

        i += 1

def triage(text, index, tree):
    insertion = 'none' 

    parent = get_parent(tree, index)
    #print('PARENT: ' + str(parent))

    # compile_class_var_dec
    if (text == ' static ' or text == ' field '):
        tree.insert(index, '<classVarDec>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</classVarDec>')
        insertion = 'before'

    if (text == ' constructor ' or text == ' function ' or text == ' method ' ):
        tree.insert(index, '<subroutineDec>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</subroutineDec>')
        insertion = 'before'

    if (text == ' ( ' and 'ifStatement' not in parent):
        tree.insert(index + 1, '<parameterList>')
        final_element_index = find_next(tree, ' ) ', index)
        tree.insert(final_element_index - 1, '</parameterList>')
        insertion = 'after'

    if (parent == '<subroutineDec>' and text == ' { '):
        tree.insert(index, '<subroutineBody>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</subroutineBody>')
        insertion = 'before'

    if (text == ' let '):
        tree.insert(index, '<letStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</letStatement>')
        insertion = 'before'

    if (text == ' do '):
        tree.insert(index, '<doStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</doStatement>')
        insertion = 'before'

    if (text == ' return '):
        tree.insert(index, '<returnStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</returnStatement>')
        insertion = 'before'

    if (text == ' if '):
        tree.insert(index, '<ifStatement>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</ifStatement>')
        insertion = 'before'

    if (text == ' while '):
        tree.insert(index, '<whileStatement>')
        final_element_index = find_next(tree, ' } ', index)
        tree.insert(final_element_index, '</whileStatement>')
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

def group_lets(tree):
    index = 0
    statements = ['<letStatement>', '<ifStatement>', '<doStatement>', '<returnStatement>', '<whileStatement>']
    closing_statements = ['</letStatement>', '</ifStatement>', '</doStatement>', '</returnStatement>', '</whileStatement>']
    prev_opening = False
    prev_closing = False
    flag = False

    for element in tree:
        opening = any(substring in element for substring in statements)
        closing = any(substring in element for substring in closing_statements)

        if flag:
            flag = False
            continue

        #print('\n\nELEMENT: ' + str(element))
        #print('OPENING: ' + str(opening))
        #print('CLOSING: ' + str(closing))

        if opening and not prev_closing: 
            tree.insert(index, '<statements>')
            index += 1
            flag = True

        if prev_closing and not opening:
            tree.insert(index, '</statements>')
            index += 1
            flag = True
            
        index += 1
        prev_opening = opening
        prev_closing = closing

        if flag:
            prev_opening = False
            prev_closing = False

def wrap(tree, index, content):
    tree.insert(index, '<' + content + '>')
    tree.insert(index+2, '</' + content + '>')

def expressions(tree):
    statements = ['<doStatement>', '<letStatement>', '<ifStatement>', '<returnStatement>', '<whileStatement>']
    closing_statements = ['</doStatement>', '</letStatement>', '</ifStatement>', '</returnStatement>', '</whileStatement>']
    index = 0
    flag = False
    insertion_count = 0
    insertion_flag = False
    last3 = None
    last2 = None
    last = None

    for element in tree:

        if insertion_count > 0:
            insertion_count -= 1
            continue

        opening = any(substring in element for substring in statements)
        closing = any(substring in element for substring in closing_statements)

        if flag:
            if parent == '<ifStatement>':
                if '(' in last:
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
                if ')' in element:
                    tree.insert(index, '</expression>')
                    tree.insert(index, '</term>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
            if parent == '<letStatement>':
                if '=' in last:
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                if ';' in last:
                    tree.insert(index-1, '</expression>')
                    tree.insert(index-1, '</term>')
                    index += 2
                    insertion_count += 2
            if parent == '<doStatement>':
                tree[index] = element.replace('parameter', 'expression')
                if 'List' in last and not '/' in last and get_text(element):
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
                if ')' in last and insertion_flag and '<parameterList>' not in last2 and 'parameterList' not in last3:
                    print('index: ' + str(index))
                    print('element: ' + element)
                    print('last: ' + last)
                    print('last2: ' + last2)
                    print('last3: ' + last3)
                    print('\n\n\n\n')
                    tree.insert(index-2, '</expression>')
                    tree.insert(index-2, '</term>')
                    index += 2
                    insertion_count += 2
                    insertion_flag = False
                if ',' in element:
                    tree.insert(index, '</expression>')
                    tree.insert(index, '</term>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
                if ',' in last and 'identifier' in element:
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
      
            if parent == '<returnStatement>':
                if ' return ' in last and not ' ; ' in element:
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
                if ';' in last and insertion_flag:
                    tree.insert(index-1, '</expression>')
                    tree.insert(index-1, '</term>')
                    index += 2
                    insertion_count += 2
                    insertion_flag = False

        if opening:
            flag = True
            parent = element
        if closing:
            flag = False

        last3 = last2
        last2 = last
        last = element

        index += 1

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

        #print(element)
        # print('\n' + element + '\n')
        text = get_text(element)
        insertion = triage(text, index, tree)
        index += 1
        # print('INDEX: ' + str(index))
        # print('ELEMENT: ' + str(element))

    group_lets(tree)
    expressions(tree)
#    for item in tree:
#        print(item)

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

