@256
D=A
@SP
M=D
@999
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@1
M=D
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@2
M=D
@777
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@3
M=D
@666
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@4
M=D
// call Sys.init 0
@Sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init$ret.1)
// ~Sys.vm
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
@Class1.set$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$ret.2)
// pop temp 0 
@SP
M=M-1
A=M
D=M
@R5
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
@Class2.set$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$ret.3)
// pop temp 0 
@SP
M=M-1
A=M
D=M
@R5
M=D
// call Class1.get 0
@Class1.get$ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$ret.4)
// call Class2.get 0
@Class2.get$ret.5
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$ret.5)
// label END
(END)
// goto END
@END
0;JMP
// ~Class2.vm
// function Class2.set 0
(Class2.set)
// push argument 0
@2
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
A=M
D=M
@Class2.vm.0
M=D
// push argument 1
@2
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@Class2.vm.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R15
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
D=D+1
@SP
M=D
@R15
D=M
D=D-1
A=D
D=M
@THAT
M=D
@R15
D=M
D=D-1
D=D-1
A=D
D=M
@THIS
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@R13
M=D-M
@13
D=M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R15
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
D=D+1
@SP
M=D
@R15
D=M
D=D-1
A=D
D=M
@THAT
M=D
@R15
D=M
D=D-1
D=D-1
A=D
D=M
@THIS
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
// ~Class1.vm
// function Class1.set 0
(Class1.set)
// push argument 0
@2
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
A=M
D=M
@Class1.vm.0
M=D
// push argument 1
@2
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@Class1.vm.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R15
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
D=D+1
@SP
M=D
@R15
D=M
D=D-1
A=D
D=M
@THAT
M=D
@R15
D=M
D=D-1
D=D-1
A=D
D=M
@THIS
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@R13
M=D-M
@13
D=M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R15
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
D=D+1
@SP
M=D
@R15
D=M
D=D-1
A=D
D=M
@THAT
M=D
@R15
D=M
D=D-1
D=D-1
A=D
D=M
@THIS
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@R15
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
