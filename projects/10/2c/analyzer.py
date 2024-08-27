import os
import sys
import tokenizer as t
import engine as e

directory = sys.argv[1]

# TOKENIZER
t.main(directory)

# COMPILER
e.constructor(directory)

