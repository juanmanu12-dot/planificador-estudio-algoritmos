# ══════════════════════════════════════════════════════════════════════════════
# COMPARATIVA FINAL — Planificador Óptimo de Estudio con Restricciones
# Ejecuta las 5 técnicas, mide tiempos reales y genera tabla + gráficas
#
# Rúbrica cubierta (Entrega 3):
#   ✓ Tabla: Comp.Temporal, Comp.Espacial, ¿Óptima?, t(n=100), t(n=1000)
#   ✓ Gráfica tiempos de ejecución (barras, escala log)
#   ✓ Gráfica calidad: completados vs fuera de plazo
#   ✓ Gráfica escalabilidad: tiempo vs tamaño de entrada
# ══════════════════════════════════════════════════════════════════════════════

import time
import threading
import sys
import os

sys.setrecursionlimit(500000)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    GRAFICAS = True
except ImportError:
    GRAFICAS = False
    print("[AVISO] matplotlib no disponible — instala con: pip install matplotlib\n")


# ══════════════════════════════════════════════════════════════════════════════
# LECTURA DE ARCHIVOS
# ══════════════════════════════════════════════════════════════════════════════

def leer_caso(ruta):
    temas, dias, hpd = [], 0, 0
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea.startswith("dias="):
                dias = int(linea.split("=")[1])
            elif linea.startswith("horas_por_dia="):
                hpd = int(linea.split("=")[1])
            else:
                p = linea.split(",")
                temas.append((p[0], p[1], int(p[2]), int(p[3]), int(p[4])))
    return temas, dias, hpd


# ══════════════════════════════════════════════════════════════════════════════
# 1. FUERZA BRUTA  —  O(n! · n) temporal,  O(n! · días) espacial
#    Genera todas las permutaciones posibles y evalúa cada asignación.
#    Garantiza la solución óptima al explorar exhaustivamente el espacio.
# ══════════════════════════════════════════════════════════════════════════════

def _permutaciones(lst):
    if len(lst) <= 1:
        return [lst]
    res = []
    for i, e in enumerate(lst):
        for p in _permutaciones(lst[:i] + lst[i+1:]):
            res.append([e] + p)
    return res

def fuerza_bruta(temas, dias, hpd):
    mejor_c, mejor_f, mejor_plan = -1, 999999, None
    for perm in _permutaciones(list(temas)):
        hd = [0] * (dias + 1)
        plan = [[] for _ in range(dias + 1)]
        c = f = 0
        for mat, nom, _, hrs, dl in perm:
            ok = False
            for d in range(1, dias + 1):
                if hd[d] + hrs <= hpd:
                    hd[d] += hrs
                    plan[d].append((mat, nom, hrs))
                    if d <= dl:
                        c += 1
                    else:
                        f += 1
                    ok = True
                    break
            if not ok:
                f += 1
        if c > mejor_c or (c == mejor_c and f < mejor_f):
            mejor_c, mejor_f, mejor_plan = c, f, plan
    return mejor_plan, mejor_c, mejor_f


# ══════════════════════════════════════════════════════════════════════════════
# 2. RECURSIVO  —  O(días^n) temporal,  O(n · días) espacial
#    Para cada tema decide en qué día colocarlo, llamando recursivamente.
#    Caso base : idx == n → evaluar plan acumulado.
#    Caso recur: probar cada día + opción de no asignar el tema.
# ══════════════════════════════════════════════════════════════════════════════

def _rec_aux(temas, idx, dias, hpd, hd, plan, mejor):
    if idx == len(temas):
        c = f = asig = 0
        for d in range(1, dias + 1):
            for (_, _, hrs, dl) in plan[d]:
                asig += 1
                if d <= dl:
                    c += 1
                else:
                    f += 1
        f += len(temas) - asig
        if c > mejor[0] or (c == mejor[0] and f < mejor[1]):
            mejor[0] = c
            mejor[1] = f
            mejor[2] = [list(x) for x in plan]
        return
    mat, nom, _, hrs, dl = temas[idx]
    for d in range(1, dias + 1):
        if hd[d] + hrs <= hpd:
            hd[d] += hrs
            plan[d].append((mat, nom, hrs, dl))
            _rec_aux(temas, idx + 1, dias, hpd, hd, plan, mejor)
            plan[d].pop()
            hd[d] -= hrs
    _rec_aux(temas, idx + 1, dias, hpd, hd, plan, mejor)  # no asignar

def recursivo(temas, dias, hpd):
    mejor = [-1, 999999, None]
    _rec_aux(temas, 0, dias, hpd,
             [0] * (dias + 1), [[] for _ in range(dias + 1)], mejor)
    return mejor[2], mejor[0], mejor[1]


# ══════════════════════════════════════════════════════════════════════════════
# 3. GREEDY  —  O(n log n) temporal,  O(n · días) espacial
#    Decisión local: ordenar por (deadline asc, dificultad desc) y asignar
#    cada tema al primer día con espacio disponible.
#    No garantiza óptimo global: puede fallar si temas urgentes desplazan
#    a otros igualmente urgentes pero de menor dificultad.
# ══════════════════════════════════════════════════════════════════════════════

def greedy(temas, dias, hpd):
    temas_ord = sorted(temas, key=lambda x: (x[4], -x[2]))
    hd = [0] * (dias + 1)
    plan = [[] for _ in range(dias + 1)]
    c = f = 0
    for mat, nom, _, hrs, dl in temas_ord:
        ok = False
        for d in range(1, dias + 1):
            if hd[d] + hrs <= hpd:
                hd[d] += hrs
                plan[d].append((mat, nom, hrs))
                if d <= dl:
                    c += 1
                else:
                    f += 1
                ok = True
                break
        if not ok:
            f += 1
    return plan, c, f


# ══════════════════════════════════════════════════════════════════════════════
# 4. BACKTRACKING  —  O(días^n) peor caso, mejor con poda
#    Igual que recursivo pero con poda por cota superior:
#    si c_parcial + temas_restantes ≤ mejor conocido → descartar rama.
#    Reduce drásticamente el espacio de búsqueda en la práctica.
# ══════════════════════════════════════════════════════════════════════════════

def _bt_aux(temas, idx, dias, hpd, hd, plan, mejor, c_parcial, restantes):
    if mejor[0] != -1 and c_parcial + restantes <= mejor[0]:
        return  # poda: imposible mejorar
    if idx == len(temas):
        c = f = 0
        asig = sum(len(plan[d]) for d in range(1, dias + 1))
        for d in range(1, dias + 1):
            for (_, _, hrs, dl) in plan[d]:
                if d <= dl:
                    c += 1
                else:
                    f += 1
        f += len(temas) - asig
        if c > mejor[0] or (c == mejor[0] and f < mejor[1]):
            mejor[0] = c
            mejor[1] = f
            mejor[2] = [list(x) for x in plan]
        return
    mat, nom, _, hrs, dl = temas[idx]
    for d in range(1, dias + 1):
        if hd[d] + hrs <= hpd:
            hd[d] += hrs
            plan[d].append((mat, nom, hrs, dl))
            nueva_c = c_parcial + (1 if d <= dl else 0)
            _bt_aux(temas, idx+1, dias, hpd, hd, plan, mejor, nueva_c, restantes-1)
            plan[d].pop()
            hd[d] -= hrs
    _bt_aux(temas, idx+1, dias, hpd, hd, plan, mejor, c_parcial, restantes-1)

def backtracking(temas, dias, hpd):
    mejor = [-1, 999999, None]
    _bt_aux(temas, 0, dias, hpd,
            [0]*(dias+1), [[] for _ in range(dias+1)],
            mejor, 0, len(temas))
    return mejor[2], mejor[0], mejor[1]


# ══════════════════════════════════════════════════════════════════════════════
# 5. DIVIDE Y VENCERÁS  —  T(n) = 2T(n/2) + O(n) → O(n log n) Teorema Maestro
#    Divide el intervalo de días en dos mitades.
#    Temas con deadline ≤ dia_medio → subproblema izquierdo.
#    Temas con deadline > dia_medio → subproblema derecho.
#    Combina los planes de ambos subproblemas.
# ══════════════════════════════════════════════════════════════════════════════

def _dyv(temas, d_ini, d_fin, hpd):
    plan = {d: [] for d in range(d_ini, d_fin + 1)}
    hu   = {d: 0  for d in range(d_ini, d_fin + 1)}
    if not temas:
        return plan
    if d_fin == d_ini or len(temas) == 1:   # caso base
        for mat, nom, _, hrs, _ in sorted(temas, key=lambda t: (t[4], -t[2])):
            rest = hrs
            for d in range(d_ini, d_fin + 1):
                esp = hpd - hu[d]
                if esp > 0 and rest > 0:
                    h = min(esp, rest)
                    plan[d].append((nom, h))
                    hu[d] += h
                    rest -= h
        return plan
    # Dividir
    d_mid = (d_ini + d_fin) // 2
    urg  = [t for t in temas if t[4] <= d_mid]
    nurg = [t for t in temas if t[4] >  d_mid]
    if not urg or not nurg:             # fallback por cantidad
        tord  = sorted(temas, key=lambda t: (t[4], -t[2]))
        mitad = max(1, len(tord) // 2)
        urg, nurg = tord[:mitad], tord[mitad:]
    # Vencer y combinar
    plan.update(_dyv(urg,  d_ini,    d_mid, hpd))
    plan.update(_dyv(nurg, d_mid+1, d_fin,  hpd))
    return plan

def _dyv_indicadores(plan, temas):
    horas_asig = {}
    ultimo_dia = {}
    for d in sorted(plan):
        for nom, h in plan[d]:
            horas_asig[nom] = horas_asig.get(nom, 0) + h
            ultimo_dia[nom] = d
    c = f = 0
    for _, nom, _, hrs_req, dl in temas:
        asig = horas_asig.get(nom, 0)
        if asig >= hrs_req:
            if ultimo_dia.get(nom, 999) <= dl:
                c += 1
            else:
                f += 1
        else:
            f += 1
    return c, f

def divide_y_venceras(temas, dias, hpd):
    if not temas or dias <= 0:
        return {}, 0, len(temas)
    plan = _dyv(temas, 1, dias, hpd)
    c, f = _dyv_indicadores(plan, temas)
    return plan, c, f


# ══════════════════════════════════════════════════════════════════════════════
# MEDICIÓN CON TIMEOUT REAL (threading)
# ══════════════════════════════════════════════════════════════════════════════

TIMEOUT_SEG = 15   # segundos máximos por técnica por caso

def medir(func, temas, dias, hpd, timeout=TIMEOUT_SEG):
    """
    Ejecuta func en un hilo con timeout real.
    Devuelve (completados, fuera, tiempo_ms) o None si timeout/error.
    """
    box = [None, None]   # box[0] = resultado, box[1] = ms

    def _run():
        try:
            t0 = time.perf_counter()
            res = func(temas, dias, hpd)
            box[1] = (time.perf_counter() - t0) * 1000
            box[0] = res
        except Exception:
            pass

    hilo = threading.Thread(target=_run, daemon=True)
    hilo.start()
    hilo.join(timeout=timeout)

    if hilo.is_alive() or box[0] is None:
        return None   # timeout o error

    _, c, f = box[0]
    return (c, f, box[1])


# ══════════════════════════════════════════════════════════════════════════════
# TABLA COMPARATIVA — Rúbrica Entrega 3
# ══════════════════════════════════════════════════════════════════════════════

TECNICAS = ["Fuerza Bruta", "Recursivo", "Greedy", "Backtracking", "Divide y Vencerás"]
COMP_T   = ["O(n! · n)",    "O(días^n)", "O(n log n)", "O(días^n)*", "O(n log n)"]
COMP_E   = ["O(n! · días)", "O(n·días)", "O(n·días)",  "O(n·días)",   "O(n·días)"]
OPTIMA   = ["Sí",           "Sí",        "No",          "Sí",          "Aproximada"]

COLORES = {
    "Fuerza Bruta":      "#e74c3c",
    "Recursivo":         "#3498db",
    "Greedy":            "#2ecc71",
    "Backtracking":      "#f39c12",
    "Divide y Vencerás": "#9b59b6",
}
MARCADORES = {
    "Fuerza Bruta": "o", "Recursivo": "s", "Greedy": "^",
    "Backtracking": "D", "Divide y Vencerás": "*",
}


def imprimir_tabla(resultados, n_por_caso):
    SEP = "═" * 115
    print("\n" + SEP)
    print("  TABLA COMPARATIVA FINAL — Sistema de Planificación Óptima de Estudio")
    print(SEP)

    # Complejidades
    print(f"\n  {'Técnica':<24} {'Comp. Temporal':<22} {'Comp. Espacial':<16} {'¿Óptima?'}")
    print(f"  {'-'*24} {'-'*22} {'-'*16} {'-'*12}")
    for i, t in enumerate(TECNICAS):
        print(f"  {t:<24} {COMP_T[i]:<22} {COMP_E[i]:<16} {OPTIMA[i]}")
    print("  * Backtracking con poda de cota superior: mejor en promedio que el peor caso.")

    # Tiempos por caso
    casos = list(resultados.keys())
    print(f"\n  {'Técnica':<24}", end="")
    for caso in casos:
        n = n_por_caso.get(caso, "?")
        etiq = f"{caso}(n={n})"
        print(f"  {etiq:>26}", end="")
    print()
    print(f"  {'-'*24}", end="")
    for _ in casos:
        print(f"  {'─'*26}", end="")
    print()

    for t in TECNICAS:
        print(f"  {t:<24}", end="")
        for caso in casos:
            r = resultados[caso].get(t)
            if r is None:
                celda = "TIMEOUT / N/A"
            else:
                celda = f"c={r[0]} f={r[1]} {r[2]:.2f}ms"
            print(f"  {celda:>26}", end="")
        print()
    print()


# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS
# ══════════════════════════════════════════════════════════════════════════════

def _guardar(fig, ruta):
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"    Guardada: {ruta}")


def grafica_tiempos(resultados, carpeta):
    """Barras de tiempo de ejecución por técnica, un subplot por caso."""
    casos = list(resultados.keys())
    fig, axes = plt.subplots(1, len(casos), figsize=(5 * len(casos), 5), sharey=False)
    if len(casos) == 1:
        axes = [axes]

    for ax, caso in zip(axes, casos):
        ts   = []
        cols = []
        etiq = []
        for t in TECNICAS:
            r = resultados[caso].get(t)
            ts.append(r[2] if r else 0)
            cols.append(COLORES[t])
            etiq.append(t.replace("Divide y Vencerás", "DyV").replace(" ", "\n", 1))

        barras = ax.bar(range(len(TECNICAS)), ts, color=cols, edgecolor="white", linewidth=0.7)
        ax.set_title(caso, fontsize=10, fontweight="bold")
        ax.set_xticks(range(len(TECNICAS)))
        ax.set_xticklabels(etiq, fontsize=7)
        ax.set_ylabel("Tiempo (ms)" if caso == casos[0] else "")

        positivos = [v for v in ts if v > 0]
        if len(positivos) >= 2 and max(positivos) / min(positivos) > 50:
            ax.set_yscale("log")

        for bar, v in zip(barras, ts):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() * 1.05,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=6.5)

    fig.suptitle("Tiempo de Ejecución por Técnica (escala log cuando aplica)",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    _guardar(fig, os.path.join(carpeta, "grafica_tiempos.png"))


def grafica_calidad(resultados, carpeta):
    """Barras agrupadas: completados a tiempo vs fuera de plazo."""
    casos = list(resultados.keys())
    fig, axes = plt.subplots(1, len(casos), figsize=(5 * len(casos), 5))
    if len(casos) == 1:
        axes = [axes]
    ancho = 0.35

    for ax, caso in zip(axes, casos):
        comps  = [(resultados[caso].get(t) or (0,0,0))[0] for t in TECNICAS]
        fueras = [(resultados[caso].get(t) or (0,0,0))[1] for t in TECNICAS]
        x = range(len(TECNICAS))
        ax.bar([i - ancho/2 for i in x], comps,  ancho, label="Completados",    color="#2ecc71", edgecolor="white")
        ax.bar([i + ancho/2 for i in x], fueras, ancho, label="Fuera de plazo", color="#e74c3c", edgecolor="white")
        ax.set_title(caso, fontsize=10, fontweight="bold")
        ax.set_xticks(list(x))
        etiq = [t.replace("Divide y Vencerás", "DyV").replace(" ", "\n", 1) for t in TECNICAS]
        ax.set_xticklabels(etiq, fontsize=7)
        ax.set_ylabel("Temas" if caso == casos[0] else "")
        ax.legend(fontsize=8)

    fig.suptitle("Calidad de Solución: Temas Completados vs Fuera de Plazo",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    _guardar(fig, os.path.join(carpeta, "grafica_calidad.png"))


def grafica_escalabilidad(resultados_todos, n_por_caso, carpeta):
    """Tiempo vs n para todas las técnicas disponibles."""
    fig, ax = plt.subplots(figsize=(10, 6))

    for t in TECNICAS:
        pares = []
        for caso, res in resultados_todos.items():
            r = res.get(t)
            if r is not None:
                pares.append((n_por_caso[caso], r[2]))
        if pares:
            pares.sort()
            ns = [p[0] for p in pares]
            ts = [p[1] for p in pares]
            ax.plot(ns, ts, marker=MARCADORES[t], color=COLORES[t],
                    label=t, linewidth=2, markersize=8)

    ax.set_xlabel("Número de temas (n)", fontsize=12)
    ax.set_ylabel("Tiempo de ejecución (ms)", fontsize=12)
    ax.set_title("Escalabilidad: Tiempo de Ejecución vs Tamaño de Entrada",
                 fontsize=13, fontweight="bold")
    ax.set_yscale("log")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    _guardar(fig, os.path.join(carpeta, "grafica_escalabilidad.png"))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    carpeta_datos  = "1-Datos"
    carpeta_salida = "."

    casos_completos = [
        ("Pequeño", "1-caso_pequeno.txt"),
        ("Mediano", "2-caso_mediano.txt"),
        ("Grande",  "3-caso_grande.txt"),
    ]
    casos_grandes = [
        ("n=100",  "4-caso_100.txt"),
        ("n=1000", "5-caso_1000.txt"),
    ]

    FUNCS_TODAS = {
        "Fuerza Bruta":      fuerza_bruta,
        "Recursivo":         recursivo,
        "Greedy":            greedy,
        "Backtracking":      backtracking,
        "Divide y Vencerás": divide_y_venceras,
    }
    FUNCS_RAPIDAS = {
        "Greedy":            greedy,
        "Divide y Vencerás": divide_y_venceras,
    }

    resultados = {}
    n_por_caso = {}

    # ── Casos pequeño / mediano / grande ─────────────────────────────────────
    print("\n" + "═"*72)
    print("  EJECUTANDO — Pequeño, Mediano, Grande  (5 técnicas, timeout=15s c/u)")
    print("═"*72)
    for nombre, archivo in casos_completos:
        ruta = os.path.join(carpeta_datos, archivo)
        if not os.path.exists(ruta):
            print(f"  [OMITIDO] {ruta}")
            continue
        temas, dias, hpd = leer_caso(ruta)
        n_por_caso[nombre] = len(temas)
        resultados[nombre] = {}
        print(f"\n  Caso '{nombre}' — n={len(temas)}, {dias} días, {hpd}h/día")
        for t_nom, func in FUNCS_TODAS.items():
            print(f"    → {t_nom:<24}", end=" ", flush=True)
            r = medir(func, temas, dias, hpd)
            resultados[nombre][t_nom] = r
            if r:
                print(f"completados={r[0]}, fuera={r[1]}, {r[2]:.4f} ms")
            else:
                print(f"TIMEOUT (>{TIMEOUT_SEG}s) — impracticable")

    # ── Casos grandes ─────────────────────────────────────────────────────────
    print("\n" + "═"*72)
    print("  EJECUTANDO — n=100 y n=1000  (solo Greedy y Divide y Vencerás)")
    print("  Fuerza Bruta, Recursivo y Backtracking son computacionalmente")
    print("  impracticables a esta escala (O(n!) y O(dias^n)).")
    print("═"*72)
    for nombre, archivo in casos_grandes:
        ruta = os.path.join(carpeta_datos, archivo)
        if not os.path.exists(ruta):
            print(f"  [OMITIDO] {ruta}")
            continue
        temas, dias, hpd = leer_caso(ruta)
        n_por_caso[nombre] = len(temas)
        resultados[nombre] = {}
        print(f"\n  Caso '{nombre}' — n={len(temas)}, {dias} días, {hpd}h/día")
        for t_nom in TECNICAS:
            if t_nom in FUNCS_RAPIDAS:
                print(f"    → {t_nom:<24}", end=" ", flush=True)
                r = medir(FUNCS_RAPIDAS[t_nom], temas, dias, hpd)
                resultados[nombre][t_nom] = r
                if r:
                    print(f"completados={r[0]}, fuera={r[1]}, {r[2]:.4f} ms")
                else:
                    print("TIMEOUT / ERROR")
            else:
                print(f"    → {t_nom:<24} N/A (impracticable para n={len(temas)})")
                resultados[nombre][t_nom] = None

    # ── Tabla ─────────────────────────────────────────────────────────────────
    imprimir_tabla(resultados, n_por_caso)

    # ── Gráficas ──────────────────────────────────────────────────────────────
    if GRAFICAS:
        print("  Generando gráficas...")
        res_graf = {k: v for k, v in resultados.items() if k in dict(casos_completos)}
        grafica_tiempos(res_graf, carpeta_salida)
        grafica_calidad(res_graf, carpeta_salida)
        grafica_escalabilidad(resultados, n_por_caso, carpeta_salida)
    else:
        print("  [AVISO] Instala matplotlib para gráficas: pip install matplotlib")

    print("\n  ¡Comparativa completada!\n")


if __name__ == "__main__":
    main()