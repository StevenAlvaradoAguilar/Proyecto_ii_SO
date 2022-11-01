from builtins import list

import webScraping

import funcionespostgres

from concurrent.futures import  ThreadPoolExecutor
import time

from multiprocessing import Pool

from functools import partial

def cargar():
    webS = webScraping
    webS.webscraping()
    lista = webS.listaPaginas
    for objeto in lista:
        palabras = []
        words = ''
        for x in objeto[1]:
            palabras.append(str(x))
        for y in palabras:
            y = y.replace("\\", "")
            y = y.replace("\'", "")
            y = y.replace("\"", "")
            y = y.replace(",", "")
            y = y.replace(".", "")
            y = y.replace(";", "")
            y = y.replace("'", "")
            y = y.replace("<", " ")
            y = y.replace(">", " ")
            words = words + y.lower()
        try:
            funcionespostgres.insertarResultados(objeto[0], words)
            #print("Si agrega")
        except:
            print(objeto[0],"No agrega")

#funcionespostgres.eliminarR()
#cargar()

resultados = funcionespostgres.llenarResultador()
listaPalabras = list()

for i in resultados:
    palabras = i[1].split()
    listaPalabras.append([i[0],palabras])



l = []
for i in listaPalabras:
    frecuenciaPalab = [i[1].count(w) for w in i[1]] # a list comprehension
    lis = list(zip(i[1], frecuenciaPalab))
    word = []
    for j in lis:
        if j not in word:
            word.append(j)
    l.append([i[0],word])


def imprimirL():
    for i in l:
        print("__________________________________________________________________________________________________________________________________________\n")
        for j in i:
            print(j)
            print("\n")
        #    print(j[0] + " -----  "+ str(j[1]))
#imprimirL()

def corregirLista(lista):
    lis = list()
    for objeto in lista[1]:
        palabras = []
        words = ''
        for x in objeto:
            palabras.append(str(x))
        for y in palabras:
            y = y.replace("\\", "")
            y = y.replace(".", "")
            y = y.replace(",", "")
            y = y.replace("\'", "")
            y = y.replace("\"", "")
            y = y.replace("<", " ")
            y = y.replace(">", " ")
            words = words + y.lower()
        lis.append(words)
    return lis

def segmentarlista(lis):
    nueva = []
    for i in lis:
        nueva = nueva + i.split()
    frecuenciaPalab = [nueva.count(w) for w in nueva]  # a list comprehension
    lis = list(zip(nueva, frecuenciaPalab))
    nueva1 = []
    for x in range(len(lis) - 1):
        if lis[x] not in nueva1:
            nueva1.append(lis[x])
    return nueva1

def verificarLis(listaC1,listaC2,var):
    if var in listaC1:
        return 1
    if var in listaC2:
        return 2

def bayes(cd, cs, universo, url, listaC1, listaC2):
    #print("_________________________________________________________________________ BAYES ________________________________________________________________\n")
    pVd = cd / universo
    pVs = cs / universo
    webScraping.extraer(url)
    lista = webScraping.listaPaginas[0]
    lis = corregirLista(lista)
    listaWords = segmentarlista(lis)
    cantD = 0
    cantS = 0

    for i in range (0,len(listaWords) - 1,10):
        try:
            palabra1 = listaWords[i][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra2 = listaWords[i+1][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra3 = listaWords[i+2][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra4 = listaWords[i+3][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra5 = listaWords[i+4][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra6  = listaWords[i+5][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra7 = listaWords[i+6][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra8 = listaWords[i+7][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra9 = listaWords[i+8][0]
        except:
            print("Se acabo la lista")
            break
        try:
            palabra10 = listaWords[i+9][0]
        except:
            print("Se acabo la lista")
            break
        #print("___________________________________________")
        var = Pool(3).map(partial(verificarLis,listaC1,listaC2),[palabra1,palabra2, palabra3, palabra4,palabra5,palabra6,palabra7,palabra8,palabra9,palabra10])
        for i in var:
            #print(i)
            if i == 1:
                cantD += 1
            if i == 2:
                cantS += 1
    print("Palabras de deportes: " + str(cantD))
    print("Palabras de SEXUAL: " + str(cantS))
    print("______________________________________________________________________________")
    probabilidadD = pVd * cantD/cd
    probabilidadS = pVs * cantS/cs
    print("Probabilidad de Deportes: "+ str(probabilidadD)+"\n")
    print("Probabilidad de Porno: " + str(probabilidadS) + "\n")


def sacarProbabilidadPrevia(url ,categoria1 , categoria2):
    listaC1 = funcionespostgres.consultarCategoria(categoria1)
    listaC2 = funcionespostgres.consultarCategoria(categoria2)

    universo = len(l)
    cant1 = 0
    cant2 = 0
    otro = 0
    for i in l:
        l1 = []
        l2 = []
        #print("______________________________________________________________________________")
        #print(i[0])
        for j in i[1]:
            #print(j)
            if j[0] in listaC1 and j[1] < 5:
                #print(j[0] + "-- DEPORTES")
                l1.append(j[0])
            if j[0] in listaC2 and j[1] <5:
                #print(j[0] + "-- SEXUAL")
                l2.append(j[0])
        if(len(l1)== len(l2)):
            #print("Sin Clasificar")
            otro += 1
        else:
            if(len(l1) > len(l2)):
                #print("Clasificado como Deporte")
                cant1 += 1
            else:
                #print("Clasificado como Sexual")
                cant2 += 1
    #print(str(universo) + "--"+ str(cant1) + "--"+ str(cant2) +"----------"+ str(otro))
    bayes(cant1,cant2,universo,url,listaC1,listaC2)




if __name__ == '__main__':
    sacarProbabilidadPrevia("https://www.espn.com/","deportes","sexual")

#https://www.xvideos.com/tags/espanol