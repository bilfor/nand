from lxml import etree
import re

def find_next(tree, symbol, start):
    index = start
    for item in tree[start:]:
        if get_text(item) == symbol:
            return index + 1
        else:
            index += 1

def sub_find_next(tree, symbol, start):
    index = start
    for item in tree[start:]:
        if get_text(item) == symbol:
            new_start = start + index + 1
            ans = find_next(tree, symbol, new_start)
            if ans is not None:
                return ans
            else:
                return index
        else:
            index += 1

def get_parent(tree, index):
    i = 0
    stack = []
    for element in tree:
        if element.count('<') == 1 and element.count('/') == 1:
            popped = stack.pop()
        if element.count('<') == 1 and element.count('/') == 0:
            stack.append(element)
        if index == i:
            if stack:
                return stack.pop()
            else:
                return 'class'

        i += 1

def get_parent_list(tree, index):
    i = 0
    stack = []
    for element in tree:
        if element.count('<') == 1 and element.count('/') == 1:
            try: 
                popped = stack.pop()
            except IndexError:
                return 'class'
        if element.count('<') == 1 and element.count('/') == 0:
            stack.append(element)
        if index == i:
            if stack:
                return stack
            else:
                return 'class'

        i += 1

def find_match(tags, start_index):
    opening_tag = tags[start_index]
    nested_level = 0

    for i in range(start_index, len(tags)):
        tag = tags[i]
        if "<symbol> { </symbol>" in tag:
            nested_level += 1
        elif "<symbol> } </symbol>" in tag:
            nested_level -= 1
            if nested_level == 0:
                return i  # Found the matching closing tag

    # If no matching closing tag is found
    return None

def substring_in_list(substring, string_list):
    for string in string_list:
        if substring in string:
            return True
    return False

def triage(text, index, tree):
    insertion = 'none' 

    parent = get_parent(tree, index)
    parent_list = get_parent_list(tree, index)

    if (text == ' static ' or text == ' field '):
        tree.insert(index, '<classVarDec>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</classVarDec>')
        insertion = 'before'

    elif (text == ' constructor ' or text == ' function ' or text == ' method ' ):
        opening = find_next(tree, ' { ', index) - 1
        closing = find_match(tree, opening)
        tree.insert(index, '<subroutineDec>')
        tree.insert(closing+2, '</subroutineDec>')
        insertion = 'before'

    elif (text == ' ( ' and 'ifStatement' not in parent and 'while' not in parent):
        tree.insert(index + 1, '<parameterList>')
        final_element_index = find_next(tree, ' ) ', index)
        tree.insert(final_element_index - 1, '</parameterList>')
        insertion = 'after'

    elif (parent == '<subroutineDec>' and text == ' { '):
        closing = find_match(tree, index)
        tree.insert(index, '<subroutineBody>')
        tree.insert(closing+2, '</subroutineBody>')
        insertion = 'before'

    elif (text == ' let '):
        tree.insert(index, '<letStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</letStatement>')
        insertion = 'before'

    elif (text == ' do '):
        tree.insert(index, '<doStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</doStatement>')
        insertion = 'before'

    elif (text == ' return '):
        tree.insert(index, '<returnStatement>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</returnStatement>')
        insertion = 'before'

    elif (text == ' if '):
        opening = find_next(tree, ' { ', index) - 1
        closing = find_match(tree, opening)
        tree.insert(index, '<ifStatement>')
        if 'else' in tree[closing + 2]:
            opening = find_next(tree, ' { ', closing) - 1
            closing = find_match(tree, opening)
            tree.insert(closing + 1, '</ifStatement>')
        else:
            tree.insert(closing + 2, '</ifStatement>')
        insertion = 'before'

    elif (text == ' while '):
        opening = find_next(tree, ' { ', index) - 1
        closing = find_match(tree, opening)
        tree.insert(index, '<whileStatement>')
        tree.insert(closing+2, '</whileStatement>')
        insertion = 'before'

    elif (text == ' var '):
        tree.insert(index, '<varDec>')
        final_element_index = find_next(tree, ' ; ', index)
        tree.insert(final_element_index, '</varDec>')
        insertion = 'before'

    return insertion

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
    op_list = [' + ', ' - ', ' * ', ' / ', ' & ', ' | ', ' < ', ' > ', ' = ']
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

        parent_list = get_parent_list(tree, index)
        if '<term>' in parent_list:
            if get_text(element) in op_list: 
                tree.insert(index, '</term>')
                insertion_count += 1
                index += 1

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
                if '{' in last and '}' in element:
                    tree.insert(index, '</statements>')
                    tree.insert(index, '<statements>')
                    insertion_count += 2
                    index += 2
                    insertion_flag = True
                #if '}' in element:
                    #tree.insert(index, '</statements>')
                    #insertion_count += 1
                    #index += 1
                    #insertion_flag = True
            if parent == '<whileStatement>':
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
                if '[' in last:
                    tree.insert(index, '<term>')
                    tree.insert(index, '<expression>')
                    insertion_count += 2
                    index += 2
                if ']' in element:
                    tree.insert(index, '</expression>')
                    tree.insert(index, '</term>')
                    insertion_count += 2
                    index += 2
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
                    tree.insert(index-2, '</expression>5')
                    tree.insert(index-2, '</term>')
                    index += 2
                    insertion_count += 2
                    insertion_flag = False
                if ',' in element:
                    tree.insert(index, '</expression>5')
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
                if ';' in element and insertion_flag and not 'return' in last:
                    tree.insert(index, '</expression>6')
                    tree.insert(index, '</term>')
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

def rename_lists(tree):
    index = 0

    for element in tree:
        if 'parameterList' in element:
            parent_list = get_parent_list(tree, index)
            #if '<expression>' in parent_list and '<term>' in parent_list:
                #tree[index] = element.replace('parameterList', 'expression')
            if '<expression>' in parent_list:
                tree[index] = element.replace('parameter', 'expression')
        index += 1

def replace_first_and_last(lst, x, y):
    if len(lst) >= 1:
        lst[0] = x
    if len(lst) >= 2:
        lst[-1] = y
    return lst

def get_expression_elements(tree):
    new_tree = []
    for element in tree:
        if 'term' not in element:
            new_tree.append(element)

    tree = new_tree

def mark_on_condition(tree):
    for i in range(len(tree)):
        parent_list = get_parent_list(tree, i)
        if '<expression>' in parent_list:
            tree[i] = tree[i].upper()

def compile_expressions(statements):

    op_list = [' + ', ' - ', ' * ', ' / ', ' & ', ' | ', ' < ', ' > ', ' = ']

    processed_statements = []
    inside_expression = False
    term_open = False
    last = ''

    for statement in statements:
        if "<expression>" in statement:
            processed_statements.append(statement)
            processed_statements.append("<term>")
            inside_expression = True
            term_open = True
        elif "</expression>" in statement:
            if term_open:
                processed_statements.append("</term>")
                term_open = False
            if ']' in last:
                processed_statements.append('</term>')
            processed_statements.append(statement)
            inside_expression = False
        elif any(op in statement for op in op_list):
            if term_open:
                processed_statements.append("</term>")
                term_open = False
            processed_statements.append(statement)
        elif "(" in statement and inside_expression and not term_open:
            processed_statements.append("<term>")
            processed_statements.append(statement)
        #    if term_open:
        #        processed_statements.append("</term>")
        #        term_open = False
        #    processed_statements.append("<term>")
        #    term_open = True
        else:
            processed_statements.append(statement)

        last = statement

    return processed_statements

def search_tuples(data, value):
    for first, second in data:
        if first == value:
            #print('search_tuples: 0\n')
            return 0  # Found in the first position
        elif second == value:
            #print('search_tuples: 1\n')
            return 1  # Found in the second position
    #print('search_tuples: -1\n')
    return -1  # Value not found

def check_consec(lst, a, b):
    print('CHECKING')
    # Ensure the indices are within the bounds of the list
    if a < 0 or b >= len(lst) or a > b:
        return False
    
    # Iterate through the subset of the list
    print('\nNEW')
    for i in range(a, b):
        print('i: ' + str(i) + ' ' + lst[i])
        #if '(' in lst[i] and '-' in lst[i + 1]:
            #return True
    print('b: ' + str(b) + ' ' + lst[b])
    
    return False

def find_unary_ops(input_list):
    opens = []
    ends = []
    output_list = []
    results = []
    expression_list_count = 0
    in_exp_list = False

    for index, line in enumerate(input_list):
        if '<expressionList>' in line:
            opens.append(index)
        if '</expressionList>' in line:
            ends.append(index)

    index_tuples = list(zip(opens, ends))
    #print(index_tuples)

    for a, b in index_tuples:
        result = check_consec(input_list, a, b)
        results.append(result)


    for index, line in enumerate(input_list):
        #print(results)
        #print(expression_list_count)
        #print(results[expression_list_count])
        key = search_tuples(index_tuples, index)

        if key == 0:
            in_exp_list = True
            
            if results[expression_list_count]:
                output_list.append('<expression>')
                output_list.append('<term>')
            else:
                output_list.append(line)

        elif in_exp_list and results[expression_list_count]:
            if 'identifier' in line and '-' in input_list[index-1]:
                output_list.append('<term>')
                output_list.append(line)
                output_list.append('</term>')
            else:
                output_list.append(line)

        elif key == 1:
            if results[expression_list_count]:
                output_list.append('</term>')
                output_list.append('</expression>')
            else:
                output_list.append(line)

            if expression_list_count < len(results) - 1:
                expression_list_count += 1
            else:
                results[expression_list_count] = False

            in_unary_exp = False

        else:
            output_list.append(line)

    return output_list

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

        text = get_text(element)
        insertion = triage(text, index, tree)
        index += 1

    expressions(tree)
    group_lets(tree)
    rename_lists(tree)
    #mark_on_condition(tree)
    #get_expression_elements(tree)
