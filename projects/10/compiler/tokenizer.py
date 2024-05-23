import re
####
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
