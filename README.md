# Sistema de Planificación Óptima de Estudio con Restricciones

> **Análisis y Diseño de Algoritmos **  
> Docente: Juan Esteban Gómez Tirado  
> Integrantes: Juan Manuel Moreno Muñoz · Andres Felipe Ortega Solano · Juan Esteban Vallejo

---

## Descripción

Sistema que genera un plan de estudio óptimo para un estudiante que debe prepararse para varias materias en un tiempo limitado. Cada tema tiene materia, dificultad, horas requeridas y fecha límite. El sistema distribuye los temas en los días disponibles respetando la capacidad diaria y minimizando los temas fuera de plazo.

El objetivo principal es **comparar cinco técnicas algorítmicas** aplicadas al mismo problema, evaluando eficiencia, complejidad y calidad de solución.

---

## Técnicas Implementadas

| # | Técnica | Complejidad Temporal | ¿Óptima? | ¿Escala a n=1000? |
|---|---------|----------------------|----------|-------------------|
| 1 | Fuerza Bruta | O(n! · n) |  Sí — revisa todo |  No |
| 2 | Recursivo | O(días^n) |  Sí — explora todo |  No |
| 3 | Greedy | O(n log n) |  No garantizado |  Sí |
| 4 | Backtracking | O(días^n) + poda |  Sí — poda ramas imposibles | ❌ No |
| 5 | Divide y Vencerás | O(n log n) |  Aproximada |  Sí |

> **¿Óptima significa rápida?** No. Una técnica es óptima si garantiza la mejor solución posible cuando termina de ejecutar. Fuerza Bruta, Recursivo y Backtracking son óptimas porque no se les escapa ninguna combinación — pero para n grande tardan años. Greedy siempre termina rápido pero puede perder la mejor solución.

---

## Estructura del Proyecto

```
trabajo-final/
├── README.md
├── 1-Datos/
│   ├── 1-caso_pequeno.txt       # n=3  temas, 4 días, 4h/día
│   ├── 2-caso_mediano.txt       # n=6  temas, 8 días, 5h/día
│   ├── 3-caso_grande.txt        # n=10 temas, 10 días, 6h/día
│   ├── 4-caso_100.txt           # n=100 temas generados (seed=42)
│   └── 5-caso_1000.txt          # n=1000 temas generados (seed=42)
├── 2-Src/
│   ├── 1-Fuerza_bruta.py
│   ├── 2-recursivo.py
│   ├── 3-greedy.py
│   ├── 4-backtracking.py
│   ├── 5-divide_y_venceras.py
│   └── 6-comparativa.py        # ejecuta todo y genera las 3 gráficas
├── 3-Docs/
│   ├── entrega1.pdf
│   ├── entrega2.pdf
│   └── entrega3_final.pdf
└── 4-Presentacion/
    └── presentacion_final.pdf
```

---

## Cómo Ejecutar

**Requisito previo:** tener Python instalado. Para las gráficas:

```bash
pip install matplotlib
```

### Ejecutar cada técnica individualmente

```bash
# Desde la raíz del proyecto
python 2-Src/1-Fuerza_bruta.py       # corre casos pequeño, mediano, grande + aviso n=100/1000
python 2-Src/2-recursivo.py           # igual
python 2-Src/3-greedy.py              # corre TODOS los casos incluyendo n=100 y n=1000
python 2-Src/4-backtracking.py        # corre pequeño, mediano, grande + aviso n=100/1000
python 2-Src/5-divide_y_venceras.py   # corre TODOS los casos incluyendo n=100 y n=1000
```

### Ejecutar la comparativa completa

```bash
python 2-Src/6-comparativa.py
```

Ejecuta las 5 técnicas con timeout de 15 segundos por caso, imprime la tabla comparativa y genera:

```
grafica_tiempos.png        → tiempo de ejecución por técnica (escala log)
grafica_calidad.png        → temas completados vs fuera de plazo
grafica_escalabilidad.png  → tiempo vs tamaño de entrada (n)
```

---

## Entradas del Sistema

Cada archivo `.txt` en `1-Datos/` sigue este formato:

```
Materia,Nombre,Dificultad,Horas,Deadline
Matemáticas,Integrales,5,3,3
Física,Cinemática,4,2,2
Química,Átomos,3,2,4
dias=4
horas_por_dia=4
```

| Campo | Descripción |
|---|---|
| Materia | Nombre de la asignatura |
| Nombre | Nombre del tema |
| Dificultad | Escala de 1 (fácil) a 5 (difícil) |
| Horas | Horas necesarias para estudiar el tema |
| Deadline | Día máximo para completarlo |

---

## Salidas del Sistema

Todos los algoritmos siguen el mismo formato de salida:

```
==================================================
  CASO GREEDY: Mediano
==================================================

  Dia 1 :
    [Inglés] Reading - 2h
    [Matemáticas] Derivadas - 3h

  Completados a tiempo : 6
  Fuera de plazo       : 0
  Tiempo de ejecucion  : 0.018433 ms
```

Para los casos n=100 y n=1000, Fuerza Bruta, Recursivo y Backtracking muestran:

```
==================================================
  CASO: n=100
==================================================
  Fuerza Bruta es IMPRACTICABLE para n = 100
  Complejidad : O(n! * n)
  Resultado   : N/A
```

---

## Resultados Obtenidos

### Tiempos de ejecución reales

| Técnica | n=3 | n=6 | n=10 | n=100 | n=1000 |
|---|---|---|---|---|---|
| Fuerza Bruta | 0.03 ms | 2.35 ms | ~31,000 ms | N/A | N/A |
| Recursivo | 0.08 ms | 204 ms | TIMEOUT | N/A | N/A |
| Greedy | 0.01 ms | 0.02 ms | 0.02 ms | 0.11 ms | 1.24 ms |
| Backtracking | 0.02 ms | 0.03 ms | 0.05 ms | N/A | N/A |
| Divide y Vencerás | 0.07 ms | 0.03 ms | 0.05 ms | 0.18 ms | 0.82 ms |

### Calidad de solución (temas completados a tiempo)

| Técnica | n=3 | n=6 | n=10 |
|---|---|---|---|
| Fuerza Bruta | 3/3  | 6/6  | 10/10  |
| Recursivo | 3/3  | 6/6  | TIMEOUT |
| Greedy | 3/3  | 6/6  | 10/10  |
| Backtracking | 3/3  | 6/6  | 10/10  |
| Divide y Vencerás | 3/3  | 5/6  | 8/10  |

### Conclusión

La técnica más adecuada para este problema es **Greedy**: escala a cualquier tamaño en O(n log n), obtiene el resultado óptimo en todos los casos de prueba y es la más simple de implementar. Backtracking con poda es la mejor técnica exacta para n pequeño, pero no escala a n=100.

---

## Integrantes y Contribuciones

| Integrante | Contribución principal |
|---|---|
| Juan Manuel Moreno Muñoz | Fuerza Bruta, Recursivo, análisis de complejidad |
| Andres Felipe Ortega Solano | Greedy, Backtracking, casos de prueba |
| Juan Esteban Vallejo | Divide y Vencerás, comparativa, documento final |

---

## Consideraciones

- Todo el código fue desarrollado en **Python puro** sin librerías externas de optimización.
- Los datos de prueba n=100 y n=1000 fueron generados por el equipo con `seed=42` (reproducibles).
- Cada integrante contribuyó con commits propios al repositorio.
- El código que corre con timeout (Fuerza Bruta y Recursivo en n=10) lo hace en la máquina local — los tiempos pueden variar según el hardware.
