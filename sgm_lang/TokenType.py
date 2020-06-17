from enum import Enum

from sgm_lang.Opcode import Opcode


class TokenType(Enum):
    L_BRACE = '{'
    R_BRACE = '}'
    L_PAREN = '('
    R_PAREN = ')'

    COMMENT = '#'
    ASSIGN = '='
    EQUAL = "=="
    LESS = '<'
    GREATER = '>'
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="

    OR = "||"
    AND = "&&"
    NOT = '!'

    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    STR_INDICATOR = '\"'
    SEMICOLON = ';'

    WHILE = "youSpinMeRound"
    PRINT = "showMeYourGoods"
    IF = "doItIf"

    def __repr__(self):
        return str(self.name)

    def getOpcode(self) -> Opcode:
        if self == TokenType.EQUAL:
            return Opcode.EQ
        elif self == TokenType.LESS:
            return Opcode.LESS
        elif self == TokenType.GREATER:
            return Opcode.GRT
        elif self == TokenType.LESS_EQUAL:
            return Opcode.LE
        elif self == TokenType.GREATER_EQUAL:
            return Opcode.GE
        elif self == TokenType.ADD:
            return Opcode.ADD
        elif self == TokenType.SUB:
            return Opcode.SUB
        elif self == TokenType.MUL:
            return Opcode.MUL
        elif self == TokenType.DIV:
            return Opcode.DIV
        elif self == TokenType.MOD:
            return Opcode.MOD
        elif self == TokenType.AND:
            return Opcode.BINARY_AND
        elif self == TokenType.OR:
            return Opcode.BINARY_OR