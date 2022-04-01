import random, csv
import matplotlib.pyplot as plt
import pandas as pd
import copy
def evaluarSolucion(solucion, precios, pesos, pesoMax):
    precio = 0
    peso = 0
    for i in range(len(solucion)):
        precio += precios[i]*solucion[i]
        peso += pesos[i]*solucion[i]

    if peso > pesoMax:
        return 0
    else:
        return precio

def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb):

    #Seleccionar padres mediante torneo tamaño k
    mejor=[]
    for i in range(len(poblacion)):
        propuestos=[]
        for j in range (k):
            propuesto=poblacion[random.randint(0, len(poblacion)-1)]
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
        padre1=mejor[i].copy()

        if(i+1 == len(mejor)):
            generacion.append(copy.deepcopy(padre1))
            break

        padre2=mejor[i+1].copy()

        if random.randint(1,100) <= (cProb*100):
            posicionCruce=random.randint(0,tam-1)
            for j in range (posicionCruce, tam-1):
                auxiliar=padre1[0][j]
                padre1[0][j]=padre2[0][j]
                padre2[0][j]=auxiliar

        generacion.append(copy.deepcopy(padre2))
        generacion.append(copy.deepcopy(padre1))

    #Mutar padres con probabilidad mProb para binario
    for a in range (len(generacion)):
        if random.randint(1,100) <= (mProb*100):
            posicionMutacion=random.randint(1,len(mejor[0][0])-1)
            generacion[a][0][posicionMutacion]+=random.randint(-2, 2);
            if generacion[a][0][posicionMutacion] < 0:
                generacion[a][0][posicionMutacion] = 0
         

    return generacion,  mejorValor #Devolver la nueva poblacion (sin evaluar)


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
            # Descomentar para obtener soluciones válidas de primera mano
           # if peso <= pesoMax:
            #    solucion.append(objeto)
             #   objetos.remove(objeto)

        s = []
        for i in range(l):
            s.append(0)
        for i in solucion:
            s[i] = 1
        poblacion.append([s,evaluarSolucion(s,precios,pesos,pesoMax)])
    it=1
   
    peoresSoluciones = []
    mejoresSoluciones = []
    solucionesMedias = []
    while it < maxGeneraciones:
        sumatorio=0
        nSoluciones, valorActual = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)

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
        solucionMedia/=len(nSoluciones)
        peoresSoluciones.append(peorSolucion)
        mejoresSoluciones.append(mejorSolucion)
        solucionesMedias.append(solucionMedia) 
        it+=1

    
    return peoresSoluciones, solucionesMedias, mejoresSoluciones

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 20 #Tamaño de la poblacion
    maxGeneraciones = 40 #Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.7 #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion
    parametros = [pesoMax, nSoluciones, maxGeneraciones, k, cProb, mProb]
    peorSolucion, SoluMedia, mejorSolu = ejecutar(pesos, precios, parametros)  

    for b in SoluMedia:
        print(b)


if __name__ == "__main__":
    main()




    
