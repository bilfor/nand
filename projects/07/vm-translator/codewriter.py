import os
import sys
import parser as p

def generate_push_asm(sp, segment, index):
  code = []

  if segment == 'constant':
      code.append('@' + str(index)) #if constant, index is the constant
      code.append('D=A')
  else:
      seg_loc = p.switcher(segment)
      address = seg_loc + index
      code.append('@' + str(address))
      code.append('D=M')
  code.append('@SP')
  code.append('A=M')
  code.append('M=D')
  code.append('@SP')
  code.append('M=M+1')

  sp += 1

  return code

def generate_pop_asm(sp, segment, index):
  code = []

  seg_loc = p.switcher(segment)
  address = seg_loc + index
  
  if segment == 'temp' or segment == 'constant':
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@R' + str(address))
      code.append('M=D') # top of stack is in r{base+index}

  else:

      address = seg_loc + index
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@R7')
      code.append('M=D') # top of stack is in R7
  
      code.append('@' + str(seg_loc))
      code.append('D=M') # seg base is in D
      code.append('@' + str(index)) #index is in A
      code.append('D=D+A') #base + index is in D
      code.append('@R8')
      code.append('M=D') #base + index is in R8
  
      code.append('@R7') #top of stack in A
      code.append('D=M') #top of stack in D
      code.append('@R8') #base + index in M
      code.append('A=M') #base + index in A
      code.append('M=D') #top of stack in base + index
    
  sp -= 1

  return code

def generate_add_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0))
  code.extend(generate_pop_asm(sp, 'temp', 1))
 
  code.append('@R6')
  code.append('D=M')
  code.append('@R5')
  code.append('M=D+M')
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code

def generate_sub_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #y to r5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #x to r6
 
  code.append('@R6')
  code.append('D=M')
  code.append('@R5')
  code.append('M=D-M') # r5 = r6 - r5, x - y
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code

def generate_neg_asm(sp, op1):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
 
  code.append('@R5')
  code.append('D=0')
  code.append('M=D-M')
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code

def generate_eq_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #second pop to R6

  code.extend(generate_push_asm(sp, 'constant', 0))
  if op2 == op1:
      code.extend(generate_push_asm(sp, 'constant', 1))
      code.extend(generate_sub_asm(sp, op1, op2))

  return code

def generate_lt_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #second pop to R6

  code.extend(generate_push_asm(sp, 'constant', 0))
  if op2 < op1:
      code.extend(generate_push_asm(sp, 'constant', 1))
      code.extend(generate_sub_asm(sp, op1, op2))

  return code

def generate_gt_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #second pop to R6

  code.extend(generate_push_asm(sp, 'constant', 0))
  if op2 > op1:
      code.extend(generate_push_asm(sp, 'constant', 1))
      code.extend(generate_sub_asm(sp, op1, op2))

  return code

def generate_and_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #second pop to R6

  code.append('@R6')
  code.append('D=M')
  code.append('@R5')
  code.append('M=M&D')
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code

def generate_or_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5
  code.extend(generate_pop_asm(sp, 'temp', 1)) #second pop to R6

  code.append('@R6')
  code.append('D=M')
  code.append('@R5')
  code.append('M=M|D')
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code

def generate_not_asm(sp, op1):
  code = []
  code.extend(generate_pop_asm(sp, 'temp', 0)) #first pop to R5

  code.append('@R5')
  code.append('M=!M')
  code.extend(generate_push_asm(sp, 'temp', 0))

  return code
