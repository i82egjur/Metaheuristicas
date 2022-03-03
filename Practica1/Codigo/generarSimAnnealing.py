import random
import math
import TSPGenerator
import random, csv


def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerVecino(solucion, datos):
    ##ObtenciÃ³n de los vecinos
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtengo un vecino aleatorio
    vecino=vecinos[random.randint(0, len(vecinos) - 1)]
    longitud = evaluarSolucion(datos, vecino)

    return vecino, longitud

def simAnnealing(datos,t0, ce, tLimite, alpha):
    t=t0
    l=len(datos)

    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)
 

    it=0
    '''parada'''
    while t > 0.05: 
        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]
        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]

        it+=1

        if(ce == 1):
            t=alpha*t
        if(ce == 2):
            t=(alpha*t0)/math.log(1+it, math.e)
        if(ce == 3):
            t=pow(alpha,it)*t0

     
    return solucion, longitud

def main():
    t=10
    datos = TSPGenerator.generador(t)
    nombreDelCsvAGenerar = "escribaAquiElTitulo.csv"
    coeficienteDeEnfriamiento = 3 
    tLimite = 0.1
    numeroDeVecesARepetirHillClimbing = 100

    with open(nombreDelCsvAGenerar, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='|',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["Alpha", "Peor distancia", "Distancia media", "Mejor distancia", "Veces que se repite el optimo", "Relacion de optimos/totales" ])

            alphas = [0.99, 0.98, 0.88, 0.77, 0.66, 0.55, 0.2, 0.001]
            for al in alphas:
                listaSoluciones = []
                min = 999999999999999999
                max = 0
                ocurrencia = 0
                media = 0
                total = 0

                   
                for a in range(numeroDeVecesARepetirHillClimbing):
                    s=simAnnealing(datos,t, coeficienteDeEnfriamiento, tLimite, al)
                
                    if s[1] < min:
                        min = s[1]

                    if s[1] > max:
                        max = s[1]

                    listaSoluciones.append(s[1])

                for a in listaSoluciones:
                    total += a
                    if(a == min):
                        ocurrencia+=1

                media = total/len(listaSoluciones)

                spamwriter.writerow([al, max, media, min, ocurrencia, ocurrencia/len(listaSoluciones)])





if __name__ == "__main__":
    main()
