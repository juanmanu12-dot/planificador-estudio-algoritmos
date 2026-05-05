# ──────────────────────────────────────────────
# FUERZA BRUTA - Planificador de Estudio
# Lee los casos de prueba desde archivos .txt
# ──────────────────────────────────────────────


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
            materia = partes[0]
            nombre = partes[1]
            dificultad = int(partes[2])
            horas = int(partes[3])
            deadline = int(partes[4])
            temas.append((materia, nombre, dificultad, horas, deadline))
    archivo.close()

    return temas, dias, horas_por_dia


# ──────────────────────────────────────────────
# GENERAR PERMUTACIONES (sin importaciones)
# ──────────────────────────────────────────────

def generar_permutaciones(lista):
    if len(lista) == 0:
        return [[]]
    if len(lista) == 1:
        return [lista]

    resultado = []
    for i in range(len(lista)):
        elemento = lista[i]
        resto = lista[:i] + lista[i+1:]
        for perm in generar_permutaciones(resto):
            resultado.append([elemento] + perm)
    return resultado


# ──────────────────────────────────────────────
# EVALUAR UN PLAN
# ──────────────────────────────────────────────

def evaluar_plan(permutacion, dias, horas_por_dia):
    horas_dia = [0] * (dias + 1)
    plan = []
    for d in range(dias + 1):
        plan.append([])

    completados = 0
    fuera_de_plazo = 0

    for tema in permutacion:
        materia, nombre, dificultad, horas, deadline = tema
        asignado = False

        for dia in range(1, dias + 1):
            if horas_dia[dia] + horas <= horas_por_dia:
                horas_dia[dia] += horas
                plan[dia].append((materia, nombre, horas))
                if dia <= deadline:
                    completados += 1
                else:
                    fuera_de_plazo += 1
                asignado = True
                break

        if not asignado:
            fuera_de_plazo += 1

    return plan, completados, fuera_de_plazo



# FUERZA BRUTA


def fuerza_bruta(temas, dias, horas_por_dia):
    mejor_plan = None
    mejor_completados = -1
    mejor_fuera = 999999
    total_permutaciones = 0

    todas = generar_permutaciones(list(temas))

    for perm in todas:
        total_permutaciones += 1
        plan, completados, fuera = evaluar_plan(perm, dias, horas_por_dia)

        if completados > mejor_completados:
            mejor_completados = completados
            mejor_fuera = fuera
            mejor_plan = plan
        elif completados == mejor_completados and fuera < mejor_fuera:
            mejor_fuera = fuera
            mejor_plan = plan

    return mejor_plan, mejor_completados, mejor_fuera, total_permutaciones



# IMPRIMIR RESULTADOS


def imprimir_plan(nombre_caso, plan, completados, fuera, total_permutaciones):
    print("=" * 50)
    print("  CASO:", nombre_caso)
    print("=" * 50)
    for dia in range(1, len(plan)):
        if plan[dia]:
            print("\n  Dia", dia, ":")
            for materia, nombre, horas in plan[dia]:
                print("    [" + materia + "] " + nombre + " - " + str(horas) + "h")
    print("\n  Completados a tiempo :", completados)
    print("  Fuera de plazo       :", fuera)
    print("  Permutaciones        :", total_permutaciones)
    print()


# ──────────────────────────────────────────────
# MAIN - Lee y ejecuta los 3 casos
# ──────────────────────────────────────────────

archivos = [
    ("Pequeño",  "1-Datos/1-caso_pequeno.txt"),
    ("Mediano",  "1-Datos/2-caso_mediano.txt"),
    ("Grande",   "1-Datos/3-caso_grande.txt"),
]

for nombre, ruta in archivos:
    print("\nEjecutando caso", nombre, "...")
    temas, dias, hpd = leer_caso(ruta)
    mejor_plan, completados, fuera, total_perms = fuerza_bruta(temas, dias, hpd)
    imprimir_plan(nombre, mejor_plan, completados, fuera, total_perms)