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


# ── NUCLEO RECURSIVO ──────────────────────────────────────────────────────────

def _planificar_recursivo(temas, dia_inicio, dia_fin, horas_por_dia):
    n_dias = dia_fin - dia_inicio + 1
    plan = {d: [] for d in range(dia_inicio, dia_fin + 1)}
    horas_usadas = {d: 0 for d in range(dia_inicio, dia_fin + 1)}

    if not temas:
        return plan

    if n_dias == 1 or len(temas) == 1:
        temas_ord = sorted(temas, key=lambda t: (t[4], -t[2]))
        for tema in temas_ord:
            _, nombre, _, horas_req, _ = tema
            horas_rest = horas_req
            for d in range(dia_inicio, dia_fin + 1):
                espacio = horas_por_dia - horas_usadas[d]
                if espacio > 0 and horas_rest > 0:
                    h = min(espacio, horas_rest)
                    plan[d].append((nombre, h))
                    horas_usadas[d] += h
                    horas_rest -= h
        return plan

    # ── DIVIDIR ───────────────────────────────────────────────────────────────
    dia_medio = (dia_inicio + dia_fin) // 2
    urgentes = [t for t in temas if t[4] <= dia_medio]
    no_urgentes = [t for t in temas if t[4] > dia_medio]

    if not urgentes or not no_urgentes:
        temas_ord = sorted(temas, key=lambda t: (t[4], -t[2]))
        mitad = max(1, len(temas_ord) // 2)
        urgentes = temas_ord[:mitad]
        no_urgentes = temas_ord[mitad:]

    # ── VENCER ────────────────────────────────────────────────────────────────
    plan_izq = _planificar_recursivo(urgentes, dia_inicio, dia_medio, horas_por_dia)
    plan_der = _planificar_recursivo(no_urgentes, dia_medio + 1, dia_fin, horas_por_dia)

    # ── COMBINAR ──────────────────────────────────────────────────────────────
    plan.update(plan_izq)
    plan.update(plan_der)

    return plan


def divide_y_venceras(temas, dias, horas_por_dia):
    if not temas or dias <= 0 or horas_por_dia <= 0:
        return {}
    return _planificar_recursivo(temas, 1, dias, horas_por_dia)


def calcular_indicadores(plan, temas, horas_por_dia):
    horas_asignadas = {}
    for sesiones in plan.values():
        for nombre, horas in sesiones:
            horas_asignadas[nombre] = horas_asignadas.get(nombre, 0) + horas

    total_horas_req = sum(t[3] for t in temas)
    total_horas_asig = sum(horas_asignadas.values())
    total_horas_disp = len(plan) * horas_por_dia

    temas_completos = 0
    temas_parciales = 0
    temas_omitidos = 0
    temas_deadline_ok = 0

    for _, nombre, _, horas_req, deadline in temas:
        asignado = horas_asignadas.get(nombre, 0)
        if asignado == 0:
            temas_omitidos += 1
        elif asignado < horas_req:
            temas_parciales += 1
        else:
            temas_completos += 1

        if asignado > 0:
            acum, dia_fin_tema = 0, None
            for d in sorted(plan.keys()):
                for n, h in plan[d]:
                    if n == nombre:
                        acum += h
                if acum >= horas_req and dia_fin_tema is None:
                    dia_fin_tema = d
            if dia_fin_tema is not None and dia_fin_tema <= deadline:
                temas_deadline_ok += 1

    return {
        "total_horas_requeridas": total_horas_req,
        "total_horas_asignadas": total_horas_asig,
        "total_horas_disponibles": total_horas_disp,
        "temas_completos": temas_completos,
        "temas_parciales": temas_parciales,
        "temas_omitidos": temas_omitidos,
        "temas_deadline_ok": temas_deadline_ok,
        "horas_asignadas": horas_asignadas,
    }

