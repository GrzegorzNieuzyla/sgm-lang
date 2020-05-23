from typing import List
from sgm_lang.Opcode import Opcode, Operation, ParameterType, Parameter


class InterpreterException(Exception):
    pass


class BytecodeInterpreter:
    def __init__(self, operations: List[Operation]):
        self.operations = operations
        self.ip = 0
        self.sp = 0
        self.stack = []
        self.variables = {}

    def run(self):
        while self.ip < len(self.operations):
            try:
                self.processInstruction()
            except InterpreterException:
                raise
            except Exception as e:
                raise InterpreterException(e)

    def processInstruction(self):
        current_op = self.operations[self.ip]
        parameters = current_op.params
        if current_op.opcode == Opcode.ADD:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b + a)
        elif current_op.opcode == Opcode.SUB:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b - a)
        elif current_op.opcode == Opcode.MUL:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b * a)
        elif current_op.opcode == Opcode.DIV:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b / a)
        elif current_op.opcode == Opcode.MOD:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b % a)
        elif current_op.opcode == Opcode.LOAD:
            self._validateParametersLength(current_op, parameters, 1)
            if parameters[0].value not in self.variables:
                raise InterpreterException(
                    f"Variable {parameters[0].value} is not defined")
            self.stack.append(self.variables[parameters[0].value])
        elif current_op.opcode == Opcode.STORE:
            self._validateParametersLength(current_op, parameters, 1)
            self.variables[parameters[0].value] = self.stack.pop()
        elif current_op.opcode == Opcode.PRINT:
            self._validateParametersLength(current_op, parameters, 0)
            print(self.stack.pop())
        elif current_op.opcode == Opcode.PRINTC:
            self._validateParametersLength(current_op, parameters, 1)
            print(parameters[0].value)
        elif current_op.opcode == Opcode.PUSH:
            self._validateParametersLength(current_op, parameters, 1)
            self.stack.append(parameters[0].value)
        elif current_op.opcode == Opcode.POP:
            self._validateParametersLength(current_op, parameters, 1)
            self.variables[parameters[0].value] = self.stack.pop()
        elif current_op.opcode == Opcode.JMP:
            self._validateParametersLength(current_op, parameters, 1)
            if parameters[0].paramType == ParameterType.IMMEDIATE:
                self.ip = parameters[0].value
            elif parameters[0].paramType == ParameterType.RELATIVE:
                self.ip += parameters[0].value
        elif current_op.opcode == Opcode.JMP_IF:
            self._validateParametersLength(current_op, parameters, 1)
            if self.stack.pop():
                if parameters[0].paramType == ParameterType.IMMEDIATE:
                    self.ip = parameters[0].value
                elif parameters[0].paramType == ParameterType.RELATIVE:
                    self.ip += parameters[0].value
        elif current_op.opcode == Opcode.JMP_NOT_IF:
            self._validateParametersLength(current_op, parameters, 1)
            if not self.stack.pop():
                if parameters[0].paramType == ParameterType.IMMEDIATE:
                    self.ip = parameters[0].value
                elif parameters[0].paramType == ParameterType.RELATIVE:
                    self.ip += parameters[0].value
        elif current_op.opcode == Opcode.EQ:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b == a)
        elif current_op.opcode == Opcode.NEQ:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b != a)
        elif current_op.opcode == Opcode.GE:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b >= a)
        elif current_op.opcode == Opcode.GRT:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b > a)
        elif current_op.opcode == Opcode.LE:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b <= a)
        elif current_op.opcode == Opcode.LESS:
            self._validateParametersLength(current_op, parameters, 0)
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b < a)
        else:
            raise InterpreterException("Invalid operation")
        self.ip += 1

    def _validateParametersLength(self, operation, parameters, length):
        if len(parameters) != length:
            raise InterpreterException(
                f"Invalid number of parameters for operation {operation}: Expected {length}, got {len(parameters)}")


if __name__ == "__main__":
    """
    1: a = 2 + 2
    2: print(a)
    3: b = 2 - 1
    4: print(b)
    5: c = a * b
    6: print(c)
    7: d = c / 2
    8: print(d)
    9: e = 10 % 3 
    10: print(e)
    11: if c == 2: print("if 1")
    12: if e == 1: print("if 2")
    13: if d > 1: print("d > 1")
    14: if d != 2: print("d != 2")
    15: if d <= 2: print("d <= 2")
    16: if d >= 2: print("d >= 2")
    17: if d < 2: print("d < 2")
    
    """
    program = [
        # 1
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.ADD, []),
        Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, "a")]),
        # 2
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "a")]),
        Operation(Opcode.PRINT, []),
        # 3
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 1)]),
        Operation(Opcode.SUB, []),
        Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, "b")]),
        # 4
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "b")]),
        Operation(Opcode.PRINT, []),
        # 5
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "b")]),
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "a")]),
        Operation(Opcode.MUL, []),
        Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, "c")]),
        # 6
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "c")]),
        Operation(Opcode.PRINT, []),
        # 7
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "c")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.DIV, []),
        Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, "d")]),
        # 8
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PRINT, []),
        # 9
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 10)]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 3)]),
        Operation(Opcode.MOD, []),
        Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, "e")]),
        # 10
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "e")]),
        Operation(Opcode.PRINT, []),
        # 11
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "c")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.EQ, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "if 1")]),
        # 12
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "e")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 1)]),
        Operation(Opcode.EQ, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "if 2")]),
        # 13
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 1)]),
        Operation(Opcode.GRT, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "d > 1")]),
        # 14
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.NEQ, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "d != 2")]),
        # 15
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.LE, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "d <= 2")]),
        # 16
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.GE, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "d >= 2")]),
        # 17
        Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, "d")]),
        Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, 2)]),
        Operation(Opcode.LESS, []),
        Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, 1)]),
        Operation(Opcode.PRINTC, [Parameter(ParameterType.RELATIVE, "d < 2")]),
    ]
    from pprint import pprint
    pprint(program)
    interpreter = BytecodeInterpreter(program)
    interpreter.run()