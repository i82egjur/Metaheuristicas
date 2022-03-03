import random
import math
import TSPGenerator

def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerVecino(solucion, datos):
    ##Obtencion de los vecinos
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

def simAnnealing(datos,t0):
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
    #print("Longitud de la ruta: ", longitud)
    #print("Temperatura: ", t)

    it=0
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
        t=0.99*t
        #print("Longitud de la ruta: ", longitud)
        #print("It ", it)
    return solucion, longitud

def simAnnealingMejora(datos,t0,maxRecalentar):
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
    #print("Longitud de la ruta: ", longitud)
    #print("Temperatura: ", t)

    '''mejora 2, guardar y utilizar la mejor solucion'''
    mejorSolucion=solucion
    mejorLongitud=longitud

    it=0
    recalentar=0
    '''parada'''
    '''mejora 1, limitar el numero de iteraciones'''
    while t > 0.05:

        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]
            recalentar=0

            if(longitud<mejorLongitud):
                mejorLongitud=longitud
                mejorSolucion=solucion

            
        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]
            recalentar=0
            if(longitud<mejorLongitud):
                mejorLongitud=longitud
                mejorSolucion=solucion
        
        else:
            recalentar +=1;

        it+=1
        '''lineal'''
        '''por defecto'''
        t=0.99*t
        '''logaritmico'''
        '''t=(0.99*t0)/math.log(1+t,math.e)'''
        '''geometrica'''
        '''t=por(0.99,t)*t0'''

        '''mejora 2, recalentamiento'''
        if(recalentar>=maxRecalentar):
            recalentar=0
            t=t+(t*0.35)
        #print("Longitud de la ruta: ", longitud)
        #print("Temperatura: ", t)
    return mejorSolucion, mejorLongitud

def main():
    
    '''temperatura inicial'''
    t0=10 
    '''mejora 2, recaliento cada x tiempo, en este caso, iteraciones'''
    recalentar=50 
    mejorMejora=0
    mejorOtro=0
    for i in range(50):
        datos = TSPGenerator.generador(20)
        s=simAnnealingMejora(datos,t0,recalentar)
        s1=simAnnealing(datos,t0)
        if(s1[1]<s[1]):
            mejorOtro+=1
        elif(s1[1]>s[1]):
            mejorMejora+=1
    print("--------------")
    #print("Solucion final: ",s[0])
    #print("Longitud de la ruta final: ",s[1])
    print("Mejorado "+str(mejorMejora))
    print("Normal "+str(mejorOtro))



if __name__ == "__main__":
    main()
