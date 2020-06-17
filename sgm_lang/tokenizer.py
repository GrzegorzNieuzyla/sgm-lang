from sgm_lang.DataType import DataType
from sgm_lang.TokenType import TokenType
from sgm_lang.CompoundToken import CompoundToken


class TokenizerError(Exception):
    pass


class Tokenizer:

    def __init__(self, code):
        self.position = 0
        self.code = code
        self.splitCode = []
        self.tokensList = []

        # jak wystąpi {()} to możesz powstawiać między spacje i semantycznie bez zmiany: {()} == { ( ) }
        self.splittable = "(){}![]+/-*;"
        # Tych nie można rozdzielać bez zmiany znaczenia: == [to nie to samo co ] = =
        self.unSplittable = "<>=|&"

        self.keyWords = [x.value for x in TokenType]
        self.dataTypes = [x.value for x in DataType]

    def isParsableToInt(self, string):
        try:
            int(string)
        except ValueError:
            return False
        return True

    def isParsableToFloat(self, string):
        try:
            float(string)
        except ValueError:
            return False
        return True

    def isSplittable(self, char):
        return char in self.splittable

    def isUnSplittable(self, char):
        return char in self.unSplittable

    def isSymbol(self, char):
        return self.isUnSplittable(char) or self.isSplittable(char)

    # czy dane dwa znaki występujące po sobię można rozdzielić?
    # == -> nie
    # a= -> tak (a= [to to samo co ] a = )
    def canBeSplit(self, char1, char2):
        return char1.isalnum() and self.isSymbol(char2) or \
               char2.isalnum() and self.isSymbol(char1) or \
               self.isSplittable(char1) and self.isSymbol(char2) or \
               self.isSplittable(char2) and self.isSymbol(char1)

    # Działa jak split(), ale dodatkowo uwzględnia Stringi w ciągu-> nie rozdzieli spacjami słów wewnątrz "...".
    # Powinno skipowac wyeskejpowane " -> \"
    def splitWithStrings(self):
        result = []
        accumulator = ""
        position = 0
        while position < len(self.code):
            if self.code[position] == "\"":
                if accumulator != "":
                    result.append(accumulator)
                    accumulator = ""
                accumulator += self.code[position]
                position += 1
                hasSecondDelimiter = False
                while position < len(self.code):
                    accumulator += self.code[position]
                    if self.code[position] == "\"":
                        if self.code[position - 1] != "\\":
                            result.append(accumulator)
                            accumulator = ""
                            hasSecondDelimiter = True
                            break
                    position += 1
                if not hasSecondDelimiter:
                    raise TokenizerError("Unfinished String")
            elif self.code[position].isspace():
                if accumulator != "":
                    result.append(accumulator)
                    accumulator = ""
            else:
                accumulator += self.code[position]
            position += 1
        if accumulator != "":
            result.append(accumulator)
        return result

    def insertSpacesAndSplit(self):
        index = 1
        inString = True if self.code[0] == '"' else False
        while index < len(self.code):
            if self.code[index] == '"':
                inString = not inString
            if not inString and self.canBeSplit(self.code[index - 1], self.code[index]):
                self.code = self.code[:index] + ' ' + self.code[index:]
                index += 1
            if self.code[index] == '"':
                inString = not inString
            index += 1
        self.splitCode = self.splitWithStrings()

    def tokenize(self):
        self.deleteComments()
        if len(self.code) != 0:
            self.insertSpacesAndSplit()
            while self.position < len(self.splitCode):
                word = self.splitCode[self.position]

                if word in self.keyWords:
                    self.tokensList.append((TokenType(word), None))
                elif word in self.dataTypes:
                    self.tokensList.append((CompoundToken.DATA_TYPE, DataType(word)))

                elif word == "true" or word == "false":
                    self.tokensList.append((CompoundToken.BOOL, bool(word)))
                elif self.isParsableToInt(word):
                    self.tokensList.append((CompoundToken.INT, int(word)))
                elif self.isParsableToFloat(word):
                    self.tokensList.append((CompoundToken.FLOAT, float(word)))
                elif "\"" in word:
                    self.tokensList.append((CompoundToken.STRING, word))

                elif word.isidentifier():
                    self.tokensList.append((CompoundToken.ID, word))
                else:
                    raise TokenizerError("Something is wrong in Tokenizer")
                self.position += 1
        return self.tokensList

    def deleteComments(self):
        commentStart = self.position
        while commentStart < len(self.code):
            if self.code[commentStart] == TokenType.COMMENT.value:
                commentEnd = commentStart
                while commentEnd < len(self.code) and self.code[commentEnd] != '\n':
                    commentEnd += 1

                if commentEnd == len(self.code):
                    # Ends with a comment
                    self.code = self.code[:commentStart]
                else:
                    self.code = self.code[:commentStart] + self.code[commentEnd:]
            commentStart += 1


if __name__ == "__main__":
    tests = [
        " 123.456",
        "123 456 78",
        "12....3",
        "32.2.2.2.2",
        " = == === ==== ",
        "a+b / a + b %",
        "mrINTernational a = 12.3",
        "stringiBoi s = 12",
        "\"It i()s a String\"",
        """
        bool x = True # comment
        # comment2
        12#comment
        #comment
        """,
        """
            mrINTernational a = 12;
            doItIf(a==2)
            {
                showMeYourGoods("asd");
            }
        """,
        "{()}",
        "# Kom",
        """
        # to jest komentarz
        bool zmienna = True;
        # Tu też jest komentarz
        """,
        ";;"

    ]

    for theCode in tests:
        try:
            print(f'{theCode}\nTOKENIZED AS: {Tokenizer(theCode).tokenize()}\n')
        except TokenizerError as e:
            print(f'{theCode}\nTOKENIZED AS: {e}\n')
