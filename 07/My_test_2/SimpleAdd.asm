//push constant 7
@7
D=A
@SP
A=M
M=D
D=A+1
@SP
M=D
//push constant 8
@8
D=A
@SP
A=M
M=D
D=A+1
@SP
M=D
//add
@SP
A=M-1
D=M
A=A-1
M=D+M
D=A
@SP
M=D
