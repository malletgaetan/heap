from unary_ast_lib import Lexer, Parser, Interpreter

def main():
   while True:
      try:
         text = input("calc> ")
      except EOFError:
         break
      if not text:
         continue
      lexer = Lexer(calculus=text)
      parser = Parser(lexer=lexer)
      # ast= parser.parse()
      interpreter = Interpreter(parser=parser)
      print(interpreter.interpret())
	
if __name__ == "__main__":
	main()