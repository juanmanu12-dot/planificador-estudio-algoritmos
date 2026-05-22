# ──────────────────────────────────────────────
# RECURSIVO - Planificador de Estudio
# Lee los casos de prueba desde archivos .txt
# ──────────────────────────────────────────────

import time

# ──────────────────────────────────────────────
# LEER CASO DESDE ARCHIVO
# ──────────────────────────────────────────────

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
            temas.append((partes[0], partes[1], int(partes[2]), int(partes[3]), int(partes[4])))
    archivo.close()
    return temas, dias, horas_por_dia


# ──────────────────────────────────────────────
# NÚCLEO RECURSIVO
#
# Idea: procesar tema por tema (índice idx).
# En cada llamada decidimos en qué día colocar
# el tema actual y llamamos recursivamente para
# el siguiente tema.
#
# Caso base  : idx == len(temas)  →  evaluamos el plan completo.
# Caso recurs: probamos cada día válido para el tema idx
#              y llamamos con idx+1.
#
# Complejidad: O(dias^n) en peor caso  (n = número de temas),
#              ya que cada tema puede ir en cualquiera de los días.
# ──────────────────────────────────────────────

def _resolver_recursivo(temas, idx, dias, horas_por_dia,
                         horas_dia, plan_actual, mejor):
    # ── CASO BASE ─────────────────────────────
    if idx == len(temas):
        completados = 0
        fuera = 0
        for dia in range(1, dias + 1):
            for (materia, nombre, horas, deadline) in plan_actual[dia]:
                if dia <= deadline:
                    completados += 1
                else:
                    fuera += 1

        no_asignados = len(temas) - sum(len(plan_actual[d]) for d in range(1, dias + 1))
        fuera += no_asignados

        if (completados > mejor["completados"] or
                (completados == mejor["completados"] and fuera < mejor["fuera"])):
            mejor["completados"] = completados
            mejor["fuera"] = fuera
            mejor["plan"] = [list(d) for d in plan_actual]
        return

    # ── CASO RECURSIVO ────────────────────────
    materia, nombre, dificultad, horas, deadline = temas[idx]

    # Opción A: asignar el tema en algún día
    for dia in range(1, dias + 1):
        if horas_dia[dia] + horas <= horas_por_dia:
            # Poda: si el tema solo tiene días posteriores a su deadline
            # no tiene sentido seguir buscando días más tardíos
            horas_dia[dia] += horas
            plan_actual[dia].append((materia, nombre, horas, deadline))

            _resolver_recursivo(temas, idx + 1, dias, horas_por_dia,
                                 horas_dia, plan_actual, mejor)

            plan_actual[dia].pop()
            horas_dia[dia] -= horas

    # Opción B: no asignar el tema (quedará fuera de plazo)
    _resolver_recursivo(temas, idx + 1, dias, horas_por_dia,
                         horas_dia, plan_actual, mejor)


def planificador_recursivo(temas, dias, horas_por_dia):
    mejor = {"plan": None, "completados": -1, "fuera": 999999}
    horas_dia = [0] * (dias + 1)
    plan_actual = [[] for _ in range(dias + 1)]
    _resolver_recursivo(temas, 0, dias, horas_por_dia,
                         horas_dia, plan_actual, mejor)
    return mejor["plan"], mejor["completados"], mejor["fuera"]


# ──────────────────────────────────────────────
# IMPRIMIR RESULTADOS
# ──────────────────────────────────────────────

def imprimir_plan(nombre_caso, plan, completados, fuera, tiempo_ms):
    print("=" * 50)
    print("  CASO RECURSIVO:", nombre_caso)
    print("=" * 50)
    for dia in range(1, len(plan)):
        if plan[dia]:
            print("\n  Dia", dia, ":")
            for materia, nombre, horas, deadline in plan[dia]:
                en_plazo = "OK" if dia <= deadline else "TARDE"
                print("    [" + materia + "] " + nombre +
                      " - " + str(horas) + "h  (" + en_plazo + ")")
    print("\n  Completados a tiempo :", completados)
    print("  Fuera de plazo       :", fuera)
    print("  Tiempo de ejecucion  : {:.6f} ms".format(tiempo_ms))
    print()


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

archivos = [
    ("Pequeño", "1-Datos/1-caso_pequeno.txt"),
    ("Mediano", "1-Datos/2-caso_mediano.txt"),
    ("Grande",  "1-Datos/3-caso_grande.txt"),
]

for nombre, ruta in archivos:
    print("Ejecutando caso", nombre, "...")
    temas, dias, hpd = leer_caso(ruta)
    inicio = time.perf_counter()
    mejor_plan, completados, fuera = planificador_recursivo(temas, dias, hpd)
    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    imprimir_plan(nombre, mejor_plan, completados, fuera, tiempo_ms)

# ──────────────────────────────────────────────
# CASOS GRANDES (n=100 y n=1000)
# Recursivo tiene complejidad O(dias^n) — para n=100
# con 15 dias disponibles seria 15^100, impracticable.
# Se registra el aviso para el analisis de complejidad.
# ──────────────────────────────────────────────

casos_grandes = [
    ("n=100",  "1-Datos/4-caso_100.txt"),
    ("n=1000", "1-Datos/5-caso_1000.txt"),
]

for nombre, ruta in casos_grandes:
    temas, dias, hpd = leer_caso(ruta)
    n = len(temas)
    print("=" * 50)
    print("  CASO RECURSIVO:", nombre)
    print("=" * 50)
    print("\n  Recursivo es IMPRACTICABLE para n =", n)
    print("  Nodos del arbol       : " + str(dias) + "^" + str(n) + " (astronomico)")
    print("  Complejidad           : O(dias^n)")
    print("  Tiempo estimado       : impracticable")
    print("  Resultado             : N/A")
    print()