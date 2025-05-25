from AnalisadorSintatico import AnalisadorSintatico

tokens =  ["ID", "=", "NUM_INT", ";"]

AS = AnalisadorSintatico(tokens)

try:
    AS.iniciar_analise()
    print("Analise sintatica concluida com sucesso!")
except SyntaxError as e:
    print(f"SyntaxError: {e}")