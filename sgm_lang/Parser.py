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

    def __str__(self):
        return ",".join( map( str, self.children ) )

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'[{self.left.__str__()} == {self.op} == {self.right.__str__()}]'

    def __repr__(self):
        return self.__str__()

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, dataType, ID):
        self.dataType = dataType
        self.ID = ID

    def __str__(self):
        return f'{self.dataType} -> {self.ID}'

class NoOp(AST):
    def __str__(self):
        return "NoOp"

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
        """factor : INTEGER | BOOL | FLOAT | STRING
        | LPAREN expr RPAREN | LBRACE expr RBRACE
        | variable"""
        token = self.current_token
        if token[0] == CompoundToken.INT:
            self.eat(CompoundToken.INT)
            return Num(token)
        elif token[0] == CompoundToken.BOOL:
            self.eat(CompoundToken.BOOL)
            return Num(token)
        elif token[0] == CompoundToken.FLOAT:
            self.eat(CompoundToken.FLOAT)
            return Num(token)
        elif token[0] == CompoundToken.STRING:
            self.eat(CompoundToken.STRING)
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
        elif token[0] == CompoundToken.DATA_TYPE:
            node = self.variableDefinition()
            return node
        elif token[0] == CompoundToken.ID:
            node = self.variable()
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
        factor : INTEGER | BOOL | FLOAT | STRING
                | LPAREN expr RPAREN | LBRACE expr RBRACE
                | variable
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

    def compound_statement(self):
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMICOLON statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token[0] == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            results.append(self.statement())

        if self.current_token[0] == CompoundToken.ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token[0] == CompoundToken.DATA_TYPE:
            node = self.assignment_statement()
        elif self.current_token[0] == CompoundToken.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : DataType variable ASSIGN expr
            | variable ASSIGN expr
        """
        if self.current_token[0] == CompoundToken.DATA_TYPE:
            left = self.variableDefinition()
        elif self.current_token[0] == CompoundToken.ID:
            left = self.variable();

        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variableDefinition(self):
        """
        DataType variable
        """
        node = Var(self.current_token[0], self.current_token[1])
        self.eat(CompoundToken.DATA_TYPE)
        self.eat(CompoundToken.ID)
        return node

    def variable(self):
        """
        variable
        """
        node = Var(None, self.current_token[1])
        self.eat(CompoundToken.ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def parse(self):
        prog = self.compound_statement()
        return prog

    def getNextToken(self):
        if (self.index >= len(self.lexer)):
            return (None, None)
        token = self.lexer[self.index]
        print(self.index)
        self.index += 1

        print(token[0])

        return token


if __name__ == "__main__":
    #text = "1 + 5 * 9 - ( 20 / 10 )"
    text = "mrINTernational zmienna = 12 * 4 - 5;" \
           "stringiBoi slowo = \"SloWa Ze Spacjami 1 2 +\";" \
           "zmienna2 = (zmienna + 2) * 5;"
    lexer = Tokenizer(text).tokenize()
    type, val = lexer[0]
    print(f'Lexer: {lexer[0]}')
    print(f'Lexer: {lexer}')

    parser = Parser(lexer)
    print(f'Parser: {parser}')
    print(f'Parser2: {parser.parse()}')