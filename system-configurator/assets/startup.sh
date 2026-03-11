#!/bin/bash

clear

# Define color codes
orange_color="\033[1;33m"  # Orange
purple_color="\033[1;35m"  # Purple
default="\033[1;0m"        # Reset to default

# Function to print colored text
print_colored_text() {
    printf "$1$2$default\n"
}

# Use blue for the ASCII art
print_colored_text "$purple_color" " ____  ___     ___ _____ ___         _   _____ ___ "
print_colored_text "$purple_color" "|    \|   |___|_  |_   _|   |_ _ ___| |_|     |_  |"
print_colored_text "$purple_color" "|  |  | | |   | | | | | | | | | |  _|   | | | |_  |"
print_colored_text "$purple_color" "|____/|___|_|_| |_| |_| |___|___|___|_|_|_|_|_|___|"
print_colored_text "$purple_color" "       _____         _      _____     _ _   _ "
print_colored_text "$purple_color" "      |  _  |___ ___| |_   | __  |_ _|_| |_| |"
print_colored_text "$purple_color" "      |     |  _|  _|   |  | __ -| | | | | . |"
print_colored_text "$purple_color" "      |__|__|_| |___|_|_|  |_____|___|_|_|___|"

# Use orange for version and social links
print_colored_text "$orange_color" "Version: 1.01"
