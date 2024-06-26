import os
import sys
import parser as p

def generate_bootstrap_asm():
    code = []
    code.extend(['@256', 'D=A', '@SP', 'M=D']) # setting SP to 256
    code.extend(generate_push_asm('', 'constant', 999))
    code.extend(generate_pop_asm('', 'direct', 1))
    code.extend(generate_push_asm('', 'constant', 888))
    code.extend(generate_pop_asm('', 'direct', 2))
    code.extend(generate_push_asm('', 'constant', 777))
    code.extend(generate_pop_asm('', 'direct', 3))
    code.extend(generate_push_asm('', 'constant', 666))
    code.extend(generate_pop_asm('', 'direct', 4))

    return code

def generate_call_asm(f, n, ret_addr):
    code = []

    # push return-address // (Using the label declared below)
    code.extend(generate_push_asm('', 'constant', ret_addr)) # need to make this string
    # push LCL // Save LCL of the calling function
    code.append('@1') # a to desired register
    code.append('D=M') # load value in register into D
    code.append('@SP') # a to stack pointer
    code.append('A=M') # a to top of stack
    code.append('M=D') # D ( reg val) to top of stack
    code.append('@SP') # increment stack pointer step 1
    code.append('M=M+1') # increment stack pointer step 2
    # push ARG // Save ARG of the calling function
    code.append('@2') # a to desired register
    code.append('D=M') # load value in register into D
    code.append('@SP') # a to stack pointer
    code.append('A=M') # a to top of stack
    code.append('M=D') # D ( reg val) to top of stack
    code.append('@SP') # increment stack pointer step 1
    code.append('M=M+1') # increment stack pointer step 2
    # push THIS // Save THIS of the calling function
    code.append('@3') # a to desired register
    code.append('D=M') # load value in register into D
    code.append('@SP') # a to stack pointer
    code.append('A=M') # a to top of stack
    code.append('M=D') # D ( reg val) to top of stack
    code.append('@SP') # increment stack pointer step 1
    code.append('M=M+1') # increment stack pointer step 2
    # push THAT // Save THAT of the calling function
    code.append('@4') # a to desired register
    code.append('D=M') # load value in register into D
    code.append('@SP') # a to stack pointer
    code.append('A=M') # a to top of stack
    code.append('M=D') # D ( reg val) to top of stack
    code.append('@SP') # increment stack pointer step 1
    code.append('M=M+1') # increment stack pointer step 2
    # ARG = SP-n-5 // Reposition ARG (n = number of args.)
    code.append('@SP')
    code.append('D=M')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    for i in range(n):
        code.append('D=D-1')
    code.append('@ARG')
    code.append('M=D')
    # LCL = SP // Reposition LCL
    code.append('@SP')
    code.append('D=M')
    code.append('@LCL')
    code.append('M=D')
    # goto f // Transfer control
    code.extend(generate_goto_asm(f))
    # (return-address) // Declare a label for the return-addres
    code.extend(generate_label_asm(ret_addr))

    return code

def generate_function_asm(name, lcls):
    code = [] 
    code.extend(generate_label_asm(name))
    for i in range(lcls):
        code.extend(generate_push_asm('', 'constant', 0))
        # code.extend(generate_pop_asm('', 'local', i))
    print(code)
    return code

def generate_return_asm():
    code = []
    # we will store FRAME in R15
    # we will store RET in R14
    # we will use R13 for movement

    # FRAME = LCL // FRAME is a temporary variable
    code.append('@LCL') # go to the true address
    code.append('D=M') # load value inside true address into D
    code.append('@SP')
    code.append('A=M')
    code.append('M=D')
    code.append('@SP')
    code.append('M=M+1')
    code.extend(generate_pop_asm('', 'gpr', 2)) # FRAME in R15
    # RET = *(FRAME-5) // Put the return-address in a temp. var.
    code.append('@R15')
    code.append('D=M')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('A=D')
    code.append('D=M')
    code.append('@R14')
    code.append('M=D') # RET in R14
    # *ARG = pop() // Reposition the return value for the caller
    # go to SP-1
    code.append('@SP')
    code.append('A=M')
    code.append('A=A-1')
    # store value of SP-1 in D
    code.append('D=M')
    # go to reg2 (ARG)
    code.append('@ARG')
    # go to value in reg2 (ARG) (somewhere on the stack)
    code.append('A=M')
    # put return value in *ARG
    code.append('M=D')
    # decrement stack pointer
    code.append('@SP')
    code.append('M=M-1')
    #code.extend(generate_pop_asm('', 'argument', 0)) #pops return value to arg
    # SP = ARG+1 // Restore SP of the caller
    code.append('@ARG')
    code.append('D=M')
    code.append('D=D+1')
    code.append('@SP')
    code.append('M=D')
    # THAT = *(FRAME-1) // Restore THAT of the caller
    code.append('@R15')
    code.append('D=M')
    code.append('D=D-1')
    code.append('A=D')
    code.append('D=M')
    code.append('@THAT')
    code.append('M=D')
    # THIS = *(FRAME-2) // Restore THIS of the caller
    code.append('@R15')
    code.append('D=M')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('A=D')
    code.append('D=M')
    code.append('@THIS')
    code.append('M=D')
    # ARG = *(FRAME-3) // Restore ARG of the caller
    code.append('@R15')
    code.append('D=M')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('A=D')
    code.append('D=M')
    code.append('@ARG')
    code.append('M=D')
    # LCL = *(FRAME-4) // Restore LCL of the caller
    code.append('@R15')
    code.append('D=M')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('D=D-1')
    code.append('A=D')
    code.append('D=M')
    code.append('@LCL')
    code.append('M=D')
    # goto RET // Goto return-address (in the caller’s code
    code.append('@R14')
    code.append('A=M')
    code.append('0;JMP')
    
    return code
     
def generate_label_asm(segment):
    code = []
    code.append('(' + segment + ')')
    return code

def generate_ifgoto_asm(label):
    code = []
    code.extend(generate_pop_asm('', 'gpr', 0)) #tos in R13
    code.append('@R13')
    code.append('D=M')
    code.append('@' + label)
    code.append('D;JNE')
    return code

def generate_goto_asm(segment):
    code = []
    code.append('@' + segment)
    code.append('0;JMP')
    return code

def generate_push_asm(sp, segment, index):
    code = []

    if segment == 'constant':
        code.append('@' + str(index)) # if constant, index is the constant
        code.append('D=A') # is the constant

    elif segment == 'temp' or segment == 'gpr' or segment == 'pointer':
        seg_loc = p.switcher(segment) # seg_loc is the base address
        address = seg_loc + index # address is the true address
        code.append('@' + str(address)) # go to the true address
        code.append('D=M') # load value inside true address into D

    elif segment == 'static':
        seg_loc = p.switcher(segment) # seg_loc is the base address
        address = seg_loc + index # address is the true address
        code.append('@' + sp + '.' + str(index)) # go to the address in symboltable
        code.append('D=M') # load value inside true address into D

    else:
        seg_loc = p.switcher(segment) # seg_loc is the register holding base address
        code.append('@' + str(seg_loc)) # go to seg_loc
        code.append('D=M') # load segment base into D
        code.append('@' + str(index)) # load index into A
        code.append('A=D+A') # go to segment base + index
        code.append('D=M') # set D to value inside true address

    # put above D onto the stack
    code.append('@SP')
    code.append('A=M')
    code.append('M=D')

    # increment the stack pointer
    code.append('@SP')
    code.append('M=M+1')

    return code

def generate_pop_asm(sp, segment, index):
  code = []

  seg_loc = p.switcher(segment)
  address = seg_loc + index
  
  if segment == 'temp' or segment == 'constant' or segment == 'gpr' or segment == 'pointer':
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@R' + str(address))
      code.append('M=D') # top of stack is in r{base+index}

  elif segment == 'static':
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@' + sp + '.' + str(index))
      code.append('M=D') # top of stack is in filename.index}

  elif segment == 'direct':
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@' + str(index))
      code.append('M=D')

  else:
      code.append('@SP')
      code.append('M=M-1')
      code.append('A=M')
      code.append('D=M') #top of stack is in D
      code.append('@R13')
      code.append('M=D') # top of stack is in R13
  
      code.append('@' + str(seg_loc))
      code.append('D=M') # seg base is in D
      code.append('@' + str(index)) #index is in A
      code.append('D=D+A') #base + index is in D
      code.append('@R14')
      code.append('M=D') #base + index is in R14
  
      code.append('@R13') #top of stack in A
      code.append('D=M') #top of stack in D
      code.append('@R14') #base + index in M
      code.append('A=M') #base + index in A
      code.append('M=D') #top of stack in base + index
    
  return code

def generate_add_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0))
  code.extend(generate_pop_asm(sp, 'gpr', 1))
 
  code.append('@R14')
  code.append('D=M')
  code.append('@R13')
  code.append('M=D+M')
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code

def generate_sub_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0)) #y to r5
  code.extend(generate_pop_asm(sp, 'gpr', 1)) #x to r6
 
  code.append('@R14')
  code.append('D=M')
  code.append('@R13')
  code.append('M=D-M') # r5 = r6 - r5, x - y
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code

def generate_neg_asm(sp, op1):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0)) #first pop to R13
 
  code.append('@R13')
  code.append('D=0')
  code.append('M=D-M')
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code

def generate_eq_asm(eq_counter):
  ### setup
  code = []
  # code.extend(generate_pop_asm('', 'gpr', 0)) #first pop to R13
  # code.extend(generate_pop_asm('', 'gpr', 1)) #second pop to R14

  code.extend(generate_sub_asm('','','')) # now, difference in on stack
  code.extend(generate_pop_asm('', 'gpr', 0)) # difference in R13

  code.append('@R13')
  code.append('D=M') # difference is in D

  ### check equality and jump

  code.append('@EQUAL_' + str(eq_counter)) # target equal block
  code.append('D;JEQ') # jump to equal block if equal (diff is 0)

  code.append('@NOT_EQUAL_' + str(eq_counter)) # target not equal block
  code.append('0;JMP') # jump to it always if you're here

  ###

  code.append('(EQUAL_' + str(eq_counter) + ')') 
  # what to do if they're equal
  code.extend(generate_true_asm()) # put true on the stack

  code.append('@END_EQ_' + str(eq_counter)) # target end of equality check
  code.append('0;JMP')

  ###

  code.append('(NOT_EQUAL_' + str(eq_counter) + ')')
  # what to do if they're not equal
  code.extend(generate_push_asm('', 'constant', 0))
  
  code.append('(END_EQ_' + str(eq_counter) + ')')

  return code

def generate_true_asm():
  code = []
  code.extend(generate_push_asm('', 'constant', 0))
  code.extend(generate_push_asm('', 'constant', 1))
  code.extend(generate_sub_asm('','',''))

  return code

def generate_lt_asm(lt_counter):
  ### setup
  code = []
  # code.extend(generate_pop_asm('', 'gpr', 0)) #first pop to R13
  # code.extend(generate_pop_asm('', 'gpr', 1)) #second pop to R14

  code.extend(generate_sub_asm('','','')) # now, difference in on stack
  code.extend(generate_pop_asm('', 'gpr', 0)) # difference in R13

  code.append('@R13')
  code.append('D=M') # difference is in D

  ### check equality and jump

  code.append('@LT_' + str(lt_counter)) # target equal block
  code.append('D;JLT') # jump to equal block if equal (diff is 0)

  code.append('@NOT_LT_' + str(lt_counter)) # target not equal block
  code.append('0;JMP') # jump to it always if you're here

  ###

  code.append('(LT_' + str(lt_counter) + ')') 
  # what to do if they're equal
  code.extend(generate_true_asm()) # put true on the stack

  code.append('@END_LT_' + str(lt_counter)) # target end of equality check
  code.append('0;JMP')

  ###

  code.append('(NOT_LT_' + str(lt_counter) + ')')
  # what to do if they're not equal
  code.extend(generate_push_asm('', 'constant', 0))
  
  code.append('(END_LT_' + str(lt_counter) + ')')

  return code

def generate_gt_asm(gt_counter):
  ### setup
  code = []
  # code.extend(generate_pop_asm('', 'gpr', 0)) #first pop to R13
  # code.extend(generate_pop_asm('', 'gpr', 1)) #second pop to R14

  code.extend(generate_sub_asm('','','')) # now, difference in on stack
  code.extend(generate_pop_asm('', 'gpr', 0)) # difference in R13

  code.append('@R13')
  code.append('D=M') # difference is in D

  ### check equality and jump

  code.append('@GT_' + str(gt_counter)) # target equal block
  code.append('D;JGT') # jump to equal block if equal (diff is 0)

  code.append('@NOT_GT_' + str(gt_counter)) # target not equal block
  code.append('0;JMP') # jump to it always if you're here

  ###

  code.append('(GT_' + str(gt_counter) + ')') 
  # what to do if they're equal
  code.extend(generate_true_asm()) # put true on the stack

  code.append('@END_GT_' + str(gt_counter)) # target end of equality check
  code.append('0;JMP')

  ###

  code.append('(NOT_GT_' + str(gt_counter) + ')')
  # what to do if they're not equal
  code.extend(generate_push_asm('', 'constant', 0))
  
  code.append('(END_GT_' + str(gt_counter) + ')')

  return code

def generate_and_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0)) #first pop to R13
  code.extend(generate_pop_asm(sp, 'gpr', 1)) #second pop to R14

  code.append('@R14')
  code.append('D=M')
  code.append('@R13')
  code.append('M=M&D')
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code

def generate_or_asm(sp, op1, op2):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0)) #first pop to R13
  code.extend(generate_pop_asm(sp, 'gpr', 1)) #second pop to R14

  code.append('@R14')
  code.append('D=M')
  code.append('@R13')
  code.append('M=M|D')
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code

def generate_not_asm(sp, op1):
  code = []
  code.extend(generate_pop_asm(sp, 'gpr', 0)) #first pop to R13

  code.append('@R13')
  code.append('M=!M')
  code.extend(generate_push_asm(sp, 'gpr', 0))

  return code
