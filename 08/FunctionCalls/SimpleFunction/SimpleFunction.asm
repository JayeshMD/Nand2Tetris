//function SimpleFunction.test 2
(SimpleFunction.test)
@SP
D=M
@LCL
M=D
@0
D=A
@SP
A=M
M=D
A=A+1
M=D
A=A+1
D=A
@SP
M=D
//push local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//push local 1
@1
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//not
@SP
A=M-1
M=!M
//push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//return
@LCL
D=M
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@LCL
D=M
@R13
AM=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
