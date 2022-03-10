class AFN:
    # Função construtora da classe AFN
    def __init__(self):
        self.estados = []
        self.simbolos = []
        self.alfabetoPilha = []
        self.mapa = dict()
        self.palavras = []
        self.estadosFinais = []
        self.estadoInicial = str
        self.pilha = []

    # Cria um dicionário (mapa em python) para armazenar as transições do AFN
    def preencheDic(self):
        #recebe o número de transições
        num_transicoes = int(input())

        for i in range (0, num_transicoes):
            transicoes = input().split()
            trans = transicoes[0]+transicoes[1]
            if(trans in self.mapa):
                self.mapa[trans] = self.mapa[trans] + [transicoes[2]] 
            else:
                novaTransicao = {transicoes[0]+transicoes[1]:[transicoes[2]]}
                self.mapa.update(novaTransicao)

    # Percorre a palavra a partir do seu estado inicial
    def lePalavra(self, palavra, estadoInicial):
        self.pilha = [estadoInicial]
        for char in palavra:
            novaPilha = []
            for estado in self.pilha:
                if ((estado + char) in self.mapa):
                    proximoEstado = self.mapa.get(estado+char)
                else:
                    proximoEstado = False

                if(proximoEstado):
                    for estado in proximoEstado:
                        novaPilha.append(estado)
            self.pilha = novaPilha
        
        self.aceitaPalavra()
    
    # Escreve 'S' se a palavra for aceita e 'N' se a apalvra não for aceita pelo AFN
    def aceitaPalavra(self):
        ehAceita = False
        for estado in self.pilha:
            if(estado in self.estadosFinais):
                ehAceita = True
                break
    
        if(ehAceita):
            print('S')
        else:
            print('N')

# Testa as palavras presentes no array palavras
def testaPalavra(L):
    for palavra in L.palavras:
        L.lePalavra(palavra, L.estadoInicial)

# Cria um novo objeto da classe linguagem e preenche seus atributos com parâmetros definitos pelo usuário
def criaAFN():

    L = AFN()

    L.estados = input()
    L.simbolos = input()
    L.preencheDic()
    L.estadoInicial = input()
    L.estadosFinais = input().split()
    L.palavras = input().split()
    return L

novaL = criaAFN()
testaPalavra(novaL)

