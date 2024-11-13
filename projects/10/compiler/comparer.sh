#!/bin/bash

# Define the commands to run
commands=(
    "../../../tools/TextComparer.sh ../Square/SquareC.xml ../Square/Square.xml"
    "../../../tools/TextComparer.sh ../Square/SquareGameC.xml ../Square/SquareGame.xml"
    "../../../tools/TextComparer.sh ../Square/MainC.xml ../Square/Main.xml"
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

