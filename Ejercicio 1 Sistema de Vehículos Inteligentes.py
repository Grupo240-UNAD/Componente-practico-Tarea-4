import tkinter as tk
from tkinter import ttk, font
import time
import math

class Vehiculo:
    """Clase base para todos los vehículos del sistema."""

    def __init__(self, marca, modelo):
        self.marca = marca                  # Almacena la marca del vehículo
        self.modelo = modelo                # Almacena el modelo del vehículo
        self.velocidad_actual = 0           # Velocidad inicial en 0
        self.total_aceleraciones = 0        # Contador de veces que aceleró
        self.velocidad_maxima = 0           # Registra la velocidad máxima alcanzada

    def acelerar(self, turbo=False, terreno="normal"):
        """Incrementa la velocidad según el tipo, turbo y terreno."""
        incremento = 10                     # Incremento base del vehículo normal
        if turbo:
            incremento += 10               # Turbo suma 10 km/h adicionales
        if terreno == "mountain":
            incremento -= 5                # Terreno montañoso reduce el incremento
        elif terreno == "track":
            incremento += 5                # Pista de carreras aumenta el incremento

        self.velocidad_actual += incremento                        # Aplica el incremento
        self.total_aceleraciones += 1                              # Registra la aceleración
        self.velocidad_maxima = max(self.velocidad_maxima,         # Actualiza velocidad máxima
                                    self.velocidad_actual)

    def frenar(self):
        """Reduce la velocidad gradualmente en 20 km/h."""
        self.velocidad_actual = max(0, self.velocidad_actual - 20) # No permite velocidades negativas

    def detener(self):
        """Detiene el vehículo por completo."""
        self.velocidad_actual = 0           # Resetea la velocidad a 0

    def estado(self):
        """Devuelve el nivel de velocidad como texto."""
        if self.velocidad_actual == 0:
            return "Detenido"
        elif self.velocidad_actual < 40:
            return "Lento"
        elif self.velocidad_actual < 80:
            return "Moderado"
        elif self.velocidad_actual < 120:
            return "Rápido"
        else:
            return "¡Máxima velocidad!"

    def info(self):
        """Retorna un string con la información básica del vehículo."""
        return f"{self.marca} {self.modelo} — {self.velocidad_actual} km/h"

    def tipo_nombre(self):
        return "Vehículo"

    def icono(self):
        return "🚗"


class AutoElectrico(Vehiculo):
    """Vehículo eléctrico con batería limitada."""

    def __init__(self, marca, modelo):
        super().__init__(marca, modelo)     # Llama al constructor de la clase padre
        self.bateria = 100                  # Batería inicial al 100%

    def acelerar(self, turbo=False, terreno="normal"):
        """Acelera consumiendo batería."""
        if self.bateria <= 0:               # Verifica si hay batería disponible
            return False                    # No acelera si no hay batería
        incremento = 8 + (5 if turbo else 0)   # Incremento base eléctrico + turbo
        self.velocidad_actual += incremento     # Aplica el incremento
        self.bateria = max(0, self.bateria - 2) # Descuenta 2% de batería (mínimo 0)
        self.total_aceleraciones += 1           # Cuenta la aceleración
        self.velocidad_maxima = max(self.velocidad_maxima, self.velocidad_actual)
        return True

    def recargar(self):
        """Recarga la batería al 100%."""
        self.bateria = 100                  # Restablece la batería completa

    def info(self):
        return f"{self.marca} {self.modelo} — {self.velocidad_actual} km/h | 🔋 {self.bateria}%"

    def tipo_nombre(self):
        return "Auto Eléctrico"

    def icono(self):
        return "⚡"


class Moto(Vehiculo):
    """Motocicleta: más ágil y rápida que un vehículo normal."""

    def acelerar(self, turbo=False, terreno="normal"):
        """La moto acelera más rápido que otros vehículos."""
        incremento = 15 + (10 if turbo else 0)  # Base más alto por ser moto
        if terreno == "mountain":
            incremento -= 3                      # Penalización menor en montaña
        elif terreno == "track":
            incremento += 8                      # Mejor rendimiento en pista
        self.velocidad_actual += incremento
        self.total_aceleraciones += 1
        self.velocidad_maxima = max(self.velocidad_maxima, self.velocidad_actual)

    def tipo_nombre(self):
        return "Motocicleta"

    def icono(self):
        return "🏍️"


class Camion(Vehiculo):
    """Camión: lento pero constante, penalizado en terrenos difíciles."""

    def acelerar(self, turbo=False, terreno="normal"):
        """El camión acelera poco y se ve afectado por el terreno."""
        incremento = 5                           # Base baja por ser camión pesado
        if turbo:
            incremento += 3                      # Turbo tiene poco efecto en camión
        if terreno == "mountain":
            incremento -= 3                      # Terreno montañoso lo penaliza mucho
        elif terreno == "track":
            incremento += 2
        self.velocidad_actual += max(1, incremento)  # Mínimo 1 km/h de incremento
        self.total_aceleraciones += 1
        self.velocidad_maxima = max(self.velocidad_maxima, self.velocidad_actual)

    def tipo_nombre(self):
        return "Camión"

    def icono(self):
        return "🚛"



class SmartVehiclesApp:
    """Interfaz gráfica profesional del sistema Smart Vehicles."""

    
    COLORS = {
        "bg_dark":      "#0A0E1A",     
        "bg_panel":     "#111827",     
        "bg_card":      "#1F2937",     
        "bg_input":     "#1A2233",     
        "accent":       "#3B82F6",     
        "accent_hover": "#2563EB",     
        "success":      "#10B981",     
        "warning":      "#F59E0B",     
        "danger":       "#EF4444",     
        "text_primary": "#F9FAFB",     
        "text_muted":   "#6B7280",     
        "text_accent":  "#93C5FD",     
        "border":       "#374151",     
        "electric":     "#8B5CF6",     
        "moto":         "#F97316",     
        "truck":        "#6B7280",     
    }

    def __init__(self, root):
        self.root = root                        # Ventana principal de tkinter
        self.vehiculos = []                     # Lista donde se guardan todos los vehículos
        self.historial = []                     # Lista del historial de eventos
        self.animating = False                  # Bandera para controlar animaciones

        self._configurar_ventana()              # Configura tamaño y título
        self._configurar_estilos()              # Aplica estilos globales de ttk
        self._construir_ui()                    # Construye todos los widgets

   
    def _configurar_ventana(self):
        """Configura la ventana principal."""
        self.root.title("SISTEMA DE VEHICULOS INTELIGENTES  •  Sistema de Control**Est: Ever Martinez")   # Título de la ventana
        self.root.geometry("920x700")                                   # Tamaño inicial
        self.root.minsize(860, 640)                                     # Tamaño mínimo permitido
        self.root.configure(bg=self.COLORS["bg_dark"])                  # Color de fondo

        # Centra la ventana en la pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 920) // 2
        y = (self.root.winfo_screenheight() - 700) // 2
        self.root.geometry(f"920x700+{x}+{y}")

    def _configurar_estilos(self):
        """Define los estilos personalizados para widgets ttk."""
        style = ttk.Style()
        style.theme_use("clam")                 # Usa el tema base 'clam' para personalizar

        # Estilo del Combobox
        style.configure("Pro.TCombobox",
            fieldbackground=self.COLORS["bg_input"],
            background=self.COLORS["bg_card"],
            foreground=self.COLORS["text_primary"],
            selectbackground=self.COLORS["accent"],
            selectforeground="white",
            bordercolor=self.COLORS["border"],
            arrowcolor=self.COLORS["text_accent"],
            padding=8
        )

        # Estilo del Frame separador
        style.configure("Pro.TSeparator",
            background=self.COLORS["border"]
        )

 
    def _construir_ui(self):
        """Construye la interfaz completa."""
        # Frame contenedor principal con padding
        main = tk.Frame(self.root, bg=self.COLORS["bg_dark"])
        main.pack(fill="both", expand=True, padx=16, pady=16)

        # ── Encabezado ──
        self._crear_header(main)

        # ── Cuerpo: panel izquierdo + panel derecho ──
        body = tk.Frame(main, bg=self.COLORS["bg_dark"])
        body.pack(fill="both", expand=True, pady=(12, 0))

        body.columnconfigure(0, weight=1)   # Panel izquierdo flexible
        body.columnconfigure(1, weight=2)   # Panel derecho más ancho
        body.rowconfigure(0, weight=1)

        left_panel = tk.Frame(body, bg=self.COLORS["bg_dark"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        right_panel = tk.Frame(body, bg=self.COLORS["bg_dark"])
        right_panel.grid(row=0, column=1, sticky="nsew")

        # Construye cada sección
        self._crear_panel_registro(left_panel)
        self._crear_panel_control(right_panel)

    def _crear_header(self, parent):
        """Crea el encabezado superior con título y estadísticas."""
        header = tk.Frame(parent, bg=self.COLORS["bg_panel"],
                          relief="flat", bd=0)
        header.pack(fill="x")

        # Borde superior de color azul (efecto decorativo)
        accent_bar = tk.Frame(header, bg=self.COLORS["accent"], height=3)
        accent_bar.pack(fill="x")

        content = tk.Frame(header, bg=self.COLORS["bg_panel"])
        content.pack(fill="x", padx=20, pady=14)

        # Icono + título
        tk.Label(content, text="🚀  SIMULADOR DE VEHICULOS ",
                 font=("Courier New", 18, "bold"),
                 bg=self.COLORS["bg_panel"],
                 fg=self.COLORS["text_primary"]).pack(side="left")

        # Subtítulo / versión
        tk.Label(content, text="  •  Sistema de Control Vehicular",
                 font=("Courier New", 10),
                 bg=self.COLORS["bg_panel"],
                 fg=self.COLORS["text_muted"]).pack(side="left", padx=14)

        # Contador de vehículos en tiempo real
        self.lbl_contador = tk.Label(content, text="● 0 vehículos activos",
                                      font=("Courier New", 10, "bold"),
                                      bg=self.COLORS["bg_panel"],
                                      fg=self.COLORS["success"])
        self.lbl_contador.pack(side="right")

    def _card(self, parent, titulo, pady=(0, 10)):
        """Crea un panel tipo 'card' con título y retorna el frame interior."""
        outer = tk.Frame(parent, bg=self.COLORS["bg_card"],
                         relief="flat", bd=0)
        outer.pack(fill="x", pady=pady)

        # Franja de color izquierda
        tk.Frame(outer, bg=self.COLORS["accent"], width=3).pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=self.COLORS["bg_card"])
        inner.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        # Título de la card
        tk.Label(inner, text=titulo.upper(),
                 font=("Courier New", 9, "bold"),
                 bg=self.COLORS["bg_card"],
                 fg=self.COLORS["text_muted"]).pack(anchor="w")

        # Línea separadora
        sep = tk.Frame(inner, bg=self.COLORS["border"], height=1)
        sep.pack(fill="x", pady=(4, 10))

        return inner

    def _label_field(self, parent, texto):
        """Crea una etiqueta de campo con estilo consistente."""
        tk.Label(parent, text=texto,
                 font=("Courier New", 9),
                 bg=self.COLORS["bg_card"],
                 fg=self.COLORS["text_muted"]).pack(anchor="w", pady=(6, 2))

    def _entry(self, parent, placeholder=""):
        """Crea un campo de texto estilizado con placeholder."""
        frame = tk.Frame(parent, bg=self.COLORS["border"], padx=1, pady=1)
        frame.pack(fill="x")

        entry = tk.Entry(frame,
                         font=("Courier New", 11),
                         bg=self.COLORS["bg_input"],
                         fg=self.COLORS["text_primary"],
                         insertbackground=self.COLORS["accent"],
                         relief="flat",
                         bd=6)
        entry.pack(fill="x")

        # Lógica de placeholder
        entry.insert(0, placeholder)
        entry.config(fg=self.COLORS["text_muted"])

        def on_focus_in(e):                             # Al hacer clic, limpia placeholder
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=self.COLORS["text_primary"])

        def on_focus_out(e):                            # Al salir, restaura placeholder si vacío
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=self.COLORS["text_muted"])

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def _boton(self, parent, texto, comando, color=None, texto_color="white", ancho=None):
        """Crea un botón estilizado con efecto hover."""
        color = color or self.COLORS["accent"]     # Color por defecto: azul

        btn = tk.Button(parent,
                        text=texto,
                        command=comando,
                        font=("Courier New", 10, "bold"),
                        bg=color,
                        fg=texto_color,
                        activebackground=self.COLORS["accent_hover"],
                        activeforeground="white",
                        relief="flat",
                        bd=0,
                        padx=16,
                        pady=8,
                        cursor="hand2")             # Cursor de mano al pasar sobre el botón

        if ancho:
            btn.config(width=ancho)

        # Efectos hover
        btn.bind("<Enter>", lambda e: btn.config(bg=self._oscurecer(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

        return btn

    def _oscurecer(self, hex_color):
        """Oscurece un color hexadecimal para efecto hover."""
        r = max(0, int(hex_color[1:3], 16) - 20)   # Reduce componente rojo
        g = max(0, int(hex_color[3:5], 16) - 20)   # Reduce componente verde
        b = max(0, int(hex_color[5:7], 16) - 20)   # Reduce componente azul
        return f"#{r:02x}{g:02x}{b:02x}"            # Retorna el nuevo color

    

    def _crear_panel_registro(self, parent):
        """Crea el panel izquierdo de registro de vehículos."""

        # ── Card: Nuevo vehículo ──
        card = self._card(parent, "➕  Registrar Vehículo")

        self._label_field(card, "TIPO DE VEHÍCULO")
        self.cmb_tipo = ttk.Combobox(card,
                                      values=["⚡ Auto Eléctrico", "🏍️ Motocicleta", "🚛 Camión"],
                                      style="Pro.TCombobox",
                                      state="readonly",
                                      font=("Courier New", 10))
        self.cmb_tipo.set("⚡ Auto Eléctrico")         # Valor por defecto
        self.cmb_tipo.pack(fill="x", pady=(0, 4))

        self._label_field(card, "MARCA")
        self.ent_marca = self._entry(card, "Ej: Tesla, BMW, Yamaha...")

        self._label_field(card, "MODELO")
        self.ent_modelo = self._entry(card, "Ej: Model S, M3, MT-09...")

        btn_add = self._boton(card, "➕  AGREGAR VEHÍCULO",
                               self._agregar_vehiculo,
                               color=self.COLORS["success"])
        btn_add.pack(fill="x", pady=(14, 0))

        # ── Card: Selector ──
        card2 = self._card(parent, "🎯  Seleccionar Vehículo", pady=(0, 10))

        self._label_field(card2, "VEHÍCULO ACTIVO")
        self.cmb_selector = ttk.Combobox(card2,
                                          style="Pro.TCombobox",
                                          state="readonly",
                                          font=("Courier New", 10))
        self.cmb_selector.pack(fill="x")
        self.cmb_selector.bind("<<ComboboxSelected>>", self._al_seleccionar)  # Evento al cambiar selección

        # Tarjeta de info del vehículo seleccionado
        self.frame_info_vehiculo = tk.Frame(card2, bg=self.COLORS["bg_input"],
                                             relief="flat", bd=0)
        self.frame_info_vehiculo.pack(fill="x", pady=(10, 0))

        self.lbl_vehiculo_tipo = tk.Label(self.frame_info_vehiculo, text="Sin selección",
                                           font=("Courier New", 11, "bold"),
                                           bg=self.COLORS["bg_input"],
                                           fg=self.COLORS["text_muted"],
                                           pady=10, padx=10)
        self.lbl_vehiculo_tipo.pack(anchor="w")

        self.lbl_vehiculo_tipo = tk.Label(self.frame_info_vehiculo, text="EST: EVER MARTINEZ",
                                           font=("Courier New", 14, "bold"),
                                           bg=self.COLORS["bg_input"],
                                           fg=self.COLORS["text_muted"],
                                           pady=10, padx=10)
        self.lbl_vehiculo_tipo.pack(anchor="w")
        
        self.lbl_vehiculo_stats = tk.Label(self.frame_info_vehiculo, text="",
                                            font=("Courier New", 9),
                                            bg=self.COLORS["bg_input"],
                                            fg=self.COLORS["text_muted"],
                                            pady=4, padx=10, justify="left")
        self.lbl_vehiculo_stats.pack(anchor="w")

  
    def _crear_panel_control(self, parent):
        """Crea el panel derecho con controles y métricas."""

        # ── Card: Velocímetro ──
        card_vel = self._card(parent, "📊  Velocímetro", pady=(0, 10))

        # Frame del velocímetro visual
        vel_frame = tk.Frame(card_vel, bg=self.COLORS["bg_card"])
        vel_frame.pack(fill="x")

        # Velocidad actual grande
        self.lbl_velocidad = tk.Label(vel_frame, text="0",
                                       font=("Courier New", 52, "bold"),
                                       bg=self.COLORS["bg_card"],
                                       fg=self.COLORS["accent"])
        self.lbl_velocidad.pack(side="left", padx=(0, 4))

        unidad_frame = tk.Frame(vel_frame, bg=self.COLORS["bg_card"])
        unidad_frame.pack(side="left", pady=12)

        tk.Label(unidad_frame, text="km/h",
                 font=("Courier New", 14),
                 bg=self.COLORS["bg_card"],
                 fg=self.COLORS["text_muted"]).pack(anchor="w")

        self.lbl_estado = tk.Label(unidad_frame, text="● DETENIDO",
                                    font=("Courier New", 9, "bold"),
                                    bg=self.COLORS["bg_card"],
                                    fg=self.COLORS["text_muted"])
        self.lbl_estado.pack(anchor="w")

        # Barra de progreso de velocidad
        self.canvas_vel = tk.Canvas(card_vel, height=8,
                                     bg=self.COLORS["bg_input"],
                                     highlightthickness=0)
        self.canvas_vel.pack(fill="x", pady=(8, 0))

        # Velocidad máxima
        self.lbl_max_vel = tk.Label(card_vel, text="Máx: 0 km/h",
                                     font=("Courier New", 9),
                                     bg=self.COLORS["bg_card"],
                                     fg=self.COLORS["text_muted"])
        self.lbl_max_vel.pack(anchor="e", pady=(4, 0))

        # ── Card: Controles ──
        card_ctrl = self._card(parent, "🎮  Controles de Conducción", pady=(0, 10))

        # Opciones: turbo y terreno en la misma fila
        opts_frame = tk.Frame(card_ctrl, bg=self.COLORS["bg_card"])
        opts_frame.pack(fill="x", pady=(0, 10))
        opts_frame.columnconfigure(0, weight=1)
        opts_frame.columnconfigure(1, weight=1)

        # Turbo
        turbo_f = tk.Frame(opts_frame, bg=self.COLORS["bg_input"], padx=10, pady=8)
        turbo_f.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        tk.Label(turbo_f, text="TURBO",
                 font=("Courier New", 9),
                 bg=self.COLORS["bg_input"],
                 fg=self.COLORS["text_muted"]).pack(anchor="w")

        self.var_turbo = tk.BooleanVar()                              # Variable ligada al checkbox
        self.chk_turbo = tk.Checkbutton(turbo_f,
                                         text="Activar ⚡",
                                         variable=self.var_turbo,
                                         font=("Courier New", 10, "bold"),
                                         bg=self.COLORS["bg_input"],
                                         fg=self.COLORS["warning"],
                                         selectcolor=self.COLORS["bg_card"],
                                         activebackground=self.COLORS["bg_input"],
                                         relief="flat",
                                         cursor="hand2")
        self.chk_turbo.pack(anchor="w")

        # Terreno
        terrain_f = tk.Frame(opts_frame, bg=self.COLORS["bg_input"], padx=10, pady=8)
        terrain_f.grid(row=0, column=1, sticky="ew")

        tk.Label(terrain_f, text="TERRENO",
                 font=("Courier New", 9),
                 bg=self.COLORS["bg_input"],
                 fg=self.COLORS["text_muted"]).pack(anchor="w")

        self.cmb_terreno = ttk.Combobox(terrain_f,
                                         values=["normal", "mountain", "track"],
                                         style="Pro.TCombobox",
                                         state="readonly",
                                         font=("Courier New", 10),
                                         width=10)
        self.cmb_terreno.set("normal")                                # Terreno por defecto
        self.cmb_terreno.pack(anchor="w", pady=(4, 0))

        # Botones de acción en cuadrícula
        btns_frame = tk.Frame(card_ctrl, bg=self.COLORS["bg_card"])
        btns_frame.pack(fill="x")
        btns_frame.columnconfigure(0, weight=1)
        btns_frame.columnconfigure(1, weight=1)
        btns_frame.columnconfigure(2, weight=1)

        btn_acel = self._boton(btns_frame, "▶  ACELERAR",
                                self._acelerar, color="#1D4ED8")
        btn_acel.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)

        btn_frenar = self._boton(btns_frame, "⏸  FRENAR",
                                  self._frenar, color=self.COLORS["warning"])
        btn_frenar.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        btn_stop = self._boton(btns_frame, "⏹  STOP",
                                self._detener, color=self.COLORS["danger"])
        btn_stop.grid(row=0, column=2, sticky="ew", padx=(4, 0), pady=2)

        # Botón recargar (solo eléctrico)
        self.btn_recargar = self._boton(btns_frame, "🔋  RECARGAR BATERÍA",
                                         self._recargar, color=self.COLORS["electric"])
        self.btn_recargar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0))

        # ── Card: Batería ──
        self.card_bateria = self._card(parent, "🔋  Estado de Batería", pady=(0, 10))

        bat_row = tk.Frame(self.card_bateria, bg=self.COLORS["bg_card"])
        bat_row.pack(fill="x")

        self.lbl_bateria_pct = tk.Label(bat_row, text="— %",
                                         font=("Courier New", 20, "bold"),
                                         bg=self.COLORS["bg_card"],
                                         fg=self.COLORS["electric"])
        self.lbl_bateria_pct.pack(side="left")

        tk.Label(bat_row, text="  carga restante",
                 font=("Courier New", 9),
                 bg=self.COLORS["bg_card"],
                 fg=self.COLORS["text_muted"]).pack(side="left", pady=6)

        self.canvas_bat = tk.Canvas(self.card_bateria, height=10,
                                     bg=self.COLORS["bg_input"],
                                     highlightthickness=0)
        self.canvas_bat.pack(fill="x", pady=(6, 0))

        # ── Card: Historial ──
        card_hist = self._card(parent, "📜  Registro de Eventos")

        self.txt_historial = tk.Text(card_hist,
                                      height=8,
                                      font=("Courier New", 9),
                                      bg=self.COLORS["bg_input"],
                                      fg=self.COLORS["text_primary"],
                                      relief="flat",
                                      bd=4,
                                      wrap="word",
                                      state="disabled")          # Solo lectura
        self.txt_historial.pack(fill="both", expand=True)

        # Scrollbar para el historial
        scroll = tk.Scrollbar(card_hist, command=self.txt_historial.yview,
                               bg=self.COLORS["bg_card"])
        self.txt_historial.config(yscrollcommand=scroll.set)

        # Tags de colores para el historial
        self.txt_historial.tag_config("add",     foreground=self.COLORS["success"])
        self.txt_historial.tag_config("accel",   foreground=self.COLORS["accent"])
        self.txt_historial.tag_config("stop",    foreground=self.COLORS["danger"])
        self.txt_historial.tag_config("warn",    foreground=self.COLORS["warning"])
        self.txt_historial.tag_config("muted",   foreground=self.COLORS["text_muted"])

    
    def _tiempo(self):
        """Retorna la hora actual formateada como string."""
        return time.strftime("%H:%M:%S")                            # Formato horas:minutos:segundos

    def _log(self, mensaje, tag="muted"):
        """Agrega una línea al historial con marca de tiempo y color."""
        self.txt_historial.config(state="normal")                   # Habilita escritura
        self.txt_historial.insert("end", f"[{self._tiempo()}] {mensaje}\n", tag)
        self.txt_historial.see("end")                               # Desplaza al final
        self.txt_historial.config(state="disabled")                 # Bloquea escritura

    def _agregar_vehiculo(self):
        """Crea y registra un nuevo vehículo según los datos ingresados."""
        tipo  = self.cmb_tipo.get()                                 # Obtiene el tipo seleccionado
        marca = self.ent_marca.get().strip()                        # Obtiene y limpia la marca
        modelo = self.ent_modelo.get().strip()                      # Obtiene y limpia el modelo

        # Ignora placeholders como valor real
        placeholders = ["Ej: Tesla, BMW, Yamaha...", "Ej: Model S, M3, MT-09..."]
        if marca in placeholders or modelo in placeholders:
            marca, modelo = "", ""

        if not marca or not modelo:                                 # Valida que no estén vacíos
            self._log("⚠ Debes ingresar marca y modelo.", "warn")
            return

        # Instancia la clase según el tipo elegido
        if "Eléctrico" in tipo:
            v = AutoElectrico(marca, modelo)
        elif "Moto" in tipo:
            v = Moto(marca, modelo)
        else:
            v = Camion(marca, modelo)

        self.vehiculos.append(v)                                    # Agrega a la lista de vehículos

        # Actualiza el combobox selector con los nombres disponibles
        self.cmb_selector["values"] = [f"{veh.icono()} {veh.marca} {veh.modelo}"
                                        for veh in self.vehiculos]
        self.cmb_selector.current(len(self.vehiculos) - 1)         # Selecciona el recién agregado
        self._al_seleccionar()                                      # Refresca la vista

        # Actualiza el contador del header
        self.lbl_contador.config(text=f"● {len(self.vehiculos)} vehículo(s) activo(s)")

        self._log(f"Agregado: {v.icono()} {marca} {modelo} [{v.tipo_nombre()}]", "add")

        # Limpia los campos de entrada
        self.ent_marca.delete(0, "end")
        self.ent_modelo.delete(0, "end")

    def _vehiculo_activo(self):
        """Retorna el vehículo actualmente seleccionado en el combobox."""
        idx = self.cmb_selector.current()                           # Índice seleccionado
        if idx >= 0 and idx < len(self.vehiculos):
            return self.vehiculos[idx]                              # Retorna el vehículo
        return None                                                 # Si no hay selección retorna None

    def _al_seleccionar(self, event=None):
        """Actualiza la UI cuando se cambia el vehículo seleccionado."""
        v = self._vehiculo_activo()
        if not v:
            return

        # Actualiza la tarjeta de información
        self.lbl_vehiculo_tipo.config(
            text=f"{v.icono()}  {v.marca} {v.modelo}  —  {v.tipo_nombre()}",
            fg=self.COLORS["text_primary"]
        )
        stats = f"Aceleraciones: {v.total_aceleraciones}   Máx: {v.velocidad_maxima} km/h"
        self.lbl_vehiculo_stats.config(text=stats)

        self._actualizar_medidores(v)                               # Refresca velocímetro y batería

    def _acelerar(self):
        """Accionado por el botón Acelerar."""
        v = self._vehiculo_activo()
        if not v:
            self._log("⚠ Selecciona un vehículo primero.", "warn")
            return

        turbo   = self.var_turbo.get()                              # Estado del checkbox turbo
        terreno = self.cmb_terreno.get()                            # Terreno seleccionado

        resultado = v.acelerar(turbo, terreno)                      # Llama al método acelerar

        if resultado is False:                                      # Solo AutoElectrico retorna False
            self._log(f"⚠ {v.marca}: batería agotada. Recarga necesaria.", "warn")
            return

        self._actualizar_medidores(v)                               # Refresca la UI
        turbo_txt = " [TURBO]" if turbo else ""
        self._log(f"Aceleró{turbo_txt}: {v.info()} | {v.estado()}", "accel")

    def _frenar(self):
        """Accionado por el botón Frenar."""
        v = self._vehiculo_activo()
        if not v:
            return
        v.frenar()                                                  # Reduce la velocidad
        self._actualizar_medidores(v)
        self._log(f"Frenó: {v.info()}", "warn")

    def _detener(self):
        """Accionado por el botón Stop."""
        v = self._vehiculo_activo()
        if not v:
            return
        v.detener()                                                 # Velocidad a 0
        self._actualizar_medidores(v)
        self._log(f"Detenido: {v.marca} {v.modelo}", "stop")

    def _recargar(self):
        """Recarga la batería si el vehículo es eléctrico."""
        v = self._vehiculo_activo()
        if not v:
            return
        if isinstance(v, AutoElectrico):                            # Verifica que sea eléctrico
            v.recargar()
            self._actualizar_medidores(v)
            self._log(f"🔋 Batería recargada: {v.marca}", "add")
        else:
            self._log(f"⚠ {v.marca} no es eléctrico.", "warn")

    def _actualizar_medidores(self, v):
        """Actualiza velocímetro, barra de velocidad, batería y stats del vehículo."""
        # ── Velocímetro ──
        self.lbl_velocidad.config(text=str(v.velocidad_actual))

        # Color dinámico según velocidad
        if v.velocidad_actual == 0:
            color_vel = self.COLORS["text_muted"]
        elif v.velocidad_actual < 60:
            color_vel = self.COLORS["success"]
        elif v.velocidad_actual < 100:
            color_vel = self.COLORS["warning"]
        else:
            color_vel = self.COLORS["danger"]

        self.lbl_velocidad.config(fg=color_vel)

        # Texto de estado
        estado = v.estado()
        self.lbl_estado.config(text=f"● {estado.upper()}", fg=color_vel)

        # Velocidad máxima registrada
        self.lbl_max_vel.config(text=f"Máx alcanzada: {v.velocidad_maxima} km/h")

        # ── Barra de velocidad ──
        self._dibujar_barra(self.canvas_vel, v.velocidad_actual, 200, color_vel)

        # ── Batería ──
        if isinstance(v, AutoElectrico):                            # Solo para eléctricos
            bat = v.bateria
            if bat > 50:
                color_bat = self.COLORS["success"]
            elif bat > 20:
                color_bat = self.COLORS["warning"]
            else:
                color_bat = self.COLORS["danger"]

            self.lbl_bateria_pct.config(text=f"{bat}%", fg=color_bat)
            self._dibujar_barra(self.canvas_bat, bat, 100, color_bat)
        else:
            self.lbl_bateria_pct.config(text="N/A", fg=self.COLORS["text_muted"])
            self._dibujar_barra(self.canvas_bat, 0, 100, self.COLORS["text_muted"])

        # ── Stats del vehículo en el panel izquierdo ──
        stats = f"Aceleraciones: {v.total_aceleraciones}   Máx: {v.velocidad_maxima} km/h"
        self.lbl_vehiculo_stats.config(text=stats)

    def _dibujar_barra(self, canvas, valor, maximo, color):
        """Dibuja una barra de progreso horizontal en un Canvas."""
        canvas.update_idletasks()                                   # Fuerza actualización del tamaño
        ancho = canvas.winfo_width()                                # Ancho disponible del canvas
        canvas.delete("all")                                        # Borra el dibujo anterior

        if ancho <= 1:
            return                                                  # Evita dibujar si el canvas no tiene tamaño aún

        # Fondo de la barra
        canvas.create_rectangle(0, 0, ancho, 10,
                                 fill=self.COLORS["bg_input"],
                                 outline="")

        # Porción llena según el valor
        fill_w = int((valor / maximo) * ancho) if maximo > 0 else 0
        if fill_w > 0:
            canvas.create_rectangle(0, 0, fill_w, 10,
                                     fill=color,
                                     outline="")



if __name__ == "__main__":
    root = tk.Tk()                          # Crea la ventana principal de tkinter
    app = SmartVehiclesApp(root)            # Instancia la aplicación
    root.mainloop()                         # Inicia el bucle principal de eventos
