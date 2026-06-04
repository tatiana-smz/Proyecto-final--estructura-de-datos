"""
EXAMEN FINAL - ESTRUCTURAS DE DATOS
Árbol AVL Interactivo — Interfaz Gráfica Tkinter
Estudiante: MEDINA ZAMBRANO TATIANA STEFANY
Codigo: 20252578026 - Estudiante #15
Secuencia: 77, 47, 102, 37, 62, 87, 107, 60, 61, 59, 58, 63
"""

import tkinter as tk
from tkinter import messagebox
import time
import random

# ═══════════════════════════════════════════════════════
#  LÓGICA AVL — igual que el código base de terminal
# ═══════════════════════════════════════════════════════

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1
        # posición visual (asignada al dibujar)
        self.x = 0
        self.y = 0

class ArbolAVL:
    def __init__(self):
        self.raiz      = None
        self.rotaciones = 0
        self.log       = []

    def altura(self, nodo):
        return nodo.altura if nodo else 0

    def factor_equilibrio(self, nodo):
        return self.altura(nodo.izq) - self.altura(nodo.der) if nodo else 0

    def actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    def rotar_derecha(self, y):
        x = y.izq; T2 = x.der
        x.der = y; y.izq = T2
        self.actualizar_altura(y); self.actualizar_altura(x)
        self.rotaciones += 1
        self._log(f"Rotacion DERECHA sobre nodo {y.valor}")
        return x

    def rotar_izquierda(self, x):
        y = x.der; T2 = y.izq
        y.izq = x; x.der = T2
        self.actualizar_altura(x); self.actualizar_altura(y)
        self.rotaciones += 1
        self._log(f"Rotacion IZQUIERDA sobre nodo {x.valor}")
        return y

    def balancear(self, nodo):
        self.actualizar_altura(nodo)
        fe = self.factor_equilibrio(nodo)
        if fe > 1 and self.factor_equilibrio(nodo.izq) >= 0:
            self._log(f"Desbalance en {nodo.valor}: caso Izq-Izq")
            return self.rotar_derecha(nodo)
        if fe > 1 and self.factor_equilibrio(nodo.izq) < 0:
            self._log(f"Desbalance en {nodo.valor}: caso Izq-Der")
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)
        if fe < -1 and self.factor_equilibrio(nodo.der) <= 0:
            self._log(f"Desbalance en {nodo.valor}: caso Der-Der")
            return self.rotar_izquierda(nodo)
        if fe < -1 and self.factor_equilibrio(nodo.der) > 0:
            self._log(f"Desbalance en {nodo.valor}: caso Der-Izq")
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)
        return nodo

    def _insertar(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)
        else:
            self._log(f"{valor} ya existe, se ignora")
            return nodo
        return self.balancear(nodo)

    def insertar(self, valor):
        self._log(f"INSERT {valor}")
        self.raiz = self._insertar(self.raiz, valor)
        self._log(f"  Altura: {self.altura(self.raiz)}  FE raiz: {self.factor_equilibrio(self.raiz)}")

    def _minimo(self, nodo):
        while nodo.izq: nodo = nodo.izq
        return nodo

    def _eliminar(self, nodo, valor):
        if nodo is None: return None
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if not nodo.izq: return nodo.der
            if not nodo.der: return nodo.izq
            sucesor = self._minimo(nodo.der)
            nodo.valor = sucesor.valor
            nodo.der = self._eliminar(nodo.der, sucesor.valor)
        return self.balancear(nodo)

    def eliminar(self, valor):
        if not self.buscar(valor, silencioso=True):
            self._log(f"DELETE {valor} -> No existe")
            return False
        self._log(f"DELETE {valor}")
        self.raiz = self._eliminar(self.raiz, valor)
        self._log(f"  Altura: {self.altura(self.raiz)}  FE raiz: {self.factor_equilibrio(self.raiz)}")
        return True

    def buscar(self, valor, silencioso=False):
        camino = []; nodo = self.raiz
        while nodo:
            camino.append(nodo)
            if valor == nodo.valor:
                if not silencioso:
                    self._log(f"SEARCH {valor} -> Camino: {' -> '.join(str(n.valor) for n in camino)} ENCONTRADO")
                return True
            nodo = nodo.izq if valor < nodo.valor else nodo.der
        if not silencioso:
            self._log(f"SEARCH {valor} -> Camino: {' -> '.join(str(n.valor) for n in camino)} NO ENCONTRADO")
        return False

    def buscar_camino(self, valor):
        """Devuelve lista de nodos del camino (para animación)."""
        camino = []; nodo = self.raiz
        while nodo:
            camino.append(nodo)
            if valor == nodo.valor: return camino, True
            nodo = nodo.izq if valor < nodo.valor else nodo.der
        return camino, False

    def inorden(self):
        r = []
        def f(n):
            if n: f(n.izq); r.append(n.valor); f(n.der)
        f(self.raiz); return r

    def preorden(self):
        r = []
        def f(n):
            if n: r.append(n.valor); f(n.izq); f(n.der)
        f(self.raiz); return r

    def postorden(self):
        r = []
        def f(n):
            if n: f(n.izq); f(n.der); r.append(n.valor)
        f(self.raiz); return r

    def contar_nodos(self):
        def c(n): return 0 if not n else 1 + c(n.izq) + c(n.der)
        return c(self.raiz)

    def _log(self, msg):
        self.log.append(msg)


# ═══════════════════════════════════════════════════════
#  COLORES Y CONSTANTES VISUALES
# ═══════════════════════════════════════════════════════

 
BG         = "#0e0818"   # fondo negro con tono morado
PANEL      = "#1a0f2e"   # panel morado muy oscuro
BORDE      = "#4a2080"   # borde morado medio
ACENTO     = "#d4a8e8"   # lila claro — titulos y detalles
VERDE      = "#9b4dca"   # morado medio — boton cargar secuencia
AMARILLO   = "#7ecfed"   # azul claro — boton buscar
ROJO       = "#c084fc"   # lila — boton eliminar
MORADO     = "#4ab8d8"   # azul medio — boton aleatorio
TEXTO      = "#ede9fe"   # blanco con tono lila
GRIS       = "#8b7aaa"   # gris morado — texto secundario
 
NODO_NORMAL  = "#2d1054"   # nodo en reposo morado oscuro
NODO_BORDE   = "#d4a8e8"   # borde lila claro
NODO_NUEVO   = "#9b4dca"   # insertar morado medio
NODO_BUSCAR  = "#7ecfed"   # buscando azul claro
NODO_FOUND   = "#4ab8d8"   # encontrado azul medio
NODO_DELETE  = "#f472b6"   # eliminar rosa fucsia (contraste)
NODO_ROTAR   = "#6b2d9e"   # rotacion morado oscuro
 
R = 22   # radio del nodo

# ═══════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════

SECUENCIA_15 = [77, 47, 102, 37, 62, 87, 107, 60, 61, 59, 58, 63]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol AVL — Tatiana Stefany Medina Zambrano #15")
        self.geometry("1300x750")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.arbol    = ArbolAVL()
        self.velocidad = 600   # ms entre pasos de animación
        self._job     = None   # referencia al after() en curso
        # colores especiales temporales por nodo id()
        self._colores = {}

        self._construir_ui()
        self._log_gui("Bienvenida, Tatiana! Carga la secuencia #15 o inserta nodos.")

    # ───────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ───────────────────────────────────────────

    def _construir_ui(self):
        # ── Encabezado ──
        hdr = tk.Frame(self, bg="#0a0f1e", pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text="AVL INTERACTIVO",
                 fg=ACENTO, bg="#0a0f1e",
                 font=("Courier New", 16, "bold")).pack(side="left", padx=16)
        tk.Label(hdr, text="MEDINA ZAMBRANO TATIANA STEFANY  ·  20252578026  ·  #15",
                 fg=GRIS, bg="#0a0f1e",
                 font=("Courier New", 10)).pack(side="left")

        # ── Contenedor principal ──
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        # Panel izquierdo
        izq = tk.Frame(main, bg=PANEL, width=220)
        izq.pack(side="left", fill="y")
        izq.pack_propagate(False)
        self._panel_izquierdo(izq)

        # Canvas central
        centro = tk.Frame(main, bg=BG)
        centro.pack(side="left", fill="both", expand=True)
        self._panel_canvas(centro)

        # Panel derecho
        der = tk.Frame(main, bg=PANEL, width=260)
        der.pack(side="right", fill="y")
        der.pack_propagate(False)
        self._panel_derecho(der)

    # ── Panel izquierdo: controles ──
    def _panel_izquierdo(self, f):
        def seccion(txt):
            tk.Label(f, text=txt, fg=ACENTO, bg=PANEL,
                     font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(12,2))
            tk.Frame(f, bg=BORDE, height=1).pack(fill="x", padx=12, pady=(0,6))

        # Insertar
        seccion("INSERTAR")
        fila = tk.Frame(f, bg=PANEL); fila.pack(fill="x", padx=12, pady=(0,8))
        self.v_ins = tk.StringVar()
        e = tk.Entry(fila, textvariable=self.v_ins, bg="#0f172a", fg=TEXTO,
                     insertbackground=TEXTO, font=("Courier New", 13),
                     relief="flat", bd=4, width=7)
        e.pack(side="left", expand=True, fill="x")
        e.bind("<Return>", lambda _: self._insertar())
        tk.Button(fila, text="+", bg=ACENTO, fg="#000",
                  font=("Courier New", 13, "bold"), relief="flat",
                  padx=6, command=self._insertar).pack(side="right")

        # Eliminar
        seccion("ELIMINAR")
        fila2 = tk.Frame(f, bg=PANEL); fila2.pack(fill="x", padx=12, pady=(0,8))
        self.v_del = tk.StringVar()
        e2 = tk.Entry(fila2, textvariable=self.v_del, bg="#0f172a", fg=TEXTO,
                      insertbackground=TEXTO, font=("Courier New", 13),
                      relief="flat", bd=4, width=7)
        e2.pack(side="left", expand=True, fill="x")
        e2.bind("<Return>", lambda _: self._eliminar())
        tk.Button(fila2, text="–", bg=ROJO, fg="#000",
                  font=("Courier New", 13, "bold"), relief="flat",
                  padx=6, command=self._eliminar).pack(side="right")

        # Buscar
        seccion("BUSCAR (animado)")
        fila3 = tk.Frame(f, bg=PANEL); fila3.pack(fill="x", padx=12, pady=(0,8))
        self.v_bus = tk.StringVar()
        e3 = tk.Entry(fila3, textvariable=self.v_bus, bg="#0f172a", fg=TEXTO,
                      insertbackground=TEXTO, font=("Courier New", 13),
                      relief="flat", bd=4, width=7)
        e3.pack(side="left", expand=True, fill="x")
        e3.bind("<Return>", lambda _: self._buscar())
        tk.Button(fila3, text="?", bg=AMARILLO, fg="#000",
                  font=("Courier New", 13, "bold"), relief="flat",
                  padx=6, command=self._buscar).pack(side="right")

        # Velocidad
        seccion("VELOCIDAD")
        self.v_vel = tk.IntVar(value=5)
        self.lbl_vel = tk.Label(f, text="600 ms", fg=ACENTO, bg=PANEL,
                                font=("Courier New", 9))
        self.lbl_vel.pack(anchor="e", padx=14)
        tk.Scale(f, from_=1, to=10, variable=self.v_vel, orient="horizontal",
                 bg=PANEL, fg=TEXTO, troughcolor=BORDE, highlightthickness=0,
                 command=self._actualizar_vel).pack(fill="x", padx=12, pady=(0,8))

        # Acciones
        seccion("ACCIONES")
        botones = [
            ("Cargar Secuencia #15", VERDE,  "#000", self._cargar_secuencia),
            ("Generar Aleatorio",    MORADO, "#fff", self._generar_aleatorio),
            ("Reiniciar Arbol",      ROJO,   "#fff", self._reiniciar),
        ]
        for txt, bg, fg, cmd in botones:
            tk.Button(f, text=txt, bg=bg, fg=fg,
                      font=("Courier New", 10, "bold"), relief="flat",
                      pady=5, command=cmd).pack(fill="x", padx=12, pady=2)

        # Leyenda
        seccion("LEYENDA")
        leyenda = [
            (NODO_NUEVO,  "Nodo nuevo"),
            (NODO_BUSCAR, "Buscando"),
            (NODO_FOUND,  "Encontrado"),
            (NODO_DELETE, "Eliminado"),
            (NODO_ROTAR,  "Rotacion"),
        ]
        for color, txt in leyenda:
            fila_ley = tk.Frame(f, bg=PANEL)
            fila_ley.pack(anchor="w", padx=14, pady=1)
            tk.Canvas(fila_ley, width=14, height=14, bg=PANEL,
                      highlightthickness=0).pack(side="left")
            c = tk.Canvas(fila_ley, width=14, height=14, bg=PANEL, highlightthickness=0)
            c.pack(side="left")
            c.create_oval(1, 1, 13, 13, fill=color, outline="")
            tk.Label(fila_ley, text=txt, fg=GRIS, bg=PANEL,
                     font=("Courier New", 9)).pack(side="left", padx=4)

    # ── Canvas central ──
    def _panel_canvas(self, parent):
        self.canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Estado en la parte de arriba
        self.lbl_estado = tk.Label(parent, text="Listo",
                                   fg=ACENTO, bg=BG,
                                   font=("Courier New", 11))
        self.lbl_estado.place(relx=0.5, rely=0.0, anchor="n", y=6)

        self.canvas.bind("<Configure>", lambda _: self._dibujar())

    # ── Panel derecho: estadísticas + log ──
    def _panel_derecho(self, f):
        tk.Label(f, text="ESTADÍSTICAS", fg=ACENTO, bg=PANEL,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(12,2))
        tk.Frame(f, bg=BORDE, height=1).pack(fill="x", padx=12, pady=(0,8))

        self.stats = {}
        grid = tk.Frame(f, bg=PANEL); grid.pack(fill="x", padx=12, pady=(0,8))
        campos = [("Nodos","nodos"),("Altura","altura"),
                  ("Rotaciones","rots"),("FE raiz","fe")]
        for i, (lbl, key) in enumerate(campos):
            card = tk.Frame(grid, bg="#0f172a", padx=4, pady=4)
            card.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
            grid.columnconfigure(i%2, weight=1)
            var = tk.StringVar(value="0")
            self.stats[key] = var
            tk.Label(card, textvariable=var, fg=ACENTO, bg="#0f172a",
                     font=("Courier New", 18, "bold")).pack()
            tk.Label(card, text=lbl, fg=GRIS, bg="#0f172a",
                     font=("Courier New", 8)).pack()

        # Recorridos
        tk.Label(f, text="RECORRIDOS", fg=ACENTO, bg=PANEL,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(8,2))
        tk.Frame(f, bg=BORDE, height=1).pack(fill="x", padx=12, pady=(0,6))
        self.v_inorden   = tk.StringVar(value="—")
        self.v_preorden  = tk.StringVar(value="—")
        self.v_postorden = tk.StringVar(value="—")
        for lbl, var in [("Inorden", self.v_inorden),
                         ("Preorden", self.v_preorden),
                         ("Postorden", self.v_postorden)]:
            tk.Label(f, text=lbl+":", fg=GRIS, bg=PANEL,
                     font=("Courier New", 8)).pack(anchor="w", padx=14)
            tk.Label(f, textvariable=var, fg=TEXTO, bg=PANEL,
                     font=("Courier New", 8), wraplength=230,
                     justify="left").pack(anchor="w", padx=14, pady=(0,4))

        # Log
        tk.Label(f, text="LOG DE OPERACIONES", fg=ACENTO, bg=PANEL,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=12, pady=(8,2))
        tk.Frame(f, bg=BORDE, height=1).pack(fill="x", padx=12, pady=(0,6))

        scroll = tk.Scrollbar(f)
        scroll.pack(side="right", fill="y", padx=(0,4))
        self.log_box = tk.Text(f, bg="#0a0f1e", fg=TEXTO,
                               font=("Courier New", 8), relief="flat",
                               state="disabled", yscrollcommand=scroll.set,
                               wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=(12,0))
        scroll.config(command=self.log_box.yview)

        # colores log
        for tag, col in [("insert", VERDE), ("delete", ROJO),
                         ("search", AMARILLO), ("rotate", MORADO),
                         ("info", ACENTO)]:
            self.log_box.tag_config(tag, foreground=col)

        tk.Button(f, text="Limpiar log", bg=PANEL, fg=GRIS,
                  font=("Courier New", 8), relief="flat",
                  command=self._limpiar_log).pack(pady=4)

    # ───────────────────────────────────────────
    #  DIBUJO DEL ÁRBOL
    # ───────────────────────────────────────────

    def _asignar_posiciones(self, nodo, contador):
        """Inorden: cada nodo recibe columna única — nunca se enciman."""
        if nodo is None:
            return
        self._asignar_posiciones(nodo.izq, contador)
        nodo._col = contador[0]
        contador[0] += 1
        self._asignar_posiciones(nodo.der, contador)

    def _dibujar(self, highlight=None):
        """
        highlight: dict { id(nodo): color } para resaltar nodos específicos.
        """
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 2 or H < 2 or not self.arbol.raiz:
            if not self.arbol.raiz:
                c.create_text(W//2, H//2,
                              text="Árbol vacío\nInserta un nodo o carga la secuencia #15",
                              fill=GRIS, font=("Courier New", 13), justify="center")
            return

        # Asignar columnas
        contador = [0]
        self._asignar_posiciones(self.arbol.raiz, contador)
        total = contador[0]

        celda  = max(52, W // max(total, 1))
        margen_top = 50

        # Calcular coordenadas x,y de cada nodo
        def calcular_xy(nodo, nivel):
            if nodo is None: return
            nodo.x = nodo._col * celda + celda // 2
            nodo.y = margen_top + nivel * 80
            calcular_xy(nodo.izq, nivel + 1)
            calcular_xy(nodo.der, nivel + 1)

        calcular_xy(self.arbol.raiz, 0)

        # Dibujar aristas
        def dibujar_aristas(nodo):
            if nodo is None: return
            for hijo in (nodo.izq, nodo.der):
                if hijo:
                    c.create_line(nodo.x, nodo.y, hijo.x, hijo.y,
                                  fill=BORDE, width=2)
                    dibujar_aristas(hijo)

        dibujar_aristas(self.arbol.raiz)

        # Dibujar nodos
        def dibujar_nodo(nodo):
            if nodo is None: return
            x, y = nodo.x, nodo.y
            fe   = self.arbol.factor_equilibrio(nodo)

            # Color según highlight
            if highlight and id(nodo) in highlight:
                relleno  = highlight[id(nodo)]
                contorno = relleno
                color_txt = "#000" if relleno not in (NODO_ROTAR,) else "#fff"
            else:
                relleno   = NODO_NORMAL
                contorno  = NODO_BORDE
                color_txt = TEXTO

            # Sombra
            c.create_oval(x-R+3, y-R+3, x+R+3, y+R+3,
                          fill="#000000", outline="", stipple="gray25")
            # Círculo
            c.create_oval(x-R, y-R, x+R, y+R,
                          fill=relleno, outline=contorno, width=2)
            # Valor
            c.create_text(x, y-3, text=str(nodo.valor),
                          fill=color_txt,
                          font=("Courier New", 11, "bold"))
            # h y fe debajo
            fe_color = ROJO if abs(fe) > 1 else GRIS
            c.create_text(x, y+R+10,
                          text=f"h:{nodo.altura} fe:{fe}",
                          fill=fe_color,
                          font=("Courier New", 8))

            dibujar_nodo(nodo.izq)
            dibujar_nodo(nodo.der)

        dibujar_nodo(self.arbol.raiz)

    def _actualizar_stats(self):
        a = self.arbol
        self.stats["nodos"].set(str(a.contar_nodos()))
        self.stats["altura"].set(str(a.altura(a.raiz)))
        self.stats["rots"].set(str(a.rotaciones))
        fe = a.factor_equilibrio(a.raiz) if a.raiz else "N/A"
        self.stats["fe"].set(str(fe))
        self.v_inorden.set(str(a.inorden()))
        self.v_preorden.set(str(a.preorden()))
        self.v_postorden.set(str(a.postorden()))

    # ───────────────────────────────────────────
    #  LOG
    # ───────────────────────────────────────────

    def _log_gui(self, msg, tag="info"):
        self.log_box.config(state="normal")
        self.log_box.insert("1.0", msg + "\n", tag)
        self.log_box.config(state="disabled")

    def _volcar_log_arbol(self):
        """Vuelca los mensajes nuevos del arbol al log de la GUI."""
        for msg in self.arbol.log:
            if   "INSERT"    in msg: tag = "insert"
            elif "DELETE"    in msg: tag = "delete"
            elif "SEARCH"    in msg: tag = "search"
            elif "Rotacion"  in msg: tag = "rotate"
            else:                    tag = "info"
            self._log_gui(msg, tag)
        self.arbol.log.clear()

    def _limpiar_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

    def _estado(self, msg):
        self.lbl_estado.config(text=msg)

    # ───────────────────────────────────────────
    #  ANIMACIÓN GENÉRICA
    # ───────────────────────────────────────────

    def _animar_nodo(self, nodo, color, duracion, callback=None):
        """Resalta un nodo con color durante duracion ms y luego llama callback."""
        self._dibujar(highlight={id(nodo): color})
        if callback:
            self.after(duracion, callback)

    def _animar_secuencia(self, nodos, colores, idx=0, al_final=None):
        """
        Anima una lista de nodos uno por uno.
        nodos  : lista de NodoAVL
        colores: lista de colores (uno por nodo, o uno solo para todos)
        """
        if idx >= len(nodos):
            self._dibujar()
            if al_final: al_final()
            return
        nodo  = nodos[idx]
        color = colores[idx] if isinstance(colores, list) else colores
        self._dibujar(highlight={id(nodo): color})
        self._job = self.after(self.velocidad,
                               lambda: self._animar_secuencia(nodos, colores, idx+1, al_final))

    # ───────────────────────────────────────────
    #  OPERACIONES
    # ───────────────────────────────────────────

    def _get_int(self, var):
        try:    return int(var.get().strip())
        except: return None

    def _insertar(self):
        v = self._get_int(self.v_ins)
        if v is None:
            self._estado("Ingresa un numero valido"); return
        self.arbol.insertar(v)
        self._volcar_log_arbol()
        self._actualizar_stats()
        self.v_ins.set("")

        # Animación: resaltar el nodo nuevo en verde
        nodo = self._buscar_nodo(self.arbol.raiz, v)
        if nodo:
            self._dibujar(highlight={id(nodo): NODO_NUEVO})
            self.after(self.velocidad * 2, self._dibujar)
        else:
            self._dibujar()
        self._estado(f"Insertado: {v}")

    def _eliminar(self):
        v = self._get_int(self.v_del)
        if v is None:
            self._estado("Ingresa un numero valido"); return
        nodo = self._buscar_nodo(self.arbol.raiz, v)
        if not nodo:
            self._estado(f"{v} no existe"); return
        # Animación: rojo → luego eliminar
        self._dibujar(highlight={id(nodo): NODO_DELETE})
        self.v_del.set("")
        self.after(self.velocidad, lambda: self._hacer_eliminar(v))

    def _hacer_eliminar(self, v):
        self.arbol.eliminar(v)
        self._volcar_log_arbol()
        self._actualizar_stats()
        self._dibujar()
        self._estado(f"Eliminado: {v}")

    def _buscar(self):
        v = self._get_int(self.v_bus)
        if v is None:
            self._estado("Ingresa un numero valido"); return
        camino, encontrado = self.arbol.buscar_camino(v)
        self.arbol.buscar(v)           # registra en log
        self._volcar_log_arbol()
        self.v_bus.set("")
        self._estado(f"Buscando {v}...")

        # Colores: amarillo para el camino, verde/rojo para el final
        colores = []
        for i, n in enumerate(camino):
            if i == len(camino) - 1:
                colores.append(NODO_FOUND if encontrado else NODO_DELETE)
            else:
                colores.append(NODO_BUSCAR)

        def al_final():
            self._estado(f"{v} {'ENCONTRADO' if encontrado else 'NO ENCONTRADO'}")
            self.after(800, self._dibujar)

        self._animar_secuencia(camino, colores, al_final=al_final)

    def _cargar_secuencia(self):
        self.arbol = ArbolAVL()
        self._dibujar()
        self._actualizar_stats()
        self._log_gui(f"Cargando secuencia #15: {SECUENCIA_15}", "info")
        self._cargar_paso(SECUENCIA_15, 0)

    def _cargar_paso(self, seq, idx):
        if idx >= len(seq):
            self._dibujar()
            self._actualizar_stats()
            self._estado("Secuencia #15 cargada!")
            self._log_gui("Secuencia completa.", "info")
            return
        v = seq[idx]
        self.arbol.insertar(v)
        self._volcar_log_arbol()
        self._actualizar_stats()
        nodo = self._buscar_nodo(self.arbol.raiz, v)
        hl   = {id(nodo): NODO_NUEVO} if nodo else {}
        self._dibujar(highlight=hl)
        self._estado(f"Insertando {v}...")
        self._job = self.after(self.velocidad, lambda: self._cargar_paso(seq, idx+1))

    def _generar_aleatorio(self):
        self.arbol = ArbolAVL()
        n    = random.randint(5, 15)
        vals = random.sample(range(1, 150), n)
        self._log_gui(f"Aleatorio: {vals}", "info")
        self._cargar_paso(vals, 0)

    def _reiniciar(self):
        if self._job: self.after_cancel(self._job)
        self.arbol = ArbolAVL()
        self._dibujar()
        self._actualizar_stats()
        self._log_gui("Arbol reiniciado.", "info")
        self._estado("Arbol reiniciado")

    # ───────────────────────────────────────────
    #  UTILIDAD: encontrar nodo por valor
    # ───────────────────────────────────────────

    def _buscar_nodo(self, raiz, valor):
        if raiz is None: return None
        if raiz.valor == valor: return raiz
        return self._buscar_nodo(raiz.izq, valor) if valor < raiz.valor \
               else self._buscar_nodo(raiz.der, valor)

    def _actualizar_vel(self, _=None):
        v = self.v_vel.get()
        self.velocidad = int(1100 - v * 100)
        self.lbl_vel.config(text=f"{self.velocidad} ms")


# ═══════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()