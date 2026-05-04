#  Planificador de Estudio con Algoritmos

##  Descripción

Este proyecto consiste en el desarrollo de un sistema de planificación de estudio óptimo, utilizando diferentes técnicas de diseño de algoritmos.

El problema se basa en organizar un conjunto de temas de distintas materias, considerando restricciones como tiempo disponible, dificultad y fechas límite, con el objetivo de generar un horario eficiente.

---

##  Objetivo

Comparar distintas técnicas algorítmicas para resolver un mismo problema de optimización, evaluando su eficiencia, complejidad y calidad de solución.

---

## ⚙️ Técnicas implementadas

- 🔴 Fuerza Bruta  
- 🔵 Recursividad  
- 🟢 Greedy  
- 🟣 Backtracking  
- 🟡 Divide y Vencerás  

---

##  Entradas del sistema

- Lista de temas:
  - Materia
  - Nombre
  - Dificultad
  - Horas requeridas
  - Fecha límite
- Restricciones:
  - Horas disponibles por día
  - Número de días

---

##  Salidas del sistema

- Plan de estudio organizado por días
- Distribución de horas por tema
- Indicadores de cumplimiento

---

##  Estructura del proyecto

```
trabajo-final/
├── README.md                  
├── datos/                     
│   ├── caso_pequeno.txt
│   ├── caso_mediano.txt
│   └── caso_grande.txt
├── src/
│   ├── fuerza_bruta.py
│   ├── recursivo.py
│   ├── greedy.py
│   ├── backtracking.py
│   ├── divide_y_venceras.py
│   └── comparativa.py         
├── docs/
│   ├── entrega1.pdf
│   ├── entrega2.pdf
│   └── entrega3_final.pdf
└── presentacion/
    └── presentacion_final.pdf
```

---
##  Metodología

Se implementa cada técnica algorítmica sobre el mismo problema y se comparan:

- Tiempo de ejecución
- Complejidad computacional
- Calidad de la solución

---

##  Cómo ejecutar cada codigo

