from sgm_lang.Opcode import Opcode, Operation, ParameterType, Parameter
from sgm_lang.Interpreter import BytecodeInterpreter
from typing import List, Union


class BytecodeGenerator():
    """
    Helper class to generate code structures in bytecode
    """
    @staticmethod
    def generateIf(instructions: List[Operation], condition: List[Operation]) -> List[Operation]:
        """
        Generates if block.
        'instructions' will be executed if after executing the 'condition' instructions stack.pop() will be truthy
        """
        result = condition[:]
        result.append(Operation(Opcode.JMP_NOT_IF, [Parameter(ParameterType.RELATIVE, len(instructions))]))
        result += instructions
        return result

    @staticmethod
    def generateWhile(instructions: List[Operation], condition: List[Operation]) -> List[Operation]:
        """
        Generates while block.
        'instructions' will be executed as long after executing the 'condition' instructions stack.pop() will be truthy
        """
        new_instructions = instructions + [Operation(Opcode.JMP, [Parameter(ParameterType.RELATIVE, -(len(instructions) + len(condition) + 2))])]
        return BytecodeGenerator.generateIf(new_instructions, condition)

    @staticmethod
    def generateMathExpression(left: List[Operation], right: List[Operation], opcode: Opcode) -> List[Operation]:
        """
        Applies math operation to left and right operand, result is pushed to stack
        Left and right operations have to leave stack the same as before execution except for the result at top
        """
        result = left + right
        result.append(Operation(opcode, []))
        return result
    
    @staticmethod
    def generateUnaryExpression(operand: List[Operation], opcode: Opcode) -> List[Operation]:
        """
        Applies unary operation to operand, result is pushed to stack
        Operand operation has to leave stack the same as before execution except for the result at top
        """
        result = operand
        result.append(Operation(opcode, []))
        return result

    @staticmethod
    def generateConstant(value: Union[str, bool, int, float]) -> List[Operation]:
        return [Operation(Opcode.PUSH, [Parameter(ParameterType.IMMEDIATE, value)])]

    @staticmethod
    def generateVariableDereference(variable_name: str) -> List[Operation]:
        return [Operation(Opcode.LOAD, [Parameter(ParameterType.IMMEDIATE, variable_name)])]

    @staticmethod
    def generateVariableSet(variable_name: str, expression: List[Operation]) -> List[Operation]:
        """
        Sets variable to the result of expression
        """
        result = expression[:]
        result.append(Operation(Opcode.STORE, [Parameter(ParameterType.IMMEDIATE, variable_name)]))
        return result
    
    @staticmethod
    def generateVariableSetConstant(variable_name: str, value: Union[str, bool, int, float]) -> List[Operation]:
        """
        Sets variable to the constant value
        """
        return BytecodeGenerator.generateVariableSet(variable_name, BytecodeGenerator.generateConstant(value))

    @staticmethod
    def generatePrintExpression(expression: List[Operation]) -> List[Operation]:
        result = expression[:]
        result.append(Operation(Opcode.PRINT, []))
        return result

    @staticmethod
    def generatePrintConstant(value: Union[str, bool, int, float]) -> List[Operation]:
        return [Operation(Opcode.PRINTC, [Parameter(ParameterType.IMMEDIATE, value)])]

if __name__ == '__main__':
    """
    a = 0
    print("start")
    while a != 10
        a = a + 1
        print(a)
        if !(a % 2 == 0)
            print("odd")
    print("end")
    """
    from pprint import pprint
    if_cond = BytecodeGenerator.generateMathExpression(
        BytecodeGenerator.generateMathExpression(
            BytecodeGenerator.generateVariableDereference("a"),
            BytecodeGenerator.generateConstant(2),
            Opcode.MOD
        ),
        BytecodeGenerator.generateConstant(0),
        Opcode.EQ
    )
    if_cond = BytecodeGenerator.generateUnaryExpression(if_cond, Opcode.NOT)
    if_block = BytecodeGenerator.generateIf(BytecodeGenerator.generatePrintConstant("odd"), if_cond)
    while_body = (
        BytecodeGenerator.generateVariableSet(
            "a",
            BytecodeGenerator.generateMathExpression(
                BytecodeGenerator.generateVariableDereference("a"),
                BytecodeGenerator.generateConstant(1),
                Opcode.ADD
            )
        ) +
        BytecodeGenerator.generatePrintExpression(
            BytecodeGenerator.generateVariableDereference("a")
        ) +
        if_block
    )
    
    while_cond = BytecodeGenerator.generateMathExpression(
        BytecodeGenerator.generateVariableDereference("a"),
        BytecodeGenerator.generateConstant(10),
        Opcode.NEQ
    )
    while_block = BytecodeGenerator.generateWhile(
        while_body,
        while_cond
    )
    program = (
        BytecodeGenerator.generateVariableSetConstant("a", 0) +
        BytecodeGenerator.generatePrintConstant("start") +
        while_block +
        BytecodeGenerator.generatePrintConstant("end")
    )
    pprint(program)
    print()
    interpreter = BytecodeInterpreter(program)
    interpreter.run()




