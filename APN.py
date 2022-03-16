import json
import time


test_res = []
media = []


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

    def leTransicoes(self, num, data):
        for i in range(0, num):
            transicoes = data["quintuplas"][i].split()
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

        # if(aceita):
        #     print('S')
        # else:
        #     print('N')


def lerData():
    fData = open('data.json')
    data = json.load(fData)
    fData.close()
    return data

# adapatada para testes de performace


def testaAPN(P):
    i = 0
    for palavras in P.palavrasTeste:
        inicio = time.time()
        P.consomePilhaTransicoes(palavras, P.estadoInicial)
        fim = time.time()
        if(len(test_res) != len(P.palavrasTeste)):
            test_res.append(fim-inicio)
        else:
            test_res[i] = test_res[i]+(fim-inicio)
        i = 1+i


def criaAPN():
    data = lerData()

    P = APN()
    P.estados = data["estados"]
    P.simbolos = data["simbolos"]
    P.alfabetoPilha = data["alfabetoPilha"]
    numeroTransicoes = int(data["numTransicoes"])
    P.leTransicoes(numeroTransicoes, data)
    P.estadoInicial = data["estadoInicial"]
    P.estadosFinais = data["estadosFinais"].split()
    P.palavrasTeste = data["palavrasTeste"].split()

    return P


novoAPN = criaAPN()

for t in range(10000):
    testaAPN(novoAPN)

for res in test_res:
    media.append(res/1000)

print(media)
