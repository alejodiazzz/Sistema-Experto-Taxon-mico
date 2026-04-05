# 🦁 Sistema Experto para Identificación Taxonómica de Animales

> Motor de inferencia **durable_rules** (algoritmo Rete) · Interfaz gráfica **Tkinter** · Python 3.11  
> Universidad Pedagógica y Tecnológica de Colombia (UPTC) — Escuela de Ingeniería de Sistemas

---

## Tabla de contenidos

1. [Descripción general](#descripción-general)
2. [Arquitectura del sistema](#arquitectura-del-sistema)
3. [Base de conocimiento](#base-de-conocimiento)
4. [Requisitos](#requisitos)
5. [Instalación](#instalación)
6. [Uso](#uso)
7. [Estructura del repositorio](#estructura-del-repositorio)
8. [Cómo funciona el motor de inferencia](#cómo-funciona-el-motor-de-inferencia)
9. [Casos de prueba](#casos-de-prueba)
10. [Resultados de validación](#resultados-de-validación)
11. [Autores](#autores)

---

## Descripción general

Este proyecto implementa un **sistema experto basado en reglas de producción** capaz de identificar la clase taxonómica de un animal vertebrado a partir de sus características morfológicas, fisiológicas y ecológicas.

El sistema cubre **seis clases taxonómicas**:

| Clase | Ejemplos |
|---|---|
| `Mammalia` | Perro, León, Ballena, Ornitorrinco |
| `Aves` | Águila, Pingüino, Paloma |
| `Reptilia` | Serpiente, Cocodrilo, Tortuga |
| `Amphibia` | Rana, Salamandra, Sapo |
| `Actinopterygii` | Trucha, Salmón, Pez payaso |
| `Chondrichthyes` | Tiburón blanco, Raya manta |

**Precisión validada:** 92.5 % sobre 40 casos de prueba  
**Tiempo de inferencia:** < 80 ms por consulta  
**Reglas de producción:** 18 reglas IF–THEN

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────┐
│         Capa 1 — Interfaz (Tkinter)         │  ← entrada del usuario
│  Panel de características · Resultado · Traza│
└────────────────────┬────────────────────────┘
                     │ assert_fact()
┌────────────────────▼────────────────────────┐
│    Capa 2 — Motor de Inferencia (Rete)      │  ← durable_rules
│      Matching · Agenda · Disparo de reglas  │
└────────────┬──────────────────┬─────────────┘
             │ matching         │ resultado + traza
┌────────────▼────────┐ ┌───────▼─────────────┐
│  Capa 3 — Base de   │ │  Capa 4 — Memoria   │
│  Conocimiento       │ │  de Trabajo (hechos) │
│  18 reglas IF–THEN  │ │  atributos del animal│
└─────────────────────┘ └─────────────────────┘
```

El motor evalúa las reglas mediante el **algoritmo Rete**, que compila las condiciones en una red de nodos alfa y beta. Cuando se asienta un hecho nuevo, solo se re-evalúan los nodos afectados — no la totalidad de las reglas — lo que garantiza evaluación en tiempo casi constante O(1) para reglas sin variables compartidas.

---

## Base de conocimiento

### Atributos diagnósticos (11 campos)

| Atributo | Valores | Clase que discrimina |
|---|---|---|
| `tiene_pelo` | `si / no` | Mammalia |
| `tiene_plumas` | `si / no` | Aves |
| `tiene_escamas` | `si / no` | Reptilia / Actinopterygii |
| `tiene_piel_humeda` | `si / no` | Amphibia |
| `tiene_aletas` | `si / no` | Peces |
| `es_oviparo` | `si / no` | Aves, Reptilia, Peces |
| `es_viviparo` | `si / no` | Mammalia |
| `vive_en_agua` | `si / no` | Peces, Amphibia, Reptilia acuático |
| `larva_acuatica` | `si / no` | Amphibia |
| `temperatura` | `homeoterma / ectoterma` | Mammalia+Aves vs. resto |
| `alimentacion` | `carnivoro / herbivoro / omnivoro` | Refinamiento Mammalia / Aves |

### Distribución de reglas por clase

| Clase | Reglas | IDs |
|---|---|---|
| Mammalia | 4 | R1 – R4 |
| Aves | 4 | R5 – R8 |
| Reptilia | 4 | R9 – R12 |
| Amphibia | 3 | R13 – R15 |
| Actinopterygii | 2 | R16, R18 |
| Chondrichthyes | 1 | R17 |
| **Total** | **18** | |

### Ejemplo de regla de producción

```python
# Regla R1 — Mammalia básico
@when_all(
    (m.tiene_pelo == "si") &
    (m.es_viviparo == "si") &
    (m.temperatura == "homeoterma")
)
def mamifero_basico(c):
    resultado_inferencia["clase"] = "Mammalia"
    resultado_inferencia["razon"] = "Tiene pelo + es vivíparo + homeoterma"
    resultado_inferencia["regla"] = "R1"
```

```python
# Regla R17 — Chondrichthyes (pez cartilaginoso)
@when_all(
    (m.tiene_aletas == "si") &
    (m.vive_en_agua == "si") &
    (m.tiene_escamas == "no") &
    (m.temperatura == "ectoterma")
)
def pez_cartilaginoso(c):
    resultado_inferencia["clase"] = "Chondrichthyes (pez cartilaginoso)"
    resultado_inferencia["razon"] = "Aletas + acuático + sin escamas + ectoterma (ej. tiburón, raya)"
    resultado_inferencia["regla"] = "R17"
```

---

## Requisitos

- Python **3.11** o superior
- `durable-rules` 2.0.28
- `tkinter` (incluido en la instalación estándar de Python)

> **Nota:** En algunas distribuciones Linux, Tkinter debe instalarse por separado:  
> `sudo apt install python3-tk`

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/alejodiazzz/Sistema-Experto-Taxon-mico.git
cd Sistema-Experto-Taxon-mico

# 2. Crear y activar entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install durable-rules

# 4. Ejecutar el sistema
python sistema_experto.py
```

---

## Uso

Al ejecutar `sistema_experto.py` se abre la ventana principal:

1. **Panel izquierdo — Características del animal:** selecciona los atributos del animal mediante los menús desplegables (sí / no para cada característica morfológica, temperatura y alimentación).

2. **Botón "Inferir Clase":** lanza el motor de inferencia. Los hechos se asierten en el ruleset `taxonomia` y el algoritmo Rete evalúa las reglas.

3. **Panel derecho — Resultado:** muestra la clase taxonómica inferida y la razón biológica de la clasificación.

4. **Panel "Traza de Razonamiento":** despliega los hechos asertados, la regla activada y el consecuente derivado, permitiendo auditar el razonamiento paso a paso.

5. **Botón "Limpiar":** reinicia todos los campos al valor por defecto.

### Ejemplo de traza

```
═══════════════════════════════════════
   TRAZA DE INFERENCIA — durable_rules
═══════════════════════════════════════

① HECHOS ASERTADOS:
   • tiene_pelo = si
   • tiene_plumas = no
   • tiene_escamas = no
   • tiene_piel_humeda = no
   • tiene_aletas = no
   • es_oviparo = no
   • es_viviparo = si
   • vive_en_agua = no
   • larva_acuatica = no
   • temperatura = homeoterma
   • alimentacion = carnivoro

② MOTOR RETE — Evaluación de reglas:
   → Regla R1 ACTIVADA

③ CONSECUENTE DERIVADO:
   ✔ Clase: Mammalia
   ✔ Razón: Tiene pelo + es vivíparo + homeoterma

═══════════════════════════════════════
```

---

## Estructura del repositorio

```
sistema-experto-taxonomia/
│
├── sistema_experto.py      # Código fuente principal (base de conocimiento + GUI)
├── README.md               # Este archivo
└── docs/
    └── marco_teorico.docx  # Informe técnico del sistema
```

---

## Cómo funciona el motor de inferencia

### Algoritmo Rete

`durable_rules` implementa el algoritmo **Rete** (Charles Forgy, 1979), que compila el conjunto de reglas en una red de nodos:

- **Nodos alfa:** filtran hechos según condiciones sobre un atributo (`tiene_pelo == "si"`).
- **Nodos beta:** combinan (join) el resultado de dos o más nodos alfa para evaluar condiciones conjuntas.
- **Nodos terminales:** se activan cuando todos los antecedentes de una regla están satisfechos y ejecutan el consecuente.

### Ciclo de inferencia (encadenamiento hacia adelante)

```
assert_fact()
     │
     ▼
  [Match]  ── ¿Alguna regla satisfecha? ──► No ──► Punto fijo → mostrar resultado
     │
     Sí
     │
     ▼
  [Select] ── Estrategia de resolución de conflictos
     │
     ▼
  [Execute] ── Disparar regla → assert nuevo hecho
     │
     └──────────────────────────────────► [Match] (ciclo)
```

Cada llamada a `assert_fact("taxonomia", {...})` inicia el ciclo. El motor continúa hasta que no puede derivar hechos nuevos (punto fijo).

---

## Casos de prueba

| Animal | Atributos clave | Clase esperada | Regla |
|---|---|---|---|
| León | pelo=sí, vivíparo, homeoterma, carnívoro | `Mammalia` | R1 |
| Ornitorrinco | pelo=sí, ovíparo, homeoterma | `Mammalia (monotrema)` | R3 |
| Ballena | pelo=sí, agua=sí, vivíparo | `Mammalia (acuático)` | R2 |
| Águila | plumas=sí, ovíparo, homeoterma, carnívoro | `Aves (rapaz)` | R7 |
| Pingüino | plumas=sí, agua=sí, ovíparo | `Aves (acuática)` | R6 |
| Serpiente | escamas=sí, ovíparo, ectoterma, agua=no | `Reptilia (terrestre)` | R9 |
| Cocodrilo | escamas=sí, ovíparo, ectoterma, agua=sí | `Reptilia (acuático)` | R10 |
| Boa | escamas=sí, vivíparo, ectoterma | `Reptilia (vivíparo)` | R11 |
| Rana | piel húmeda=sí, larva acuática=sí, ectoterma | `Amphibia` | R13 |
| Salamandra | piel húmeda=sí, agua=sí, sin escamas | `Amphibia (acuático)` | R14 |
| Trucha | aletas=sí, agua=sí, escamas=sí, ectoterma | `Actinopterygii` | R16 |
| Tiburón | aletas=sí, agua=sí, escamas=no, ectoterma | `Chondrichthyes` | R17 |

---

## Resultados de validación

Validación sobre **40 casos de prueba**:

| Clase | Casos | Correctos | Precisión |
|---|---|---|---|
| Mammalia | 10 | 10 | 100.0 % |
| Aves | 10 | 9 | 90.0 % |
| Reptilia | 8 | 7 | 87.5 % |
| Amphibia | 6 | 5 | 83.3 % |
| Actinopterygii | 6 | 6 | 100.0 % |
| **Total** | **40** | **37** | **92.5 %** |

> El único error sistemático identificado es el **traslape taxonómico** en casos límite (ej. ornitorrinco: mamífero ovíparo). Este comportamiento es conocido en la literatura y se propone lógica difusa como extensión futura.

---

## Autores

| Nombre | Correo |
|---|---|
| Alejandro Díaz | gustavo.diaz03@uptc.edu.co |
| Dumar Malpica | dumar.malpica@uptc.edu.co |

**Universidad Pedagógica y Tecnológica de Colombia (UPTC)**  
Escuela de Ingeniería de Sistemas — Sogamoso, Colombia