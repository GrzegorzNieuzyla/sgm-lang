from sgm_lang.tokenizer import Tokenizer
from sgm_lang.TokenType import TokenType
from sgm_lang.Parser import Parser, Assign, Var, Num, BinOp, LogicOp, Print, NoOp, If, While, Logic
from sgm_lang.BytecodeGenerator import BytecodeGenerator
from sgm_lang.Opcode import Operation
from sgm_lang.Interpreter import BytecodeInterpreter
from typing import List
from pprint import pprint

class AstToBytecodeGenerator():
    def __init__(self, ast):
        self.ast = ast

    def generate(self) -> List[Operation]:
        print(self.ast)
        program = []
        for node in self.ast.children:

            op = None
            print("node:")
            print(node)
            if node.__class__ == NoOp:
                continue
            elif node.__class__ == Assign:
                op = self.generateAssign(node)
            elif node.__class__ == Print:
                op = self.generatePrint(node)
            elif node.__class__ == If:
                op = self.generateIf(node)
            elif node.__class__ == While:
                op = self.generateWhile(node)

            print("op:")
            print(op)
            program.extend(op)
            print("program:")
            pprint(program)
            print("--------")
        return program

    def generateSubprogram(self, nodes) -> List[Operation]:
        print(nodes)
        program = []
        for node in nodes.children:

            op = None
            print("node:")
            print(node)
            if node.__class__ == NoOp:
                return program
            elif node.__class__ == Assign:
                op = self.generateAssign(node)
            elif node.__class__ == Print:
                op = self.generatePrint(node)
            elif node.__class__ == If:
                op = self.generateIf(node)
            elif node.__class__ == While:
                op = self.generateWhile(node)

            print("op:")
            print(op)
            program.extend(op)
            print("program:")
            pprint(program)
            print("--------")
        return program

    def generateAssign(self, node) -> Operation:
        op = None
        if(node.right.__class__ == Var):
            op = BytecodeGenerator.generateVariableSetConstant(
                node.left.name, node.right.name)
        elif (node.right.__class__ in (Num, Logic)):
            op = BytecodeGenerator.generateVariableSetConstant(
                node.left.name, node.right.value)
        elif (node.right.__class__ in (BinOp, LogicOp)):
            print("match exp")
            op = BytecodeGenerator.generateVariableSet(node.left.name, self.generateExpresion(node.right))

        return op

    def generateExpresion(self, node):
        leftOp = None
        rightOp = None

        if node.left.__class__ in (BinOp, LogicOp):
            leftOp = self.generateExpresion(node.left)
        else:
            if (node.left.__class__ == Var):
                leftOp = BytecodeGenerator.generateVariableDereference(node.left.name)
            elif (node.left.__class__ in (Num, Logic)):
                leftOp = BytecodeGenerator.generateConstant(node.left.value)

        if node.right.__class__ in (BinOp, LogicOp):
            rightOp = self.generateExpresion(node.right)
        else:
            if (node.right.__class__ == Var):
                rightOp = BytecodeGenerator.generateVariableDereference(node.right.name)
            elif (node.right.__class__ in (Num, Logic)):
                rightOp = BytecodeGenerator.generateConstant(node.right.value)

        if node.op[0] == TokenType.NOT:
            return BytecodeGenerator.generateUnaryExpression(rightOp, node.op[0].getOpcode())

        return BytecodeGenerator.generateMathExpression(leftOp, rightOp, node.op[0].getOpcode())

    def generatePrint(self, node):
        op = None
        if (node.value.__class__ == Var):
            op = BytecodeGenerator.generatePrintExpression(
                BytecodeGenerator.generateVariableDereference(node.value.name))
        elif(node.value.__class__ in (Num, Logic)):
            op = BytecodeGenerator.generatePrintConstant(node.value.value)
        elif (node.value.__class__ in (BinOp, LogicOp)):
            print("match exp")
            op = BytecodeGenerator.generatePrintExpression(
                self.generateExpresion(node.value))

        return op

    def generateIf(self, node):
        cond = self.generateExpresion(node.expression)
        body = self.generateSubprogram(node.statements)

        return BytecodeGenerator.generateIf(body, cond)

    def generateWhile(self, node):
        cond = self.generateExpresion(node.expression)
        body = self.generateSubprogram(node.statements)

        return BytecodeGenerator.generateWhile(body, cond)

if __name__ == "__main__":
    text = "bool zmienna = True && False;" \
            "showMeYourGoods(\"slowo\");" \
            "showMeYourGoods(4);" \
            "showMeYourGoods(zmienna);"
    text2 = "mrINTernational zmienna = 12 * 4 - 5;" \
             "stringiBoi slowo = \"SloWa Ze Spacjami 1 2 +\";" \
            "mrINTernational zmienna2 = 12 * 4 - zmienna;" \
            "showMeYourGoods(slowo);" \
            "showMeYourGoods(1+2*4-(90 / 10));" \
            "showMeYourGoods(zmienna);" \
            "showMeYourGoods(zmienna2);"
    text3 = "bool zmienna = 1 + 3;" \
            "showMeYourGoods(zmienna);"# !(1 + 4 < 2 *4 ) ||
    text4 =  "doItIf((!(1 + 4 < 2 *4 )) || (!( False && !True))) {" \
            "bool zmienna = !(1 + 4 < 2 *4 ) || ( False && !True);" \
            "}" \
            "showMeYourGoods(123);"
    text5 = "showMeYourGoods(!(1 + 4 < 2 *4 ) || ( 0 && !(1)));" \
            "youSpinMeRound((1 + 4 < 2 *4 ) || ( 0 && !(1))) {" \
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
        mrINTernational a = 0;
        showMeYourGoods("start");
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
    lexer = Tokenizer(text3).tokenize()
    type, val = lexer[0]
    print(f'Lexer: {lexer[0]}')
    print(f'Lexer: {lexer}')

    parser = Parser(lexer)
    print(f'Parser: {parser}')

    # try:
    #     result = parser.parse()
    #     print(f'Parser2: {result}')
    #     program = AstToBytecodeGenerator(result).generate()
    #     print(program.__class__.__name__)
    #
    #     print("inter")
    #     interpreter = BytecodeInterpreter(program)
    #     interpreter.run()
    # except:
    #     print("Error")

    result = parser.parse()
    print(f'Parser2: {result}')
    program = AstToBytecodeGenerator(result).generate()
    print(program.__class__.__name__)

    print("inter")
    interpreter = BytecodeInterpreter(program)
    interpreter.run()