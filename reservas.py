# Módulo de Reservas para Gestion de Clientes y Servicios.
# Este módulo contiene la clase Reserva, su ciclo de vida y las validaciones asociadas.


# Importa Enum para representar los estados posibles de una reserva.
from enum import Enum

# Importa Any para tipar diccionarios de parametros.
from typing import Any

# Importa Cliente y EntidadBase.
from entidades import Cliente, EntidadBase

# Importa las excepciones de dominio necesarias.
from excepciones import (
    CalculoFinancieroError,
    OperacionReservaError,
    ServicioNoDisponibleError,
    ValidacionError,
)

# Importa AlquilerEquipo y la clase base Servicio.
from servicios import AlquilerEquipo, Servicio


# Enumeracion de estados del ciclo de vida de una reserva.
class EstadoReserva(str, Enum):
    # Reserva creada pero aun no confirmada.
    PENDIENTE = "PENDIENTE"
    # Reserva confirmada (y con stock apartado si es equipo).
    CONFIRMADA = "CONFIRMADA"
    # Reserva cerrada financieramente con monto final registrado.
    PROCESADA = "PROCESADA"
    # Reserva cancelada.
    CANCELADA = "CANCELADA"


# Clase Reserva que integra un cliente, un servicio, duracion y estado.
class Reserva(EntidadBase):
    # Inicializa una reserva validando cliente, servicio y parametros.
    def __init__(
        self,
        id_entidad: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        parametros_servicio: dict[str, Any] | None = None,
    ):
        # Inicializa EntidadBase con el ID de reserva.
        super().__init__(id_entidad)

        # Verifica que 'cliente' sea una instancia de Cliente.
        if not isinstance(cliente, Cliente):
            # Lanza ValidacionError si no es Cliente.
            raise ValidacionError(
                "La reserva requiere una instancia valida de Cliente.", campo="cliente"
            )
        # Verifica que el cliente este activo y tenga datos validos.
        if not cliente.validar_estado():
            # Lanza ValidacionError si el cliente no es valido o esta inactivo.
            raise ValidacionError(
                f"El cliente '{cliente.id}' no esta activo o tiene datos invalidos.",
                campo="cliente",
            )
        # Verifica que 'servicio' sea una instancia de Servicio.
        if not isinstance(servicio, Servicio):
            # Lanza ValidacionError si no es Servicio.
            raise ValidacionError(
                "La reserva requiere una instancia valida de Servicio.",
                campo="servicio",
            )
        # Verifica que el servicio este activo y en estado valido.
        if not servicio.activo or not servicio.validar_estado():
            # Lanza ServicioNoDisponibleError si el servicio no puede reservarse.
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' ({servicio.id}) no esta disponible.",
                servicio_id=servicio.id,
            )

        # Copia los parametros adicionales o crea un diccionario vacio.
        params = dict(parametros_servicio or {})
        # Valida la duracion y los parametros especificos del servicio.
        servicio.validar_parametros_reserva(duracion, **params)

        # Guarda la referencia al cliente.
        self._cliente = cliente
        # Guarda la referencia al servicio.
        self._servicio = servicio
        # Guarda la duracion como flotante.
        self._duracion = float(duracion)
        # Guarda los parametros del servicio.
        self._parametros_servicio = params
        # Establece el estado inicial en PENDIENTE.
        self._estado = EstadoReserva.PENDIENTE
        # Inicializa el monto final como None hasta que sea procesada.
        self._monto_final: float | None = None

    # Propiedad de solo lectura para consultar el cliente de la reserva.
    @property
    def cliente(self) -> Cliente:
        # Retorna _cliente.
        return self._cliente

    # Propiedad de solo lectura para consultar el servicio de la reserva.
    @property
    def servicio(self) -> Servicio:
        # Retorna _servicio.
        return self._servicio

    # Propiedad de solo lectura para consultar la duracion.
    @property
    def duracion(self) -> float:
        # Retorna _duracion.
        return self._duracion

    # Propiedad de solo lectura para consultar el estado actual.
    @property
    def estado(self) -> EstadoReserva:
        # Retorna _estado.
        return self._estado

    # Propiedad de solo lectura para consultar el monto final procesado.
    @property
    def monto_final(self) -> float | None:
        # Retorna _monto_final.
        return self._monto_final

    # Confirma una reserva pendiente y descuenta stock si aplica.
    def confirmar(self) -> None:
        # Inicia bloque try para capturar y encadenar errores de validacion.
        try:
            # Impide confirmar si la reserva fue cancelada.
            if self._estado == EstadoReserva.CANCELADA:
                # Lanza OperacionReservaError.
                raise OperacionReservaError(
                    f"No se puede confirmar la reserva '{self._id}' porque esta CANCELADA.",
                    reserva_id=self._id,
                    estado_actual=self._estado.value,
                )
            # Impide confirmar si no esta en estado PENDIENTE.
            if self._estado != EstadoReserva.PENDIENTE:
                # Lanza OperacionReservaError.
                raise OperacionReservaError(
                    f"Solo se pueden confirmar reservas PENDIENTES; estado actual: {self._estado.value}.",
                    reserva_id=self._id,
                    estado_actual=self._estado.value,
                )
            # Verifica que el servicio siga activo al momento de confirmar.
            if not self._servicio.activo:
                # Lanza ServicioNoDisponibleError.
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.id}' dejo de estar disponible.",
                    servicio_id=self._servicio.id,
                )

            # Si es alquiler de equipo, descuenta la cantidad solicitada del stock.
            if isinstance(self._servicio, AlquilerEquipo):
                # Obtiene cantidad (1 por defecto).
                cantidad = self._parametros_servicio.get("cantidad", 1)
                # Consume el stock disponible.
                self._servicio.consumir_stock(cantidad)

            # Cambia el estado de la reserva a CONFIRMADA.
            self._estado = EstadoReserva.CONFIRMADA
        # Captura ValidacionError y la encadena como OperacionReservaError.
        except ValidacionError as exc:
            # Usa 'from exc' para encadenar la excepcion original.
            raise OperacionReservaError(
                f"Fallo de validacion al confirmar la reserva '{self._id}': {exc.mensaje}",
                reserva_id=self._id,
                estado_actual=self._estado.value,
            ) from exc

    # Cancela una reserva y libera el stock si estaba confirmada y era alquiler de equipo.
    def cancelar(self, motivo: str = "Cancelacion solicitada por el usuario") -> None:
        # Impide cancelar una reserva ya procesada.
        if self._estado == EstadoReserva.PROCESADA:
            # Lanza OperacionReservaError.
            raise OperacionReservaError(
                f"No se puede cancelar la reserva '{self._id}' porque ya fue PROCESADA.",
                reserva_id=self._id,
                estado_actual=self._estado.value,
            )
        # Impide cancelar una reserva que ya esta cancelada.
        if self._estado == EstadoReserva.CANCELADA:
            # Lanza OperacionReservaError.
            raise OperacionReservaError(
                f"La reserva '{self._id}' ya se encuentra CANCELADA.",
                reserva_id=self._id,
                estado_actual=self._estado.value,
            )

        # Si estaba confirmada y era alquiler de equipo, devuelve las unidades al stock.
        if self._estado == EstadoReserva.CONFIRMADA and isinstance(
            self._servicio, AlquilerEquipo
        ):
            # Obtiene la cantidad reservada.
            cantidad = self._parametros_servicio.get("cantidad", 1)
            # Devuelve el stock al servicio.
            self._servicio.devolver_stock(cantidad)

        # Cambia el estado a CANCELADA.
        self._estado = EstadoReserva.CANCELADA
        # Registra el motivo de cancelacion en los parametros.
        self._parametros_servicio["motivo_cancelacion"] = motivo

    # Procesa una reserva confirmada registrando el monto final calculado.
    def procesar(self, monto_calculado: float) -> float:
        # Inicia bloque try para encadenar errores financieros o de validacion.
        try:
            # Verifica que la reserva este en estado CONFIRMADA.
            if self._estado != EstadoReserva.CONFIRMADA:
                # Lanza OperacionReservaError.
                raise OperacionReservaError(
                    f"La reserva '{self._id}' debe estar CONFIRMADA para procesarse (actual: {self._estado.value}).",
                    reserva_id=self._id,
                    estado_actual=self._estado.value,
                )
            # Verifica que monto_calculado sea un numero positivo y no un booleano.
            if (
                isinstance(monto_calculado, bool)
                or not isinstance(monto_calculado, (int, float))
                or monto_calculado <= 0
            ):
                # Lanza CalculoFinancieroError.
                raise CalculoFinancieroError(
                    f"Monto invalido para procesar la reserva '{self._id}': {monto_calculado}.",
                    detalles={"monto": monto_calculado},
                )

            # Guarda el monto final redondeado a dos decimales.
            self._monto_final = round(float(monto_calculado), 2)
            # Cambia el estado de la reserva a PROCESADA.
            self._estado = EstadoReserva.PROCESADA
            # Retorna el monto procesado.
            return self._monto_final
        # Captura errores financieros o de validacion y los encadena.
        except (CalculoFinancieroError, ValidacionError) as exc:
            # Encadena usando 'from exc'.
            raise OperacionReservaError(
                f"Error financiero al procesar la reserva '{self._id}': {exc.mensaje}",
                reserva_id=self._id,
                estado_actual=self._estado.value,
            ) from exc

    # Verifica la integridad de la reserva y sus entidades asociadas.
    def validar_estado(self) -> bool:
        # Retorna True si la reserva y sus entidades estan validas.
        return bool(
            self._id
            and self._cliente.validar_estado()
            and self._servicio.validar_estado()
        )

    # Genera un resumen legible con datos de la reserva, estado y monto.
    def resumen(self) -> str:
        # Formatea el monto final si ya existe.
        monto_str = (
            f"${self._monto_final:,.2f}"
            if self._monto_final is not None
            else "No procesado"
        )
        # Retorna la cadena de resumen completa.
        return (
            f"[Reserva {self._id}] Cliente: {self._cliente.nombre} ({self._cliente.id}) | "
            f"Servicio: {self._servicio.nombre} ({self._servicio.id}) | "
            f"Duracion: {self._duracion} {self._servicio.unidad_tiempo} | "
            f"Estado: {self._estado.value} | Monto: {monto_str}"
        )
