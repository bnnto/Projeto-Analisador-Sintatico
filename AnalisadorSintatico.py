class AnalisadorSintatico:

    # funcoes para comecar analise e consumir token
    def __init__(self, tokens):
        self.indice = 0
        self.tokens = tokens
        self.token_atual = self.tokens[self.indice] if self.tokens else None
 
    def iniciar_analise(self):
        self.analisar_programa()
        if self.token_atual is not None:
            raise SyntaxError(f"A entrada nao foi correta. Sobrou: {self.token_atual}")
        
    def consumir_token(self, token_expectado):
        print(f"Esperando: {token_expectado}, atual: {self.token_atual}")
        if self.token_atual == token_expectado:
            self.indice += 1
            self.token_atual = self.tokens[self.indice] if self.indice < len(
                self.tokens) else None
            print(f"O token foi consumido. Proximo token: {self.token_atual}")
        else:
            raise SyntaxError(f"Esperado {token_expectado}, encontrado {self.token_atual}")

    # programa (1)
    def analisar_programa(self):
        while self.token_atual is not None:
            self.analisar_declaracao()

    # declaracao (2)
    # comentarios (7)
    # arrays (11) id [expressao]
    def analisar_declaracao(self):
        print(f"Token atual: {self.token_atual}")
        if self.token_atual in {'int', 'float', 'double', 'char', 'boolean'}:
            tipo = self.token_atual
            print(f"Tipo detectado: {tipo}")
            self.consumir_token(tipo)
            print(f"Token depois consumir tipo: {self.token_atual}")
            if self.token_atual == 'ID':
                self.consumir_token('ID')
                if self.token_atual == '(':
                    self.declaracao_funcao()
                elif self.token_atual == ';' or (self.token_atual and self.token_atual[0] == '='):
                    self.declaracao_variavel()
                elif self.token_atual == '[':
                    self.consumir_token('[')
                    if self.token_atual == ']':
                        self.consumir_token(']')
                        self.declaracao_variavel()
                    else:
                        self.expressao()
                        self.consumir_token(']')
                        self.declaracao_variavel()
                else:
                    raise SyntaxError("A declaracao esta invalida")
        elif self.token_atual == 'struct':
            self.declaracao_estrutura()
        elif self.token_atual == '//':
            self.consumir_token('//')
            while self.token_atual and self.token_atual != 'NEWLINE':
                self.consumir_token(self.token_atual)
            self.consumir_token('NEWLINE')
        elif self.token_atual == '/*':
            self.consumir_token('/*')
            while self.token_atual and self.token_atual != '*/':
                self.consumir_token(self.token_atual)
            self.consumir_token('*/')
        elif self.token_atual in {'if', 'while', 'for', 'switch', 'break', 'continue', 'return'}:
            self.estrutura_controle()
        elif self.token_atual == 'ID':
            self.atribuicao()
            if self.token_atual != ';':
                raise SyntaxError("Esperado ';' após expressão")
            self.consumir_token(';')
        else:
            raise SyntaxError("A declaracao esta invalida")
        
    # declaracao variavel (3)
    def declaracao_variavel(self):
        print(f"Token atual: {self.token_atual}")
        if self.token_atual == '=':
            self.consumir_token('=')
            print(f"Token depois de  consumir '=': {self.token_atual}")
            if self.token_atual == '{':
                self.array_inicializacao()
            else:
                self.expressao()
            print(f"Token depois de  expressao: {self.token_atual}")
        self.consumir_token(';')
        print(f"Token depois de consumir ';': {self.token_atual}")

    # declaracao funcao (4)
    def declaracao_funcao(self):
        self.consumir_token('(')
        if self.token_atual != ')':
            self.parametros()
        self.consumir_token(')')
        self.bloco()

    # parametro (5) - parametro .. parametro, parametro
    def parametros(self):
        self.parametro()
        while self.token_atual == ',':
            self.consumir_token(',')
            self.parametro()

    # parametro (5) - tipo id..
    def parametro(self):
        if self.token_atual in {'int', 'float', 'double', 'char', 'boolean'}:
            self.consumir_token(self.token_atual)
            if self.token_atual == '...':
                self.consumir_token('...')
            self.consumir_token('ID')
            if self.token_atual == '[':
                self.consumir_token('[')
                self.consumir_token(']')
        else:
            raise SyntaxError("O parametro esta invalido")

    # bloco (6)
    def bloco(self):
        self.consumir_token('{')
        while self.token_atual and self.token_atual != '}':
            self.analisar_declaracao()
        self.consumir_token('}')

    # expressao (8)
    def expressao(self):
        print(f"Token atual: {self.token_atual}")
        self.atribuicao()
        print(f"Token depois de atribuicao: {self.token_atual}")

    # expressao (8) - atribuicoes
    def atribuicao(self):
        if self.token_atual == 'ID':
            self.consumir_token('ID')
            
            while self.token_atual == '[':
                self.consumir_token('[')
                self.expressao()
                self.consumir_token(']')
            
            if self.token_atual in {'=', '+=', '-=', '*=', '/=', '%=', '&&=', '||='}:
                self.consumir_token(self.token_atual)
                self.expressao()
            else:
                self.possivel_expressao_relacional_ou_nada()
        else:
            self.expressao_logica()

    # expressao (8) - atribuicoes - funcao pra ajudar atribuicoes
    def possivel_expressao_relacional_ou_nada(self):
        while self.token_atual in {'==', '!=', '>', '<', '>=', '<='}:
            self.consumir_token(self.token_atual)
            self.expressao_aritmetica()

    # estruturas de controle (9)
    def estrutura_controle(self):
        if self.token_atual == 'if':
            self.consumir_token('if')
            self.consumir_token('(')
            self.expressao()
            self.consumir_token(')')
            self.bloco()
            if self.token_atual == 'else':
                self.consumir_token('else')
                self.bloco()
        elif self.token_atual == 'while':
            self.consumir_token('while')
            self.consumir_token('(')
            self.expressao()
            self.consumir_token(')')
            self.bloco()
        elif self.token_atual == 'for':
            self.consumir_token('for')
            self.consumir_token('(')
            self.expressao()
            self.consumir_token(';')
            self.expressao()
            self.consumir_token(';')
            self.expressao()
            self.consumir_token(')')
            self.bloco()
        elif self.token_atual == 'switch':
            self.consumir_token('switch')
            self.consumir_token('(')
            self.expressao()
            self.consumir_token(')')
            self.case_lista()
        elif self.token_atual == 'break':
            self.consumir_token('break')
            self.consumir_token(';')
        elif self.token_atual == 'continue':
            self.consumir_token('continue')
            self.consumir_token(';')
        elif self.token_atual == 'return':
            self.consumir_token('return')
            self.expressao()
            self.consumir_token(';')

    # estruturas de controle (9) case lista
    def case_lista(self):
        while self.token_atual in {'case', 'default'}:
            self.case_decl()

    # estruturas de controle (9) case decl
    def case_decl(self):
        if self.token_atual == 'case':
            self.consumir_token('case')
            self.expressao()
            self.consumir_token(':')
            self.bloco()
        elif self.token_atual == 'default':
            self.consumir_token('default')
            self.consumir_token(':')
            self.bloco()

    # declaracao de estruturas (10) 
    def declaracao_estrutura(self):
        self.consumir_token('struct')
        self.consumir_token('ID')
        self.consumir_token('{')
        
        while self.token_atual in {'int', 'float', 'double', 'char', 'boolean'}:
            self.consumir_token(self.token_atual) 
            self.consumir_token('ID')  
            self.consumir_token(';')  
        self.consumir_token('}')
        self.consumir_token(';')
    
    # array (11) array incializacao
    def array_inicializacao(self):
        self.consumir_token('{')
        if self.token_atual != '}':
            self.expressao()
            while self.token_atual == ',':
                self.consumir_token(',')
                self.expressao()
        self.consumir_token('}')

    # expressoes (12) logica
    def expressao_logica(self):
        self.expressao_relacional()
        while self.token_atual and self.token_atual in {'&&', '||'}:
            self.consumir_token(self.token_atual)
            self.expressao_relacional()

    # expressoes (12) relacional
    def expressao_relacional(self):
        self.expressao_aritmetica()
        if self.token_atual in {'>', '>=', '<', '<=', '!=', '=='}:
            self.consumir_token(self.token_atual)
            self.expressao_aritmetica()

    # expressoes (12) aritmetica
    def expressao_aritmetica(self):
        self.expressao_multiplicativa()
        while self.token_atual and self.token_atual in {'+', '-'}:
            self.consumir_token(self.token_atual)
            self.expressao_multiplicativa()
    
    # expressoes (12) mutiplicativa
    def expressao_multiplicativa(self):
        self.expressao_unaria()
        while self.token_atual and self.token_atual in {'*', '/', '%'}:
            self.consumir_token(self.token_atual)
            self.expressao_unaria()

    # expressoes (12) unaria
    def expressao_unaria(self):
        if self.token_atual in {'-', '++', '--', '!'}:
            self.consumir_token(self.token_atual)
        self.expressao_postfix()

    # expressoes (12) postfix
    def expressao_postfix(self):
        self.primaria()
        while self.token_atual and self.token_atual in {'[', '(', '.', '->'}:
            if self.token_atual == '[':
                self.consumir_token('[')
                self.expressao()
                self.consumir_token(']')
            elif self.token_atual == '(':
                self.consumir_token('(')
                if self.token_atual != ')':
                    self.argumentos()
                self.consumir_token(')')
            elif self.token_atual == '.':
                self.consumir_token('.')
                self.consumir_token('ID')
            elif self.token_atual == '->':
                self.consumir_token('->')
                self.consumir_token('ID')

    # expressoes (12) argumentos
    def argumentos(self):
        self.expressao()
        while self.token_atual and self.token_atual == ',':
            self.consumir_token(',')
            self.expressao()

    # expressoes (12) primaria
    def primaria(self):
        if self.token_atual in {'ID', 'NUM_INT', 'NUM_DEC', 'TEXTO'}:
            self.consumir_token(self.token_atual)
        elif self.token_atual == '(':
            self.consumir_token('(')
            self.expressao()
            self.consumir_token(')')
        else:
            raise SyntaxError("Expressao primaria invalida")