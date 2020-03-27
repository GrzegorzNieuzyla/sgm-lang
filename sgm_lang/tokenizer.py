from sgm_lang.TokenType import TokenType

specialCharacters = ['{', '}', '(', ')']  # ...


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
        elif currentElement in specialCharacters:
            print(f'{currentElement} <- is special character')
        position += 1

    return tokensList


print(tokenize("123.231 12 0.1 1."))
