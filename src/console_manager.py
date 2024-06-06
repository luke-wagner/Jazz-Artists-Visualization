import sys
import os
from colorama import Fore, Back, Style

def console_out_on():
    sys.stdout = sys.__stdout__

def console_out_off():
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')

def write_error(text):
    old_out = sys.stdout
    sys.stdout = sys.__stdout__
    console_out_on()
    print(Fore.RED + f"\nERROR: {text}\n")
    print(Style.RESET_ALL, end='')
    sys.stdout = old_out

def write_warning(text):
    old_out = sys.stdout
    sys.stdout = sys.__stdout__
    console_out_on()
    print(Fore.RED + f"\n{text}\n")
    print(Style.RESET_ALL, end='')
    sys.stdout = old_out