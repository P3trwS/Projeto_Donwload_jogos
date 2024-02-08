
#Cod ultra
"""
Este Código faz o download do conteúdo de dentro dos links que estão dentro
do arquivo base_links
"""
#%%
import time
import tkinter as ttk 
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from base_links import forza_horizon_links

def escolhe_jogo(driver:WebDriver):
    driver.get("https://www.elamigos-games.net/")
    mensagem = "ainda nn"
    while mensagem != "ok":
        mensagem = messagebox.showwarning("LEIA COM ATENÇÃO", "CLIQUE EM OK SE JÁ ESCOLHEU O JOGO QUE DESEJA \n APENAS PERMACEÇA NA PÁGINA...")
        if mensagem == "ok":
            print(type(mensagem))
    selected_game = driver.find_element(By.CLASS_NAME,"my-4").text
    messagebox.showinfo("Beleza", f"Voçê selecionou: {selected_game}")

def extrator_links(driver:WebDriver):
    print("Vou entrar resgatar os links do media fire")
    driver.find_element(By.XPATH, "/html/body/div[4]/div[6]/div/a[8]").click()
    time.sleep(2.5)
    cookies = driver.get_cookies()
    print(cookies)

# def download_game(driver:WebDriver):
#     for link in forza_horizon_links:
#         driver.get(link)
#         down = driver.find_element(By.ID, "downloadButton")
#         down.click()
#         print(f"Download do link: {link}\n Iniciado")
#         time.sleep(2)

def seleciona_diretorio(root:Tk):
    root.withdraw()
    download_dir = filedialog.askdirectory()
    if download_dir:
        return download_dir
    else:
        messagebox.showerror("Erro", "Nenhum diretório foi selecionado. Fechando o programa...")
        root.destroy()
        return None

def main():
    root = ttk.Tk()
    download_dir = seleciona_diretorio(root)
    if not download_dir :
        return

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options)
    #driver.maximize_window()
    messagebox.showinfo("Selecione", "Abrindo o site...\n Selecione o jogo que deseja...\n APENAS PERMANEÇA NA PÁGINA DO JOGO...")
    escolhe_jogo(driver)
    extrator_links(driver)
    
#%%
if __name__ == "__main__":
    main()