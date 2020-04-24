#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program = input()
# while program != 'q':
cpu.load(program)
cpu.run()
# program = input()