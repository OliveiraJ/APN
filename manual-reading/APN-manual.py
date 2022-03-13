class APN:
    # Função construtora da classe APN
    def __init__(self):
        self.estados = []
        self.simbolos = []
        self.alfabetoPilha = []
        self.mapa = dict()
        self.palavrasTeste = []
        self.estadosFinais = []
        self.pilhaTransicoes = []
        self.estadoInicial = ''

    def criaMapa(self, transicoes):
        tripla = transicoes[0]+transicoes[1]+transicoes[2]
        if(tripla in self.mapa):
            self.mapa[tripla] = self.mapa[tripla] + \
                [[transicoes[3], transicoes[4]]]
        else:
            novaTransicao = {transicoes[0]+transicoes[1] +
                             transicoes[2]: [[transicoes[3], transicoes[4]]]}
            self.mapa.update(novaTransicao)

    def leTransicoes(self, num):
        for i in range(0, num):
            transicoes = input().split()
            self.criaMapa(transicoes)

    def validaTransicoes(self, estadoAtual, palavra, pilha, pilhaTransicoes):
        carConsumido = palavra[0:1]
        simTopoPilha = pilha[0:1]

        if((estadoAtual+carConsumido+simTopoPilha) in self.mapa):
            duplas = self.mapa.get(estadoAtual+carConsumido+simTopoPilha)
            for dupla in duplas:
                pilhaTransicoes.append([dupla[0], self.consomeSim(
                    palavra), self.empilhaSim(self.consomeSim(pilha), dupla[1])])

        if((estadoAtual+'*'+simTopoPilha) in self.mapa):
            duplas = self.mapa.get(estadoAtual+'*'+simTopoPilha)
            for dupla in duplas:
                pilhaTransicoes.append(
                    [dupla[0], palavra, self.empilhaSim(self.consomeSim(pilha), dupla[1])])

        if((estadoAtual+carConsumido+'*') in self.mapa):
            duplas = self.mapa.get(estadoAtual+carConsumido+'*')
            for dupla in duplas:
                pilhaTransicoes.append([dupla[0], self.consomeSim(
                    palavra), self.empilhaSim(pilha, dupla[1])])

        if((estadoAtual+'**') in self.mapa):
            duplas = self.mapa.get(estadoAtual+'**')
            for dupla in duplas:
                pilhaTransicoes.append(
                    [dupla[0], palavra, self.empilhaSim(pilha, dupla[1])])

    def consomeSim(self, string):
        return string[1:len(string)]

    def empilhaSim(self, pilha, string):
        if(string == '*'):
            return pilha
        else:
            return string+pilha

    def ehAceito(self, estado, palavra, pilhaSim):
        if(len(palavra) == 0 and len(pilhaSim) == 0 and estado in self.estadosFinais):
            return True
        else:
            return False

    def consomePilhaTransicoes(self, palavra, estadoInicial):
        self.pilhaTransicoes = [[estadoInicial, palavra, '']]
        aceita = False
        while (not (len(self.pilhaTransicoes) == 0)):
            novaPilhaTransicoes = []

            for pilha in self.pilhaTransicoes:
                self.validaTransicoes(
                    pilha[0], pilha[1], pilha[2], novaPilhaTransicoes)
                if(self.ehAceito(pilha[0], pilha[1], pilha[2])):
                    aceita = True
                    break

            if(aceita):
                break
            self.pilhaTransicoes = novaPilhaTransicoes

        if(aceita):
            print('S')
        else:
            print('N')


def testaAPN(P):
    for palavras in P.palavrasTeste:
        P.consomePilhaTransicoes(palavras, P.estadoInicial)


def criaAPN():
    P = APN()
    P.estados = input()
    P.simbolos = input()
    P.alfabetoPilha = input()
    numeroTransicoes = int(input())
    P.leTransicoes(numeroTransicoes)
    P.estadoInicial = input()
    P.estadosFinais = input().split()
    P.palavrasTeste = input().split()

    return P


novoAPN = criaAPN()
testaAPN(novoAPN)
