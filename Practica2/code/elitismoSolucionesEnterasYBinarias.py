import random, csv
import matplotlib.pyplot as plt
import copy
import pandas as pd


def evaluarSolucion(solucion, precios, pesos, pesoMax):
    precio = 0
    peso = 0
    for i in range(len(solucion)):
        precio += precios[i]*solucion[i]
        peso += pesos[i]*solucion[i]

    #Este if hay que comentarlo para que de soluciones no validas
    if peso > pesoMax:
        return 0
    else:
        return precio


def elitismo(best,generacion):
    
    #se busca al peor individuo de la elite para ser sustituido
    peorV=generacion[0][1]
    posicionPeor=0

    for i in range(0, len(generacion)-1):
        if(generacion[i][1]<peorV):
            peorV=generacion[i][1]
            posicionPeor=i

    #Sustitucion del peor
    generacion[posicionPeor]=best
    
    
    return generacion
    
def mutarBinario(elemento):
    if elemento == 1:
        elemento = 0
    else:
        elemento = 1
    return elemento

def mutarReal(elementos):

    posicionMutacion=random.randint(1,len(elementos)-1)
    elementos[posicionMutacion]+=random.randint(-2, 2);
    if elementos[posicionMutacion] < 0:
        elementos[posicionMutacion] = 0
    
    return elementos



def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb, best):
        #Seleccionar padres mediante torneo tamaño k
    mejor=[]
    for i in range(len(poblacion)):
        propuestos=[]
        for j in range (k):
            propuesto=poblacion[random.randint(0, len(poblacion)-1)].copy()
            propuestos.append(propuesto)

        mejorValor=propuestos[0][1]
        mejorLocalizacion=propuestos[0][0]

        for j in range (k):
            if(mejorValor<propuestos[j][1]):
                mejorValor=propuestos[j][1]
                mejorLocalizacion=propuestos[j][0]
        mejor.append([mejorLocalizacion,mejorValor])
    

    #Cruzar padres con probabilidad cProb
    generacion=[]
    tam=len(mejor[0][0])

    for i in range (0,len(mejor),2):
        padre1=mejor[i]

        if(i+1 == len(mejor)):
            generacion.append(copy.deepcopy(padre1))
            break

        padre2=mejor[i+1]

        if random.randint(1,100) <= cProb*100:
            posicionCruce=random.randint(0,tam-1)

            for j in range (posicionCruce, tam-1):
                padre2[0][j], padre1[0][j] = padre1[0][j], padre2[0][j]

        generacion.append(copy.deepcopy(padre2))
        generacion.append(copy.deepcopy(padre1))

    #Mutar padres con probabilidad mProb para binario
    for a in range (len(generacion)):   
        if random.randint(1,100) <= mProb*100:
            posicionMutacion=random.randint(0,tam-1)
            #generacion[a][0][posicionMutacion] = mutarBinario(generacion[a][0][posicionMutacion])
            generacion[a][0] = mutarReal(generacion[a][0])

    print(generacion)
    elitista=elitismo(copy.deepcopy(best),generacion)
    
    return elitista, mejorValor #Devolver la nueva poblacion (sin evaluar)


def ejecutar(pesos,precios, parametros):
    pesoMax = parametros[0]
    nSoluciones = parametros[1]
    maxGeneraciones = parametros[2]
    k = parametros[3]
    cProb = parametros[4]
    mProb = parametros[5]
    
    mejorSolucion = 0
    peorSolucion=0

    l=len(pesos)
    ##Creamos n soluciones aleatorias que sean válidas
    poblacion = []
    for i in range(nSoluciones):
        objetos = list(range(l))
        solucion = []
        peso = 0
        while peso < pesoMax and objetos:
            objeto = objetos[random.randint(0, len(objetos) - 1)]
            peso += pesos[objeto]
            if peso <= pesoMax:
                solucion.append(objeto)
                objetos.remove(objeto)

        s = []
        for i in range(l):
            s.append(0)
        for i in solucion:
            s[i] = 1
        poblacion.append([s,evaluarSolucion(s,precios,pesos,pesoMax)])
    
    it=1
    sumatorio=0

    best=poblacion[0]
    mediaPorGeneracion = []
    peoresSoluciones = []
    mejoresSoluciones = []
    solucionesMedias = []
    while it < maxGeneraciones:
        sumatorio=0
        for i in range(1, len(poblacion)):
            if(best[1]<poblacion[i][1]):
                best = copy.deepcopy(poblacion[i])
             

        nSoluciones, valorActual = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb, best)
     
        #Modelo generacional
        poblacion = []
        solucionMedia = 0
        mejorSolucion = 0
        peorSolucion = 9999999999999999999
        for solucion in nSoluciones:
            solucionActual = evaluarSolucion(solucion[0],precios,pesos,pesoMax)
            poblacion.append([solucion[0], solucionActual])
            solucionMedia+=solucionActual
            
            if solucionActual > mejorSolucion:
                mejorSolucion = solucionActual
            if solucionActual < peorSolucion:
                peorSolucion = solucionActual  
        it+=1
        print(poblacion)
        peoresSoluciones.append(peorSolucion)
        mejoresSoluciones.append(mejorSolucion)
        solucionesMedias.append(solucionMedia/len(nSoluciones))

    return peoresSoluciones, solucionesMedias, mejoresSoluciones

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 10#Tamaño de la poblacion
    maxGeneraciones = 30 #Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.7  #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion
    parametros = [pesoMax, nSoluciones, maxGeneraciones, k, cProb, mProb]

    peorSolucion, SoluMedia, mejorSolu = ejecutar(pesos, precios, parametros)
    for a in SoluMedia:
        print(a)
    print("-----------------")
    for a in mejorSolu:
        print(a)



if __name__ == "__main__":
    main()

