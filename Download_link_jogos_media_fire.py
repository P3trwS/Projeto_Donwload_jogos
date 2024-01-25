
"""
Este Código faz o download do conteúdo de dentro dos links que estão dentro
do arquivo base_links
"""

import time
import tkinter as ttk 
from tkinter import filedialog
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By

from base_links import forza_horizon_links

from base_links import extator_de_links

def download_liks(driver):
  
    for link in forza_horizon_links:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)

def seleciona_diretorio():
    root = ttk.Tk()
    root.withdraw()
    download_dir = filedialog.askdirectory()
    return download_dir

def main():

    download_dir = seleciona_diretorio()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chrome_options)
    download_liks(driver)
    
    # messagebox.showinfo("Atenção !", "O google está fazendo o download do conteúdo dos links...")
    
    #EXTRATOR DE LINK EM CONSTRUCAO

    # driver = webdriver.Chrome()

    # extator_de_links(driver)
#%%
if __name__ == "__main__":
    main()