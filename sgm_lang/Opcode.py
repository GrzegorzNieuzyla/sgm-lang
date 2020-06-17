from enum import Enum, auto
from typing import List


class Opcode(Enum):
    LOAD = auto()  # push variable specified as parameter
    STORE = auto()  # pops and sets as variable specified as parameter
    ADD = auto()  # push stack.pop(1) + stack.pop(0)
    SUB = auto()  # push stack.pop(1) - stack.pop(0)
    MUL = auto()  # push stack.pop(1) * stack.pop(0)
    DIV = auto()  # push stack.pop(1) / stack.pop(0)
    MOD = auto()  # push stack.pop(1) % stack.pop(0)
    PRINT = auto()  # prints stack[0]
    PRINTC = auto()  # prints parameter
    JMP = auto()  # jump
    JMP_IF = auto()  # jump if stack.pop(0)
    JMP_NOT_IF = auto()  # jump if not stack.pop(0)
    PUSH = auto()  # push parameter
    POP = auto()  # pops to variable in parameter
    EQ = auto()  # pushes True if stack.pop(1) == stack.pop(0)
    NEQ = auto()  # pushes True if stack.pop(1) != stack.pop(0)
    GE = auto()  # pushes True if stack.pop(1) >= stack.pop(0)
    GRT = auto()  # pushes True if stack.pop(1) > stack.pop(0)
    LE = auto()  # pushes True if stack.pop(1) <= stack.pop(0)
    LESS = auto()  # pushes True if stack.pop(1) < stack.pop(0)
    NOT = auto()  # pushes !stack.pop(0)



class ParameterType(Enum):
    IMMEDIATE = auto()
    RELATIVE = auto()


class Parameter:
    def __init__(self, paramType: ParameterType, value=None):
        self.paramType = paramType
        self.value = value

    def __repr__(self):
        return f"{self.paramType.name}: {self.value}"

    def __str__(self):
        return self.__repr__()

class Operation:
    def __init__(self, opcode: Opcode, params: List[Parameter]):
        self.opcode = opcode
        self.params = params

    def __repr__(self):
        return f"{self.opcode.name}: {', '.join(map(str, self.params))}"

    def __str__(self):
        return self.__repr__()