import random, csv
import TSPGenerator

def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerMejorVecino(solucion, datos):
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    mejorVecino = vecinos[0]
    mejorLongitud = evaluarSolucion(datos, mejorVecino)
    for vecino in vecinos:
        longitud = evaluarSolucion(datos, vecino)
        if longitud < mejorLongitud:
            mejorLongitud = longitud
            mejorVecino = vecino
    return mejorVecino, mejorLongitud

def hillClimbing(datos):
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
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
      #  print("Longitud de la ruta: ", longitud)
        vecino = obtenerMejorVecino(solucion, datos)

    return solucion, longitud

def main():

    nombreDelCsvAGenerar = "escribaAquiElTitulo.csv"
    numeroDeVecesARepetirHillClimbing = 100
    with open('nombreDelCsvAGenerar', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Número de ciudades", "Peor distancia", "Distancia media", "Mejor distancia", "Veces que se repite el optimo", "Relacion de optimos/totales" ])

        #Lista con el numero de ciudades que se va a probar
        vectorCiudades = [3,5,7,10,15,20,25,30,40,50,60]
        for numeroCiudades in vectorCiudades:
            listaSoluciones = []
            min = 999999999999999999
            max = 0
            ocurrencia = 0
            media = 0
            total = 0
            datos = TSPGenerator.generador(numeroCiudades)

            for a in range(numeroDeVecesARepetirHillClimbing):
                s=hillClimbing(datos)
            
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

            spamwriter.writerow([numeroCiudades, max, media, min, ocurrencia, ocurrencia/len(listaSoluciones)])


if __name__ == "__main__":
    main()
