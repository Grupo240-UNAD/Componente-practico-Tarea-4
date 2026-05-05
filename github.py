from abc import ABC, abstractmethod
from datetime import datetime
import logging


# CONFIGURACIÓN DE LOGS

logging.basicConfig(
    filename="software_fj_logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def registrar_evento(mensaje):
    with open("software_fj_logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - EVENTO - {mensaje}\n")



# EXCEPCIONES PERSONALIZADAS

class SistemaError(Exception):
    pass


class ClienteError(SistemaError):
    pass


class ServicioError(SistemaError):
    pass


class ReservaError(SistemaError):
    pass



# CLASE ABSTRACTA BASE

class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def mostrar_info(self):
        pass



# CLIENTE

class Cliente(Entidad):
    def __init__(self, id_entidad, nombre, correo):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ClienteError("Nombre inválido. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise ClienteError("Correo electrónico inválido.")
        self._correo = valor.strip()

    def mostrar_info(self):
        return f"Cliente [{self.id_entidad}] - {self.nombre} - {self.correo}"



# SERVICIO ABSTRACTO

class Servicio(Entidad, ABC):
    def __init__(self, id_entidad, nombre, tarifa_base):
        super().__init__(id_entidad)
        if tarifa_base <= 0:
            raise ServicioError("La tarifa base debe ser mayor a cero.")
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def descripcion(self):
        pass



# SERVICIOS ESPECIALIZADOS

class ReservaSala(Servicio):
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        costo = self.tarifa_base * duracion
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def descripcion(self):
        return f"Reserva de sala: {self.nombre}"

    def mostrar_info(self):
        return f"Servicio Sala [{self.id_entidad}] - {self.nombre}"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        costo = (self.tarifa_base * duracion) + 20
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def descripcion(self):
        return f"Alquiler de equipo: {self.nombre}"

    def mostrar_info(self):
        return f"Servicio Equipo [{self.id_entidad}] - {self.nombre}"


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        costo = (self.tarifa_base * duracion) + 50
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def descripcion(self):
        return f"Asesoría especializada: {self.nombre}"

    def mostrar_info(self):
        return f"Servicio Asesoría [{self.id_entidad}] - {self.nombre}"



# RESERVA

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente no válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio no válido.")
        if duracion <= 0:
            raise ReservaError("La duración debe ser mayor a cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"
        registrar_evento(f"Reserva confirmada para {self.cliente.nombre}")

    def cancelar(self):
        self.estado = "Cancelada"
        registrar_evento(f"Reserva cancelada para {self.cliente.nombre}")

    def procesar_pago(self, impuesto=0.19, descuento=0):
        try:
            costo = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        except Exception as e:
            raise ReservaError("Error al procesar pago") from e
        else:
            registrar_evento(
                f"Pago procesado para {self.cliente.nombre} - Total: {costo}"
            )
            return costo
        finally:
            registrar_evento("Proceso de pago finalizado")

    def mostrar_reserva(self):
        return (
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | Estado: {self.estado}"
        )



# SISTEMA PRINCIPAL

class SoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        registrar_evento(f"Cliente agregado: {cliente.nombre}")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        registrar_evento(f"Servicio agregado: {servicio.nombre}")

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)
        registrar_evento(f"Reserva creada para: {reserva.cliente.nombre}")



# SIMULACIÓN DE OPERACIONES

def simular_operaciones():
    sistema = SoftwareFJ()

    operaciones = []

    # Clientes válidos e inválidos
    datos_clientes = [
        (1, "Juan Pérez", "juan@email.com"),
        (2, "Ana", "ana@email.com"),
        (3, "Li", "correo_invalido"),
        (4, "", "sin_nombre@email.com"),
    ]

    for datos in datos_clientes:
        try:
            cliente = Cliente(*datos)
            sistema.agregar_cliente(cliente)
            operaciones.append(cliente)
            print(cliente.mostrar_info())
        except Exception as e:
            logging.error(str(e))
            print(f"Error cliente: {e}")

    # Servicios válidos e inválidos
    servicios = [
        ReservaSala(101, "Sala Premium", 100),
        AlquilerEquipo(102, "Proyector HD", 80),
        AsesoriaEspecializada(103, "Consultoría TI", 150),
    ]

    for servicio in servicios:
        try:
            sistema.agregar_servicio(servicio)
            print(servicio.mostrar_info())
        except Exception as e:
            logging.error(str(e))
            print(f"Error servicio: {e}")

    try:
        servicio_invalido = ReservaSala(104, "Sala Básica", -50)
    except Exception as e:
        logging.error(str(e))
        print(f"Error servicio inválido: {e}")

    # Reservas exitosas y fallidas
    for i in range(10):
        try:
            cliente = sistema.clientes[i % len(sistema.clientes)]
            servicio = sistema.servicios[i % len(sistema.servicios)]
            duracion = i - 3  # algunas inválidas

            reserva = Reserva(cliente, servicio, duracion)
            sistema.agregar_reserva(reserva)
            reserva.confirmar()
            total = reserva.procesar_pago(descuento=0.05)
            print(reserva.mostrar_reserva())
            print(f"Total pagado: ${total:.2f}\n")

        except Exception as e:
            logging.error(str(e))
            print(f"Error reserva #{i+1}: {e}")



# EJECUCIÓN

if __name__ == "__main__":
    simular_operaciones()