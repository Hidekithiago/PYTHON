'''| Comando para instalar as bibliotecas do projeto |'''
#pip3 install selenium
import os,sys
'''| Biblioteca do Selenium |'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
'''| Biblioteca para pegar o diretorio das pastas |'''
from pathlib import Path
'''| Biblioteca para adicionar um delay na execucao |'''
import time
'''| Biblioteca pegar a data e hora atual |'''
from datetime import datetime
'''| Configuracao do chrome |'''
dir_download = str(Path.home() / "Downloads") # Pega o diretorio da pasta de Download do usuario no Windows
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {
        "download.default_directory": dir_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
chromeOptions.add_argument('--headless') #Executa o Chrome em modo invisivel
driver = webdriver.Chrome((ChromeDriverManager().install()), options=chromeOptions) #Verifica a versao do chrome instalado e baixa o driver


def downloadGit():
    print('Abrindo a pagina do repositorio')
    driver.get('https://github.com/Hidekithiago/rpaPython')    
    driver.maximize_window() #Maximiza a janela
    time.sleep(1) #Aguarda 1 segundo
    
    driver.find_element(By.XPATH,'/html/body/div[4]/div/main/turbo-frame/div/div/div/div[3]/div[1]/div[1]/span/get-repo/details/summary').click() #Clica no botao "Code"    
    driver.find_element(By.XPATH,'//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/div[1]/span/get-repo/details/div/div/div[1]/ul/li[3]/a').click() #Clica no botao "Download ZIP"
    
if __name__ == "__main__": #Inicio do programa
    print("Inicio do programa")
    inicio = datetime.now()
    downloadGit()
    
    fim = datetime.now()
    print('\n\nTempo de execucao do programa: %s'%(fim-inicio))
    