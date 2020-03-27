from enum import Enum


class TokenType(Enum):
    INT = 1
    FLOAT = 2

    def __repr__(self):
        return str(self.name)
