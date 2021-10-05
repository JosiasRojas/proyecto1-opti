import random

def generar(instancias, materias_primas):

    # Parametros
    matriz = []
    disponibilidad = random.sample(range(1,10), instancias)
    utilidades = random.sample(range(1,10), instancias)

    # Generar matriz de mezcla
    for i in range(instancias):
        cantidades_a_mezclar = random.sample(range(0,10), materias_primas)
        total_a_mezclar = sum(cantidades_a_mezclar)
        matriz.append(list(map(lambda x: round(x / total_a_mezclar,2), cantidades_a_mezclar)))

    restricciones = ""

    for variable, combinacion in enumerate(matriz):
        for i in range(instancias):
            restricciones += "{}x{}".format(combinacion[i],i+1)
        
            if i < instancias-1:
                restricciones += " + "

        restricciones += " <= {}\n".format(disponibilidad[variable])
        
    funcion_objetivo = "max z = "

    for i,utilidad in enumerate(utilidades):
        funcion_objetivo += "{}x{}".format(utilidad, i+1)

        if i < len(utilidades)-1:
            funcion_objetivo += " + "
    
    funcion_objetivo += "\n"
    
    naturaleza = ""

    for i in range(instancias):
        naturaleza += "x{} >= 0\n".format(i+1)

    print(funcion_objetivo)
    print(restricciones)
    print(naturaleza)
    



generar(5,5)



    