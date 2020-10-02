# SGM interpreted language

## Language capabilities

1. Supported data types: `mrINTernational` (`int`), `boatWhichFloat` (`float`), `stringiBoi` (`string`), `bool`
2. Comments (`# this is a comment`)
3. Parsing mathematical expressions containing of `+`, `-`, `*`, `/`, `%` and parentheses `()`
4. Mathematical relationships `==`, `<`, `>`, `<=`, `>=` 
5. Conditional statements `doItIf` (`IF`)
6. Loop `youSpinMeRound` (`WHILE`)
7. Parsing logical expressions containing of `True`, `False`, `&&`, `||`, `!`, `()`
8. Printing to STDOUT (`showMeYourGoods()` function)
---
Example program:
```java
mrINTernational x = 0;
youSpinMeRound(x < 10)
{
  showMeYourGoods(x);
  doItIf((x % 2) == 0)
  {
    showMeYourGoods(" is even");
  }
  showMeYourGoods("\n");
  x = x + 1;
}
```

## Run
```
> python sgm examples/helloworld.sgm
```
`examples` directory contains 4 files with example SGM code

---
**Responsibilities:**   
Szymon Borowy - Parser  
Marcin Kozak - Tokenizer  
Grzegorz Nieużyła - Bytecode and Interpreter  

