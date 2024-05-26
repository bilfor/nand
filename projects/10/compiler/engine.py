from lxml import etree

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

# def compile_class_var_dec(cur_loc):
# def compile_subroutine():
# def comile_var_dec():

def triage(tree):
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
  
def compile(tree):
    root = tree.getroot()   
    rename_root_element(tree, 'class') 

    #for element in root.iter():

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

