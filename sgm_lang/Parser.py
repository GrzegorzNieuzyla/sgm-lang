from sgm_lang.tokenizer import Tokenizer
from sgm_lang.CompoundToken import CompoundToken
from sgm_lang.TokenType import TokenType

class AST(object):
    def __repr__(self):
        return str(self)


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'[{self.left.__str__()} <> {self.op} <> {self.right.__str__()}]'



class LogicOp(AST):
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
        return str(self.value)

class Logic(AST):
    def __init__(self, token):
        self.token = token
        self.value = token[0] == TokenType.TRUE

    def __str__(self):
        return str(self.value)

class Compound(AST):
    def __init__(self):
        self.children = []

    def __str__(self):
        return ",".join(map(str, self.children))


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

    def __init__(self, dataType, ID, name):
        self.dataType = dataType
        self.ID = ID
        self.name = name

    def __str__(self):
        return f'{self.dataType} -> {self.ID} name: {self.name}'


class NoOp(AST):
    def __str__(self):
        return "NoOp"


class Print(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return f'[{self.token} print {self.value.__str__()}]'


class If(AST):
    def __init__(self, token, expression, statements):
        self.token = token
        self.expression = expression
        self.statements = statements

    def __str__(self):
        return f'[if {self.token} exp({self.expression.__str__()}) <{self.statements.__str__()}>]'


class While(AST):
    def __init__(self, token, expression, statements):
        self.token = token
        self.expression = expression
        self.statements = statements

    def __str__(self):
        return f'[while {self.token} exp({self.expression.__str__()}) <{self.statements.__str__()}>]'


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
        | NOT expr
        | TRUE | FALSE
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
        elif token[0] == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = LogicOp(None, token, self.expr())
            return node
        elif token[0] == TokenType.TRUE:
            node = Logic(token)
            self.eat(TokenType.TRUE)
            return node
        elif token[0] == TokenType.FALSE:
            node = Logic(token)
            self.eat(TokenType.FALSE)
            return node
        elif token[0] == CompoundToken.DATA_TYPE:
            node = self.variableDefinition()
            return node
        elif token[0] == CompoundToken.ID:
            node = self.variable()
            return node

    def term(self):
        """term : factor ((MUL | DIV | OR | AND) factor)*"""
        node = self.factor()

        while self.current_token[0] in (TokenType.MUL, TokenType.DIV, TokenType.OR, TokenType.AND):
            token = self.current_token
            if token[0] == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token[0] == TokenType.DIV:
                self.eat(TokenType.DIV)
            elif token[0] == TokenType.OR:
                self.eat(TokenType.OR)
            elif token[0] == TokenType.AND:
                self.eat(TokenType.AND)

            node = BinOp(left=node, op=token, right=self.factor())
            # print(f'Node: {node}')

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS | MOD | EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) term)*
        term   : factor ((MUL | DIV | OR | AND) factor)*
        factor : factor : INTEGER | BOOL | FLOAT | STRING
                | LPAREN expr RPAREN | LBRACE expr RBRACE
                | NOT expr
                | variable
        """
        node = self.term()

        while self.current_token[0] in \
                (TokenType.ADD, TokenType.SUB, TokenType.MOD, TokenType.EQUAL, TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL,
                 TokenType.GREATER_EQUAL):
            token = self.current_token
            if token[0] == TokenType.ADD:
                self.eat(TokenType.ADD)
            elif token[0] == TokenType.SUB:
                self.eat(TokenType.SUB)
            elif token[0] == TokenType.MOD:
                self.eat(TokenType.MOD)
            elif token[0] == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
            elif token[0] == TokenType.LESS:
                self.eat(TokenType.LESS)
            elif token[0] == TokenType.GREATER:
                self.eat(TokenType.GREATER)
            elif token[0] == TokenType.LESS_EQUAL:
                self.eat(TokenType.LESS_EQUAL)
            elif token[0] == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)

            node = BinOp(left=node, op=token, right=self.term())
            # print(f'Node: {node}')

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
        isFinished = False
        results = []
        while not isFinished:
            node = self.statement()
            if self.current_token[0] == TokenType.R_BRACE:
                self.eat(TokenType.R_BRACE)
                isFinished = True

            if self.current_token[0] == None or\
                self.current_token[0] not in (CompoundToken.DATA_TYPE, CompoundToken.ID, TokenType.PRINT, TokenType.IF, TokenType.WHILE):
                if self.current_token[0] == None:
                    isFinished = True
                else:
                    self.error()

            if self.current_token[0] == None:
                isFinished = True

            results.append(node)

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | print(expr)
                  | if(expr) { statement_list }
                  | while(expr) { statement_list }
                  | empty
        """
        if self.current_token[0] == CompoundToken.DATA_TYPE:
            node = self.assignment_statement()
            self.eat(TokenType.SEMICOLON)
        elif self.current_token[0] == CompoundToken.ID:
            node = self.assignment_statement()
            self.eat(TokenType.SEMICOLON)
        elif self.current_token[0] == TokenType.PRINT:
            node = self.print_statement()
            self.eat(TokenType.SEMICOLON)
        elif self.current_token[0] == TokenType.IF:
            node = self.if_statement()
        elif self.current_token[0] == TokenType.WHILE:
            node = self.while_statement()
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
            left = self.variable()

        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variableDefinition(self):
        """
        DataType variable
        """
        node = Var(self.current_token[0], self.current_token[1], None)
        self.eat(CompoundToken.DATA_TYPE)
        node.name = self.current_token[1]
        self.eat(CompoundToken.ID)
        return node

    def variable(self):
        """
        variable
        """
        node = Var(None, None, self.current_token[1])
        self.eat(CompoundToken.ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def print_statement(self):
        token = self.current_token
        self.eat(TokenType.PRINT)
        self.eat(TokenType.L_PAREN)
        value = self.expr()
        self.eat(TokenType.R_PAREN)

        node = Print(token, value)
        return node

    def if_statement(self):
        token = self.current_token
        self.eat(TokenType.IF)
        self.eat(TokenType.L_PAREN)
        expression = self.expr()
        self.eat(TokenType.R_PAREN)
        self.eat(TokenType.L_BRACE)
        statements = self.compound_statement()

        node = If(token, expression, statements)
        return node

    def while_statement(self):
        token = self.current_token
        self.eat(TokenType.WHILE)
        self.eat(TokenType.L_PAREN)
        expression = self.expr()
        self.eat(TokenType.R_PAREN)
        self.eat(TokenType.L_BRACE)
        statements = self.compound_statement()

        node = While(token, expression, statements)
        return node

    def parse(self):
        prog = self.compound_statement()
        return prog

    def getNextToken(self):
        if (self.index >= len(self.lexer)):
            return (None, None)
        token = self.lexer[self.index]
        self.index += 1

        return token


if __name__ == "__main__":
    text = "bool zmienna = True;"
    text2 = "mrINTernational zmienna = 12 * 4 - 5;" \
            "stringiBoi slowo = \"SloWa Ze Spacjami 1 2 +\";" \
            "zmienna2 = (zmienna + 2) * 5;" \
            "showMeYourGoods(slowo);" \
            "showMeYourGoods(1+2*4-(90 / 10));"
    text3 = "bool zmienna = !(1 + 4 < 2 *4 ) || ( False && !True);"
    text4 = "doItIf(!(1 + 4 < 2 *4 ) || ( False && !True)) {" \
            "bool zmienna = !(1 + 4 < 2 *4 ) || ( False && !True);" \
            "showMeYourGoods(zmienna);" \
            "showMeYourGoods(1+2*4-(90 / 10));" \
            "}"
    text5 = "youSpinMeRound(!(1 + 4 < 2 *4 ) || ( False && !True)) {" \
            "bool zmienna = !(1 + 4 < 2 *4 ) || ( False && !True);" \
            "showMeYourGoods(zmienna);" \
            "showMeYourGoods(1+2*4-(90 / 10) % 3);" \
            "}"
    text6 = """
        # to jest komentarz
        bool zmienna = True;
        # Tu też jest komentarz
        """
    text7 = """


        youSpinMeRound(a < 10)
        {
            a = a + 1;
            showMeYourGoods(a);
        }
        showMeYourGoods("end");
        a = 0;
        youSpinMeRound(a < 10)
        {
            a = a + 1;
            showMeYourGoods(a);
        }
    """
    lexer = Tokenizer(text7).tokenize()
    type, val = lexer[0]
    print(f'Lexer: {lexer[0]}')
    print(f'Lexer: {lexer}')

    parser = Parser(lexer)
    print(f'Parser: {parser}')

    try:
        result = parser.parse()
        print(f'Parser2: {result}')
    except:
        print("Error")
