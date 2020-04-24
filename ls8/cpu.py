"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.stack_pointer = -1
        # self.flags = {}
        self.instruction_registry = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100000: self.ADD,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
        }

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            program += '.ls8'
            with open('examples/'+program) as f:
                for line in f:
                    line = line.split('#')
                    line = line[0].strip()
                    if line == '':
                        continue
                    self.ram[address] = int(line, 2)
                    address += 1
            
        except:
            print("invalid program name")
            self.HLT()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            op = self.ram[self.pc]
            instruction = self.instruction_registry[op]
            instruction()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def HLT(self):
        sys.exit(0)

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[address] = value
        self.pc += 3

    def PRN(self):
        address = self.ram_read(self.pc + 1)
        print(self.reg[address])
        self.pc += 2

    def MUL(self):
        address1 = self.ram_read(self.pc + 1)
        address2 = self.ram_read(self.pc + 2)
        result = self.reg[address1] * self.reg[address2]
        self.reg[address1] = result
        self.pc += 3

    def ADD(self):
        address1 = self.ram_read(self.pc + 1)
        address2 = self.ram_read(self.pc + 2)
        result = self.reg[address1] + self.reg[address2]
        self.reg[address1] = result
        self.pc += 3
    
    def PUSH(self, address = None):
        if self.stack_pointer == 0:
            self.stack_pointer -=1
        if address is None:
            address = self.ram_read(self.pc + 1)
            value = self.reg[address]
        else:
            value = address
        self.ram_write(self.stack_pointer, value)
        self.stack_pointer -= 1
        self.pc += 2

    def POP(self, activate=True):
        if activate is True:
            if self.stack_pointer < 0:
                self.stack_pointer += 1
                address = self.ram_read(self.pc + 1)
                value = self.ram_read(self.stack_pointer)
                self.reg[address] = value
                self.pc += 2
        else:
            if self.stack_pointer < 0:
                self.stack_pointer += 1
                value = self.ram_read(self.stack_pointer)
                self.pc = value

    def CALL(self):
        address = self.ram_read(self.pc + 1)
        return_address = self.pc + 2
        self.PUSH(return_address)
        self.pc = self.reg[address]


    def RET(self):
        self.POP(False)

    def CMP(self):
        address1 = self.ram_read(self.pc + 1)
        address2 = self.ram_read(self.pc + 2)
        value1 = self.reg[address1]
        value2 = self.reg[address2]
        self.flags = {
            'E':0,
            'L':0,
            'G':0,
        }
        if value1 == value2:
            self.flags['E'] = 1
        elif value1 < value2:
            self.flags['L'] = 1
        elif value1 > value2:
            self.flags['G'] = 1
        self.pc += 3

    def JMP(self):
        address = self.ram_read(self.pc +1)
        value = self.reg[address]
        self.pc = value

    def JEQ(self):
        if self.flags['E'] == 1:
            address = self.ram_read(self.pc + 1)
            value = self.reg[address]
            self.pc = value
        else:
            self.pc += 2

    def JNE(self):
        if self.flags['E'] == 0:
            address = self.ram_read(self.pc + 1)
            value = self.reg[address]
            self.pc = value
        else:
            self.pc += 2
