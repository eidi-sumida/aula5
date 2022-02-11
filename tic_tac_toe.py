# -*- coding: utf-8 -*-
import os
import time
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # NÃO PRINTAR A VERSÃO DE PYGAME
import pygame

# CLASSE PARA TABULEIRO
class Tab:
    def __init__(self):
        # MICROTABULEIRO:
        # 0 <- VAZIO | 1 <- 'X' | -1  <- 'O'
        # MACROTABULEIRO
        # 0 <- EM JOGO | 1 <- 'X' É VENCEDOR | -1 <- 'O' É VENCEDOR | 6 <- EMPATE
        self.pos = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
        # 1 SE O TABULEIRO AINDA ESTIVER VÁLIDO
        # 0 SE O TABULEIRO ESTIVER FINALIZADO (HOUVE VENCEDOR / EMPATE)
        self.status = 1
        # CONTAGEM DA QUANTIDADE DE JOGADAS NO TABULEIRO
        self.contagem = 0

    def adiciona(self, linha, coluna, jogador):
        self.pos[linha][coluna] = jogador
        self.contagem += 1

    def preencheVencedor(self, jogador, tabNum, interface):
        for linha in range(3):
            for coluna in range(3):
                self.pos[linha][coluna] = jogador
        if jogador == 1:
            pygame.draw.rect(interface.tela, (0, 0, 0), ( 2 + (tabNum % 3) * 270, 2 + (int)(tabNum / 3) * 270, 265, 265))
            pygame.draw.line(interface.tela, (255, 0, 127), (20 + (tabNum % 3) * 270, 20 + (int)(tabNum / 3) * 270), ((tabNum % 3) * 270 + 250, (int)(tabNum / 3) * 270 + 250), 15)
            pygame.draw.line(interface.tela, (255, 0, 127), ((tabNum % 3) * 270 + 250, (int)(tabNum / 3) * 270 + 20), ((tabNum % 3) * 270 + 20, (int)(tabNum / 3) * 270 + 250), 15)
        else:
            pygame.draw.rect(interface.tela, (0, 0, 0), ( 2 + (tabNum % 3) * 270, 2 + (int)(tabNum / 3) * 270, 265, 265))
            pygame.draw.circle(interface.tela, (255, 204, 229), ( 135 + (tabNum % 3) * 270, 135 + (int)(tabNum / 3) * 270), 120, 15)

    def consultaStatus(self):
        # SE O JOGO ESTIVER EM JOGO RETORNA 1
        if self.status == 1:
          return 1
        else:
          return 0

    def consultaPosicao(self, linha, coluna):
        # SE A POSICAO NAO ESTIVER COM NENHUMA JOGADA RETORNA 1
        if self.pos[linha][coluna] == 0:
            return 1
        else:
            return 0

    def analisaTab(self): # ANALISA A SITUAÇÃO DO TABULEIRO
        analisa = self.somaLinColDiag()
        # VERIFICA SE HOUVE VENCEDOR NAS LINHAS, COLUNAS E DIAGONAIS
        for k in range(8):
            if analisa[k] == 3: # VENCEDOR: X
                self.status = 0
                return 1
            elif analisa[k] == -3: # VENCEDOR: O
                self.status = 0
                return -1
        if self.contagem == 9: # VERIFICA SE O TABULEIRO DEU VELHA (EMPATOU)
            return 6
        return 0

    def somaLinColDiag(self):
        somas = []
        # COLOCA NA LISTA 'analisa' A SOMA DE CADA LINHA E COLUNA
        for i in range(3):
            linha = 0
            coluna = 0
            for j in range(3):
                linha += self.pos[i][j]
                coluna += self.pos[j][i]
            somas.append(linha)
            somas.append(coluna)
        # COLOCA NA LISTA 'analisa' A SOMA NAS DUAS DIAGONAIS
        d1 = self.pos[0][0] + self.pos[1][1] + self.pos[2][2]
        somas.append(d1)
        d2 = self.pos[2][0] + self.pos[1][1] + self.pos[0][2]
        somas.append(d2)
        return somas

class InterfacePygame():
    def __init__(self):
        pygame.init()       # INICIALIZAR TODOS OS MÓDULSO IMPORTADOS DO PYGAME
        self.tela = pygame.display.set_mode([810, 810])     # TAMANHO DA LARGURA E ALTURA DA INTERFACE
        pygame.display.set_caption("Tic Tac Toe")       # DESCRIÇÃO DA JANELA
        self.tela.fill([0, 0, 0])       # PREENCHER O FUNDO DE COR PRETO
        for i in range(8):
            if i % 3 == 2 or i % 3 == -2:
                pygame.draw.line(self.tela, (255, 204, 229), (0, 90 * (i+1)), (800, 90 * (i+1)), 1)     # LINHAS HORIZONTAIS QUE SEPARAM OS MICROTABULEIROS
                pygame.draw.line(self.tela, (255, 204, 229), (90 * (i+1), 0), (90 * (i+1), 800), 1)     # LINHAS VERTICAIS QUE SEPARAM OS MICROTABULEIROS
            else:
                pygame.draw.line(self.tela, (255, 0, 127), (0, 90 * (i+1)), (800, 90 * (i+1)), 1)       # LINHAS HORIZONTAIS QUE SEPARAM LINHA E COLUNA DE CADA MICROTABULEIRO
                pygame.draw.line(self.tela, (255, 0, 127), (90 * (i+1), 0), (90 * (i+1), 800), 1)       # LINHAS VERTICAIS QUE SEPARAM LINHA E COLUNA DE CADA MICROTABULEIRO

    def marcaJogada_1(self, coluna, linha, tabNum):     # MARCAR 'X' NA INTERFACE GRÁFICA ONDE A JOGADA FORA FEITA, ATRAVÉS DE DUAS LNHAS DIAGONAIS
        pygame.draw.line(self.tela, (255, 0, 127), ((coluna*2 + 1) * 45 + (tabNum % 3) * 270 - 20, (1 + 2*linha) * 45 + (int)(tabNum / 3) * 270 - 20), ((coluna*2 + 1) * 45 + (tabNum % 3) * 270 + 20, (1 + 2*linha) * 45 + (int)(tabNum / 3) * 270 + 20), 10)
        pygame.draw.line(self.tela, (255, 0, 127), ((coluna*2 + 1) * 45 + (tabNum % 3) * 270 + 20, (1 + 2*linha) * 45 + (int)(tabNum / 3) * 270 - 20), ((coluna*2 + 1) * 45 + (tabNum % 3) * 270 - 20, (1 + 2*linha) * 45 + (int)(tabNum / 3) * 270 + 20), 10)

    def marcaJogada_2(self, coluna, linha, tabNum):     # MARCAR 'O' NA INTERFACE GRÁFICA ONDE A JOGADA FORA FEITA
        pygame.draw.circle(self.tela, (255, 204, 229), ((coluna*2 + 1) * 45 + (tabNum % 3) * 270, (1 + 2*linha) * 45 + (int)(tabNum / 3) * 270), 30, 10)

    def printaVencedor_ou_Empate(self, resultado):      # MÉTODO QUE MOSTRARÁ A MENSAGEM DO VENCEDOR OU EMPATE NA INTERFACE GRÁFICA
        pygame.draw.rect(self.tela, (255, 255, 255), (110, 390, 590, 100))  # DESENHAR UM RETÂNGULO BRANCO ONDE SERÁ MOSTRADO O TEXTO ACIMA
        fonte = pygame.font.SysFont("Arial", 50)        # DEFINIR A FONTE E O TAMANHO
        if resultado == 1:      # DE ACORDO COM O RESULTADO, RENDERIZAR O TEXTO COM A COR ESPECIFICADA (PRETO)
            texto = fonte.render("O JOGADOR 1 VENCEU!", 1, (0, 0, 0))
        elif resultado == -1:
            texto = fonte.render("O JOGADOR 2 VENCEU!", 1, (0, 0, 0))
        else:
            texto = fonte.render("O JOGO DEU EMPATE!", 1, (0, 0, 0))
        self.tela.blit(texto, (120, 405))       # MOSTRAR O TEXTO NA TELA, NAS POSIÇÕES X E Y INDICADAS
        # COMO O JOGO TERMINOU, ESSE MÉTODO BLOQUEIA ENTRADAS DE TECLAS DO USUÁRIO E DO CLIQUE DO MOUSE, SENOD NECESSÁRIO ENCERRAR A INTERFACE E O JOGO ATRAVÉS DO CLIQUE NO 'X' DA JANELA.
        pygame.event.set_blocked([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])

    def retornaJogadaMouse(self, posX, posY):
         # MÉTODO QUE RETORNA O NÚMERO DO MICROTABULEIRO, LINHA E COLUNA ONDE FORA CLICADA NA INTERFACE, A PARTIR DO PONTO X E Y
        tabColuna = (int)(posX / 270)
        tabLinha = (int)(posY / 270)
        tabNum = tabLinha * 3 + tabColuna + 1
        coluna = (int)((posX - tabColuna * 270) / 90)
        linha = (int)((posY - tabLinha * 270) / 90)
        return tabNum, linha, coluna

class Jogador:
    def __init__(self, tipo, jogadorNum):
        # '1' -> HUMANO ; '2' -> ESTABANADO ; '3' -> COME-CRÚ
        self.tipo = tipo
        # '1' -> JOGADOR 1 ; '2' -> JOGADOR 2
        self.jogadorNum = jogadorNum

class Humano(Jogador):
    # HERDA CLASSE JOGADOR, SUAS JOGADAS SÃO LIDAS ATRAVÉS DO MOUSE NA INTERFACE DE PYGAME
    pass

class Estabanado(Jogador):
    def turno(self, microtab):
        while True:
            tabNum = random.randint(0, 8)   #SORTEIA UM INTEIRO DE 0 A 8
            linha = random.randint(0, 2)    #SORTEIA UM INTEIRO DE 0 A 2
            coluna = random.randint(0, 2)   #SORTEIA UM INTEIRO DE 0 A 2
            if microtab[tabNum].consultaPosicao(linha, coluna) == 1:       # VERIFICA SE ESSA POSIÇÃO NÃO ESTÁ SENDO OCUPADO
                print("\n\t\t------- Vez do Jogador {} -------".format(self.jogadorNum))
                print("\tJOGADA ESTABANADA: Microtabuleiro {} >> Linha {} >> Coluna {}.".format(tabNum+1, linha+1, coluna+1))
                break
        return tabNum, linha, coluna    # CASO A POSIÇÃO ESTIVER LIVRE, RETORNA

class Comecru(Jogador):
    def turno(self, microtab):
        for tabNum in range(9):
            for linha in range(3):
                for coluna in range(3):
                    # VERIFICA DA PRIMEIRA POSIÇÃO DO PRIMEIRO MICROTABULEIRO ATÉ A ÚLTIMA POSIÇÃO DO ÚLTIMO MICROTABULEIRO
                    if microtab[tabNum].consultaPosicao(linha, coluna) == 1:
                        print("\n\t\t------- Vez do Jogador {} -------".format(self.jogadorNum))
                        print("\tJOGADA COME-CRU: Microtabuleiro {} >> Linha {} >> Coluna {}.".format(tabNum+1, linha+1, coluna+1))
                        return tabNum, linha, coluna     # CASO A POSIÇÃO ESTIVER LIVRE, RETORNA

class Jogo:
    def __init__(self, tipo, macrotab, microtab, jogador1, jogador2, converte):
        self.macrotab = macrotab
        self.microtab = microtab
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.converte = converte            # LISTA QUE CONVERTE O NÚMERO DO MICROTABULEIRO PARA A SUA POSIÇÃO REFERENTE NO MACROTABULEIRO
        self.tipo = tipo                    # TIPO DE JOGO
        self.vez = -1   # VEZ DO JOGADOR: '1' -> JOGADOR 1 ; '2' -> JOGADOR 2
        self.partidaEmAndamento = True      # VARIÁVEL QUE INDICA SE A PARTIDA AINDA ESTÁ EM ANDAMENTO
        self.interface = InterfacePygame()  # INSTANCIA O OBJETO InterfacePygame PARA CRIAR A INTERFACE GRAFICA DO PYGAME

    def decideVez(self):
        if self.tipo == 1:      # SE O JOGO FOR NORMAL, SERÁ NECESSÁRIO APENAS TROCAR DE '1' PARA '-1'
            self.vez *= -1
        elif self.tipo == 2:    # SE O JOGO FOR DE TURNO RANDOMICO, SERÁ SEMPRE SORTEADO ENTRE -1 E 1
            self.vez = random.choice([-1, 1])

class NormalTicTacToe(Jogo):
    def iniciarPartida(self):
        self.decideVez()
        while self.partidaEmAndamento:      # LOOP PARA VERIFICAR EVENTOS NA INTERFACE GRÁFICA
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # EVENTO PARA QUANDO O USUÁRIO FECHAR A INTERFACE
                    self.partidaEmAndamento = False
                if event.type == pygame.KEYDOWN:    # EVENTO PARA DETECTAR TECLA DE USUÁRIO E EXECUTAR AS JOGADAS DO JOGADOR ESTABANADO E COME-CRÚ
                    if (self.vez == 1 and (self.jogador1.tipo == 2 or self.jogador1.tipo == 3)) or (self.vez == -1 and (self.jogador2.tipo == 2 or self.jogador2.tipo == 3)):
                        retorno = self.vez_Jogador_Estabanado_Comecru()
                        if retorno != 0:    # SE O RETORNO != 0, SIGNIFICA QUE HOUVE VENCEDOR OU EMPATE NO MACROTABULEIRO
                            self.partidaEmAndamento = False
                        self.decideVez()    # ALTERNA A VEZ DE ACORDO COM O TIPO DE JOGADO
                if event.type == pygame.MOUSEBUTTONDOWN and ((self.vez == 1 and self.jogador1.tipo == 1) or (self.vez == -1 and self.jogador2.tipo == 1)):   # EVENTO PARA DETECTAR CLIQUE DE MOUSE DE USUÁRIO E EXECUTAR AS JOGADAS DO JOGADOR HUMANO
                    # RETORNA O NÚMERO DO MICROTABULEIRO, LINHA E COLUNA REFERENTE DE ACORDO COM A POSIÇÃO X E Y DA INTERFACE ONDE FOI CLICADO
                    tabNum, linha, coluna = self.interface.retornaJogadaMouse(event.pos[0], event.pos[1])
                    if self.consultaTab(tabNum-1, linha, coluna) == 1:  # VERIFICA SE A SEGUINTE POSIÇÃO ESTÁ DISPONÍVEL
                        retorno = self.vez_Jogador_Humano(coluna, linha, tabNum - 1)    # MARCA A JOGADA DO JOGADOR HUMANO NA INTERFACE
                        self.decideVez()
                        if retorno != 0:    # SE O RETORNO != 0, SIGNIFICA QUE HOUVE VENCEDOR OU EMPATE NO MACROTABULEIRO
                            self.interface.printaVencedor_ou_Empate(retorno)    # MÉTODO QUE PRINTA O ANÚNCIO DE VENCEDOR OU EMPATE NA INTERFACE
                            partidaEmAndamento = False
            pygame.display.update()
        return retorno

    def vez_Jogador_Humano(self, coluna, linha, tabNum):
        if self.vez == 1 and self.jogador1.tipo == 1:   # CHAMA A FUNÇÃO PARA MARCAR A JOGADA NA INTERFACE GRÁFICA DE ACORDO COM A VEZ E TIPO DE JOGADOR
            self.interface.marcaJogada_1(coluna, linha, tabNum)
        elif self.vez == -1 and self.jogador2.tipo == 1:
            self.interface.marcaJogada_2(coluna, linha, tabNum)
        return self.addJogada_e_Verifica(tabNum, linha, coluna)

    def vez_Jogador_Estabanado_Comecru(self):
        tabNum, linha, coluna = self.coletaTurnoDoJogador()
        if self.vez == 1:    # CHAMA A FUNÇÃO PARA MARCAR A JOGADA NA INTERFACE GRÁFICA DE ACORDO COM A VEZ
            self.interface.marcaJogada_1(coluna, linha, tabNum)
        else:
            self.interface.marcaJogada_2(coluna, linha, tabNum)
        return self.addJogada_e_Verifica(tabNum, linha, coluna)

    def addJogada_e_Verifica(self, tabNum, linha, coluna):
        self.microtab[tabNum].adiciona(linha, coluna, self.vez)     # ADICIONA A JOGADA NO MICROTABULEIRO
        retornoMic = self.microtab[tabNum].analisaTab()     # VERIFICA SE HOUVE VENCEDOR OU EMPATE APÓS A JOGADA
        if retornoMic == 1 or retornoMic == -1 or retornoMic == 6:      # PASSARÁ POR ESSA CONDIÇÃO SE HOUVER VENCEDOR OU EMPATE
            self.printVencedor_ou_Empate(tabNum, retornoMic)
            if __name__ == '__main__':
                time.sleep(0.5)
            # MARCAR A VITORIA OU EMPATE NO MACROTABULEIRO
            self.macrotab.adiciona(self.converte[tabNum][0], self.converte[tabNum][1], retornoMic)
            # VERIFICAR A SITUAÇÃO DE JOGO DO MACROTABULEIRO E RETORNAR SE HOUVE VENCEDOR OU EMPATE
            return self.macrotab.analisaTab()
        return 0

    def printVencedor_ou_Empate(self, tabNum, retorno):      #  PRINTA O VENCEDOR OU EMPATE DO MICROTABULEIRO, ALÉM DE PREENCHER O MICROTABULEIRO COM A JOGADA DO VENCEDOR
        if retorno == 1:
            print("\n\tO JOGADOR 1 GANHOU NO TABULEIRO {}".format(tabNum+1))
            self.microtab[tabNum].preencheVencedor(self.vez, tabNum, self.interface)
        elif retorno == -1:
            print("\n\tO JOGADOR 2 GANHOU NO TABULEIRO {}".format(tabNum+1))
            self.microtab[tabNum].preencheVencedor(self.vez, tabNum, self.interface)
        elif retorno == 6:
            print("\n\tOCORREU VELHA NO TABULEIRO {}".format(tabNum+1))

    def consultaTab(self, tabNum, linha, coluna):   # RETORNA SE O MICROTABULEIRO E A SUA POSIÇÃO ESTÁ DISPONÍVEL PARA SER JOGADO
        if self.microtab[tabNum].consultaStatus() == 0:     # CONSULTA O STATUS GERAL DO MICROTABULEIRO
            print("\n\tTABULEIRO COM JOGO TERMINADO, ESCOLHA OUTRO")
            return 0
        elif self.microtab[tabNum].consultaPosicao(linha, coluna) == 1:     # CONSULTA UMA POSIÇÃO ESPECÍFICA DO MICROTABULEIRO
            return 1
        else:
            print("\n\tESPAÇO ESCOLHIDO JÁ FOI OCUPADO, DIGITE OUTRA JOGADA.")
            return -1

    def coletaTurnoDoJogador(self):
        if self.vez == 1:
            return self.jogador1.turno(self.microtab)   # CHAMA O MÉTODO DO OBJETO JOGADOR PARA COLETAR O TURNO
        else:
            return self.jogador2.turno(self.microtab)

class RandomTicTacToe(NormalTicTacToe):
     # ESSA CLASSE SE REFERE AO TIPO DE JOGO RANDOM, HERDA TODOS OS MÉTODOS DA CLASSE NormalTicTacToe
    pass

def inicio():
    # CRIANDO OBJETOS DE TABULEIRO
    macrotab = Tab()
    microtab = []
    for i in range(9):
        microtab.append(Tab())  # CRIA 9 OBJETOS DE MICROTABULEIRO
    # LISTA QUE CONVERTE 'tabNum' EM LINHAS E COLUNAS do macrotabuleiro
    converte = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    tipoJogo = inputJogo()      # COLETA O TIPO DE JOGO DESEJADA PELO USUÁRIO
    print("\n\n\tOpções de Tipos de Jogadores:")
    print("\n\tDigite '1' para HUMANO, '2' para ESTABANADO e '3' para COME-CRÚ")
    jogador1 = inputJogador(1)      # COLETA O TIPO DE JOGADOR DESEJADO PELO USUÁRIO
    jogador2 = inputJogador(2)
    Jogo = criaObjetoJogo(tipoJogo, macrotab, microtab, jogador1, jogador2, converte)   # CRIA O OBJETO Jogo, ENVIANDO AS INSTANCIAS COMO ARGUMENTO DE INICIALIZAÇÃO
    pygameInterface = InterfacePygame()     # INSTANCIA OBJETO (INTERFACE GRÁFICA)
    return Jogo.iniciarPartida()    # CHAMA O MÉTODO DO OBJETO Jogo, INICIANDO A PARTIDA E PEGANDO COMO RETORNO O RESULTADO DA PARTIDA

def criaObjetoJogo(tipo, macrotab, microtab, jogador1, jogador2, converte):
    if tipo == 1:
        return NormalTicTacToe(tipo, macrotab, microtab, jogador1, jogador2, converte)
    elif tipo == 2:
        return RandomTicTacToe(tipo, macrotab, microtab, jogador1, jogador2, converte)

def inputJogo():
    print("\n\tOpções de Modos de Jogo:")
    print("\n\tDigite '1' para TRADICIONAL, '2' para RANDOMICO")
    # PEDE INPUT DE TIPO DE JOGO ATÉ QUE USUÁRIO DIGITE UMA ENTRADA VÁLIDA
    while True:
        tipo = (int)(input("\tMODO DE JOGO: "))
        if tipo == 1 or tipo == 2:
            return tipo
        else:
            print("\tMODO DE JOGO INVALIDO, DIGITE NOVAMENTE")
            inputJogo()

def inputJogador(numDoJogador):
    # PEGAR O INPUT DO TIPO DE JOGADOR ATÉ QUE HAJA ENTRADA VÁLIDA
    tipo = (int)(input("\tJogador {}: ".format(numDoJogador)))
    if tipo == 1 or tipo == 2 or tipo == 3:
        return criaObjetoJogador(tipo, numDoJogador)
    else:
        print("\tTIPO DE JOGADOR INVÁLIDO, DIGITE NOVAMENTE")
        inputJogador(numDoJogador)

def criaObjetoJogador(tipo, numDoJogador):
    if tipo == 1:
        return Humano(tipo, numDoJogador)
    elif tipo == 2:
        return Estabanado(tipo, numDoJogador)
    elif tipo == 3:
        return Comecru(tipo, numDoJogador)

def fimDeJogo(resultado):   # ANUNCIA O FIM DE JOGO, INDICANDO O RESULTADO DO JOGO
    print("\n\n\t\t>> FIM DE JOGO <<")
    if resultado == 1:
        print("\n\t\tO JOGADOR 1 VENCEU!")
    elif resultado == -1:
        print("\n\t\tO JOGADOR 2 VENCEU!")
    else:
        print("\n\t\tEMPATE!")
    pygame.quit()

############### INICIA O JOGO ################

def main():
    resultado = inicio()
    fimDeJogo(resultado)

if __name__ == '__main__':
    main()
