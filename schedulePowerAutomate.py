#pip3 install psutil install pyautogui
##############################| IMPORTACAO DE BIBLIOTECAS |##############################

import os, io, sys
import time
import pyautogui
import pygetwindow as gw
import psutil as ps

def startPower(nomeRobo, contaPremium, dirPower):
    premium = 0
    if contaPremium == 'nao': premium = 1 #Adicionar um tab a mais caso a conta nao for premium
    time.sleep(5)
    print('Finalizando o programa PowerAutomate')    
    os.system("taskkill /F /im PAD.Console.Host.exe")
    os.system("taskkill /F /im PAD.Robot.exe")
    #os.system("taskkill /F /im chrome.exe")
    time.sleep(2)
    print('Iniciando o Power Automate')
    os.startfile(dirPower)
    time.sleep(20) #Aguarda o tempo ate carregar o powerAutomate. Pode diminuir/aumentar o tempo dependendo se o computador inicia o processo mais rapido/lento
    
    chroWindow = gw.getWindowsWithTitle('Power Automate')[0] #Instancia na variavel "chroWindow" a janela do Power Automate
    time.sleep(1)
    chroWindow.minimize()
    time.sleep(1)
    chroWindow.maximize()    

    time.sleep(4)
    #Caso não exista a opção "Go Premium" no PowerAutomate, utilizar 11 "TABs", caso contrario utilizar 12 
    for x in range(11+int(premium)): #Percorre o menu do powerAutomate ate chegar na tabela onde fica os robos
        pyautogui.press("tab")
    time.sleep(2)
    for x in range(6): #Percorre todos os robos ate chegar no ultimo
        pyautogui.press("pagedown")
    time.sleep(3)
    for x in range(10+int(premium)): #Percorre o menu ate chegar na opcao para poder buscar um determinado robo
        pyautogui.press("tab")
    time.sleep(2)
    pyautogui.write(nomeRobo) #Digita o nome do robo a ser executado
    for x in range(6): #Percorre o menu do powerAutomate ate chegar na tabela onde fica os robos
        pyautogui.press("tab")
    pyautogui.press("right")
    pyautogui.press("up")
    for x in range(3): #Seleciona o botao de executar o robo
        pyautogui.press("tab")
    pyautogui.press("enter")

    time.sleep(30)
    for proc in ps.process_iter(): #Verifica se o robo esta sendo executado, caso nao esteja executa novamente essa funcao "startPower"
        info = proc.as_dict(attrs=['pid', 'name'])        
        if info['name'] == 'PAD.Robot.exe':            
            sys.exit()
    startPower(nomeRobo, contaPremium, dirPower)

if __name__ == "__main__":
    print('Inicio do Robo')
    #time.sleep(3600) #Tempo definido com o cliente e de 10800(3 horas) 3600(1 Hora) para aguardar antes de executar    
    dirPower = "C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe"  #Diretorio onde esta instalado o powerAutomate
    nomeRobo = "B2P-GerenciadorFAP(fullCNPJ)" #Nome do robo a ser executado
    contaPremium = "sim" #Caso a conta do usuario seja "Licença por usuário" ou "Licença por fluxo" preencher com "sim", caso nao seja preencher com "nao"
    startPower(nomeRobo, contaPremium, dirPower)    
    
