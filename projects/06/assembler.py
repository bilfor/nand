import os
import time
import sys

def process_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        print(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    process_file(file_path)

Start_Time = time.time()

def To_Int(s):
    try:
        return (True, int(s))
    except ValueError:
        return (False, False)

def C_Inst_A(Line, Print_Line):
    return(Print_Line)

def C_Inst_C(Line, Print_Line):
    return(Print_Line)

def C_Inst_D(Line, Print_Line):
    return(Print_Line)

def C_Inst_J(Line, Print_Line):
    Check = line[-3:]

    if (Check == "JGT"):
        Print_Line += "001"
    elif(Check == "JEQ"):
        Print_Line += "010"
    elif(Check == "JGE"):
        Print_Line += "011"
    elif(Check == "JLT"):
        Print_Line += "100"
    elif(Check == "JNE"):
        Print_Line += "101"
    elif(Check == "JLE"):
        Print_Line += "110"
    elif(Check == "JMP"):
        Print_Line += "111"
    else:
        Print_Line += "000"
    return(Print_Line)



with open(File_Read, "r") as f:
    program = f
    with open(File_Write, "w") as w:
        
        for line in program:
            if (line.strip() and):    # If line is not empty
                Symbol_Check = To_Int(line[1:])
                if (line[0] == "@" and Symbol_Check[0]):    # Check if A instruction that is not a symbol
                    Bin_Int = bin(Symbol_Check[1])[2:]
                    Bin_Int_Pad =  Bin_Int.zfill(16)
                    print(Bin_Int_Pad)
                elif (line[0] == "@" and not Symbol_Check[0]):  # Check if A instruction that is a symbol
                    print("Symbol Instruction")
                else: # If item is not an A instruction then it must be a C instruction
                    C_Inst = "111"
                    C_Inst = C_Inst_A(line, C_Inst)
                    C_Inst = C_Inst_C(line, C_Inst)
                    C_Inst = C_Inst_D(line, C_Inst)
                    C_Inst = C_Inst_J(line, C_Inst)
                    print(C_Inst)





print("Done. Run Time %s seconds" % (time.time() - Start_Time))

