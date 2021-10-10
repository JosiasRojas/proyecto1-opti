import random
from ortools.linear_solver import pywraplp
import time
import psutil

def generar(instancias, materias_primas, d, u):

    # Parametros
    matriz = []
    disponibilidad = []
    utilidades = []

    maxima_cantidad = 0

    for _ in range(instancias):
        utilidades.append(random.randint(1,u))

    # Generar matriz de mezcla
    cantidades_a_mezclar = []
    for i in range(instancias):
        cantidades_a_mezclar.append([])
        for _ in range(materias_primas):
            cantidad = random.randint(0,d)
            maxima_cantidad = max(maxima_cantidad,cantidad)
            cantidades_a_mezclar[i].append(cantidad)

        matriz.append(cantidades_a_mezclar[i])        

    for _ in range(materias_primas):
        disponibilidad.append(random.randint(maxima_cantidad,maxima_cantidad*100))

    return (matriz,disponibilidad,utilidades)

for iteracion in range(10):

    funcion_objetivo = "max z = "
    restricciones = ""
    naturaleza = ""

    # 0-99 variables
    variables = random.randint(100,800)
    materias_primas = random.randint(100,800)
    disponibilidad = random.randint(2,1000)
    utilidades = random.randint(2,1000)

    m,d,u = generar(variables,materias_primas,disponibilidad,utilidades)

    # Instanciar solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    infinity = solver.infinity()

    # Generar variables reales x >= 0
    x = {}
    for i in range(len(m)):
        x[i] =  solver.NumVar(0, infinity, 'x[%i]' %i)
        # Para imprimir modelo
        naturaleza += "x{} >= 0\n".format(i+1)

    # Restricciones
    for i in range(len(m[0])):
        ct1 = solver.Sum(m[j][i] * x[j] for j in range(len(m)))
        solver.Add(ct1 <= d[i])
        # Para imprimir modelo
        for j in range(len(m)):
            restricciones += "{}x{}".format(m[j][i],j+1)
            if(j < len(m) - 1):
                restricciones += " + "
        restricciones += " <= {}\n".format(d[i])

            

    Z = solver.Sum(u[i] * x[i] for i in range(len(u)))
    solver.Maximize(Z)
    # Para imprimir modelo
    for i in range(len(u)):
        funcion_objetivo += "{}x{}".format(u[i],i+1)
        if(i < len(u) - 1):
            funcion_objetivo += " + "
    funcion_objetivo += "\n"

    # Momento en que comienza a resolver
    start_time = time.time()
    status = solver.Solve()

    with open("test100-{}.txt".format(iteracion),"w") as f:
        f.write("restricciones: {}\n".format(solver.NumConstraints()))

        if status == pywraplp.Solver.OPTIMAL:
            f.write("Solucion:\n")
            f.write("Valor Objetivo Z = {}\n".format(solver.Objective().Value()))
            f.write("Asignacion de Variables\n")
            for i in range(len(m)):
                f.write("x{} = {}\n".format(i+1,x[i].solution_value()))
        else:
            f.write("El problema no tiene solucion optima")

        # Termino de la solucion
        f.write("Tiempo: {}\n".format(time.time() - start_time))
        f.write("Iteraciones: {}\n".format(solver.iterations()))

        f.write("\n===== Modelo =====\n\n")
        f.write(funcion_objetivo)
        f.write("\n")
        f.write(restricciones)
        f.write("\n")
        f.write(naturaleza)
        # f.write("CPU: {}\n".format(psutil.cpu_percent()))
        # f.write("MEMORY: {}\n".format(psutil.virtual_memory()._asdict()))



    