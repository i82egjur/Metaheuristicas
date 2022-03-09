import random, csv
import matplotlib.pyplot as plt
import pandas as pd

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

    #Cruzar padres con probabilidad cProb
    #if random.randint(1,100) <= cProb:

    #Mutar padres con probabilidad mProb
    #if random.randint(1,100) <= mProb:


    return poblacion #Devolver la nueva poblacion (sin evaluar)

def ejecutar(pesos,precios,pesoMax,nSoluciones,maxGeneraciones,cProb,mProb):
	pesoMax = parametros[0]
	nSoluciones = parametros[1]
	maxGeneraciones = parametros[2]
	cProb = parametros[3]
	mProb = parametros[4]


    l=len(pesos)
    ##Creamos n soluciones aleatorias que sean válidas
    poblacion = []
    for i in range(nSoluciones):
        objetos = list(range(l))
        solucion = []
        peso = 0
        while peso < pesoMax:
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
    while it < maxGeneraciones:
        nSoluciones = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        #Modelo generacional
        poblacion = []
        for solucion in nSoluciones:
            poblacion.append([solucion[0],evaluarSolucion(solucion[0],precios,pesos,pesoMax)])
        it+=1
    peorSolucion, SoluMedia, mejorSolu = 0,0,0
    return peorSolucion, SoluMedia, mejorSolu

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 25 #Tamaño de la poblacion
    maxGeneraciones = 1 #Numero de generaciones
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
    nombreMediciones = ["Numero de soluciones", "Tamaño del torneo", "Maximo generaciones", "Probabilidad de cruce", "Probabilidad de mutacion"]

    valoresDistintosValoresMediciones = [   [5, 10, 15, 20, 25, 30], 
										    [1, 2, 4, 5, 10, 25], 
										    [1, 2, 3, 4, 5, 6], 
										    [0.1, 0.3, 0.5, 0.6, 0.7] ]
										    [0.1, 0.3, 0.5, 0.6, 0.7], 

    for nMedicion in range(len(nombreMediciones)):
    	with open(nombreMediciones[nMedicion], 'w', newline='') as csvfile:
       		spamwriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	        spamwriter.writerow([nombreMediciones[nMedicion], "Peor solución", "Solución media", "Mejor solución"])
	    	
	    	for valor in range(0, len(valoresDistintosValoresMediciones[nMedicion]))
	    		parametros[nMedicion] = valoresDistintosValoresMediciones[nMedicion][valor]
	    		peorSolucion, SoluMedia, mejorSolu = ejecutar(pesos, precios, parametros)
	            spamwriter.writerow([valoresDistintosValoresMediciones[nMedicion], peorSolucion, SoluMedia, mejorSolu])

		data = pd.read_csv(nombreMediciones[nMedicion])
		df = pd.DataFrame(data)
		X = list(df.iloc[:, 0])
		Y = list(df.iloc[:, 1])
		plt.bar(X, Y, color='g')
		plt.title(nombreMediciones[nMedicion])
		plt.xlabel("Variación parámetros")
		plt.ylabel("Soluciones")
		plt.savefig(nombreMediciones[nMedicion]+".png")



if __name__ == "__main__":
    main()




  
  
# Initialize the lists for X and Y
  
df = pd.DataFrame(data)
  
X = list(df.iloc[:, 0])
Y = list(df.iloc[:, 1])
  
# Plot the data using bar() method
plt.bar(X, Y, color='g')
plt.title("Students over 11 Years")
plt.xlabel("Years")
plt.ylabel("Number of Students")
  
# Show the plot
plt.show()
