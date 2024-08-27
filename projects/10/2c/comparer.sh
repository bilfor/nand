#!/bin/bash

# Define the commands to run
commands=(
    "../../../tools/TextComparer.sh ../Square/SquareT.xml ../Square/SquareTstock.xml"
    "../../../tools/TextComparer.sh ../Square/SquareGameT.xml ../Square/SquareGameTstock.xml"
    "../../../tools/TextComparer.sh ../Square/MainT.xml ../Square/MainTstock.xml"
    "../../../tools/TextComparer.sh ../ArrayTest/MainT.xml ../../../stock/nand2tetris/projects/10/ArrayTest/MainT.xml"
)

# Loop through each command
for cmd in "${commands[@]}"; do
    echo "Running command: $cmd"
    eval $cmd
    echo "Press any key to continue..."
    read -n 1
    echo ""
done

echo "All comparisons done."

