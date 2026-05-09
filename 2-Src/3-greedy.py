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

def algoritmo_greedy(temas, dias, horas_por_dia):
    temas_ordenados = sorted(temas, key=lambda x: (x[4], -x[2]))
    
    horas_dia = [0] * (dias + 1)
    plan = [[] for _ in range(dias + 1)]
    completados = 0
    fuera_de_plazo = 0

    for tema in temas_ordenados:
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

def imprimir_plan(nombre_caso, plan, completados, fuera):
    print("=" * 50)
    print("  CASO GREEDY:", nombre_caso)
    print("=" * 50)
    for dia in range(1, len(plan)):
        if plan[dia]:
            print("\n  Dia", dia, ":")
            for materia, nombre, horas in plan[dia]:
                print("    [" + materia + "] " + nombre + " - " + str(horas) + "h")
    print("\n  Completados a tiempo :", completados)
    print("  Fuera de plazo       :", fuera)
    print()

archivos = [
    ("Pequeño", "1-Datos/1-caso_pequeno.txt"),
    ("Mediano", "1-Datos/2-caso_mediano.txt"),
    ("Grande",  "1-Datos/3-caso_grande.txt"),
]

for nombre, ruta in archivos:
    temas, dias, hpd = leer_caso(ruta)
    plan, comp, fuera = algoritmo_greedy(temas, dias, hpd)
    imprimir_plan(nombre, plan, comp, fuera)