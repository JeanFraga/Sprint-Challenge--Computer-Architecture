#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
import os

cpu = CPU()
print('Type the name of the program you would like to run:')
programs = os.listdir('examples/')
for program in programs:
    program = program.split('.')[0]
    print('>> ', program)
program = input('Program: ')
cpu.load(program)
cpu.run()