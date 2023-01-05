//push constant 3030
@3030
D=A
@SP
AM=M+1
A=A-1
M=D
//pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
//push constant 3040
@3040
D=A
@SP
AM=M+1
A=A-1
M=D
//pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
//push constant 32
@32
D=A
@SP
AM=M+1
A=A-1
M=D
//pop this 2
@2
D=A
@THIS
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@13
A=M
M=D
//push constant 46
@46
D=A
@SP
AM=M+1
A=A-1
M=D
//pop that 6
@6
D=A
@THAT
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@13
A=M
M=D
//push pointer 0
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
//push pointer 1
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
//add
//add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//push this 2
@2
D=A
@THIS
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//sub
//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//push that 6
@6
D=A
@THAT
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
//add
//add
@SP
AM=M-1
D=M
A=A-1
M=M+D
