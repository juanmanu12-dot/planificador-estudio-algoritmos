import time
import math
import os


# ── LECTURA DE CASOS DE PRUEBA ────────────────────────────────────────────────

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

