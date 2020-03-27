from enum import Enum, auto


class TokenType(Enum):

    INT = 1
    FLOAT = 2

    L_BRACE = auto()
    R_BRACE = auto()
    L_PAREN = auto()
    R_PAREN = auto()

    COMMENT = auto()
    ASSIGN = auto()
    EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()

    def __repr__(self):
        return str(self.name)
