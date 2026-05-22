import time

def leer_caso(ruta):
    temas = []
    dias = 0
    horas_por_dia = 0
    archivo = open(ruta, "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea == "":
            continue
        if linea.startswith("dias="):
            dias = int(linea.split("=")[1])
        elif linea.startswith("horas_por_dia="):
            horas_por_dia = int(linea.split("=")[1])
        else:
            partes = linea.split(",")
            materia = partes[0]
            nombre = partes[1]
            dificultad = int(partes[2])
            horas = int(partes[3])
            deadline = int(partes[4])
            temas.append((materia, nombre, dificultad, horas, deadline))
    archivo.close()
    return temas, dias, horas_por_dia

def resolver_backtracking(temas, idx, dias, hpd, horas_dia, plan_actual, mejor_estado):
    if idx == len(temas):
        completados = 0
        fuera = 0
        for dia in range(1, dias + 1):
            for t in plan_actual[dia]:
                if dia <= t[3]:
                    completados += 1
                else:
                    fuera += 1

        total_asignados = sum(len(plan_actual[d]) for d in range(1, dias + 1))
        total_fuera = fuera + (len(temas) - total_asignados)

        if completados > mejor_estado["completados"]:
            mejor_estado["completados"] = completados
            mejor_estado["fuera"] = total_fuera
            mejor_estado["plan"] = [list(d) for d in plan_actual]
        elif completados == mejor_estado["completados"] and total_fuera < mejor_estado["fuera"]:
            mejor_estado["fuera"] = total_fuera
            mejor_estado["plan"] = [list(d) for d in plan_actual]
        return

    materia, nombre, dif, horas, deadline = temas[idx]

    for dia in range(1, dias + 1):
        if horas_dia[dia] + horas <= hpd:
            horas_dia[dia] += horas
            plan_actual[dia].append((materia, nombre, horas, deadline))

            resolver_backtracking(temas, idx + 1, dias, hpd, horas_dia, plan_actual, mejor_estado)

            plan_actual[dia].pop()
            horas_dia[dia] -= horas

    resolver_backtracking(temas, idx + 1, dias, hpd, horas_dia, plan_actual, mejor_estado)

def backtracking_inicio(temas, dias, hpd):
    mejor_estado = {
        "plan": None,
        "completados": -1,
        "fuera": 999999
    }
    horas_dia = [0] * (dias + 1)
    plan_actual = [[] for _ in range(dias + 1)]

    resolver_backtracking(temas, 0, dias, hpd, horas_dia, plan_actual, mejor_estado)
    return mejor_estado["plan"], mejor_estado["completados"], mejor_estado["fuera"]

def imprimir_plan(nombre_caso, plan, completados, fuera, tiempo_ms):
    print("=" * 50)
    print("  CASO BACKTRACKING:", nombre_caso)
    print("=" * 50)
    if plan:
        for dia in range(1, len(plan)):
            if plan[dia]:
                print("\n  Dia", dia, ":")
                for item in plan[dia]:
                    print("    [" + item[0] + "] " + item[1] + " - " + str(item[2]) + "h")
    print("\n  Completados a tiempo :", completados)
    print("  Fuera de plazo       :", fuera)
    print("  Tiempo de ejecucion  : {:.6f} ms".format(tiempo_ms))
    print()

archivos = [
    ("Pequeño", "1-Datos/1-caso_pequeno.txt"),
    ("Mediano", "1-Datos/2-caso_mediano.txt"),
    ("Grande",  "1-Datos/3-caso_grande.txt"),
]

for nombre, ruta in archivos:
    print("Procesando " + nombre + "...")
    temas, dias, hpd = leer_caso(ruta)
    inicio = time.perf_counter()
    mejor_plan, comp, fuera = backtracking_inicio(temas, dias, hpd)
    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    imprimir_plan(nombre, mejor_plan, comp, fuera, tiempo_ms)

# ──────────────────────────────────────────────
# CASOS GRANDES (n=100 y n=1000)
# Backtracking con poda mejora el peor caso O(dias^n),
# pero sigue siendo impracticable para n grande.
# ──────────────────────────────────────────────

casos_grandes = [
    ("n=100",  "1-Datos/4-caso_100.txt"),
    ("n=1000", "1-Datos/5-caso_1000.txt"),
]

for nombre, ruta in casos_grandes:
    temas, dias, hpd = leer_caso(ruta)
    n = len(temas)
    print("=" * 50)
    print("  CASO BACKTRACKING:", nombre)
    print("=" * 50)
    print("\n  Backtracking es IMPRACTICABLE para n =", n)
    print("  Complejidad peor caso : O(dias^n) con poda")
    print("  Tiempo estimado       : impracticable")
    print("  Resultado             : N/A")
    print()