
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
from base_links import update_forza_1
from base_links import update_forza_2
from base_links import update_forza_3
from base_links import update_forza_4
from base_links import update_forza_5

from base_links import extator_de_links

def download_liks(driver):
    
    esc_up= int(input( "Esolha o qual update quer fazer\n 1- update 0 para 1 \n 2- update 1 para 2 \n 3- update 2 para 3 \n 4- update 3 para 4 \n 5- update 4 para 5 \n"))

    if esc_up == 1:
      for link in update_forza_1:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)  

    elif esc_up == 2:
       for link in update_forza_2:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)

    elif esc_up == 3:
       for link in update_forza_3:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)

    elif esc_up == 4:
       for link in update_forza_4:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)

    elif esc_up == 5:
       for link in update_forza_5:
        driver.get(link)
        down = driver.find_element(By.ID, "downloadButton")
        down.click()
        print(f"Download do link: {link}\n Iniciado")
        time.sleep(2)

    else:
       print("Escoha uma das options")
  
    # for link in forza_horizon_links:
    #     driver.get(link)
    #     down = driver.find_element(By.ID, "downloadButton")
    #     down.click()
    #     print(f"Download do link: {link}\n Iniciado")
    #     time.sleep(2)


        
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