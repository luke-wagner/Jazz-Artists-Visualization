# File: console_manager.py
# Author: Luke Wagner
# Description:
# Custom module providing supplemental functions for console output
# -------------------------------------------------------------------------------------------------

import sys
import os
from colorama import Fore, Back, Style

# Turn console output on, setting stdout to default
def console_out_on():
    sys.stdout = sys.__stdout__

# Turn console output off, setting stdout to devnull
def console_out_off():
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')

# Write an error message to the console
# @param: text (string) - the message text
def write_error(text):
    old_out = sys.stdout
    sys.stdout = sys.__stdout__
    console_out_on()
    print(Fore.RED + f"\nERROR: {text}\n")
    print(Style.RESET_ALL, end='')
    sys.stdout = old_out

# Write a warning message to the console
# @param: text (string) - the message text
def write_warning(text):
    old_out = sys.stdout
    sys.stdout = sys.__stdout__
    console_out_on()
    print(Fore.YELLOW + f"\nWARNING: {text}\n")
    print(Style.RESET_ALL, end='')
    sys.stdout = old_out