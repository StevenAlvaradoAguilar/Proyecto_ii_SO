import webScraping

import funcionespostgres

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
print(resultados)




