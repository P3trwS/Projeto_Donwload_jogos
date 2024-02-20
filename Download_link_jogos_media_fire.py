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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

from base_links import forza_horizon_links


def seleciona_diretorio(root: Tk):
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


def get_page_load_time(driver: WebDriver, url: str) -> float:
    start_time = time.time()
    driver.get(url)
    end_time = time.time()
    return round(end_time - start_time)


def instalando_adblock(driver: WebDriver):

    url = "https://chrome.google.com/webstore/detail/adblock-%E2%80%94-the-best-ad-b/gighmmpiobklfepjocnamgkkbiglidom?hl=pt-br"
    get_page_load_time(driver, url)

    messagebox.showwarning(
        "ATENÇÃO",
        "INSTALE O ADBLOCK PARA QUE O SCRIPT FUNCIONE CORRETAMENTE \n CLIQUE EM OK APENAS SE JÁ INSTALOU...\n NÃO FECHE A PÁGINA",
    )


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

    #print(id_notiene)

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
        driver.find_element(By.ID,"downloadButton").click()
        time.sleep(5)
        
        
    # for download in lista_game[0]:
    #     driver.get(download)
    #     down = driver.find_element(By.ID, "downloadButton")
    #     down.click()
    #     print(f"Download do link: {lista_game}\n Iniciado")
    #     time.sleep(2.5)


def main():
    root = ttk.Tk()
    download_dir = seleciona_diretorio(root)
    if not download_dir:
        return

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("disable-notifications")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options)
    # driver.maximize_window()
    instalando_adblock(driver)
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
