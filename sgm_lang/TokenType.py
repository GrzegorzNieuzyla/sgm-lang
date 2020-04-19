from enum import Enum


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
