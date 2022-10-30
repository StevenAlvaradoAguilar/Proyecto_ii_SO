from bs4 import BeautifulSoup
import pandas as pd
import requests
import Conexion

from translate import Translator

import funcionespostgres

import time
import logging

from concurrent.futures import  ThreadPoolExecutor

from multiprocessing import pool

listaPaginas = []

def extraer(url):
    try:
        page = requests.get(url, timeout=2)
        soup = BeautifulSoup(page.content, 'html.parser')
        palabras = soup.find_all('p')
        listaPaginas.append([url,palabras])
    except:
        pass
        #print("No se puede acceder")


def webscraping():
    con = Conexion.conexion()
    cur = con.cursor()
    query = "Select url from direcciones where id >= 2000 and id < 2050"
    cur.execute(query)
    exc = ThreadPoolExecutor(max_workers=3)
    for objeto in cur.fetchall():
        url = objeto[0]
        time.sleep(2)
        exc.submit(extraer, url)
    cur.close()
    con.close()


def extraercategoria(url):
    lista = []
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        palabras = soup.find_all('div',class_='word-ctn')
        for i in palabras:
            lista.append(i.text)
        listaDeportesNew = []
        for i in range(0, len(lista), 1):
            palabra = ''
            for j in range(0, len(lista[i]), 1):
                if lista[i][j] != '\n':
                    palabra = palabra + lista[i][j]
            listaDeportesNew.append(palabra)
        lista = listaDeportesNew
        funcionespostgres.insertarcategoria("sexual",lista)
    except:
        pass
        #print("No se puede acceder")

#extraercategoria("https://relatedwords.io/sexual")







