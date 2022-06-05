from pascal_lib import Token, Lexer, Parser, Interpreter

program = """
PROGRAM Part10;
VAR
   a, b, c, x : INTEGER;
   number     : INTEGER;
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
   parser = Parser(lexer=lexer)
   interpreter = Interpreter(parser=parser)
   print(interpreter.interpret())

# output = """
# {'A': {'value': 2, 'type': 'INTEGER'}, 'B': {'value': 25, 'type': 'INTEGER'}, 'C': {'value': 27, 'type': 'INTEGER'}, 'X': {'value': 11, 'type': 'INTEGER'}, 'NUMBER': {'value': 2, 'type': 'INTEGER'}, 'Y': {'value': 5.997142857142857, 'type': 'REAL'}} 
# """
# it works!
if __name__ == '__main__':
   main()