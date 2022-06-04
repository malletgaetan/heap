from pascal_lib import Token, Lexer, Parser, Interpreter

program = """
PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;

BEGIN {Part10}
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - - b
   END;
   x := 11;
   y := 20 / 7 + 3.14;
   { writeln('a = ', a); }
   { writeln('b = ', b); }
   { writeln('c = ', c); }
   { writeln('number = ', number); }
   { writeln('x = ', x); }
   { writeln('y = ', y); }
END.  {Part10}
"""

def main():
   lexer = Lexer(program=program)
   while a := lexer.get_next_token():
      if a.type == Token.EOF:
         break
      print(a.value)
   # parser = Parser(lexer=lexer)
   # interpreter = Interpreter(parser=parser)
   # ast = interpreter.interpret()
   # print(ast)
   # print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
   main()