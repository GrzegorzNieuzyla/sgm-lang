from enum import Enum


class DataType(Enum):

    BOOL = "bool"
    INT = "mrINTernational"
    FLOAT = "boatWhichFloat"
    STRING = "stringiBoi"

    def __repr__(self):
        return str(self.name)
