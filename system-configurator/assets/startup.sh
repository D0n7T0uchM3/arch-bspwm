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
print_colored_text "$purple_color" "  _______   _____  __  __   ____  _   _ ___ _     ____  "
print_colored_text "$purple_color" " |_   _\ \ / / _ \|  \/  | | __ )| | | |_ _| |   |  _ \ "
print_colored_text "$purple_color" "   | |  \ V / | | | |\/| | |  _ \| | | || || |   | | | |"
print_colored_text "$purple_color" "   | |   | || |_| | |  | | | |_) | |_| || || |___| |_| |"
print_colored_text "$purple_color" "   |_|   |_| \___/|_|  |_| |____/ \___/|___|_____|____/ "

# Use orange for version and social links
print_colored_text "$orange_color" "Version: 1.0"
