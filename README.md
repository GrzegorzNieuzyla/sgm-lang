# SGM interpreted language

## Temat:
Interpreter nowo zdefiniowanego języka w Pythonie

## Zakres funkcjonalności języka

1. Wspierane typy zmiennych: `mrINTernational` (`int`), `boatWhichFloat` (`float`), `stringiBoi` (`string`), `bool`
2. Komentarze (`# this is a comment`)
3. Parsowanie wyrażeń matematycznych składających się z `+`, `-`, `*`, `/`, `%` oraz nawiasów `()`
4. Relacje `==`, `<`, `>`, `<=`, `>=` 
5. Instrukcja warunkowe `doItIf` (`IF`)
6. Pętla `youSpinMeRound` (`WHILE`)
7. Parsowanie operacji logicznych złożonych z `True`, `False`, `&&`, `||`, `!`, `()`
8. Wypisywanie na standardowe wyjście (funkcja `showMeYourGoods()`)
---
Przykładowy program:
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

---
**Skład grupy i podział pracy:**   
Szymon Borowy - Parser  
Marcin Kozak - Tokenizer  
Grzegorz Nieużyła - Bytecode i Interpreter  

