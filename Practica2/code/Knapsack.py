import random


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

        if random.randint(1,100) <= cProb:
            posicionCruce=random.randint(0,tam-1)

            for j in range (posicionCruce, tam-1):
                auxiliar=padre1[j]
                padre1=padre2[j]
                padre2=auxiliar

        generacion.append(padre2)
        generacion.append(padre1)

    #Mutar padres con probabilidad mProb para binario
    for a in range (len(generacion)):
        if random.randint(1,100) <= mProb:
            posicionMutacion=random.randint(0,tam-1)

            if generacion[a][posicionMutacion]==1:
                generacion[a][posicionMutacion]=0 
            else:
                generacion[a][posicionMutacion]=1



    return generacion #Devolver la nueva poblacion (sin evaluar)

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 20 #Tamaño de la poblacion
    maxGeneraciones = 20#Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.7 #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion

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

    print(str(poblacion))
    print("_______________")



    it=1
    sumatorio=0
    while it < maxGeneraciones:
        sumatorio=0
        nSoluciones = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        #Modelo generacional
        poblacion = []
        for solucion in nSoluciones:
            poblacion.append([solucion[0],evaluarSolucion(solucion[0],precios,pesos,pesoMax)])
            sumatorio+=evaluarSolucion(solucion[0],precios,pesos,pesoMax)
        sumatorio/=20
            
        it+=1
        print("Generacion "+str(it-1))
        print("Poblacion ")
        print(str(poblacion))
        print("Valor medio de la generacion "+str(sumatorio))
        print("_______________")
    
    

if __name__ == "__main__":
    main()
