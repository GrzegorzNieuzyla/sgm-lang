from sgm_lang.TokenType import TokenType


class TokenizerError(Exception):
    pass


def tokenizeNumber(code, position):
    number = ""
    isFloat = False
    while position < len(code) and (code[position].isdigit() or code[position] == '.'):
        if code[position] == '.':
            isFloat = True
        number += code[position]
        position += 1
    if isFloat:
        return position, (TokenType.FLOAT, number)
    else:
        return position, (TokenType.FLOAT, number)


def tokenizeSpecialCharacter(code, position):
    currentElement = code[position]
    if currentElement == '{':
        token = TokenType.L_BRACE
    elif currentElement == '}':
        token = TokenType.R_BRACE
    elif currentElement == '(':
        token = TokenType.L_PAREN
    elif currentElement == ')':
        token = TokenType.R_PAREN
    elif currentElement == '#':
        token = TokenType.COMMENT
    elif currentElement == '=':
        position += 1
        if position < len(code) and code[position] == '=':
            token = TokenType.EQUAL
        else:
            position -= 1
            token = TokenType.ASSIGN
    elif currentElement == '<':
        position += 1
        if position < len(code) and code[position] == '=':
            token = TokenType.LESS_EQUAL
        else:
            position -= 1
            token = TokenType.LESS
    elif currentElement == '>':
        position += 1
        if position < len(code) and code[position] == '=':
            token = TokenType.GREATER_EQUAL
        else:
            position -= 1
            token = TokenType.GREATER
    elif currentElement == '|':
        position += 1
        if position < len(code) and code[position] == '|':
            token = TokenType.OR
        else:
            raise TokenizerError("Single \'|\' found")
    elif currentElement == '&':
        position += 1
        if position < len(code) and code[position] == '&':
            token = TokenType.AND
        else:
            raise TokenizerError("Single \'&\' found")
    elif currentElement == '!':
        token = TokenType.NOT
    elif currentElement == '+':
        token = TokenType.ADD
    elif currentElement == '-':
        token = TokenType.SUB
    elif currentElement == '*':
        token = TokenType.MUL
    elif currentElement == '/':
        token = TokenType.DIV
    elif currentElement == '%':
        token = TokenType.MOD
    else:
        raise TokenizerError("Unknown character")
    position += 1
    return position, (token, None)


def tokenize(code):
    tokensList = []
    position = 0
    while position < len(code):
        currentElement = code[position]

        if currentElement.isspace():
            pass
        elif currentElement.isalpha():
            print(f'{currentElement} <- is character')
        elif currentElement.isdigit():
            position, token = tokenizeNumber(code, position)
            tokensList.append(token)
        else:
            position, token = tokenizeSpecialCharacter(code, position)
            tokensList.append(token)
        position += 1

    return tokensList


print(tokenize("123.231 12 0.1 1."))
print(tokenize(" - + = == = { }"))
