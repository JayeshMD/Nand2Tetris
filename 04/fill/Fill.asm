// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
@KBD
D = M

@BLACK
D;JNE

@WHITE
D;JEQ

(BLACK)
// initializing counter to screen memory map size 512x256 pixel => 16x32X256 => 16x8192
@8192
D = A
@i
M = D  

(L1)
    @SCREEN
    D = A

    @i
    D = D + M

    A = D
    M = -1

    @1
    D =A

    @i
    M = M-D

    @i
    D = M

    @L1
    D;JGE

@START
0;JMP
(WHITE)
// initializing counter to screen memory map size 512x256 pixel => 16x32X256 => 16x8192
@8192
D = A
@i
M = D  

(L2)
    @SCREEN
    D = A

    @i
    D = D + M

    A = D
    M = 0

    @1
    D =A

    @i
    M = M-D


    @i
    D = M

    @L2
    D;JGE


@START
0;JMP
