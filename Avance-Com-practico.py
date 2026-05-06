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

    def _init_(self, root):                 # Constructor recibe la ventana raíz de Tkinter
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
            f"🛠️  Servicios: {len(self.servicios)}\n"  # Total de servicios
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
