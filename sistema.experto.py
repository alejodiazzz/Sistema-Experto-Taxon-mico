"""
Sistema Experto para Identificación Taxonómica de Animales
Motor de Inferencia: durable_rules (algoritmo Rete, encadenamiento hacia adelante)
Interfaz Gráfica: Tkinter
UPTC — Escuela de Ingeniería de Sistemas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from durable.lang import *

# ──────────────────────────────────────────────────────────────
#  BASE DE CONOCIMIENTO — 18 reglas de producción
# ──────────────────────────────────────────────────────────────

resultado_inferencia = {"clase": None, "razon": None, "regla": None}

with ruleset("taxonomia"):

    # ── MAMMALIA (4 reglas) ──────────────────────────────────

    @when_all(
        (m.tiene_pelo == "si") &
        (m.es_viviparo == "si") &
        (m.temperatura == "homeoterma")
    )
    def mamifero_basico(c):
        resultado_inferencia["clase"] = "Mammalia"
        resultado_inferencia["razon"] = "Tiene pelo + es vivíparo + homeoterma"
        resultado_inferencia["regla"] = "R1"

    @when_all(
        (m.tiene_pelo == "si") &
        (m.vive_en_agua == "si") &
        (m.es_viviparo == "si")
    )
    def mamifero_acuatico(c):
        resultado_inferencia["clase"] = "Mammalia (acuático)"
        resultado_inferencia["razon"] = "Tiene pelo + vive en agua + vivíparo (ej. ballena, delfín)"
        resultado_inferencia["regla"] = "R2"

    @when_all(
        (m.tiene_pelo == "si") &
        (m.es_oviparo == "si") &
        (m.temperatura == "homeoterma")
    )
    def mamifero_oviparo(c):
        resultado_inferencia["clase"] = "Mammalia (monotrema)"
        resultado_inferencia["razon"] = "Tiene pelo + ovíparo + homeoterma (ej. ornitorrinco)"
        resultado_inferencia["regla"] = "R3"

    @when_all(
        (m.tiene_pelo == "si") &
        (m.alimentacion == "herbivoro") &
        (m.temperatura == "homeoterma")
    )
    def mamifero_herbivoro(c):
        resultado_inferencia["clase"] = "Mammalia (herbívoro)"
        resultado_inferencia["razon"] = "Tiene pelo + herbívoro + homeoterma (ej. vaca, caballo)"
        resultado_inferencia["regla"] = "R4"

    # ── AVES (4 reglas) ──────────────────────────────────────

    @when_all(
        (m.tiene_plumas == "si") &
        (m.es_oviparo == "si") &
        (m.temperatura == "homeoterma")
    )
    def ave_basica(c):
        resultado_inferencia["clase"] = "Aves"
        resultado_inferencia["razon"] = "Tiene plumas + ovíparo + homeoterma"
        resultado_inferencia["regla"] = "R5"

    @when_all(
        (m.tiene_plumas == "si") &
        (m.vive_en_agua == "si") &
        (m.es_oviparo == "si")
    )
    def ave_acuatica(c):
        resultado_inferencia["clase"] = "Aves (acuática)"
        resultado_inferencia["razon"] = "Tiene plumas + vive en agua + ovíparo (ej. pingüino, pato)"
        resultado_inferencia["regla"] = "R6"

    @when_all(
        (m.tiene_plumas == "si") &
        (m.alimentacion == "carnivoro") &
        (m.temperatura == "homeoterma")
    )
    def ave_rapaz(c):
        resultado_inferencia["clase"] = "Aves (rapaz)"
        resultado_inferencia["razon"] = "Tiene plumas + carnívoro + homeoterma (ej. águila, halcón)"
        resultado_inferencia["regla"] = "R7"

    @when_all(
        (m.tiene_plumas == "si") &
        (m.alimentacion == "herbivoro") &
        (m.temperatura == "homeoterma")
    )
    def ave_herbivora(c):
        resultado_inferencia["clase"] = "Aves (granívora/herbívora)"
        resultado_inferencia["razon"] = "Tiene plumas + herbívora + homeoterma (ej. paloma, loro)"
        resultado_inferencia["regla"] = "R8"

    # ── REPTILIA (4 reglas) ──────────────────────────────────

    @when_all(
        (m.tiene_escamas == "si") &
        (m.es_oviparo == "si") &
        (m.temperatura == "ectoterma") &
        (m.vive_en_agua == "no")
    )
    def reptil_terrestre(c):
        resultado_inferencia["clase"] = "Reptilia (terrestre)"
        resultado_inferencia["razon"] = "Tiene escamas + ovíparo + ectoterma + terrestre (ej. lagarto, serpiente)"
        resultado_inferencia["regla"] = "R9"

    @when_all(
        (m.tiene_escamas == "si") &
        (m.es_oviparo == "si") &
        (m.temperatura == "ectoterma") &
        (m.vive_en_agua == "si")
    )
    def reptil_acuatico(c):
        resultado_inferencia["clase"] = "Reptilia (acuático)"
        resultado_inferencia["razon"] = "Tiene escamas + ovíparo + ectoterma + acuático (ej. cocodrilo, tortuga marina)"
        resultado_inferencia["regla"] = "R10"

    @when_all(
        (m.tiene_escamas == "si") &
        (m.es_viviparo == "si") &
        (m.temperatura == "ectoterma")
    )
    def reptil_viviparo(c):
        resultado_inferencia["clase"] = "Reptilia (vivíparo)"
        resultado_inferencia["razon"] = "Tiene escamas + vivíparo + ectoterma (ej. boa, víbora)"
        resultado_inferencia["regla"] = "R11"

    @when_all(
        (m.tiene_escamas == "si") &
        (m.alimentacion == "carnivoro") &
        (m.temperatura == "ectoterma") &
        (m.tiene_piel_humeda == "no")
    )
    def reptil_carnivoro(c):
        if not resultado_inferencia["clase"]:
            resultado_inferencia["clase"] = "Reptilia (carnívoro)"
            resultado_inferencia["razon"] = "Tiene escamas + carnívoro + ectoterma (ej. varano, cocodrilo)"
            resultado_inferencia["regla"] = "R12"

    # ── AMPHIBIA (3 reglas) ──────────────────────────────────

    @when_all(
        (m.tiene_piel_humeda == "si") &
        (m.larva_acuatica == "si") &
        (m.temperatura == "ectoterma")
    )
    def anfibio_basico(c):
        resultado_inferencia["clase"] = "Amphibia"
        resultado_inferencia["razon"] = "Piel húmeda + larva acuática + ectoterma"
        resultado_inferencia["regla"] = "R13"

    @when_all(
        (m.tiene_piel_humeda == "si") &
        (m.vive_en_agua == "si") &
        (m.tiene_escamas == "no") &
        (m.tiene_pelo == "no")
    )
    def anfibio_acuatico(c):
        resultado_inferencia["clase"] = "Amphibia (acuático)"
        resultado_inferencia["razon"] = "Piel húmeda + acuático + sin escamas + sin pelo (ej. salamandra acuática)"
        resultado_inferencia["regla"] = "R14"

    @when_all(
        (m.tiene_piel_humeda == "si") &
        (m.es_oviparo == "si") &
        (m.temperatura == "ectoterma") &
        (m.tiene_escamas == "no")
    )
    def anfibio_oviparo(c):
        resultado_inferencia["clase"] = "Amphibia (ovíparo)"
        resultado_inferencia["razon"] = "Piel húmeda + ovíparo + ectoterma + sin escamas (ej. rana, sapo)"
        resultado_inferencia["regla"] = "R15"

    # ── ACTINOPTERYGII / PECES (3 reglas) ────────────────────

    @when_all(
        (m.tiene_aletas == "si") &
        (m.vive_en_agua == "si") &
        (m.tiene_escamas == "si") &
        (m.temperatura == "ectoterma")
    )
    def pez_basico(c):
        resultado_inferencia["clase"] = "Actinopterygii (pez óseo)"
        resultado_inferencia["razon"] = "Aletas + acuático + escamas + ectoterma (ej. trucha, salmón)"
        resultado_inferencia["regla"] = "R16"

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

    @when_all(
        (m.tiene_aletas == "si") &
        (m.vive_en_agua == "si") &
        (m.es_oviparo == "si") &
        (m.tiene_pelo == "no") &
        (m.tiene_plumas == "no")
    )
    def pez_oviparo(c):
        resultado_inferencia["clase"] = "Actinopterygii (pez ovíparo)"
        resultado_inferencia["razon"] = "Aletas + acuático + ovíparo + sin pelo + sin plumas"
        resultado_inferencia["regla"] = "R18"


# ──────────────────────────────────────────────────────────────
#  FUNCIÓN DE INFERENCIA
# ──────────────────────────────────────────────────────────────

def inferir(atributos: dict) -> dict:
    """
    Recibe un diccionario de atributos del animal,
    aserta los hechos en durable_rules y retorna el resultado.
    """
    resultado_inferencia["clase"] = None
    resultado_inferencia["razon"] = None
    resultado_inferencia["regla"] = None

    try:
        # Construir hecho con todos los atributos
        hecho = dict(atributos)
        assert_fact("taxonomia", hecho)
    except Exception:
        pass  # Si la regla ya fue disparada o hay colisión, continuar

    return dict(resultado_inferencia)


# ──────────────────────────────────────────────────────────────
#  INTERFAZ GRÁFICA — TKINTER
# ──────────────────────────────────────────────────────────────

class SistemaExpertoGUI:

    OPCIONES_BINARIAS = ["si", "no"]
    OPCIONES_TEMP = ["homeoterma", "ectoterma"]
    OPCIONES_ALIM = ["carnivoro", "herbivoro", "omnivoro"]

    CAMPOS = [
        ("tiene_pelo",       "¿Tiene pelo?",                  OPCIONES_BINARIAS),
        ("tiene_plumas",     "¿Tiene plumas?",                OPCIONES_BINARIAS),
        ("tiene_escamas",    "¿Tiene escamas?",               OPCIONES_BINARIAS),
        ("tiene_piel_humeda","¿Tiene piel húmeda y sin pelo?",OPCIONES_BINARIAS),
        ("tiene_aletas",     "¿Tiene aletas?",                OPCIONES_BINARIAS),
        ("es_oviparo",       "¿Es ovíparo (pone huevos)?",    OPCIONES_BINARIAS),
        ("es_viviparo",      "¿Es vivíparo?",                 OPCIONES_BINARIAS),
        ("vive_en_agua",     "¿Vive principalmente en agua?", OPCIONES_BINARIAS),
        ("larva_acuatica",   "¿Su larva/cría es acuática?",   OPCIONES_BINARIAS),
        ("temperatura",      "Regulación térmica:",           ["homeoterma", "ectoterma"]),
        ("alimentacion",     "Tipo de alimentación:",         ["carnivoro", "herbivoro", "omnivoro"]),
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema Experto — Identificación Taxonómica de Animales")
        self.root.geometry("820x680")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(True, True)

        self.vars = {}
        self._construir_ui()

    def _construir_ui(self):
        # ── Título ────────────────────────────────────────────
        frm_titulo = tk.Frame(self.root, bg="#1a3a5c", pady=10)
        frm_titulo.pack(fill="x")
        tk.Label(
            frm_titulo,
            text="🦁  Sistema Experto para Identificación Taxonómica",
            font=("Helvetica", 14, "bold"),
            fg="white", bg="#1a3a5c"
        ).pack()
        tk.Label(
            frm_titulo,
            text="Motor: durable_rules (Rete) | UPTC — Ingeniería de Sistemas",
            font=("Helvetica", 9),
            fg="#aac4e0", bg="#1a3a5c"
        ).pack()

        # ── Contenedor principal ──────────────────────────────
        frm_main = tk.Frame(self.root, bg="#f0f4f8")
        frm_main.pack(fill="both", expand=True, padx=15, pady=10)

        # columna izquierda: preguntas
        frm_izq = tk.LabelFrame(
            frm_main, text=" Características del Animal ",
            font=("Helvetica", 10, "bold"),
            bg="#f0f4f8", fg="#1a3a5c",
            bd=2, relief="groove"
        )
        frm_izq.pack(side="left", fill="both", expand=True, padx=(0, 8))

        for campo, etiqueta, opciones in self.CAMPOS:
            frm_row = tk.Frame(frm_izq, bg="#f0f4f8", pady=3)
            frm_row.pack(fill="x", padx=10)

            tk.Label(
                frm_row, text=etiqueta,
                font=("Helvetica", 9), bg="#f0f4f8",
                anchor="w", width=32
            ).pack(side="left")

            var = tk.StringVar(value=opciones[0])
            self.vars[campo] = var

            combo = ttk.Combobox(
                frm_row, textvariable=var,
                values=opciones, state="readonly",
                width=12, font=("Helvetica", 9)
            )
            combo.pack(side="left", padx=5)

        # Botones
        frm_btns = tk.Frame(frm_izq, bg="#f0f4f8", pady=8)
        frm_btns.pack(fill="x", padx=10)

        tk.Button(
            frm_btns, text="🔍  Inferir Clase",
            command=self._inferir,
            font=("Helvetica", 10, "bold"),
            bg="#1a7a4a", fg="white",
            relief="flat", padx=10, pady=6,
            cursor="hand2"
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            frm_btns, text="🔄  Limpiar",
            command=self._limpiar,
            font=("Helvetica", 10),
            bg="#c0392b", fg="white",
            relief="flat", padx=10, pady=6,
            cursor="hand2"
        ).pack(side="left")

        # columna derecha: resultado + traza
        frm_der = tk.Frame(frm_main, bg="#f0f4f8")
        frm_der.pack(side="right", fill="both", expand=True)

        # panel resultado
        frm_res = tk.LabelFrame(
            frm_der, text=" Resultado de Inferencia ",
            font=("Helvetica", 10, "bold"),
            bg="#f0f4f8", fg="#1a3a5c",
            bd=2, relief="groove"
        )
        frm_res.pack(fill="x", pady=(0, 8))

        self.lbl_clase = tk.Label(
            frm_res,
            text="—",
            font=("Helvetica", 18, "bold"),
            fg="#1a7a4a", bg="#f0f4f8"
        )
        self.lbl_clase.pack(pady=(8, 2))

        self.lbl_razon = tk.Label(
            frm_res,
            text="Ingresa las características y presiona 'Inferir'",
            font=("Helvetica", 9),
            fg="#555", bg="#f0f4f8",
            wraplength=340, justify="center"
        )
        self.lbl_razon.pack(pady=(0, 10))

        # panel traza
        frm_traza = tk.LabelFrame(
            frm_der, text=" Traza de Razonamiento ",
            font=("Helvetica", 10, "bold"),
            bg="#f0f4f8", fg="#1a3a5c",
            bd=2, relief="groove"
        )
        frm_traza.pack(fill="both", expand=True)

        self.txt_traza = tk.Text(
            frm_traza,
            font=("Courier", 9),
            bg="#1e1e2e", fg="#cdd6f4",
            relief="flat", padx=8, pady=6,
            wrap="word", state="disabled"
        )
        scr = ttk.Scrollbar(frm_traza, command=self.txt_traza.yview)
        self.txt_traza.configure(yscrollcommand=scr.set)
        scr.pack(side="right", fill="y")
        self.txt_traza.pack(fill="both", expand=True, padx=4, pady=4)

        # barra de estado
        self.lbl_estado = tk.Label(
            self.root,
            text="Listo — Selecciona las características del animal",
            font=("Helvetica", 8), bg="#d0dce8",
            anchor="w", padx=8
        )
        self.lbl_estado.pack(fill="x", side="bottom")

    # ── Lógica ─────────────────────────────────────────────────

    def _inferir(self):
        """Recopila los atributos, llama al motor de inferencia y muestra resultado."""
        atributos = {campo: var.get() for campo, var in self.vars.items()}

        self.lbl_estado.config(text="Procesando inferencia...")
        self.root.update_idletasks()

        resultado = inferir(atributos)

        if resultado["clase"]:
            self.lbl_clase.config(text=resultado["clase"], fg="#1a7a4a")
            self.lbl_razon.config(text=f"Razón: {resultado['razon']}")
            self.lbl_estado.config(
                text=f"✔ Clasificación completada — Regla activada: {resultado['regla']}"
            )
            self._mostrar_traza(atributos, resultado)
        else:
            self.lbl_clase.config(text="Sin clasificación", fg="#c0392b")
            self.lbl_razon.config(
                text="No se encontró una regla que coincida con los atributos ingresados. "
                     "Verifica que la combinación sea válida."
            )
            self.lbl_estado.config(text="⚠ No se activó ninguna regla")
            self._mostrar_traza_vacia(atributos)

    def _mostrar_traza(self, atributos: dict, resultado: dict):
        """Escribe la traza del razonamiento en el panel de texto."""
        self.txt_traza.config(state="normal")
        self.txt_traza.delete("1.0", "end")

        lineas = [
            "═══════════════════════════════════════",
            "   TRAZA DE INFERENCIA — durable_rules",
            "═══════════════════════════════════════",
            "",
            "① HECHOS ASERTADOS:",
        ]
        for k, v in atributos.items():
            lineas.append(f"   • {k} = {v}")

        lineas += [
            "",
            "② MOTOR RETE — Evaluación de reglas:",
            f"   → Regla {resultado['regla']} ACTIVADA",
            "",
            "③ CONSECUENTE DERIVADO:",
            f"   ✔ Clase: {resultado['clase']}",
            f"   ✔ Razón: {resultado['razon']}",
            "",
            "═══════════════════════════════════════",
        ]

        self.txt_traza.insert("end", "\n".join(lineas))
        self.txt_traza.config(state="disabled")

    def _mostrar_traza_vacia(self, atributos: dict):
        self.txt_traza.config(state="normal")
        self.txt_traza.delete("1.0", "end")
        lineas = [
            "═══════════════════════════════════════",
            "   TRAZA — Sin coincidencia de reglas",
            "═══════════════════════════════════════",
            "",
            "① HECHOS ASERTADOS:",
        ]
        for k, v in atributos.items():
            lineas.append(f"   • {k} = {v}")
        lineas += [
            "",
            "② MOTOR RETE — Ninguna regla satisfecha",
            "   → Combina mejor los atributos del animal",
            "═══════════════════════════════════════",
        ]
        self.txt_traza.insert("end", "\n".join(lineas))
        self.txt_traza.config(state="disabled")

    def _limpiar(self):
        """Resetea todos los campos al valor por defecto."""
        for campo, _, opciones in self.CAMPOS:
            self.vars[campo].set(opciones[0])
        self.lbl_clase.config(text="—", fg="#1a7a4a")
        self.lbl_razon.config(
            text="Ingresa las características y presiona 'Inferir'"
        )
        self.txt_traza.config(state="normal")
        self.txt_traza.delete("1.0", "end")
        self.txt_traza.config(state="disabled")
        self.lbl_estado.config(text="Listo — Selecciona las características del animal")


# ──────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoGUI(root)
    root.mainloop()