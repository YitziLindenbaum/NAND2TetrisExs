@256
D=A
@SP
M=D
@return-Sys.init
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(return-Sys.init)
(Class1.set)
@0
D=A
@R2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@SP
M=M-1
@Class1.0
M=D
@1
D=A
@R2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@SP
M=M-1
@Class1.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@5
D=A
@frame
A=M-D
D=M
@ret
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@frame
A=M-D
D=M
@THAT
M=D
@2
D=A
@frame
A=M-D
D=M
@THIS
M=D
@3
D=A
@frame
A=M-D
D=M
@ARG
M=D
@4
D=A
@frame
A=M-D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Class1.get)
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@frame
M=D
@5
D=A
@frame
A=M-D
D=M
@ret
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@frame
A=M-D
D=M
@THAT
M=D
@2
D=A
@frame
A=M-D
D=M
@THIS
M=D
@3
D=A
@frame
A=M-D
D=M
@ARG
M=D
@4
D=A
@frame
A=M-D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Sys.init)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@return-Class1.set
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@2
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(return-Class1.set)
@SP
A=M-1
D=M
@SP
M=M-1
@R5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@return-Class2.set
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@2
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(return-Class2.set)
@SP
A=M-1
D=M
@SP
M=M-1
@R5
M=D
@return-Class1.get
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(return-Class1.get)
@return-Class2.get
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(return-Class2.get)
(WHILE)
@WHILE
0;JMP
(Class2.set)
@0
D=A
@R2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@SP
M=M-1
@Class2.0
M=D
@1
D=A
@R2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@SP
M=M-1
@Class2.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@5
D=A
@frame
A=M-D
D=M
@ret
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@frame
A=M-D
D=M
@THAT
M=D
@2
D=A
@frame
A=M-D
D=M
@THIS
M=D
@3
D=A
@frame
A=M-D
D=M
@ARG
M=D
@4
D=A
@frame
A=M-D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Class2.get)
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@frame
M=D
@5
D=A
@frame
A=M-D
D=M
@ret
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@frame
A=M-D
D=M
@THAT
M=D
@2
D=A
@frame
A=M-D
D=M
@THIS
M=D
@3
D=A
@frame
A=M-D
D=M
@ARG
M=D
@4
D=A
@frame
A=M-D
D=M
@LCL
M=D
@ret
A=M
0;JMP
