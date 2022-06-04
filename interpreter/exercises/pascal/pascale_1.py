from pascal_lib import Lexer, Parser, Interpreter

program = """
BEGIN
   BEGIN
      a := 200;
      b := a + 100;
      BEGIN END
   END
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