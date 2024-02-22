# Cod ultra
"""
Este Código faz o download do conteúdo de dentro dos links que estão dentro
do arquivo base_links
"""
# %%
import time
import tkinter as ttk
import re
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def seleciona_diretorio_donwload_game(root: Tk):
    root.withdraw()
    download_dir = filedialog.askdirectory()
    if download_dir:
        return download_dir
    else:
        messagebox.showerror(
            "Erro", "Nenhum diretório foi selecionado. Fechando o programa..."
        )
        root.destroy()
        return None

def diretorio_download():
    root = ttk.Tk()
    download_dir = seleciona_diretorio_donwload_game(root)
    if not download_dir:
        return exit()
    return download_dir

def seleciona_arquivo_CRX(root: Tk):
    root.withdraw()
    arquivo_crx = filedialog.askopenfilename(filetypes=[("Arquivos CRX", "*.crx")])
    print(arquivo_crx)
    if arquivo_crx:
        return arquivo_crx
    else:
        messagebox.showerror(
            "Erro", "Nenhum arquivo CRX foi selecionado. Fechando o programa..."
        )
        root.destroy()
        return None

def arquivo_crx():
    root = ttk.Tk()
    file_crx = seleciona_arquivo_CRX(root)
    if not file_crx:
        return exit()
    return file_crx

def navegador(download_dir,file_crx) -> WebDriver:
    chrome_options = Options()
    prefs = {"download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("disable-notifications")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.page_load_strategy = 'normal'
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_extension(f'{file_crx}')
    driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()

    return driver

def escolhe_jogo(driver: WebDriver):
    driver.get("https://www.elamigos-games.net/")
    mensagem = "ainda nn"
    while mensagem != "ok":
        mensagem = messagebox.showwarning(
            "LEIA COM ATENÇÃO",
            "CLIQUE EM OK SE JÁ ESCOLHEU O JOGO QUE DESEJA \n APENAS PERMACEÇA NA PÁGINA...",
        )
        if mensagem == "ok":
            print(type(mensagem))
    selected_game = driver.find_element(By.CLASS_NAME, "my-4").text
    messagebox.showinfo("Beleza", f"Voçê selecionou: {selected_game}")


def extrator_links(driver: WebDriver):

    links_downlaod = []
    link_mediafire = []

    print("Vou entrar resgatar os links do site selecionado...")
    html_da_pagina = driver.page_source

    soup = BeautifulSoup(html_da_pagina, "html.parser")

    id_notiene = soup.find(id="notiene")

    if id_notiene:
        print("Pegando links:...")
        links = id_notiene.find_all("a")
        for link in links:

            links_downlaod.append({"nome": link.text.strip(), "link": link["href"]})

            if re.search(r"\bMEDIAFIRE\b", link.text):
                link_mediafire.append(link["href"])
                print(f"Link MEDIAFIRE:{link_mediafire}\n")

    else:
        print("Elemento com notiene id nsao emcontrado")

    return link_mediafire, links_downlaod


def remover_aspas_simples(link):
    return link.replace("'", "")


def extrator_de_links_game(driver: WebDriver):

    messagebox.showinfo(
        "ATENÇÃO", "Vou selecionar para baixar o jogo pelo MEDIA FIRE..."
    )

    mediafire, outros = extrator_links(driver)

    if mediafire:
        mediafire_link = mediafire[0]
        print("Outros links:", outros)

    driver.get(mediafire_link)

    messagebox.showwarning(
        "Atenção",
        "FAÇA O reCAPTCHA DIREITO E CLIQUE EM OK PARA CONTINUAR\n !!!CLIQUE EM OK DEPOIS DE RESOLVER O RECAPTCHA",
    )

    time.sleep(4)

    lista_game = []

    html_dos_links = driver.page_source

    soup = BeautifulSoup(html_dos_links, "html.parser")

    game_links = soup.find(id="zPaste-links")

    if game_links:

        game = game_links.find_all("a")

        print(game)

        for link in game:
            link_text = link.text
            if link_text not in lista_game:
                lista_game.append(link_text)

    print(lista_game)

    return lista_game

def download_game(driver: WebDriver, lista_game: list):

    partes = lista_game.__len__()

    messagebox.showinfo("Atencao", f"Começarei a fazer o download do jogo...\nNeste jogo temos: {partes} partes\n")

    for media_url in lista_game:
        driver.get(media_url)
        time.sleep(10)
        driver.find_element(By.ID, "downloadButton").click
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "downloadButton"))).click()
        
def main():
    
    diretorio = diretorio_download()
    arquivo_adblock = arquivo_crx()

    driver = navegador(diretorio,arquivo_adblock)

    messagebox.showinfo(
        "Selecione",
        "Abrindo o site...\n Selecione o jogo que deseja...\n APENAS PERMANEÇA NA PÁGINA DO JOGO...",
    )
    escolhe_jogo(driver)
    lista_game = extrator_de_links_game(driver)
    download_game(driver,lista_game)

# %%
if __name__ == "__main__":
    main()

# %%
