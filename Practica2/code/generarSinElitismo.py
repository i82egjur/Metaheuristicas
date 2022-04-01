import random, csv
import matplotlib.pyplot as plt
import pandas as pd

def evaluarSolucion(solucion, precios, pesos, pesoMax):
    precio = 0
    peso = 0
    for i in range(len(solucion)):
        precio += precios[i]*solucion[i]
        peso += pesos[i]*solucion[i]

   
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
    tam=len(mejor[0])

    for i in range (0,len(mejor),2):
        padre1=mejor[i].copy()

        if(i+1 == len(mejor)):
            generacion.append(padre1)
            break

        padre2=mejor[i+1].copy()

        if random.uniform(0,1) <= cProb:
            posicionCruce=random.randint(0,tam-1)

            for j in range (posicionCruce, tam-1):
                auxiliar=padre1[j]
                padre1=padre2[j]
                padre2=auxiliar
                

        generacion.append(padre2)
        generacion.append(padre1)

    #Mutar padres con probabilidad mProb para binario
    for a in range (len(generacion)):
        if random.uniform(0,1) <= mProb:
            posicionMutacion=random.randint(0,tam-1)

            if generacion[a][0][posicionMutacion]==1:
                generacion[a][0][posicionMutacion]=0 
            else:
                generacion[a][0][posicionMutacion]=1



    return generacion, mejorValor #Devolver la nueva poblacion (sin evaluar)


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
            #Descomentar para obtener soluciones validas de primera mano
            #if peso <= pesoMax:
            #    solucion.append(objeto)
            #    objetos.remove(objeto)

        s = []
        for i in range(l):
            s.append(0)
        for i in solucion:
            s[i] = 1
        poblacion.append([s,evaluarSolucion(s,precios,pesos,pesoMax)])
    it=1
    sumatorio=0
    while it < maxGeneraciones:
        sumatorio=0
        nSoluciones, valorActual = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        if valorActual > mejorSolucion:
            mejorSolucion = valorActual
        if (valorActual < peorSolucion) or (it == 1):
            peorSolucion = valorActual

        #Modelo generacional
        poblacion = []
        for solucion in nSoluciones:
            poblacion.append([solucion[0],evaluarSolucion(solucion[0],precios,pesos,pesoMax)])
            sumatorio+=evaluarSolucion(solucion[0],precios,pesos,pesoMax)
        sumatorio/=len(nSoluciones)
            
        it+=1

    
    return peorSolucion, sumatorio, mejorSolucion

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 25 #Tamaño de la poblacion
    maxGeneraciones = 3 #Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.7 #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion

    parametros = [pesoMax, nSoluciones, maxGeneraciones, k, cProb, mProb]


    '''
        setNSoluciones = [5, 10, 15, 20, 25, 30]
        setTamaniosTorneo = [1, 2, 4, 5, 10, 25]
        setMaxGeneraciones = [1, 2, 3, 4, 5, 6]
        setProbabilidadDeCruce = [0.1, 0.3, 0.5, 0.6, 0.7]
        setProbabilidadDeMutacion = [0.1, 0.3, 0.5, 0.6, 0.7]   
    '''
    nombreMediciones = ["Peso maximo", "Numero de soluciones", "Tamaño del torneo", "Maximo generaciones", "Probabilidad de cruce", "Probabilidad de mutación"]

    valoresDistintosValoresMediciones = [   [1, 10, 30, 100, 200],
                                            [5, 10, 15, 20, 30, 60, 100, 200], 
                                            [1, 2, 3, 4, 5, 6,7,8,9,10,15,20], 
                                            [1, 2, 3, 4, 5, 10, 20, 30], 
                                            [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                                            [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1]] 

    for nMedicion in range(len(nombreMediciones)):
        with open(nombreMediciones[nMedicion], 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([nombreMediciones[nMedicion], "Peor solución", "Solución media", "Mejor solución"])
            
            for valor in range(0, len(valoresDistintosValoresMediciones[nMedicion])):
                parametrosSave = parametros[nMedicion] 
                parametros[nMedicion] = valoresDistintosValoresMediciones[nMedicion][valor]
                peorSolucion, SoluMedia, mejorSolu = ejecutar(pesos, precios, parametros)
                spamwriter.writerow([valoresDistintosValoresMediciones[nMedicion][valor], peorSolucion, SoluMedia, mejorSolu])
                parametros[nMedicion] = parametrosSave


        data = pd.read_csv(nombreMediciones[nMedicion], sep='|')
        df = pd.DataFrame(data)
        print(df)
        X = df.iloc[:, 0].values
        Y = df.iloc[:, 2].values
        plt.plot(X, Y)
        plt.title(nombreMediciones[nMedicion])
        plt.xlabel("Variación parámetros")
        plt.ylabel("Soluciones")
        plt.savefig(nombreMediciones[nMedicion]+"elit.png")
        plt.clf()


if __name__ == "__main__":
    main()




    