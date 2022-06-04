from pascal_lib import Lexer, Parser

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
   ast = parser.parse()
   print(ast)

if __name__ == '__main__':
   main()