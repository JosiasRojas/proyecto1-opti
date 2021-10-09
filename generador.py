import random
from ortools.linear_solver import pywraplp

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
        # cantidades_a_mezclar = random.sample(range(0,d), materias_primas)
        # total_a_mezclar = sum(cantidades_a_mezclar[i])
        matriz.append(cantidades_a_mezclar[i])
        # matriz.append(list(map(lambda x: round(x / total_a_mezclar,2), cantidades_a_mezclar[i])))

    for _ in range(materias_primas):
        disponibilidad.append(random.randint(maxima_cantidad,maxima_cantidad*100))

    return (matriz,disponibilidad,utilidades)
    

# variables = int(input("Numero de variables: "))
# materias_primas = int(input("Numero de materias primas: "))
# disponibilidad = int(input("Maxima a usar de producto: "))
# utilidades = int(input("Maxima utilidad: "))

for iteracion in range(10):

    # 0-99 variables
    variables = random.randint(1000,1500)
    materias_primas = random.randint(1000,1500)
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
    # print("vars:",solver.NumVariables())

    # Restricciones
    for i in range(len(m[0])):
        ct1 = solver.Sum(m[j][i] * x[j] for j in range(len(m)))
        solver.Add(ct1 <= d[i])

    # print("constrains:",solver.NumConstraints())

    Z = solver.Sum(u[i] * x[i] for i in range(len(u)))
    solver.Maximize(Z)
    status = solver.Solve()

    with open("decenas-{}.txt".format(iteracion),"w") as f:
        if status == pywraplp.Solver.OPTIMAL:
            f.write("Solucion:\n")
            f.write("Valor Objetivo Z = {}\n".format(solver.Objective().Value()))
            f.write("Asignacion de Variables\n")
            for i in range(len(m)):
                f.write("x{} = {}\n".format(i+1,x[i].solution_value()))
        else:
            f.write("El problema no tiene solucion optima")



    