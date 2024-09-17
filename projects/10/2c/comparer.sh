#!/bin/bash

# Define the commands to run
commands=(
    "../../../tools/TextComparer.sh ../ExpressionLessSquare/SquareC.xml ../ExpressionLessSquare/Square.xml"
    "../../../tools/TextComparer.sh ../ExpressionLessSquare/SquareGameC.xml ../ExpressionLessSquare/SquareGame.xml"
    "../../../tools/TextComparer.sh ../ExpressionLessSquare/MainC.xml ../ExpressionLessSquare/Main.xml"
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

