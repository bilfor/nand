// computes the product of R0*R1 and stores the result in R2

@R2   //point at product
M=0   //initalize product as 0

@R0   //point at first number
D=M   //load first number into D

@R3   //holds the remaining iterations
M=D   //remaining iterations starts as first number

(LOOP)
    @END    //point at end
    D;JEQ   //if there are no remaining iterations, end

    @R1     //point at second number
    D=M     //load second number into D

    @R2     //point at product
    M=D+M   //add product and second number, store sum in product

    @R3     //point at counter
    M=M-1   //decrement the counter
    D=M     //store counter in D

    @LOOP
    0;JMP

(END)
    @END
    0;JMP 
