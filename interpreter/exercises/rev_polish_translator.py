from arithmetic_ast_lib import Token, Lexer, Parser, ASTNum, ASTOp

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
      print(parser.parse())
	
if __name__ == "__main__":
	main()
