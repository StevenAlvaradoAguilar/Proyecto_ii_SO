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
            y = y.replace("\"", "*")
            y = y.replace("\'", "*")
            words = words + y
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


def bayes(cd, cs, universo, url, listaC1, listaC2):
    pVd = cd / universo
    pVs = cs / universo

    webScraping.extraer(url)
    lista = webScraping.listaPaginas[0]

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
    nueva = []
    for i in lis:
        nueva = nueva + i.split()
    frecuenciaPalab = [nueva.count(w) for w in nueva]  # a list comprehension
    lis = list(zip(nueva, frecuenciaPalab))
    nueva1 = []
    for x in range (len(lis)-1):
        if lis[x]  not in  nueva1:
            nueva1.append(lis[x])
    cantD = 0
    cantS = 0
    for i in nueva1:
            if i[0] in listaC1:
                print(i[0] + "-- DEPORTES")
                cantD += 1
            if i[0] in listaC2:
                print(i[0] + "-- SEXUAL")
                cantS +=1

    print("Palabras de deportes: " + str(cantD))
    print("Palabras de SEXUAL: " + str(cantS))

    probabilidadD = pVd * cantD/cd
    probabilidadS = pVs * cantS/cs

    print("Probabilidad de Deportes: "+ str(probabilidadD)+"\n")
    print("Probabilidad de Porno: " + str(probabilidadS) + "\n")





def sacarProbabilidadPrevia(lista, categoria1 , categoria2):
    listaC1 = funcionespostgres.consultarCategoria(categoria1)
    listaC2 = funcionespostgres.consultarCategoria(categoria2)
    universo = len(lista)
    cant1 = 0
    cant2 = 0
    otro = 0
    for i in lista:
        l1 = []
        l2 = []
        #print(i[0])
        for j in i[1]:
            if j[0] in listaC1 and j[1] < 5:
                #print(j[0] + "-- DEPORTES")
                l1.append(j[0])
            if j[0] in listaC2 and j[1] <5:
                #print(j[0] + "-- SEXUAL")
                l2.append(j[0])
        if(len(l1)== len(l2)):
            otro += 1
        else:
            if(len(l1) > len(l2)):
                cant1 += 1
            else:
                cant2 += 1
    #print(str(universo) + "--"+ str(cant1) + "--"+ str(cant2) +"----------"+ str(otro))
    bayes(cant1,cant2,universo,"https://www.britannica.com/place/New-York-state/Sports-and-recreation",listaC1,listaC2)

sacarProbabilidadPrevia(l,"deportes","sexual")

