    def _registrar_cliente(self):             # Lee el formulario y crea un nuevo cliente
        """Valida el formulario y agrega un nuevo cliente al sistema"""
        try:                                   # Intenta crear el cliente con los datos del form
            c = Cliente(                       # Crea el objeto Cliente
                self.vars_cli["cli_nombre"].get(),    # Lee el campo nombre
                self.vars_cli["cli_cedula"].get(),    # Lee el campo cédula
                self.vars_cli["cli_correo"].get(),    # Lee el campo correo
                self.vars_cli["cli_telefono"].get(),  # Lee el campo teléfono
            )
            self.clientes.append(c)           # Agrega el cliente a la lista en memoria
            SistemaLogs.registrar_evento(     # Registra el evento en el log
                f"Cliente registrado: {c.nombre} | CC: {c.cedula}")
            for var in self.vars_cli.values():  # Limpia todos los campos del formulario
                var.set("")                   # Resetea cada variable a cadena vacía
            self._refrescar_tabla_clientes()  # Actualiza la tabla de clientes
            self._refrescar_dashboard()       # Actualiza las métricas del dashboard
            messagebox.showinfo(              # Muestra mensaje de éxito
                "✅ Éxito",
                f"Cliente '{c.nombre}' registrado correctamente.")
        except ErrorClienteInvalido as e:     # Captura errores de validación del cliente
            SistemaLogs.registrar_error(f"Registro cliente: {e}")  # Registra en el log
            messagebox.showerror("❌ Error de Validación", str(e))  # Muestra el error al usuario

    def _refrescar_tabla_clientes(self):      # Recarga la tabla con los datos actuales
        """Borra y recarga todas las filas de la tabla de clientes"""
        for row in self.tabla_cli.get_children():  # Obtiene todas las filas actuales
            self.tabla_cli.delete(row)        # Elimina cada fila
        for i, c in enumerate(self.clientes, 1):  # Itera los clientes con índice desde 1
            self.tabla_cli.insert(            # Inserta una nueva fila en la tabla
                "", tk.END,
                values=(i, c.nombre, c.cedula, c.correo, c.telefono))  # Datos de la fila

    def _construir_tab_servicios(self):       # Construye la pestaña de servicios
        """Formulario para agregar servicios y tabla de servicios disponibles"""
        frame = self.tab_servicios            # Referencia al frame de la pestaña

        tk.Label(                             # Título de la sección
            frame, text="Gestión de Servicios",
            font=self.FUENTE_TITULO,          # Fuente grande
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(pady=(20, 2), anchor="w", padx=25)

        form = tk.LabelFrame(                 # Formulario con borde
            frame,
            text=" ✏  Nuevo Servicio ",       # Título del formulario
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["tarjeta"],       # Fondo oscuro
            relief="flat")                    # Sin relieve
        form.pack(fill="x", padx=20, pady=10)  # Ocupa el ancho

        tk.Label(                             # Etiqueta del selector de tipo
            form, text="Tipo de Servicio",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["tarjeta"]        # Fondo del formulario
        ).grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

        self.var_tipo_srv = tk.StringVar(value="Sala")  # Variable del selector, por defecto Sala
        combo_tipo = ttk.Combobox(            # Selector desplegable de tipo de servicio
            form,
            textvariable=self.var_tipo_srv,   # Variable vinculada
            values=["Sala", "Equipo", "Asesoría"],  # Opciones disponibles
            state="readonly",                 # Solo lectura, no se puede escribir
            font=self.FUENTE_NORMAL)          # Fuente estándar
        combo_tipo.grid(                      # Posición en la grilla
            row=1, column=0,
            padx=15, pady=(2, 5), sticky="ew", ipady=4)
        form.columnconfigure(0, weight=1)     # Columna 0 se expande
        form.columnconfigure(1, weight=1)     # Columna 1 se expande

        tk.Label(                             # Etiqueta del campo de nombre/área
            form, text="Nombre / Área / Tipo",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["tarjeta"]        # Fondo
        ).grid(row=0, column=1, padx=15, pady=(10, 0), sticky="w")

        self.var_srv_nombre = tk.StringVar()  # Variable para el nombre del servicio
        self.entry_srv_nombre = tk.Entry(     # Campo para el nombre del servicio
            form,
            textvariable=self.var_srv_nombre, # Variable vinculada
            font=self.FUENTE_NORMAL,          # Fuente estándar
            bg=self.COLORES["entrada"],       # Fondo oscuro del campo
            fg=self.COLORES["texto"],         # Texto claro
            insertbackground=self.COLORES["texto"],  # Cursor blanco
            relief="flat", bd=0)              # Sin borde
        self.entry_srv_nombre.grid(           # Posición en la grilla
            row=1, column=1,
            padx=15, pady=(2, 5), sticky="ew", ipady=6)

        tk.Label(                             # Etiqueta del campo extra (capacidad/cantidad/nivel)
            form, text="Capacidad / Cantidad / Nivel",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["tarjeta"]        # Fondo
        ).grid(row=2, column=0, padx=15, pady=(5, 0), sticky="w")

        self.var_srv_extra = tk.StringVar()   # Variable para el campo extra
        self.entry_srv_extra = tk.Entry(      # Campo extra según el tipo de servicio
            form,
            textvariable=self.var_srv_extra,  # Variable vinculada
            font=self.FUENTE_NORMAL,          # Fuente estándar
            bg=self.COLORES["entrada"],       # Fondo oscuro
            fg=self.COLORES["texto"],         # Texto claro
            insertbackground=self.COLORES["texto"],  # Cursor blanco
            relief="flat", bd=0)              # Sin borde
        self.entry_srv_extra.grid(            # Posición en la grilla
            row=3, column=0,
            padx=15, pady=(2, 10), sticky="ew", ipady=6)

        self._btn(                            # Botón para agregar el servicio
            form,
            "➕  Agregar Servicio",           # Texto del botón
            self.COLORES["acento2"],          # Color púrpura
            self._agregar_servicio            # Función que se ejecuta al presionar
        ).grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        tk.Label(                             # Subtítulo de la tabla
            frame, text="Servicios Disponibles",
            font=self.FUENTE_SUBTIT,          # Fuente mediana
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25, pady=(5, 5))

        cols = ("ID", "Nombre", "Precio/hr", "Disponible", "Detalle")  # Columnas de la tabla
        self.tabla_srv = self._crear_tabla(frame, cols, height=7)  # Crea la tabla
        self._refrescar_tabla_servicios()     # Llena la tabla con los servicios actuales

    def _agregar_servicio(self):              # Lee el formulario y crea un nuevo servicio
        """Lee el formulario de servicios y crea el tipo de servicio correspondiente"""
        tipo   = self.var_tipo_srv.get()      # Lee el tipo seleccionado (Sala/Equipo/Asesoría)
        nombre = self.var_srv_nombre.get().strip()  # Lee y limpia el nombre
        extra  = self.var_srv_extra.get().strip()   # Lee y limpia el campo extra
        try:                                   # Intenta crear el servicio
            if tipo == "Sala":                # Si el tipo es Sala de reuniones
                if not extra.isdigit():        # Verifica que la capacidad sea número
                    raise ErrorServicioNoDisponible("Capacidad debe ser un número entero.")
                srv = ReservaSala(nombre or "Sala Nueva", int(extra))  # Crea la sala

            elif tipo == "Equipo":            # Si el tipo es Alquiler de equipos
                if not extra.isdigit():        # Verifica que la cantidad sea número
                    raise ErrorServicioNoDisponible("Cantidad debe ser un número entero.")
                srv = AlquilerEquipo(nombre or "Equipo", int(extra))  # Crea el equipo

            else:                              # Si el tipo es Asesoría Técnica
                nivel = extra.lower() if extra else "senior"  # Nivel por defecto senior
                srv = AsesoriaTecnica(nombre or "General", nivel)  # Crea la asesoría

            self.servicios.append(srv)        # Agrega el servicio a la lista en memoria
            SistemaLogs.registrar_evento(f"Servicio creado: {srv.nombre}")  # Log del evento
            self.var_srv_nombre.set("")        # Limpia el campo de nombre
            self.var_srv_extra.set("")         # Limpia el campo extra
            self._refrescar_tabla_servicios()  # Actualiza la tabla de servicios
            self._refrescar_dashboard()        # Actualiza las métricas
            messagebox.showinfo(               # Mensaje de éxito al usuario
                "✅ Éxito",
                f"Servicio '{srv.nombre}' agregado correctamente.")
        except ErrorSistemaFJ as e:           # Captura errores del sistema
            SistemaLogs.registrar_error(f"Crear servicio: {e}")  # Registra el error
            messagebox.showerror("❌ Error", str(e))  # Muestra el error al usuario

    def _refrescar_tabla_servicios(self):     # Recarga la tabla de servicios
        """Borra y recarga todas las filas de la tabla de servicios"""
        for row in self.tabla_srv.get_children():  # Obtiene todas las filas actuales
            self.tabla_srv.delete(row)        # Elimina cada fila
        for i, s in enumerate(self.servicios, 1):  # Itera los servicios con índice desde 1
            self.tabla_srv.insert(            # Inserta una nueva fila
                "", tk.END,
                values=(
                    i,                        # Número de orden
                    s.nombre,                 # Nombre del servicio
                    f"${s.precio_hora:,.0f}", # Precio formateado con separador de miles
                    "✓ Sí" if s.disponible else "✗ No",  # Estado de disponibilidad
                    s.describir()             # Descripción específica del servicio
                ))
    def _construir_tab_reservas(self):        # Construye la pestaña de reservas
        """Formulario de nueva reserva, tabla y botones de acción"""
        frame = self.tab_reservas             # Referencia al frame de la pestaña

        tk.Label(                             # Título de la sección
            frame, text="Gestión de Reservas",
            font=self.FUENTE_TITULO,          # Fuente grande
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(pady=(20, 2), anchor="w", padx=25)

        form = tk.LabelFrame(                 # Formulario con borde
            frame,
            text=" ✏  Nueva Reserva ",        # Título del formulario
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color del título
            bg=self.COLORES["tarjeta"],       # Fondo oscuro
            relief="flat")                    # Sin relieve
        form.pack(fill="x", padx=20, pady=10)  # Ocupa el ancho

        for col in range(4):                  # Configura 4 columnas iguales en el formulario
            form.columnconfigure(col, weight=1)  # Cada columna se expande proporcionalmente

        for j, lbl in enumerate(             # Crea las etiquetas de cada campo del formulario
                ["Cliente", "Servicio", "Horas", "Descuento (0-1)"]):
            tk.Label(                         # Etiqueta de cada campo
                form, text=lbl,
                font=self.FUENTE_SMALL,       # Fuente pequeña
                fg=self.COLORES["texto_dim"], # Color gris
                bg=self.COLORES["tarjeta"]    # Fondo del formulario
            ).grid(row=0, column=j, padx=12, pady=(10, 0), sticky="w")  # Posición fila 0

        self.combo_res_cli = ttk.Combobox(    # Selector de cliente para la reserva
            form,
            state="readonly",                 # Solo se puede seleccionar, no escribir
            font=self.FUENTE_NORMAL)          # Fuente estándar
        self.combo_res_cli.grid(              # Posición en la grilla
            row=1, column=0, padx=12, pady=4, sticky="ew", ipady=4)

        self.combo_res_srv = ttk.Combobox(    # Selector de servicio para la reserva
            form,
            state="readonly",                 # Solo se puede seleccionar
            font=self.FUENTE_NORMAL)          # Fuente estándar
        self.combo_res_srv.grid(              # Posición en la grilla
            row=1, column=1, padx=12, pady=4, sticky="ew", ipady=4)

        self.var_res_horas = tk.StringVar(value="2")  # Variable de horas, por defecto 2
        tk.Entry(                             # Campo para ingresar las horas
            form,
            textvariable=self.var_res_horas,  # Variable vinculada
            font=self.FUENTE_NORMAL,          # Fuente estándar
            bg=self.COLORES["entrada"],       # Fondo oscuro
            fg=self.COLORES["texto"],         # Texto claro
            insertbackground=self.COLORES["texto"],  # Cursor blanco
            relief="flat"                     # Sin relieve
        ).grid(row=1, column=2, padx=12, pady=4, sticky="ew", ipady=6)

        self.var_res_desc = tk.StringVar(value="0")  # Variable de descuento, por defecto 0
        tk.Entry(                             # Campo para ingresar el descuento
            form,
            textvariable=self.var_res_desc,   # Variable vinculada
            font=self.FUENTE_NORMAL,          # Fuente estándar
            bg=self.COLORES["entrada"],       # Fondo oscuro
            fg=self.COLORES["texto"],         # Texto claro
            insertbackground=self.COLORES["texto"],  # Cursor blanco
            relief="flat"                     # Sin relieve
        ).grid(row=1, column=3, padx=12, pady=4, sticky="ew", ipady=6)

        self._btn(                            # Botón para crear la reserva
            form,
            "📋  Crear Reserva",              # Texto del botón
            self.COLORES["exito"],            # Color verde
            self._crear_reserva              # Función que se ejecuta al presionar
        ).grid(row=2, column=0, columnspan=4, padx=12, pady=10, sticky="ew")

        tk.Label(                             # Subtítulo de la tabla
            frame, text="Reservas del Sistema",
            font=self.FUENTE_SUBTIT,          # Fuente mediana
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25, pady=(5, 5))

        cols = ("ID", "Fecha", "Cliente", "Servicio", "Horas", "Costo", "Estado")  # Columnas
        self.tabla_res = self._crear_tabla(frame, cols, height=6)  # Tabla con 6 filas visibles

        fila_acc = tk.Frame(frame, bg=self.COLORES["fondo"])  # Frame para los botones de acción
        fila_acc.pack(fill="x", padx=20, pady=5)  # Debajo de la tabla

        self._btn(                            # Botón para confirmar la reserva seleccionada
            fila_acc, "✅ Confirmar",
            self.COLORES["exito"],            # Color verde
            self._confirmar_reserva_sel       # Función al presionar
        ).pack(side="left", padx=5, ipadx=10, ipady=4)  # Alineado a la izquierda

        self._btn(                            # Botón para procesar la reserva seleccionada
            fila_acc, "🏁 Procesar",
            self.COLORES["acento"],           # Color azul
            self._procesar_reserva_sel        # Función al presionar
        ).pack(side="left", padx=5, ipadx=10, ipady=4)

        self._btn(                            # Botón para cancelar la reserva seleccionada
            fila_acc, "❌ Cancelar",
            self.COLORES["peligro"],          # Color rojo
            self._cancelar_reserva_sel        # Función al presionar
        ).pack(side="left", padx=5, ipadx=10, ipady=4)

        self._refrescar_combos_reserva()      # Llena los combos con clientes y servicios actuales

    def _refrescar_combos_reserva(self):      # Actualiza los combos del formulario de reservas
        """Actualiza las opciones de los combos de cliente y servicio"""
        self.combo_res_cli["values"] = [      # Lista de clientes para el combo
            f"{i+1}. {c.nombre}"              # Formato: número + nombre
            for i, c in enumerate(self.clientes)]
        self.combo_res_srv["values"] = [      # Lista de servicios para el combo
            f"{i+1}. {s.nombre}"              # Formato: número + nombre del servicio
            for i, s in enumerate(self.servicios)]
        if self.clientes:                     # Si hay clientes, selecciona el primero
            self.combo_res_cli.current(0)     # Selecciona el índice 0
        if self.servicios:                    # Si hay servicios, selecciona el primero
            self.combo_res_srv.current(0)     # Selecciona el índice 0

    def _crear_reserva(self):                 # Crea una nueva reserva desde el formulario
        """Lee el formulario y crea una reserva en estado pendiente"""
        try:                                   # Intenta crear la reserva
            idx_cli = self.combo_res_cli.current()   # Índice del cliente seleccionado
            idx_srv = self.combo_res_srv.current()   # Índice del servicio seleccionado
            if idx_cli < 0 or idx_srv < 0:   # Verifica que se haya seleccionado cliente y servicio
                raise ErrorReservaInvalida("Selecciona un cliente y un servicio.")
            horas = float(self.var_res_horas.get())  # Lee las horas como número flotante
            desc  = float(self.var_res_desc.get())   # Lee el descuento como número flotante
            r = Reserva(                      # Crea el objeto Reserva
                self.clientes[idx_cli],       # Cliente por su índice en la lista
                self.servicios[idx_srv],      # Servicio por su índice en la lista
                horas, desc)                  # Horas y descuento
            self.reservas.append(r)           # Agrega la reserva a la lista en memoria
            SistemaLogs.registrar_evento(f"Reserva #{r.id} creada (pendiente).")  # Log del evento
            self._refrescar_tabla_reservas()  # Actualiza la tabla de reservas
            self._refrescar_dashboard()       # Actualiza las métricas
            messagebox.showinfo(              # Mensaje informativo al usuario
                "✅ Reserva Creada",
                f"Reserva #{r.id} creada en estado PENDIENTE.\n"
                f"Confírmala para calcular el costo.")
        except (ErrorReservaInvalida, ValueError) as e:  # Captura errores de validación o conversión
            SistemaLogs.registrar_error(f"Crear reserva: {e}")  # Registra el error
            messagebox.showerror("❌ Error", str(e))  # Muestra el error al usuario

    def _reserva_seleccionada(self):          # Obtiene la reserva seleccionada en la tabla
        """Retorna el objeto Reserva seleccionado, o None si no hay selección"""
        sel = self.tabla_res.selection()      # Obtiene el ID de la fila seleccionada
        if not sel:                            # Si no hay selección
            messagebox.showwarning(           # Muestra advertencia
                "⚠ Atención", "Selecciona una reserva en la tabla.")
            return None                        # Retorna None para indicar sin selección
        idx = self.tabla_res.index(sel[0])    # Convierte el ID de la fila a índice numérico
        return self.reservas[idx]             # Retorna el objeto Reserva correspondiente

    def _confirmar_reserva_sel(self):         # Confirma la reserva seleccionada en la tabla
        """Confirma la reserva seleccionada y calcula su costo"""
        r = self._reserva_seleccionada()      # Obtiene la reserva seleccionada
        if not r:                              # Si no hay selección, termina
            return
        try:                                   # Intenta confirmar la reserva
            r.confirmar()                     # Llama al método confirmar del objeto Reserva
            self._refrescar_tabla_reservas()  # Actualiza la tabla
            self._refrescar_dashboard()       # Actualiza las métricas
            messagebox.showinfo(              # Mensaje de éxito con el costo calculado
                "✅ Confirmada",
                f"Reserva #{r.id} confirmada.\nCosto total: ${r.costo:,.0f}")
        except ErrorReservaInvalida as e:     # Si la confirmación falla
            messagebox.showerror("❌ Error", str(e))  # Muestra el error

    def _procesar_reserva_sel(self):          # Procesa la reserva seleccionada
        """Marca como procesada la reserva seleccionada"""
        r = self._reserva_seleccionada()      # Obtiene la reserva seleccionada
        if not r:                              # Si no hay selección, termina
            return
        try:                                   # Intenta procesar la reserva
            r.procesar()                      # Llama al método procesar del objeto Reserva
            self._refrescar_tabla_reservas()  # Actualiza la tabla
            self._refrescar_dashboard()       # Actualiza las métricas
            messagebox.showinfo(              # Mensaje de éxito
                "🏁 Procesada",
                f"Reserva #{r.id} procesada exitosamente.")
        except ErrorReservaInvalida as e:     # Si el procesamiento falla
            messagebox.showerror("❌ Error", str(e))  # Muestra el error

    def _cancelar_reserva_sel(self):          # Cancela la reserva seleccionada
        """Cancela la reserva seleccionada tras pedir confirmación"""
        r = self._reserva_seleccionada()      # Obtiene la reserva seleccionada
        if not r:                              # Si no hay selección, termina
            return
        if not messagebox.askyesno(           # Pide confirmación antes de cancelar
                "¿Cancelar?",
                f"¿Seguro que deseas cancelar la reserva #{r.id}?"):
            return                             # Si el usuario dice No, no hace nada
        try:                                   # Intenta cancelar la reserva
            r.cancelar()                      # Llama al método cancelar del objeto Reserva
            self._refrescar_tabla_reservas()  # Actualiza la tabla
            self._refrescar_dashboard()       # Actualiza las métricas
            messagebox.showinfo(              # Mensaje de confirmación de cancelación
                "❌ Cancelada",
                f"Reserva #{r.id} cancelada.")
        except ErrorReservaInvalida as e:     # Si la cancelación falla
            messagebox.showerror("❌ Error", str(e))  # Muestra el error

    def _refrescar_tabla_reservas(self):      # Recarga la tabla de reservas
        """Borra y recarga todas las filas de la tabla de reservas"""
        for row in self.tabla_res.get_children():  # Obtiene todas las filas actuales
            self.tabla_res.delete(row)        # Elimina cada fila
        for r in self.reservas:               # Itera todas las reservas en memoria
            self.tabla_res.insert(            # Inserta una fila por reserva
                "", tk.END,
                values=(
                    f"#{r.id:03d}",           # ID con 3 dígitos (ej: #001)
                    r.fecha,                  # Fecha de creación
                    r.cliente.nombre,         # Nombre del cliente
                    r.servicio.nombre,        # Nombre del servicio
                    f"{r.horas}h",            # Horas con sufijo h
                    f"${r.costo:,.0f}",       # Costo formateado con separador de miles
                    r.estado.upper()          # Estado en mayúsculas
                ))  
    def _construir_tab_logs(self):            # Construye la pestaña de consola de logs
        """Consola de eventos y errores en tiempo real"""
        frame = self.tab_logs                 # Referencia al frame de la pestaña

        tk.Label(                             # Título de la sección
            frame, text="Consola de Eventos y Errores",
            font=self.FUENTE_TITULO,          # Fuente grande
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(pady=(20, 5), anchor="w", padx=25)

        tk.Label(                             # Muestra la ruta del archivo de log
            frame,
            text=f"Archivo de log: {os.path.abspath(SistemaLogs.ARCHIVO_LOG)}",  # Ruta absoluta
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25)           # Alineado a la izquierda

        consola = scrolledtext.ScrolledText(  # Área de texto con scroll automático
            frame,
            bg="#0A0C14",                     # Fondo negro para efecto terminal
            fg="#A3E635",                     # Texto verde estilo terminal
            font=self.FUENTE_MONO,            # Fuente monoespaciada para alinear columnas
            relief="flat", bd=0,              # Sin borde
            insertbackground="#A3E635"        # Cursor verde
        )
        consola.pack(fill="both", expand=True, padx=20, pady=10)  # Ocupa todo el espacio

        SistemaLogs._widget_consola = consola  # Conecta la consola con el sistema de logs

        fila = tk.Frame(frame, bg=self.COLORES["fondo"])  # Frame para los botones de la consola
        fila.pack(fill="x", padx=20, pady=(0, 10))  # Debajo de la consola

        self._btn(                            # Botón para limpiar el contenido de la consola
            fila, "🗑  Limpiar Consola",
            self.COLORES["texto_dim"],        # Color gris
            lambda: consola.delete("1.0", tk.END)  # Borra todo el texto de la consola
        ).pack(side="left", padx=5, ipadx=10, ipady=4)

        self._btn(                            # Botón para leer y mostrar el archivo de log
            fila, "📄  Ver Archivo Log",
            self.COLORES["acento"],           # Color azul
            self._abrir_log_archivo           # Función que lee el archivo
        ).pack(side="left", padx=5, ipadx=10, ipady=4)

    def _abrir_log_archivo(self):             # Lee el archivo de log y lo muestra en la consola
        """Carga el contenido del archivo de log en la consola"""
        try:                                   # Intenta abrir el archivo de log
            with open(SistemaLogs.ARCHIVO_LOG, "r", encoding="utf-8") as f:  # Abre en modo lectura
                contenido = f.read()          # Lee todo el contenido del archivo
            if SistemaLogs._widget_consola:   # Verifica que la consola esté disponible
                SistemaLogs._widget_consola.delete("1.0", tk.END)  # Limpia la consola
                SistemaLogs._widget_consola.insert(tk.END, contenido)  # Inserta el contenido
                SistemaLogs._widget_consola.see(tk.END)  # Hace scroll al final
        except FileNotFoundError:             # Si el archivo aún no existe
            messagebox.showinfo("Info", "El archivo de log aún no existe.")  # Informa al usuario
   
    def _btn(self, parent, texto, color, comando):  # Crea un botón con estilo personalizado
        """Crea y retorna un botón estilizado con el color dado"""
        return tk.Button(                     # Retorna el botón creado (sin empacar)
            parent,                           # Frame padre donde se colocará el botón
            text=texto,                       # Texto visible del botón
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg="white",                       # Texto siempre blanco
            bg=color,                         # Fondo con el color recibido
            activebackground=color,           # Mismo color al presionar
            activeforeground="white",         # Texto blanco al presionar
            relief="flat",                    # Sin relieve para look moderno
            bd=0,                             # Sin borde
            cursor="hand2",                   # Cursor de mano al pasar por encima
            command=comando                   # Función que ejecuta el botón
        )

    def _crear_tabla(self, parent, columnas, height=8):  # Crea una tabla estilizada
        """Crea un Treeview con scrollbar vertical y estilos personalizados"""
        style = ttk.Style()                   # Objeto de estilos de ttk
        style.configure(                      # Configura el estilo de las filas de la tabla
            "FJ.Treeview",
            background=self.COLORES["tarjeta"],       # Fondo oscuro de las filas
            fieldbackground=self.COLORES["tarjeta"],  # Fondo del área de datos
            foreground=self.COLORES["texto"],         # Texto claro
            rowheight=28,                             # Altura de cada fila en píxeles
            font=self.FUENTE_SMALL)                   # Fuente de las celdas
        style.configure(                      # Configura el estilo de los encabezados
            "FJ.Treeview.Heading",
            background=self.COLORES["borde"], # Fondo del encabezado
            foreground=self.COLORES["texto"], # Texto del encabezado
            font=("Segoe UI", 9, "bold"),     # Fuente negrita para encabezados
            relief="flat")                    # Sin relieve en los encabezados
        style.map(                            # Define estilos para filas seleccionadas
            "FJ.Treeview",
            background=[("selected", self.COLORES["acento"])])  # Azul al seleccionar

        contenedor = tk.Frame(                # Frame contenedor de la tabla y el scroll
            parent,
            bg=self.COLORES["fondo"])         # Fondo oscuro
        contenedor.pack(                      # Ocupa el espacio disponible
            fill="both", expand=True, padx=20, pady=(0, 10))

        scroll = ttk.Scrollbar(               # Barra de desplazamiento vertical
            contenedor,
            orient="vertical")                # Orientación vertical
        tabla  = ttk.Treeview(               # Tabla de datos (Treeview)
            contenedor,
            columns=columnas,                 # Columnas definidas
            show="headings",                  # Solo muestra encabezados, no árbol
            height=height,                    # Número de filas visibles
            style="FJ.Treeview",              # Estilo personalizado
            yscrollcommand=scroll.set)        # Vincula la barra de scroll a la tabla
        scroll.config(command=tabla.yview)    # La barra controla el scroll vertical de la tabla
        scroll.pack(side="right", fill="y")   # La barra va a la derecha y ocupa toda la altura

        for col in columnas:                  # Configura cada columna de la tabla
            tabla.heading(col, text=col)      # Establece el texto del encabezado
            tabla.column(                     # Configura el ancho y alineación de la columna
                col, width=120,               # Ancho inicial de 120 píxeles
                minwidth=60,                  # Ancho mínimo de 60 píxeles
                anchor="center")              # Contenido centrado

        tabla.pack(side="left", fill="both", expand=True)  # La tabla ocupa el resto del espacio
        return tabla                          # Retorna la tabla para guardar referencia

if __name__ == "__main__":                    # Ejecuta 
    root = tk.Tk()                            # Crea la ventana raíz de Tkinter
    app  = AplicacionFJ(root)                 # Crea la aplicación pasando la ventana raíz
    root.mainloop()                           # Inicia el bucle principal de eventos de Tkinter          

