# Symbol tables for class and subroutine scopes
class_symbol_table = {}        # Stores class-level identifiers: "STATIC" and "FIELD"
subroutine_symbol_table = {}   # Stores subroutine-level identifiers: "ARG" and "VAR"

# Counters for tracking the index of each kind of variable
class_counts = {"STATIC": 0, "FIELD": 0}  # Counters for class-level variables
subroutine_counts = {"ARG": 0, "VAR": 0}  # Counters for subroutine-level variables

def start_subroutine():
    """Clear subroutine-level symbol table and reset ARG and VAR counters."""
    global subroutine_symbol_table, subroutine_counts
    subroutine_symbol_table = {}   # Clear subroutine-level table
    subroutine_counts["ARG"] = 0   # Reset counters for subroutine scope
    subroutine_counts["VAR"] = 0

def define(name, tipe, kind):
    """
    Adds a new identifier with the given name, tipe, and kind.
    - Class-level kinds: "STATIC", "FIELD"
    - Subroutine-level kinds: "ARG", "VAR"
    """
    if kind in ["STATIC", "FIELD"]:
        index = class_counts[kind]
        class_symbol_table[name] = {"tipe": tipe, "kind": kind, "index": index}
        class_counts[kind] += 1
    else:
        index = subroutine_counts[kind]
        subroutine_symbol_table[name] = {"tipe": tipe, "kind": kind, "index": index}
        subroutine_counts[kind] += 1

def var_count(kind):
    """
    Returns the number of variables of the given kind.
    Class-level kinds: "STATIC" and "FIELD"
    Subroutine-level kinds: "ARG" and "VAR"
    """
    if kind in ["STATIC", "FIELD"]:
        return class_counts.get(kind, 0)
    else:
        return subroutine_counts.get(kind, 0)

def kind_of(name):
    """Returns the kind of the named identifier, or None if it does not exist."""
    if name in subroutine_symbol_table:
        return subroutine_symbol_table[name]["kind"]
    elif name in class_symbol_table:
        return class_symbol_table[name]["kind"]
    return None

def tipe_of(name):
    """Returns the tipe of the named identifier, or None if it does not exist."""
    if name in subroutine_symbol_table:
        return subroutine_symbol_table[name]["tipe"]
    elif name in class_symbol_table:
        return class_symbol_table[name]["tipe"]
    return None

def index_of(name):
    """Returns the index of the named identifier, or None if it does not exist."""
    if name in subroutine_symbol_table:
        return subroutine_symbol_table[name]["index"]
    elif name in class_symbol_table:
        return class_symbol_table[name]["index"]
    return None

