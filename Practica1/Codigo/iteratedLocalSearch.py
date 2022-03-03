import random
import TSPGenerator


def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerMejorVecino(solucion, datos):
    ##Obtención de los vecinos
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtención del mejor vecino
    mejorVecino = vecinos[0]
    mejorLongitud = evaluarSolucion(datos, mejorVecino)
    for vecino in vecinos:
        longitud = evaluarSolucion(datos, vecino)
        if longitud < mejorLongitud:
            mejorLongitud = longitud
            mejorVecino = vecino
    return mejorVecino, mejorLongitud

def hillClimbing(datos, solucion):
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))

    if(solucion == []):
        for i in range(l):
            ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
            solucion.append(ciudad)
            ciudades.remove(ciudad)


    longitud = evaluarSolucion(datos, solucion)
    ##Obtenemos el mejor vecino hasta que no haya vecinos mejores
    vecino = obtenerMejorVecino(solucion, datos)
    while vecino[1] < longitud:
        solucion = vecino[0]
        longitud = vecino[1]
        vecino = obtenerMejorVecino(solucion, datos)

    return solucion, longitud

def permutarSolucion(solucion, numeroIteracion):
    numeroIntercambios = 0

    for a in range(3):
        intercambiar(solucion, random.randint(0,len(solucion)-1), random.randint(0,len(solucion)-1))
    return solucion

  
def intercambiar(list, pos1, pos2): 
    list[pos1],list[pos2] = list[pos2],list[pos1] 
    return list



def iteratedLocalSearch(nIteraciones, datos):
    numeroIteracionesTotal = nIteraciones
    numeroIteracion = 0

    mejorSolucion = []
    solucionInicial, longitudInicial = hillClimbing(datos, mejorSolucion)
    mejorSolucion = solucionInicial
    mejorLongitud = longitudInicial

    while (numeroIteracion < numeroIteracionesTotal):
        nuevaSolucion = permutarSolucion(mejorSolucion, numeroIteracion)
        nuevaSolucion, nuevaLongitud = hillClimbing(datos, nuevaSolucion)

        if(nuevaLongitud < mejorLongitud):
            mejorLongitud = nuevaLongitud
            mejorSolucion = nuevaSolucion
            
        numeroIteracion += 1

    return mejorSolucion, mejorLongitud


def main():
    numeroVecesMejorIterate = 0
    numeroVecesMejorHill = 0
    iguales = 0


    for i in range(30):
        datos = TSPGenerator.generador(15)
        s=iteratedLocalSearch(300,datos)
       # print("--------------")
        #print("Solucion final iteratedLocalSearch: ",s[0])
        #print("Longitud de la ruta final iteratedLocalSearch: ",s[1])

        mini = 999999999
        solucionMinima = []

        for a in range(300):
            solucion, longitud = hillClimbing(datos, [])
            if(longitud < mini):
                mini = longitud
                solucionMinima = solucion

        #print("Solucion final hillClimbing: ",solucionMinima)
        #print("Longitud de la ruta final hillClimbing: ",mini)

        if s[1] > mini:
            numeroVecesMejorHill+=1

        elif s[1] < mini:
            numeroVecesMejorIterate+=1
        else:
            iguales+=1


    print("numeroVecesMejorHill:"+str(numeroVecesMejorHill))
    print("numeroVecesMejorIterate:"+str(numeroVecesMejorIterate))
    print("iguales:"+str(iguales))



if __name__ == "__main__":
    main()
