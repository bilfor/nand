// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

@KBD
D=A

@screenEnd      //screenEnd is the final location in the screen memory block
M=D-1

(WHITE)
    @SCREEN
    D=A
    @loc        //move A to loc
    M=D         //first location is always start of screen block

(WRITEWHITE) 
    @loc        //move A to loc
    A=M         //move A to value of loc
    M=0         //this location was checked so write it

    A=A+1       //increment A to next location
    D=A         //hold A

    @loc        //move A to loc
    M=D         //store memory location to test in loc
    
    @screenEnd        //move A to screenEnd
    D=M-D             //screenEnd - testlocation
    
    @WRITEWHITE //move A to WRITEWHITE
    D;JGE       //if screenEnd - test location > 0, goto WRITEWHITE

(READ)

    //loading KBD value
    @KBD    //store KBD address in A
    D=M     //store value at KBD in D

    //check if button is being pressed
    @BLACK  //store BLACK target in A
    D;JNE   //if D != 0, jump to BLACK
    @WHITE
    D;JEQ   //if D = 0, jump to WHITE

(BLACK)
    @SCREEN
    D=A
    @loc        //move A to loc
    M=D         //first location is always start of screen block

(WRITEBLACK) 
    @loc        //move A to loc
    A=M         //move A to value of loc
    M=-1         //this location was checked so write it

    A=A+1       //increment A to next location
    D=A         //hold A

    @loc        //move A to loc
    M=D         //store memory location to test in loc
    
    @screenEnd        //move A to screenEnd
    D=M-D       //test location - screenEnd
    
    @WRITEBLACK //move A to WRITEBLACK
    D;JGE       //if screenEnd - test location > 0, goto WRITEBLACK

@READ
0;JMP //infinite loop
