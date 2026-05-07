# Curso: Programación
# Grupo: 213023_240

# importamos las librerias sujeridas por el docente en el grupo de teams

import tkinter as tk                          # Librería principal para la ventana y widgets
from tkinter import ttk, messagebox, scrolledtext  # Widgets de cuadros de diálogo y texto
import datetime                               # Para obtener fecha y hora actuales de nuestro pc
import re                                     # Para validar correos con expresiones regulares
import os                                     # Para obtener rutas absolutas del sistema
from abc import ABC, abstractmethod           # Para definir clases y métodos abstractos

class ErrorSistemaFJ(Exception):             # Excepción raíz de todo el sistema
    """Excepción base del sistema Software FJ"""
    pass                                      # Solo define el tipo

class ErrorClienteInvalido(ErrorSistemaFJ):  # Error para datos de clientes
    """Datos del cliente no válidos"""
    pass                                      # Hereda todo de ErrorSistemaFJ

class ErrorServicioNoDisponible(ErrorSistemaFJ):  # Error cuando el servicio está inactivo
    """Servicio no disponible o inactivo"""
    pass                                      # Hereda todo de ErrorSistemaFJ

class ErrorReservaInvalida(ErrorSistemaFJ):  # Error para operaciones de reserva incorrectas
    """Parámetros de reserva incorrectos"""
    pass                                      # Hereda todo de ErrorSistemaFJ

class ErrorDuracionInvalida(ErrorReservaInvalida):  # Error específico de duración negativa o cero
    """Duración de reserva inválida"""
    pass                                      # Hereda de ErrorReservaInvalida

class ErrorCalculoCosto(ErrorSistemaFJ):     # Error cuando el cálculo de costo falla
    """Inconsistencia en el cálculo de costos"""
    pass                                      # Hereda todo de ErrorSistemaFJ

class SistemaLogs:                            # Clase utilitaria para registro de eventos
    """Registra eventos y errores en archivo y en la consola GUI"""

    ARCHIVO_LOG = "software_fj_logs.txt"      # Nombre del archivo donde se guardan los logs
    _widget_consola = None                     # Referencia al cuadro de texto de la GUI (se asigna luego)

    @staticmethod                              # Método de clase que no necesita instancia
    def registrar(tipo, mensaje):             # Recibe el tipo (ERROR/EVENTO) y el mensaje
        """Escribe un registro en archivo y en pantalla"""
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene fecha y hora actual de mi pc
        linea = f"[{ahora}] [{tipo.upper():7}] {mensaje}"              # Formatea la línea del log
        try:                                   # Intenta escribir en el archivo
            with open(SistemaLogs.ARCHIVO_LOG, "a", encoding="utf-8") as f:  # Abre en modo append
                f.write(linea + "\n")          # Escribe la línea con salto de línea
        except IOError:                        # Si el archivo no se puede abrir o escribir
            pass                               # Continúa sin interrumpir la aplicación
        if SistemaLogs._widget_consola:        # Verifica que el widget de consola exista
            SistemaLogs._widget_consola.insert(tk.END, linea + "\n")  # Inserta al final del texto
            SistemaLogs._widget_consola.see(tk.END)                   # Hace scroll automático al final

    @staticmethod                              # Método estático reutilizable
    def registrar_error(msg):                 # Atajo para registrar errores
        SistemaLogs.registrar("ERROR", msg)   # Llama a registrar con tipo ERROR

    @staticmethod                              # Método estático reutilizable
    def registrar_evento(msg):                # Atajo para registrar eventos normales
        SistemaLogs.registrar("EVENTO", msg)  # Llama a registrar con tipo EVENTO

class EntidadSistema(ABC):                    # Hereda de ABC para ser clase abstracta
    """Clase base abstracta para clientes, servicios y reservas"""

    @abstractmethod                            # Obliga a las subclases a implementar este método
    def obtener_info(self):                   # Cada entidad debe describirse
        """Retorna información descriptiva de la entidad"""
        pass                                   # Sin implementación en la clase abstracta

    @abstractmethod                            # Obliga a las subclases a implementar validación
    def validar(self):                        # Cada entidad valida sus propios datos
        """Valida que los datos de la entidad sean correctos"""
        pass                                   # Sin implementación en la clase abstracta

    def __str__(self):                         # Método especial para imprimir el objeto
        return self.obtener_info()             # Delega a obtener_info de la subclase

class Cliente(EntidadSistema):                # Hereda de EntidadSistema
    """Cliente con encapsulación completa y validaciones estrictas"""

    def __init__(self, nombre, cedula, correo, telefono):  # Constructor con 4 parámetros
        self.nombre   = nombre                # Llama el setter de nombre
        self.cedula   = cedula                # Llama el setter de cédula
        self.correo   = correo                # Llama el setter de correo
        self.telefono = telefono              # Llama el setter de teléfono 

    @property                                  # Define el getter de nombre
    def nombre(self):                         # Accede al atributo privado
        return self.__nombre                  # Retorna el valor encapsulado con doble guion bajo

    @nombre.setter                             # Define el setter de nombre
    def nombre(self, v):                      # v = valor recibido
        if not v or not v.strip():            # Verifica que no sea vacío ni solo espacios
            raise ErrorClienteInvalido("El nombre no puede estar vacío.")  # Lanza excepción
        if any(c.isdigit() for c in v):       # Verifica que no haya dígitos en el nombre
            raise ErrorClienteInvalido("El nombre no puede contener números.")  # Lanza excepción
        self.__nombre = v.strip()             # Guarda el nombre sin espacios al inicio o final


    @property                                  # Define el getter de cédula
    def cedula(self):                         # Accede al atributo privado
        return self.__cedula                  # Retorna el valor encapsulado

    @cedula.setter                             # Define el setter de cédula
    def cedula(self, v):                      # v = valor recibido
        if not str(v).isdigit() or len(str(v)) < 6:  # Verifica que sean solo dígitos y mínimo 6
            raise ErrorClienteInvalido("Cédula inválida: solo dígitos, mínimo 6.")  # Lanza excepción
        self.__cedula = str(v)                # Guarda la cédula como cadena de texto

    @property                                  # Define el getter de correo
    def correo(self):                         # Accede al atributo privado
        return self.__correo                  # Retorna el valor encapsulado

    @correo.setter                             # Define el setter de correo
    def correo(self, v):                      # v = valor recibido
        if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', v):  # Valida formato de email con regex
            raise ErrorClienteInvalido(f"Correo inválido: {v}")  # Lanza excepción con detalle
        self.__correo = v                     # Guarda el correo validado

    @property                                  # Define el getter de teléfono
    def telefono(self):                       # Accede al atributo privado
        return self.__telefono                # Retorna el valor encapsulado

    @telefono.setter                           # Define el setter de teléfono
    def telefono(self, v):                    # v = valor recibido
        if not str(v).isdigit() or len(str(v)) < 7:  # Solo dígitos y mínimo 7 caracteres
            raise ErrorClienteInvalido("Teléfono inválido: solo dígitos, mínimo 7.")  # Lanza excepción
        self.__telefono = str(v)              # Guarda el teléfono como cadena de texto

    def obtener_info(self):                   # Implementa el método abstracto de EntidadSistema
        return (f"{self.__nombre} | CC: {self.__cedula} "      # Retorna nombre y cédula
                f"| {self.__correo} | Tel: {self.__telefono}") # Agrega correo y teléfono

    def validar(self):                        # Implementa el método abstracto de EntidadSistema
        return True                           # Si llegó aquí, todos los setters ya validaron
    
class Servicio(EntidadSistema, ABC):          # Hereda de EntidadSistema y es abstracta
    """Clase abstracta base para todos los servicios de Software FJ"""

    def __init__(self, nombre, precio_hora, disponible=True):  # Constructor con disponibilidad opcional
        self.__nombre      = nombre           # Nombre del servicio (encapsulado)
        self.__precio_hora = precio_hora      # Precio base por hora (encapsulado)
        self.__disponible  = disponible       # True = activo, False = inactivo

    @property                                  # Getter del nombre del servicio
    def nombre(self):
        return self.__nombre                  # Retorna el nombre encapsulado

    @property                                  # Getter del precio por hora
    def precio_hora(self):
        return self.__precio_hora             # Retorna el precio encapsulado

    @property                                  # Getter del estado de disponibilidad
    def disponible(self):
        return self.__disponible              # Retorna True o False

    @disponible.setter                         # Setter para activar o desactivar el servicio
    def disponible(self, v):
        self.__disponible = bool(v)           # Convierte a booleano antes de guardar

    @abstractmethod                            # Subclases deben implementar calcular_costo
    def calcular_costo(self, horas, **kwargs): # **kwargs permite pasar descuento, impuesto, etc.
        pass                                   # Sin implementación en clase abstracta

    @abstractmethod                            # Subclases deben implementar describir
    def describir(self):                      # Retorna descripción específica del servicio
        pass                                   # Sin implementación en clase abstracta

    def validar(self):                        # Verifica disponibilidad del servicio
        if not self.__disponible:             # Si el servicio está inactivo
            raise ErrorServicioNoDisponible(  # Lanza excepción personalizada
                f"El servicio '{self.__nombre}' no está disponible.")
        return True                           # Si está disponible, retorna True

    def obtener_info(self):                   # Implementa el método abstracto
        estado = "✓ Disponible" if self.__disponible else "✗ No disponible"  # Texto del estado
        return f"{self.__nombre} | ${self.__precio_hora:,.0f}/hr | {estado}" # Formato legible
    
class ReservaSala(Servicio):                  # Hereda de la clase abstracta Servicio
    """Servicio para reservar salas de reuniones o conferencias"""

    def __init__(self, nombre_sala, capacidad):  # Constructor con nombre y capacidad
        super().__init__(f"Sala: {nombre_sala}", 50000)  # Llama al padre con precio $50.000/hr
        self.__capacidad   = capacidad        # Número de personas que caben en la sala
        self.__nombre_sala = nombre_sala      # Nombre de la sala para mostrar

    def calcular_costo(self, horas, descuento=0, impuesto=0.19):  # descuento e IVA son opcionales
        """Calcula costo total aplicando descuento e IVA del 19%"""
        if horas <= 0:                        # Valida que las horas sean positivas
            raise ErrorDuracionInvalida("Las horas deben ser mayores a 0.")  # Error de duración
        if not (0 <= descuento <= 1):         # El descuento debe estar entre 0 y 1 (0% a 100%)
            raise ErrorCalculoCosto("El descuento debe estar entre 0 y 1.")  # Error de cálculo
        base  = self.precio_hora * horas * (1 - descuento)  # Precio base menos el descuento
        total = base * (1 + impuesto)         # Aplica el impuesto sobre el valor descontado
        return round(total, 2)                # Retorna el total redondeado a 2 decimales

    def describir(self):                      # Implementa el método abstracto de Servicio
        return f"Sala '{self.__nombre_sala}' para {self.__capacidad} personas."  # Descripción clara

    def obtener_info(self):                   # Sobrescribe obtener_info para agregar capacidad
        return super().obtener_info() + f" | Cap: {self.__capacidad} personas"  # Agrega dato extra

    def validar(self):                        # Valida disponibilidad y capacidad
        super().validar()                     # Primero verifica disponibilidad (clase padre)
        if self.__capacidad <= 0:             # Verifica que la capacidad sea válida
            raise ErrorServicioNoDisponible("Capacidad de sala inválida.")  # Error de datos
        return True                           # Todo correcto


class AlquilerEquipo(Servicio):               # Hereda de Servicio
    """Servicio para alquilar equipos tecnológicos (laptops, proyectores, etc.)"""

    def __init__(self, tipo_equipo, cantidad):  # Constructor con tipo y cantidad
        super().__init__(f"Equipo: {tipo_equipo}", 30000)  # Precio base $30.000/hr por unidad
        self.__tipo_equipo = tipo_equipo      # Tipo de equipo (PC, Proyector, etc.)
        self.__cantidad    = cantidad         # Número de unidades a alquilar

    def calcular_costo(self, horas, descuento=0, impuesto=0.19):  # Parámetros opcionales
        """Costo por unidad multiplicado por cantidad, horas, descuento e IVA"""
        if horas <= 0:                        # Valida que las horas sean positivas
            raise ErrorDuracionInvalida("Las horas deben ser mayores a 0.")  # Error de duración
        base  = self.precio_hora * self.__cantidad * horas * (1 - descuento)  # Multiplica por cantidad
        total = base * (1 + impuesto)         # Agrega el impuesto al total
        return round(total, 2)                # Retorna con 2 decimales

    def describir(self):                      # Implementa el método abstracto
        return f"Alquiler de {self.__cantidad} {self.__tipo_equipo}(s)."  # Descripción del servicio

    def obtener_info(self):                   # Extiende la información base
        return super().obtener_info() + f" | {self.__tipo_equipo} x{self.__cantidad}"  # Agrega detalle

    def validar(self):                        # Valida disponibilidad y cantidad
        super().validar()                     # Primero verifica disponibilidad con el padre
        if self.__cantidad <= 0:              # Cantidad debe ser mayor a cero
            raise ErrorServicioNoDisponible("La cantidad de equipos debe ser > 0.")  # Muestra el error
        return True                           # Todo correcto

class AsesoriaTecnica(Servicio):              # Hereda de Servicio
    """Servicio de asesoría profesional con diferentes niveles de experiencia"""

    TARIFAS = {                               # Diccionario de tarifas según nivel del asesor
        "junior":  40000,                     # Asesor junior: $40.000/hr
        "senior":  80000,                     # Asesor senior: $80.000/hr
        "experto": 120000                     # Asesor experto: $120.000/hr
    }

    def __init__(self, area, nivel="senior"): # nivel por defecto es "senior"
        if nivel not in AsesoriaTecnica.TARIFAS:  # Verifica que el nivel exista en el diccionario
            raise ErrorServicioNoDisponible(f"Nivel '{nivel}' no reconocido.")  # Nivel inválido
        precio = AsesoriaTecnica.TARIFAS[nivel]   # Obtiene el precio según el nivel
        super().__init__(f"Asesoría {area}", precio)  # Llama al padre con nombre y precio
        self.__area  = area                   # Área de especialización (Redes, Software, etc.)
        self.__nivel = nivel                  # Guarda el nivel del asesor

    def calcular_costo(self, horas, descuento=0, impuesto=0.0):  # Sin IVA por defecto
        """Asesorías profesionales sin IVA por defecto"""
        if horas <= 0:                        # Valida que las horas sean positivas
            raise ErrorDuracionInvalida("Las horas deben ser mayores a 0.")  # Error de duración
        total = self.precio_hora * horas * (1 - descuento)  # Precio por horas menos descuento
        return round(total, 2)                # Retorna con 2 decimales

    def describir(self):                      # Implementa el método abstracto
        return f"Asesoría en {self.__area} - Nivel {self.__nivel}."  # Descripción del servicio

    def obtener_info(self):                   # Extiende la información base del servicio
        return super().obtener_info() + f" | {self.__area} ({self.__nivel})"  # Agrega área y nivel

    def validar(self):                        # Valida disponibilidad del servicio
        super().validar()                     # Verifica disponibilidad con el padre
        return True                           # Todo correcto

class Reserva:                                # Clase principal de gestión de reservas
    """Integra cliente y servicio con duración, estado y manejo de excepciones"""

    _contador = 0                             # Variable de clase para generar IDs únicos

    def __init__(self, cliente, servicio, horas, descuento=0):  # Constructor con 4 parámetros
        Reserva._contador += 1                # Incrementa el contador global de reservas
        self.__id        = Reserva._contador  # Asigna ID único a esta reserva
        self.__cliente   = cliente            # Objeto Cliente asociado a la reserva
        self.__servicio  = servicio           # Objeto Servicio que se reserva
        self.__horas     = horas              # Duración de la reserva en horas
        self.__descuento = descuento          # Descuento aplicable (0 = sin descuento)
        self.__estado    = "pendiente"        # Estado inicial: siempre empieza pendiente
        self.__costo     = 0.0               # Costo inicial: se calcula al confirmar
        self.__fecha     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # Fecha de creación

    @property                                  # Getter del ID de reserva
    def id(self):
        return self.__id                      # Retorna el ID único

    @property                                  # Getter del estado actual
    def estado(self):
        return self.__estado                  # Retorna pendiente/confirmada/cancelada/procesada

    @property                                  # Getter del costo calculado
    def costo(self):
        return self.__costo                   # Retorna el costo (0 si no está confirmada)

    @property                                  # Getter del cliente asociado
    def cliente(self):
        return self.__cliente                 # Retorna el objeto Cliente

    @property                                  # Getter del servicio asociado
    def servicio(self):
        return self.__servicio                # Retorna el objeto Servicio

    @property                                  # Getter de las horas de la reserva
    def horas(self):
        return self.__horas                   # Retorna la duración en horas

    @property                                  # Getter de la fecha de creación
    def fecha(self):
        return self.__fecha                   # Retorna la fecha como texto formateado

    def confirmar(self):                      # Método para confirmar la reserva
        """Valida datos y calcula el costo — usa try/except/else"""
        try:                                   # Bloque principal de validación
            self.__cliente.validar()          # Valida que el cliente tenga datos correctos
            self.__servicio.validar()         # Valida que el servicio esté disponible
            if self.__horas <= 0:             # Verifica que las horas sean válidas
                raise ErrorDuracionInvalida("Duración debe ser positiva.")  # Error de duración
            self.__costo = self.__servicio.calcular_costo(   # Calcula el costo total
                self.__horas, descuento=self.__descuento     # Pasa horas y descuento
            )
        except ErrorSistemaFJ as e:           # Captura cualquier error del sistema
            SistemaLogs.registrar_error(      # Registra el error en el log
                f"Error confirmando reserva #{self.__id}: {e}")
            raise ErrorReservaInvalida(       # Encadenamiento: lanza nueva excepción con causa
                f"No se pudo confirmar reserva #{self.__id}") from e  # 'from e' encadena el error
        else:                                  # El bloque else solo corre si NO hubo excepción
            self.__estado = "confirmada"      # Cambia el estado a confirmada
            SistemaLogs.registrar_evento(     # Registra el evento exitoso en el log
                f"Reserva #{self.__id} CONFIRMADA | {self.__cliente.nombre} "
                f"| {self.__servicio.nombre} | {self.__horas}h "
                f"| ${self.__costo:,.0f}")

    def cancelar(self):                       # Método para cancelar la reserva
        """Cancela la reserva si no fue procesada — usa try/except"""
        try:                                   # Intenta cancelar
            if self.__estado == "procesada":  # No se puede cancelar si ya fue procesada
                raise ErrorReservaInvalida(   # Lanza excepción específica
                    "No se puede cancelar una reserva ya procesada.")
            self.__estado = "cancelada"       # Cambia el estado a cancelada
            SistemaLogs.registrar_evento(     # Registra el evento en el log
                f"Reserva #{self.__id} CANCELADA | {self.__cliente.nombre}")
        except ErrorReservaInvalida as e:     # Captura el error de cancelación inválida
            SistemaLogs.registrar_error(str(e))  # Registra el error en el log
            raise                              # Relanza la excepción para que la GUI la muestre

    def procesar(self):                       # Método para procesar la reserva
        """Procesa la reserva — usa try/except/finally"""
        try:                                   # Intenta procesar
            if self.__estado != "confirmada": # Solo se procesan reservas confirmadas
                raise ErrorReservaInvalida(   # Lanza excepción si el estado no es correcto
                    f"Solo se procesan reservas confirmadas. "
                    f"Estado actual: {self.__estado}")
            self.__estado = "procesada"       # Cambia el estado a procesada
            SistemaLogs.registrar_evento(     # Registra el procesamiento exitoso
                f"Reserva #{self.__id} PROCESADA exitosamente.")
        except ErrorReservaInvalida as e:     # Captura errores de estado incorrecto
            SistemaLogs.registrar_error(str(e))  # Registra el error
            raise                              # Relanza para que la GUI lo informe
        finally:                               # Siempre se ejecuta, con o sin error
            SistemaLogs.registrar_evento(     # Registra el intento de procesamiento
                f"Ciclo de procesamiento reserva #{self.__id} finalizado.")

    def obtener_info(self):                   # Retorna texto con toda la info de la reserva
        iconos = {                             # Diccionario de íconos por estado
            "pendiente":  "⏳",               # Reloj de arena para pendiente
            "confirmada": "✅",               # Check verde para confirmada
            "cancelada":  "❌",               # Cruz roja para cancelada
            "procesada":  "🏁"               # Bandera para procesada
        }
        icono = iconos.get(self.__estado, "•")  # Obtiene el ícono del estado actual
        return (f"{icono} #{self.__id:03d} | {self.__fecha} | "   # ID formateado con 3 dígitos
                f"{self.__cliente.nombre} | {self.__servicio.nombre} | "  # Nombre cliente y servicio
                f"{self.__horas}h | ${self.__costo:,.0f} | {self.__estado.upper()}")  # Horas y costo  
        
class AplicacionFJ:                           # Clase principal de la aplicación gráfica
    """Interfaz gráfica principal del sistema Software FJ con Tkinter"""

    # ── Paleta de colores del tema oscuro corporativo ─────────────────
    COLORES = {
        "fondo"       : "#0F1117",            # Color de fondo principal (negro azulado)
        "panel"       : "#1A1D27",            # Color de paneles y sidebar (gris oscuro)
        "tarjeta"     : "#22263A",            # Color de tarjetas y tablas
        "borde"       : "#2E3250",            # Color de bordes sutiles
        "acento"      : "#4F6EF7",            # Azul corporativo para botones principales
        "acento2"     : "#7C3AED",            # Púrpura para servicios
        "exito"       : "#10B981",            # Verde para confirmaciones exitosas
        "peligro"     : "#EF4444",            # Rojo para errores y cancelaciones
        "advertencia" : "#F59E0B",            # Amarillo para advertencias
        "texto"       : "#E2E8F0",            # Color de texto principal (blanco suave)
        "texto_dim"   : "#64748B",            # Color de texto secundario (gris)
        "entrada"     : "#2D3250",            # Fondo oscuro para campos de texto
    }

    FUENTE_TITULO = ("Segoe UI", 20, "bold")  # Fuente grande para títulos de sección
    FUENTE_SUBTIT = ("Segoe UI", 13, "bold")  # Fuente mediana para subtítulos
    FUENTE_NORMAL = ("Segoe UI", 10)          # Fuente estándar para texto y entradas
    FUENTE_SMALL  = ("Segoe UI", 9)           # Fuente pequeña para etiquetas y botones
    FUENTE_MONO   = ("Consolas", 9)           # Fuente monoespaciada para la consola de logs

    def __init__(self, root):                 # Constructor recibe la ventana raíz de Tkinter
        self.root = root                      # Guarda referencia a la ventana principal
        self.root.title("Software FJ-Componente practico Tarea #4")  # Título de la ventana
        self.root.geometry("1280x800")        # Tamaño inicial de la ventana en píxeles
        self.root.minsize(1100, 700)          # Tamaño mínimo para no deformar la interfaz
        self.root.configure(bg=self.COLORES["fondo"])  # Fondo oscuro en la ventana raíz

        self.clientes  = []                   # Lista de objetos Cliente registrados
        self.servicios = []                   # Lista de objetos Servicio disponibles
        self.reservas  = []                   # Lista de objetos Reserva creadas

        self._cargar_datos_demo()             # Carga clientes y servicios de ejemplo al iniciar
        self._construir_ui()                  # Construye toda la interfaz gráfica
        SistemaLogs.registrar_evento("Aplicación Software FJ iniciada.")  # Log de inicio

    
    def _cargar_datos_demo(self):             # Agrega datos de ejemplo al arrancar
        """Carga datos iniciales de demostración"""
        try:                                   # Intenta crear clientes de ejemplo
            self.clientes.append(Cliente("Ana Gómez",   "1023456789", "ana@empresa.com",   "3001234567"))  # Cliente 1
            self.clientes.append(Cliente("Luis Torres", "9876543210", "luis@correo.com",   "3109876543"))  # Cliente 2
            self.clientes.append(Cliente("María Ruiz",  "1122334455", "maria@unad.edu.co", "3201234567"))  # Cliente 3
        except ErrorClienteInvalido as e:     # Si algún dato es inválido
            SistemaLogs.registrar_error(f"Demo clientes: {e}")  # Registra el error

        try:                                   # Intenta crear servicios de ejemplo
            self.servicios.append(ReservaSala("Sala Bogotá",    20))              # Sala para 20 personas
            self.servicios.append(ReservaSala("Sala Medellín",  10))              # Sala para 10 personas
            self.servicios.append(AlquilerEquipo("Laptop",       5))              # 5 laptops disponibles
            self.servicios.append(AlquilerEquipo("Proyector",    2))              # 2 proyectores
            self.servicios.append(AsesoriaTecnica("Redes",      "senior"))        # Asesor de redes senior
            self.servicios.append(AsesoriaTecnica("Software",   "experto"))       # Asesor de software experto
        except ErrorSistemaFJ as e:           # Si algún servicio tiene datos inválidos
            SistemaLogs.registrar_error(f"Demo servicios: {e}")  # Registra el error

    def _construir_ui(self):                  # Método principal de construcción de la UI
        """Construye header, sidebar y área de contenido"""
        self._crear_header()                  # Crea la barra superior con título y reloj
        self._crear_contenedor_principal()    # Crea el sidebar y el área de pestañas

    
    def _crear_header(self):                  # Construye la barra de encabezado
        """Barra superior con logo, título y reloj"""
        header = tk.Frame(                    # Crea el frame del header
            self.root,                        # Lo agrega a la ventana raíz
            bg=self.COLORES["panel"],         # Fondo del header
            height=65,                        # Altura fija de 65 píxeles
            bd=0)                             # Sin borde
        header.pack(fill="x", side="top")     # Ocupa todo el ancho en la parte superior
        header.pack_propagate(False)          # Mantiene la altura fija aunque el contenido sea menor

        tk.Label(                             # Etiqueta con el nombre del sistema
            header,
            text="⬡ SOFTWARE FJ",            # Texto con ícono hexagonal
            font=("Segoe UI", 16, "bold"),    # Fuente grande y negrita
            fg=self.COLORES["acento"],        # Color azul corporativo
            bg=self.COLORES["panel"]          # Fondo igual al header
        ).pack(side="left", padx=24, pady=15) # Alineado a la izquierda

        tk.Label(                             # Subtítulo descriptivo del sistema
            header,
            text="Sistema Integral de Gestión de Clientes, Servicios y Reservas",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris suave
            bg=self.COLORES["panel"]          # Fondo del header
        ).pack(side="left", padx=5, pady=18)  # A la derecha del logo
        
        tk.Label(                             # Subtítulo descriptivo del sistema
            header,
            text="Grupo: 213023_240",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris suave
            bg=self.COLORES["panel"]          # Fondo del header
        ).pack(side="left", padx=5, pady=15)  # A la derecha del logo
        
        tk.Label(                             # Subtítulo descriptivo del sistema
            header,
            text="Materia: Programación",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris suave
            bg=self.COLORES["panel"]          # Fondo del header
        ).pack(side="left", padx=5, pady=15)  # A la derecha del logo
        

        self.lbl_hora = tk.Label(             # Etiqueta para mostrar el reloj
            header,
            text="",                          # Texto vacío inicialmente, se actualiza cada segundo
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["panel"]          # Fondo del header
        )
        self.lbl_hora.pack(side="right", padx=24)  # Alineado a la derecha del header
        self._actualizar_hora()               # Inicia el ciclo de actualización del reloj

        tk.Frame(                             # Línea separadora debajo del header
            self.root,
            bg=self.COLORES["borde"],         # Color de borde sutil
            height=1                          # Solo 1 píxel de alto
        ).pack(fill="x")                      # Ocupa todo el ancho

    def _actualizar_hora(self):               # Método que actualiza el reloj cada segundo
        """Actualiza el reloj del header cada segundo"""
        self.lbl_hora.config(                 # Modifica el texto de la etiqueta
            text=datetime.datetime.now().strftime("📅 %A, %d/%m/%Y   🕐 %H:%M:%S"))  # Formato completo
        self.root.after(1000, self._actualizar_hora)  # Llama a sí mismo después de 1000ms (1 segundo)
            
    def _crear_contenedor_principal(self):    # Divide la ventana en dos columnas
        """Crea el layout principal: sidebar + área de pestañas"""
        contenedor = tk.Frame(                # Frame contenedor principal
            self.root,
            bg=self.COLORES["fondo"])         # Fondo oscuro
        contenedor.pack(fill="both", expand=True)  # Ocupa todo el espacio disponible

        sidebar = tk.Frame(                   # Frame del menú lateral izquierdo
            contenedor,
            bg=self.COLORES["panel"],         # Fondo más claro que el principal
            width=210,                        # Ancho fijo del sidebar
            bd=0)                             # Sin borde
        sidebar.pack(side="left", fill="y")   # Se ancla a la izquierda y ocupa toda la altura
        sidebar.pack_propagate(False)         # Mantiene el ancho fijo

        self.area_contenido = tk.Frame(       # Frame del área de contenido (pestañas)
            contenedor,
            bg=self.COLORES["fondo"])         # Mismo fondo oscuro
        self.area_contenido.pack(             # Ocupa el resto del espacio
            side="left", fill="both", expand=True)

        self._crear_sidebar(sidebar)          # Construye los botones del menú lateral
        self._crear_tabs()                    # Construye las 5 pestañas de contenido

    def _crear_sidebar(self, parent):         # Recibe el frame del sidebar como parámetro
        """Construye el menú lateral con botones de navegación"""
        tk.Label(                             # Título del menú lateral
            parent,
            text="MENÚ PRINCIPAL",            # Texto en mayúsculas
            font=("Segoe UI", 8, "bold"),     # Fuente pequeña y negrita
            fg=self.COLORES["texto_dim"],     # Color gris secundario
            bg=self.COLORES["panel"]          # Fondo del sidebar
        ).pack(pady=(20, 5), padx=15, anchor="w")  # Margen superior y alineado a la izquierda

        botones = [                            # Lista de tuplas (texto, índice de pestaña)
            ("🏠  Dashboard",      0),         # Pestaña 0: Panel de control
            ("👤  Clientes",       1),         # Pestaña 1: Gestión de clientes
            ("🛠️  Servicios",      2),         # Pestaña 2: Gestión de servicios
            ("📋  Reservas",       3),         # Pestaña 3: Gestión de reservas
            ("📊  Logs / Eventos", 4),         # Pestaña 4: Consola de eventos
        ]
        self.boton_activo = None              # Referencia al botón actualmente seleccionado
        self.botones_nav  = []                # Lista de todos los botones del menú

        for texto, idx in botones:            # Itera sobre cada opción del menú
            btn = tk.Button(                  # Crea el botón de navegación
                parent,
                text=texto,                   # Texto del botón con ícono
                font=self.FUENTE_NORMAL,      # Fuente estándar
                fg=self.COLORES["texto"],     # Texto claro
                bg=self.COLORES["panel"],     # Fondo del sidebar
                activebackground=self.COLORES["acento"],  # Azul al pasar el cursor
                activeforeground="white",     # Texto blanco al pasar el cursor
                relief="flat",                # Sin relieve para look moderno
                bd=0,                         # Sin borde
                anchor="w",                   # Texto alineado a la izquierda dentro del botón
                padx=20,                      # Padding horizontal interno
                pady=10,                      # Padding vertical interno
                cursor="hand2",               # Cursor de mano al pasar por encima
                command=lambda i=idx: self._cambiar_tab(i)  # Cambia a la pestaña correspondiente
            )
            btn.pack(fill="x", pady=1)        # Ocupa todo el ancho con separación entre botones
            self.botones_nav.append(btn)      # Agrega el botón a la lista de navegación

        tk.Frame(                             # Línea separadora en el sidebar
            parent,
            bg=self.COLORES["borde"],         # Color de borde
            height=1                          # Solo 1 píxel
        ).pack(fill="x", pady=10, padx=15)   # Con márgenes horizontales

        self.lbl_stats = tk.Label(            # Etiqueta de estadísticas rápidas
            parent,
            text="",                          # Se rellena con _actualizar_stats
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["panel"],         # Fondo del sidebar
            justify="left"                    # Texto alineado a la izquierda
        )
        self.lbl_stats.pack(pady=5, padx=15, anchor="w")  # Pegado a la izquierda
        self._actualizar_stats()              # Llena las estadísticas por primera vez

    def _actualizar_stats(self):              # Actualiza los contadores del sidebar
        """Actualiza los contadores de clientes, servicios y reservas"""
        activas = sum(                        # Cuenta reservas activas (confirmadas o procesadas)
            1 for r in self.reservas          # Itera todas las reservas
            if r.estado in ("confirmada", "procesada"))  # Solo las que están activas
        texto = (                             # Construye el texto de estadísticas
            f"📦 Clientes:  {len(self.clientes)}\n"   # Total de clientes
            f"🛠  Servicios: {len(self.servicios)}\n"  # Total de servicios
            f"📋 Reservas:  {len(self.reservas)}\n"   # Total de reservas
            f"✅ Activas:   {activas}")                # Reservas activas
        self.lbl_stats.config(text=texto)     # Actualiza el texto de la etiqueta

    def _crear_tabs(self):                    # Construye el contenedor de pestañas
        """Crea el Notebook con 5 pestañas y aplica estilos"""
        style = ttk.Style()                   # Objeto para personalizar estilos de ttk
        style.theme_use("clam")               # Usa el tema clam como base para personalizar
        style.configure(                      # Configura el estilo del contenedor de pestañas
            "Custom.TNotebook",
            background=self.COLORES["fondo"], # Fondo del notebook igual al principal
            borderwidth=0)                    # Sin borde exterior
        style.configure(                      # Configura el estilo de cada pestaña
            "Custom.TNotebook.Tab",
            background=self.COLORES["panel"], # Fondo de pestañas inactivas
            foreground=self.COLORES["texto_dim"],  # Texto gris en pestañas inactivas
            padding=[15, 8],                  # Padding interno de cada pestaña
            font=self.FUENTE_SMALL)           # Fuente de las pestañas
        style.map(                            # Define estilos para estados especiales
            "Custom.TNotebook.Tab",
            background=[("selected", self.COLORES["tarjeta"])],  # Fondo más claro en activa
            foreground=[("selected", self.COLORES["texto"])])     # Texto claro en activa

        self.notebook = ttk.Notebook(         # Crea el contenedor de pestañas
            self.area_contenido,              # Dentro del área de contenido
            style="Custom.TNotebook")         # Aplica el estilo personalizado
        self.notebook.pack(                   # Coloca el notebook en la interfaz
            fill="both", expand=True,         # Ocupa todo el espacio disponible
            padx=10, pady=10)                 # Con márgenes

        # Crea un Frame para cada pestaña
        self.tab_dashboard = tk.Frame(self.notebook, bg=self.COLORES["fondo"])  # Pestaña Dashboard
        self.tab_clientes  = tk.Frame(self.notebook, bg=self.COLORES["fondo"])  # Pestaña Clientes
        self.tab_servicios = tk.Frame(self.notebook, bg=self.COLORES["fondo"])  # Pestaña Servicios
        self.tab_reservas  = tk.Frame(self.notebook, bg=self.COLORES["fondo"])  # Pestaña Reservas
        self.tab_logs      = tk.Frame(self.notebook, bg=self.COLORES["fondo"])  # Pestaña Logs

        for tab, titulo in [                  # Itera las pestañas y sus títulos
            (self.tab_dashboard, "🏠 Dashboard"),   # Pestaña 0
            (self.tab_clientes,  "👤 Clientes"),    # Pestaña 1
            (self.tab_servicios, "🛠 Servicios"),   # Pestaña 2
            (self.tab_reservas,  "📋 Reservas"),    # Pestaña 3
            (self.tab_logs,      "📊 Logs"),        # Pestaña 4
        ]:
            self.notebook.add(tab, text=titulo)  # Agrega cada frame como pestaña con su título

        self._construir_dashboard()           # Construye el contenido del Dashboard
        self._construir_tab_clientes()        # Construye el formulario y tabla de clientes
        self._construir_tab_servicios()       # Construye el formulario y tabla de servicios
        self._construir_tab_reservas()        # Construye el formulario y tabla de reservas
        self._construir_tab_logs()            # Construye la consola de logs

    def _cambiar_tab(self, indice):           # Cambia la pestaña activa desde el sidebar
        """Cambia la pestaña seleccionada y resalta el botón del sidebar"""
        self.notebook.select(indice)          # Selecciona la pestaña por su índice
        for i, btn in enumerate(self.botones_nav):  # Recorre todos los botones del menú
            btn.config(                       # Actualiza el color del botón
                bg=self.COLORES["acento"] if i == indice  # Azul si es el activo
                else self.COLORES["panel"])   # Gris si no es el activo

    def _construir_dashboard(self):           # Construye el panel de control
        """Panel de métricas y últimas reservas"""
        frame = self.tab_dashboard            # Referencia al frame de la pestaña

        tk.Label(                             # Título principal del dashboard
            frame, text="Panel de Control",
            font=self.FUENTE_TITULO,          # Fuente grande
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(pady=(20, 5), anchor="w", padx=25)  # Alineado a la izquierda

        tk.Label(                             # Subtítulo descriptivo
            frame,
            text="Resumen general del sistema Software FJ",
            font=self.FUENTE_SMALL,           # Fuente pequeña
            fg=self.COLORES["texto_dim"],     # Color gris
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25)           # Alineado a la izquierda sin padding vertical

        fila = tk.Frame(frame, bg=self.COLORES["fondo"])  # Contenedor horizontal para las tarjetas
        fila.pack(fill="x", padx=20, pady=20)  # Ocupa el ancho completo

        metricas = [                           # Lista de configuración de cada tarjeta de métrica
            ("👤", "Clientes",    lambda: len(self.clientes),  self.COLORES["acento"]),      # Total clientes
            ("🛠",  "Servicios",  lambda: len(self.servicios), self.COLORES["acento2"]),     # Total servicios
            ("📋", "Reservas",   lambda: len(self.reservas),  self.COLORES["exito"]),       # Total reservas
            ("✅", "Confirmadas", lambda: sum(1 for r in self.reservas    # Cuenta solo confirmadas
                if r.estado == "confirmada"), self.COLORES["advertencia"]),
        ]
        self.lbl_metricas = []                # Lista para guardar referencias a las etiquetas numéricas

        for icono, etiqueta, fn, color in metricas:  # Crea una tarjeta por cada métrica
            tarjeta = tk.Frame(               # Frame de la tarjeta
                fila,
                bg=self.COLORES["tarjeta"],   # Fondo de la tarjeta
                relief="flat", bd=0)          # Sin relieve ni borde
            tarjeta.pack(                     # Coloca la tarjeta en la fila
                side="left", fill="both",
                expand=True, padx=8, ipady=20)

            tk.Label(                         # Ícono grande en la parte superior de la tarjeta
                tarjeta, text=icono,
                font=("Segoe UI", 22),        # Fuente grande para el ícono
                fg=color,                     # Color propio de cada métrica
                bg=self.COLORES["tarjeta"]    # Fondo de la tarjeta
            ).pack(pady=(15, 0))              # Margen superior

            lbl = tk.Label(                   # Número grande (el valor de la métrica)
                tarjeta, text=str(fn()),      # Llama a la función lambda para obtener el valor
                font=("Segoe UI", 28, "bold"),# Fuente grande y negrita
                fg=color,                     # Color propio de la métrica
                bg=self.COLORES["tarjeta"]    # Fondo de la tarjeta
            )
            lbl.pack()                        # Centra el número en la tarjeta
            self.lbl_metricas.append((lbl, fn))  # Guarda referencia para actualizar después

            tk.Label(                         # Etiqueta de texto debajo del número
                tarjeta, text=etiqueta,
                font=self.FUENTE_SMALL,       # Fuente pequeña
                fg=self.COLORES["texto_dim"], # Color gris
                bg=self.COLORES["tarjeta"]    # Fondo de la tarjeta
            ).pack(pady=(0, 15))              # Margen inferior

        tk.Label(                             # Subtítulo de la sección de reservas recientes
            frame, text="Últimas Reservas",
            font=self.FUENTE_SUBTIT,          # Fuente mediana
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25, pady=(5, 8))  # Con margen

        self.lista_recientes = tk.Listbox(    # Lista para mostrar las últimas reservas
            frame,
            bg=self.COLORES["tarjeta"],       # Fondo oscuro
            fg=self.COLORES["texto"],         # Texto claro
            font=self.FUENTE_MONO,            # Fuente monoespaciada para alineación
            selectbackground=self.COLORES["acento"],  # Azul al seleccionar
            relief="flat", bd=0,              # Sin borde
            height=8                          # Muestra hasta 8 filas
        )
        self.lista_recientes.pack(fill="x", padx=20, pady=(0, 10))  # Ocupa el ancho disponible
        self._refrescar_dashboard()           # Llena el dashboard con los datos actuales

    def _refrescar_dashboard(self):           # Actualiza todos los elementos del dashboard
        """Recalcula métricas y recarga la lista de reservas recientes"""
        for lbl, fn in self.lbl_metricas:    # Recorre cada par (etiqueta, función)
            lbl.config(text=str(fn()))        # Actualiza el número llamando a la función
        self.lista_recientes.delete(0, tk.END)  # Borra todos los ítems actuales de la lista
        for r in reversed(self.reservas[-8:]):  # Toma las últimas 8 reservas en orden inverso
            self.lista_recientes.insert(tk.END, "  " + r.obtener_info())  # Inserta al final
        self._actualizar_stats()              # Actualiza también los contadores del sidebar

    def _construir_tab_clientes(self):        # Construye la pestaña de clientes
        """Formulario de registro y tabla de clientes"""
        frame = self.tab_clientes             # Referencia al frame de la pestaña

        tk.Label(                             # Título de la sección
            frame, text="Gestión de Clientes",
            font=self.FUENTE_TITULO,          # Fuente grande
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(pady=(20, 2), anchor="w", padx=25)

        form = tk.LabelFrame(                 # Frame con borde y etiqueta para el formulario
            frame,
            text=" ✏  Nuevo Cliente ",        # Título del formulario
            font=self.FUENTE_SMALL,           # Fuente del título
            fg=self.COLORES["texto_dim"],     # Color del título del frame
            bg=self.COLORES["tarjeta"],       # Fondo oscuro del formulario
            relief="flat", bd=1)              # Borde mínimo
        form.pack(fill="x", padx=20, pady=10)  # Ocupa el ancho completo

        campos = [                             # Definición de campos del formulario
            ("Nombre completo", "cli_nombre"),  # Campo de nombre
            ("Cédula",          "cli_cedula"),  # Campo de cédula
            ("Correo",          "cli_correo"),  # Campo de correo
            ("Teléfono",        "cli_telefono"),# Campo de teléfono
        ]
        self.vars_cli = {}                    # Diccionario para guardar las variables de los campos

        for i, (etiqueta, key) in enumerate(campos):  # Itera cada campo del formulario
            col = (i % 2) * 2                 # Columna: 0 para pares, 2 para impares (layout 2 columnas)
            fila = i // 2                     # Fila: 0 para primeros dos campos, 1 para últimos dos
            tk.Label(                         # Etiqueta del campo
                form, text=etiqueta,
                font=self.FUENTE_SMALL,       # Fuente pequeña
                fg=self.COLORES["texto_dim"], # Color gris
                bg=self.COLORES["tarjeta"]    # Fondo del formulario
            ).grid(row=fila * 2, column=col, padx=15, pady=(10, 0), sticky="w")  # Posición en la grilla
            var = tk.StringVar()              # Variable que almacena el texto del campo
            entry = tk.Entry(                 # Campo de entrada de texto
                form,
                textvariable=var,             # Vinculado a la variable
                font=self.FUENTE_NORMAL,      # Fuente estándar
                bg=self.COLORES["entrada"],   # Fondo oscuro del campo
                fg=self.COLORES["texto"],     # Texto claro
                insertbackground=self.COLORES["texto"],  # Cursor blanco
                relief="flat", bd=0)          # Sin borde
            entry.grid(                       # Posiciona el campo en la grilla
                row=fila * 2 + 1, column=col,
                padx=15, pady=(2, 10),
                sticky="ew", ipady=6)         # ipady da más altura al campo
            form.columnconfigure(col, weight=1)  # Las columnas se expanden proporcionalmente
            self.vars_cli[key] = var          # Guarda la variable con su clave

        self._btn(                            # Botón para registrar el cliente
            form,
            "➕  Registrar Cliente",          # Texto del botón
            self.COLORES["acento"],           # Color azul
            self._registrar_cliente           # Función que se ejecuta al presionar
        ).grid(row=4, column=0, columnspan=4, padx=15, pady=10, sticky="ew")  # Ocupa todo el ancho

        tk.Label(                             # Subtítulo de la tabla
            frame, text="Clientes Registrados",
            font=self.FUENTE_SUBTIT,          # Fuente mediana
            fg=self.COLORES["texto"],         # Texto claro
            bg=self.COLORES["fondo"]          # Fondo oscuro
        ).pack(anchor="w", padx=25, pady=(5, 5))

        cols = ("ID", "Nombre", "Cédula", "Correo", "Teléfono")  # Columnas de la tabla
        self.tabla_cli = self._crear_tabla(frame, cols, height=7)  # Crea la tabla con 7 filas visibles
        self._refrescar_tabla_clientes()      # Llena la tabla con los clientes actuales

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

