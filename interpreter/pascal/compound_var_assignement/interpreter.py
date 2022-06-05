from pascal_lib import Lexer, Parser, Interpreter

program = """
BEGIN
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number div 4;
      c := a - - b
   END;
   x := 11;
END.
"""

def main():
   lexer = Lexer(program=program)
   parser = Parser(lexer=lexer)
   interpreter = Interpreter(parser=parser)
   ast = interpreter.interpret()
   print(ast)
   print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
   main()