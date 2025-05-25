from AnalisadorSintatico import AnalisadorSintatico

tokens = [
    "switch", "(", "ID", ")", "{",
    "default", ":", "{",
    "return", ";",
    "}",
    "}"
]

AS = AnalisadorSintatico(tokens)

try:
    AS.iniciar_analise()
    print("Analise sintatica concluida com sucesso!")
except SyntaxError as e:
    print(f"SyntaxError: {e}")