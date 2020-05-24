from sgm_lang.tokenizer import Tokenizer
from sgm_lang.CompoundToken import CompoundToken
from sgm_lang.TokenType import TokenType

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'[{self.left.__str__()} <> {self.op} <> {self.right.__str__()}]'

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token[1]

    def __str__(self):
        return self.value

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token[1]

class NoOp(AST):
    pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.index = 0
        self.current_token = self.getNextToken()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token[0] == token_type:
            self.current_token = self.getNextToken()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN | | LBRACE expr RBRACE"""
        token = self.current_token
        if token[0] == CompoundToken.INT:
            self.eat(CompoundToken.INT)
            return Num(token)
        elif token[0] == TokenType.L_PAREN:
            self.eat(TokenType.L_PAREN)
            node = self.expr()
            self.eat(TokenType.R_PAREN)
            return node
        elif token[0] == TokenType.L_BRACE:
            self.eat(TokenType.L_BRACE)
            node = self.expr()
            self.eat(TokenType.R_BRACE)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token[0] in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token[0] == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token[0] == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())
            print(f'Node: {node}')

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token[0] in (TokenType.ADD, TokenType.SUB):
            token = self.current_token
            if token[0] == TokenType.ADD:
                self.eat(TokenType.ADD)
            elif token[0] == TokenType.SUB:
                self.eat(TokenType.SUB)

            node = BinOp(left=node, op=token, right=self.term())
            print(f'Node: {node}')

        return node

    def parse(self):
        return self.expr()

    def getNextToken(self):
        if (self.index >= len(self.lexer)):
            return (None, None)
        token = self.lexer[self.index]
        print(self.index)
        self.index += 1

        print(token[0])

        return token


if __name__ == "__main__":
    text = "1 + 5 * 9 - ( 20 / 10 )"
    lexer = Tokenizer(text).tokenize()
    type, val = lexer[0]
    print(f'Lexer: {lexer}')

    parser = Parser(lexer)
    print(f'Parser: {parser}')
    print(f'Parser2: {parser.parse()}')