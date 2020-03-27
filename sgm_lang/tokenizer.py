from sgm_lang.TokenType import TokenType
from sgm_lang.DataType import DataType


class TokenizerError(Exception):
    pass


def isProperNameChar(currentElement):
    isNone = currentElement is not None
    return isNone and (currentElement.isdigit() or currentElement.isalpha() or currentElement == '_')


class Tokenizer:

    def __init__(self, code):
        self.position = 0
        self.code = code
        self.tokensList = []

    def getCharAt(self, x):
        if x < len(self.code):
            return self.code[x]
        else:
            return None

    def tokenize(self):
        while self.getCharAt(self.position):
            currentElement = self.getCharAt(self.position)
            if currentElement.isspace():
                pass
            elif currentElement.isalpha() or currentElement == '_':
                self.tokenizeWord()
            elif currentElement.isdigit():
                self.tokenizeNumber()
            else:
                self.tokenizeSpecialCharacter()
            self.position += 1
        return self.tokensList

    def tokenizeNumber(self):
        number = ""
        currentElement = self.getCharAt(self.position)
        while currentElement and currentElement.isdigit():
            number += currentElement
            self.position += 1
            currentElement = self.getCharAt(self.position)

        if currentElement and currentElement == '.':
            number += '.'
            self.position += 1
            currentElement = self.getCharAt(self.position)
            while currentElement and currentElement.isdigit():
                number += currentElement
                self.position += 1
                currentElement = self.getCharAt(self.position)
            self.position -= 1
            self.tokensList.append((TokenType.FLOAT, number))
        else:
            self.position -= 1
            self.tokensList.append((TokenType.INT, number))

    def tokenizeSpecialCharacter(self):
        currentElement = self.getCharAt(self.position)
        tokenValue = None
        if currentElement == TokenType.L_BRACE.value:
            token = TokenType.L_BRACE
        elif currentElement == TokenType.R_BRACE.value:
            token = TokenType.R_BRACE
        elif currentElement == TokenType.L_PAREN.value:
            token = TokenType.L_PAREN
        elif currentElement == TokenType.R_PAREN.value:
            token = TokenType.R_PAREN
        elif currentElement == TokenType.COMMENT.value:
            token = TokenType.COMMENT
        elif currentElement == TokenType.ASSIGN.value:
            self.position += 1
            currentElement = self.getCharAt(self.position)
            if currentElement and currentElement == TokenType.ASSIGN.value:
                token = TokenType.EQUAL
            else:
                self.position -= 1
                token = TokenType.ASSIGN
        elif currentElement == TokenType.LESS.value:
            self.position += 1
            currentElement = self.getCharAt(self.position)
            if currentElement and currentElement == TokenType.ASSIGN.value:
                token = TokenType.LESS_EQUAL
            else:
                self.position -= 1
                token = TokenType.LESS
        elif currentElement == TokenType.GREATER.value:
            self.position += 1
            currentElement = self.getCharAt(self.position)
            if currentElement and currentElement == TokenType.ASSIGN.value:
                token = TokenType.GREATER_EQUAL
            else:
                self.position -= 1
                token = TokenType.GREATER
        elif currentElement == TokenType.OR.value[0]:
            self.position += 1
            currentElement = self.getCharAt(self.position)
            if currentElement and currentElement == TokenType.OR.value[1]:
                token = TokenType.OR
            else:
                raise TokenizerError(f'Single \'{TokenType.OR.value[0]}\' found')
        elif currentElement == TokenType.AND.value[0]:
            self.position += 1
            currentElement = self.getCharAt(self.position)
            if currentElement and currentElement == TokenType.AND.value[1]:
                token = TokenType.AND
            else:
                raise TokenizerError(f'Single \'{TokenType.AND.value[0]}\' found')
        elif currentElement == TokenType.NOT.value:
            token = TokenType.NOT
        elif currentElement == TokenType.ADD.value:
            token = TokenType.ADD
        elif currentElement == TokenType.SUB.value:
            token = TokenType.SUB
        elif currentElement == TokenType.MUL.value:
            token = TokenType.MUL
        elif currentElement == TokenType.DIV.value:
            token = TokenType.DIV
        elif currentElement == TokenType.MOD.value:
            token = TokenType.MOD
        elif currentElement == TokenType.STR_INDICATOR.value:
            string = ""
            self.position += 1
            currentElement = self.getCharAt(self.position)
            while currentElement and currentElement != TokenType.STR_INDICATOR.value:
                string += currentElement
                self.position += 1
                currentElement = self.getCharAt(self.position)
            if currentElement is None:
                raise TokenizerError("Unfinished String")
            else:
                token = TokenType.STRING
                tokenValue = string
        else:
            raise TokenizerError("Unknown character")
        self.tokensList.append((token, tokenValue))

    def tokenizeWord(self):
        name = ""
        currentElement = self.getCharAt(self.position)
        while isProperNameChar(currentElement):
            name += currentElement
            self.position += 1
            currentElement = self.getCharAt(self.position)
        self.position -= 1

        tokenValue = None
        if name == TokenType.WHILE.value:
            token = TokenType.WHILE
        elif name == TokenType.PRINT.value:
            token = TokenType.PRINT
        elif name == TokenType.IF.value:
            token = TokenType.IF
        elif name == DataType.BOOL.value:
            token = TokenType.DATA_TYPE
            tokenValue = DataType.BOOL
        elif name == DataType.INT.value:
            token = TokenType.DATA_TYPE
            tokenValue = DataType.INT
        elif name == DataType.FLOAT.value:
            token = TokenType.DATA_TYPE
            tokenValue = DataType.FLOAT
        elif name == DataType.STRING.value:
            token = TokenType.DATA_TYPE
            tokenValue = DataType.STRING
        else:
            token = TokenType.ID
            tokenValue = name

        self.tokensList.append((token, tokenValue))


tests = [
    " 123.456",
    "123 456 78",
    "12....3",
    "32.2.2.2.2",
    " = == === ==== ",
    "a+b / a + b %",
    "mrINTernational a = 12.3",
    "stringiBoi s = 12",
    "\"It is a String\""

]

for theCode in tests:
    try:
        print(f'{theCode}\nTOKENIZED AS: {Tokenizer(theCode).tokenize()}\n')
    except TokenizerError as e:
        print(f'{theCode}\nTOKENIZED AS: {e}\n')
