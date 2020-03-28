from enum import Enum, auto
from typing import List, Any


class Opcode(Enum):
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    PRINT = auto()
    PRINTC = auto()
    JMP_IF = auto()
    JMP_NOT_IF = auto()
    PUSH = auto()
    POP = auto()
    EQ = auto()



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