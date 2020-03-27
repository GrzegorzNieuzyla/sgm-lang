from enum import Enum


class TokenType(Enum):

    BOOL = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    DATA_TYPE = 5
    ID = 6

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

    WHILE = "youSpinMeRound"
    PRINT = "showMeYourGoods"
    IF = "doItIf"

    def __repr__(self):
        return str(self.name)
