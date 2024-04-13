# %%
import time
import tkinter as ttk
import re
import os
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriverC
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import IncompleteRead

def _seleciona_diretorio_donwload_game():

    messagebox.showinfo("Selecionar","Selecione para onde quer que o jogo seja instalado...")

    download_dir = filedialog.askdirectory()
    if download_dir:
        return download_dir
    else:
        messagebox.showerror(
            "Erro", "Nenhum diretório foi selecionado. Fechando o programa..."
        )
        return None

def diretorio_download():
    download_dir = _seleciona_diretorio_donwload_game()
    if not download_dir:
        return exit()
    return download_dir

def _seleciona_arquivo_CRX1():

    diretorio_script = os.path.dirname(os.path.realpath(__file__))
    arquivo_crx1_path = os.path.join(diretorio_script, "AdBlock-—-o-melhor-bloqueador-de-anúncios.crx")
    
    if os.path.exists(arquivo_crx1_path):
        print("Arquivo CRX1 encontrado:", arquivo_crx1_path)
        return arquivo_crx1_path
    else:
        messagebox.showerror(
            "Erro", "O arquivo CRX necessário não foi encontrado. \nVerifique se esta na mesma do arquivo python\nFechando o programa..."
        )
        return None
    
def _seleciona_arquivo_CRX2():

    diretorio_script = os.path.dirname(os.path.realpath(__file__))
    arquivo_crx2_path = os.path.join(diretorio_script, "Bloqueador-de-pop-ups-para-Chrome™-Poper-Blocker.crx")

    if os.path.exists(arquivo_crx2_path):
        print("Arquivo CRX1 encontrado:", arquivo_crx2_path)
        return arquivo_crx2_path
    else:
        messagebox.showerror(
            "Erro", "O arquivo CRX necessário não foi encontrado. \nVerifique se esta na mesma do arquivo python\nFechando o programa..."
        )
        return None

def arquivo_crx():
    file_crx1 = _seleciona_arquivo_CRX1()
    file_crx2 = _seleciona_arquivo_CRX2()
    if not file_crx1 and not file_crx2:
        return exit()
    return file_crx1, file_crx2

def navegador(download_dir,file_crx) -> WebDriver:
    chrome_options = Options()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("disable-notifications")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_extension(f'{file_crx}')
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def navgoogle(file_crx1,file_crx2) -> WebDriverC:
    chrome_options = Options()
    chrome_options.add_extension(f'{file_crx1}')
    chrome_options.add_extension(f'{file_crx2}')
    chrome_options.add_argument('--no-sandbox')
    driver2 = webdriver.Chrome(options=chrome_options)

    return driver2

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

    return selected_game

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
    else:
        print("Elemento com notiene id nsao emcontrado")

    return link_mediafire, links_downlaod


def extrator_de_links_game(driver:WebDriver, file_crx, file_crx2):

    messagebox.showinfo(
        "ATENÇÃO", "Vou selecionar para baixar o jogo pelo MEDIA FIRE..."
    )

    mediafire, outros = extrator_links(driver)

    if mediafire:
        mediafire_link = mediafire[0]
        print("Outros links:", outros)
        
## Atualização para fazer a confirmação atomática do recaptcha

    driver2 = navgoogle(file_crx,file_crx2)
    
    solver = RecaptchaSolver(driver=driver2)
    
    print(mediafire_link)

    driver2.get(mediafire_link)

    time.sleep(6) #tempo para a página carregar completamente

    janela = driver2.window_handles
    driver2.switch_to.window(janela[1])
    driver2.close()
    driver2.switch_to.window(janela[0])

    recaptcha_iframe = driver2.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/main/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div/iframe")

    solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    driver2.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/main/div/div/div[1]/form/div/div/div[3]/div/div/button").click()

    time.sleep(6) #tempo para a página carregar

    driver2.find_element(By.CLASS_NAME,"wrapper").click()

    lista_game = []

    html_dos_links = driver2.page_source

    soup = BeautifulSoup(html_dos_links, "html.parser")

    game_links = soup.find(id="zPaste-links")

    if game_links:

        game = game_links.find_all("a")

        for link in game:
            link_text = link.text
            if link_text not in lista_game:
                lista_game.append(link_text)

    print(lista_game)

    return lista_game

def extrator_links_download_page(driver: WebDriver, lista_game: list):

    game_partes = lista_game.__len__()

    messagebox.showinfo("Atencao", f"Neste jogo temos: {game_partes} partes\n")

    link_button_download_mediafire = []
    
    partes_adquiridas = 0 

    for media_url in lista_game:

        driver.get(media_url)
        
        time.sleep(3)

        html_pagina_mediafire = driver.page_source
        soup = BeautifulSoup(html_pagina_mediafire, "html.parser")

        button_link = soup.find(id="download_link")

        if button_link:
            link_button = button_link.find_all("a", class_="input popsok")

            for link in link_button:
                if link["href"] not in link_button_download_mediafire:
                    link_button_download_mediafire.append(link["href"])

                    partes_adquiridas += 1
                    print(f"Obtendo Links de download: {partes_adquiridas} de {game_partes} partes")

    return link_button_download_mediafire

def download_game(link_download: list, game_selecionado, diretorio):
    
    max_tentativas = 3
    pt = 1

    print("Iniciando downloads")

    for url in link_download:
        tentativas = 0  # Inicializa o contador de tentativas

        while tentativas < max_tentativas:  # Loop enquanto o número de tentativas for menor que o máximo permitido
            try:
                # Fazendo a requisição GET para baixar o arquivo
                response = requests.get(url, stream=True)  # O parâmetro stream=True é necessário para downloads grandes      

                local_filename = os.path.join(diretorio, f"{game_selecionado}.part{pt}.rar")

                if response.status_code == 200:
                    # Obtém o tamanho total do arquivo em bytes
                    total_size_in_bytes = int(response.headers.get('content-length', 0))
                    
                    # Abre o arquivo local para escrita em modo binário
                    with open(local_filename, 'wb') as f:
                        # Inicializa a barra de progresso com o tamanho total do arquivo
                        with tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, desc=f"{game_selecionado}_part_{pt}.zip", leave=False) as progress_bar:
                            # Itera sobre os chunks do conteúdo da resposta
                            for chunk in response.iter_content(chunk_size=1024):
                                # Escreve o chunk atual no arquivo
                                f.write(chunk)
                                # Atualiza a barra de progresso com o tamanho do chunk atual
                                progress_bar.update(len(chunk))

                            print("Download concluído com sucesso para:", local_filename)
                            pt += 1
                            break  # Sai do loop de tentativas bem-sucedidas

                else:
                    tentativas += 1  # Incrementa o contador de tentativas
                    print(f"Tentativa {tentativas} de download falhou. Código de status:", response.status_code)

            except IncompleteRead as e:
                tentativas += 1  # Incrementa o contador de tentativas
                print(f"Tentativa {tentativas} de download falhou devido a IncompleteRead: {e}")

        if tentativas == max_tentativas:
            print(f"Falha ao baixar o arquivo após {max_tentativas} tentativas. URL: {url}")
            messagebox.showerror("Erro ao baixar o arquivo", f"Falha ao baixar o arquivo após {max_tentativas} tentativas.")
        else:
            tentativas = 0  # Resetar o contador de tentativas se o download foi bem-sucedido
    messagebox.showinfo("DOWNLOAD COMPLETO","Download complete pode fechar")
def main():
    
    diretorio = diretorio_download()
    arquivo_adblock = arquivo_crx()

    driver = navegador(diretorio,arquivo_adblock[0])

    time.sleep(6) #tempo para a página carregar completamente

    janela = driver.window_handles
    driver.switch_to.window(janela[1])
    driver.close()
    driver.switch_to.window(janela[0])

    game_selecionado = escolhe_jogo(driver)
    lista_game = extrator_de_links_game(driver,arquivo_adblock[0],arquivo_adblock[1])
    link_download = extrator_links_download_page(driver,lista_game)
    
    if diretorio:
        download_game(link_download,game_selecionado,diretorio)
        driver.close()

# %%
if __name__ == "__main__":
    main()
