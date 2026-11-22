# Módulo de Gestor para Gestion de Clientes y Servicios
# Este módulo contiene la clase GestorSistemaFJ que administra clientes, servicios y reservas en memoria.

# Importa singledispatchmethod para sobrecargar metodos segun el tipo del primer argumento.
from functools import singledispatchmethod

# Importa Any para tipar argumentos genericos.
from typing import Any

# Importa la clase Cliente.
from entidades import Cliente

# Importa las excepciones del sistema.
from excepciones import (
    CalculoFinancieroError,
    EntidadNoEncontradaError,
    ErrorSistemaFJ,
    ValidacionError,
)

# Importa configurar_logger para registrar en archivo.
from logger import configurar_logger

# Importa la clase Reserva.
from reservas import Reserva

# Importa la clase abstracta Servicio.
from servicios import Servicio


# Gestor principal en memoria (sin base de datos) para clientes, servicios y reservas.
class GestorSistemaFJ:
    # Inicializa el logger y las listas internas en memoria.
    def __init__(self, archivo_log: str = "software_fj.log"):
        # Crea o recupera el logger del gestor.
        self.logger = configurar_logger("GestorSistemaFJ", archivo_log)
        # Lista interna de clientes registrados.
        self._clientes: list[Cliente] = []
        # Lista interna de servicios registrados.
        self._servicios: list[Servicio] = []
        # Lista interna de reservas creadas.
        self._reservas: list[Reserva] = []
        # Registra en el log el inicio del sistema en memoria.
        self.logger.info(
            "Sistema Software FJ inicializado en modo memoria (sin base de datos)."
        )

    # Propiedad que devuelve una copia de la lista de clientes.
    @property
    def clientes(self) -> list[Cliente]:
        # Retorna una nueva lista para proteger _clientes.
        return list(self._clientes)

    # Propiedad que devuelve una copia de la lista de servicios.
    @property
    def servicios(self) -> list[Servicio]:
        # Retorna una nueva lista para proteger _servicios.
        return list(self._servicios)

    # Propiedad que devuelve una copia de la lista de reservas.
    @property
    def reservas(self) -> list[Reserva]:
        # Retorna una nueva lista para proteger _reservas.
        return list(self._reservas)

    # Registra un objeto Cliente en la lista interna tras validar duplicados y estado.
    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        # Verifica que el objeto sea instancia de Cliente.
        if not isinstance(cliente, Cliente):
            # Lanza ValidacionError si no lo es.
            raise ValidacionError(
                "Solo se pueden registrar objetos de tipo Cliente.", campo="cliente"
            )
        # Verifica que no exista ya otro cliente con el mismo ID.
        if any(c.id == cliente.id for c in self._clientes):
            # Lanza ValidacionError si el ID esta duplicado.
            raise ValidacionError(
                f"Ya existe un cliente registrado con el ID '{cliente.id}'.", campo="id"
            )
        # Verifica que el cliente este en un estado valido.
        if not cliente.validar_estado():
            # Lanza ValidacionError si el estado es invalido.
            raise ValidacionError(
                f"El cliente '{cliente.id}' contiene datos invalidos.", campo="cliente"
            )

        # Agrega el cliente a la lista interna.
        self._clientes.append(cliente)
        # Registra el evento en el archivo de logs.
        self.logger.info(f"Cliente registrado: {cliente.resumen()}")
        # Retorna el cliente registrado.
        return cliente

    # Registra un objeto Servicio en la lista interna tras validar duplicados y estado.
    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        # Verifica que el objeto sea instancia de Servicio.
        if not isinstance(servicio, Servicio):
            # Lanza ValidacionError si no lo es.
            raise ValidacionError(
                "Solo se pueden registrar objetos de tipo Servicio.", campo="servicio"
            )
        # Verifica que no exista ya otro servicio con el mismo ID.
        if any(s.id == servicio.id for s in self._servicios):
            # Lanza ValidacionError si el ID esta duplicado.
            raise ValidacionError(
                f"Ya existe un servicio registrado con el ID '{servicio.id}'.",
                campo="id",
            )
        # Verifica que el servicio sea valido.
        if not servicio.validar_estado():
            # Lanza ValidacionError si no es valido.
            raise ValidacionError(
                f"El servicio '{servicio.id}' no es valido.", campo="servicio"
            )

        # Agrega el servicio a la lista interna.
        self._servicios.append(servicio)
        # Registra el evento en el archivo de logs.
        self.logger.info(f"Servicio registrado: {servicio.resumen()}")
        # Retorna el servicio registrado.
        return servicio

    # Busca un cliente por ID o lanza EntidadNoEncontradaError.
    def buscar_cliente(self, cliente_id: str) -> Cliente:
        # Normaliza el ID buscado si es string.
        clave = cliente_id.strip().upper() if isinstance(cliente_id, str) else ""
        # Recorre la lista de clientes buscando coincidencia de ID.
        for cliente in self._clientes:
            # Si coincide, retorna el cliente encontrado.
            if cliente.id == clave:
                # Retorna cliente.
                return cliente
        # Si no se encontro, lanza EntidadNoEncontradaError.
        raise EntidadNoEncontradaError(
            f"Cliente con ID '{cliente_id}' no encontrado.",
            tipo_entidad="Cliente",
            identificador=str(cliente_id),
        )

    # Busca un servicio por ID o lanza EntidadNoEncontradaError.
    def buscar_servicio(self, servicio_id: str) -> Servicio:
        # Normaliza el ID buscado si es string.
        clave = servicio_id.strip().upper() if isinstance(servicio_id, str) else ""
        # Recorre la lista de servicios buscando coincidencia de ID.
        for servicio in self._servicios:
            # Si coincide, retorna el servicio encontrado.
            if servicio.id == clave:
                # Retorna servicio.
                return servicio
        # Si no se encontro, lanza EntidadNoEncontradaError.
        raise EntidadNoEncontradaError(
            f"Servicio con ID '{servicio_id}' no encontrado.",
            tipo_entidad="Servicio",
            identificador=str(servicio_id),
        )

    # Busca una reserva por ID o lanza EntidadNoEncontradaError.
    def buscar_reserva(self, reserva_id: str) -> Reserva:
        # Normaliza el ID buscado si es string.
        clave = reserva_id.strip().upper() if isinstance(reserva_id, str) else ""
        # Recorre la lista de reservas buscando coincidencia de ID.
        for reserva in self._reservas:
            # Si coincide, retorna la reserva encontrada.
            if reserva.id == clave:
                # Retorna reserva.
                return reserva
        # Si no se encontro, lanza EntidadNoEncontradaError.
        raise EntidadNoEncontradaError(
            f"Reserva con ID '{reserva_id}' no encontrada.",
            tipo_entidad="Reserva",
            identificador=str(reserva_id),
        )

    # Metodo sobrecargado base segun el tipo del primer argumento ('fuente').
    @singledispatchmethod
    def calcular_costo_sobrecargado(
        self, fuente: Any, *args: Any, **kwargs: Any
    ) -> float:
        # Si el tipo no tiene variante registrada, lanza ValidacionError.
        raise ValidacionError(
            f"Tipo no soportado para calculo de costos: {type(fuente).__name__}.",
            campo="fuente",
        )

    # Variante sobrecargada cuando 'fuente' es una instancia de Reserva.
    @calcular_costo_sobrecargado.register
    def _(
        self,
        reserva: Reserva,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
    ) -> float:
        # Intenta calcular el costo base y aplicar descuento e impuesto.
        try:
            # Calcula el costo base del servicio asociado a la reserva.
            base = reserva.servicio.calcular_costo(
                reserva.duracion, **reserva._parametros_servicio
            )
            # Aplica porcentajes de descuento e impuesto.
            return self._aplicar_ajustes_financieros(base, descuento_pct, impuesto_pct)
        # Captura errores de dominio y los encadena como CalculoFinancieroError.
        except ErrorSistemaFJ as exc:
            # Encadena con 'from exc'.
            raise CalculoFinancieroError(
                f"Error al calcular el costo de la reserva '{reserva.id}': {exc.mensaje}",
                detalles={"reserva_id": reserva.id},
            ) from exc

    # Variante sobrecargada cuando 'fuente' es una instancia de Servicio.
    @calcular_costo_sobrecargado.register
    def _(
        self,
        servicio: Servicio,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        **kwargs: Any,
    ) -> float:
        # Intenta calcular el costo base del servicio y aplicar ajustes.
        try:
            # Calcula el costo base segun duracion y argumentos adicionales.
            base = servicio.calcular_costo(duracion, **kwargs)
            # Aplica porcentajes de descuento e impuesto.
            return self._aplicar_ajustes_financieros(base, descuento_pct, impuesto_pct)
        # Captura errores de dominio y los encadena como CalculoFinancieroError.
        except ErrorSistemaFJ as exc:
            # Encadena con 'from exc'.
            raise CalculoFinancieroError(
                f"Error al calcular el costo del servicio '{servicio.id}': {exc.mensaje}",
                detalles={"servicio_id": servicio.id, "duracion": duracion},
            ) from exc

    # Metodo estatico auxiliar para validar y aplicar descuentos e impuestos.
    @staticmethod
    def _aplicar_ajustes_financieros(
        base: float, descuento_pct: float, impuesto_pct: float
    ) -> float:
        # Valida que descuento_pct sea un numero entre 0 y 100.
        if (
            isinstance(descuento_pct, bool)
            or not isinstance(descuento_pct, (int, float))
            or not (0 <= descuento_pct <= 100)
        ):
            # Lanza CalculoFinancieroError si esta fuera de rango.
            raise CalculoFinancieroError(
                f"El porcentaje de descuento ({descuento_pct}) debe estar entre 0 y 100.",
                detalles={"descuento_pct": descuento_pct},
            )
        # Valida que impuesto_pct sea un numero entre 0 y 100.
        if (
            isinstance(impuesto_pct, bool)
            or not isinstance(impuesto_pct, (int, float))
            or not (0 <= impuesto_pct <= 100)
        ):
            # Lanza CalculoFinancieroError si esta fuera de rango.
            raise CalculoFinancieroError(
                f"El porcentaje de impuesto ({impuesto_pct}) debe estar entre 0 y 100.",
                detalles={"impuesto_pct": impuesto_pct},
            )

        # Aplica el porcentaje de descuento al monto base.
        con_descuento = base * (1.0 - float(descuento_pct) / 100.0)
        # Aplica el porcentaje de impuesto sobre el monto con descuento.
        total = con_descuento * (1.0 + float(impuesto_pct) / 100.0)
        # Verifica que el monto total final sea mayor que cero.
        if total <= 0:
            # Lanza CalculoFinancieroError si el total es cero o negativo.
            raise CalculoFinancieroError(
                "El monto total tras descuentos e impuestos debe ser mayor que cero.",
                detalles={
                    "base": base,
                    "descuento_pct": descuento_pct,
                    "impuesto_pct": impuesto_pct,
                },
            )
        # Redondea a dos decimales y retorna.
        return round(total, 2)

    # Crea y registra una nueva reserva en la lista interna.
    def crear_reserva(
        self,
        reserva_id: str,
        cliente_id: str,
        servicio_id: str,
        duracion: float,
        parametros_servicio: dict[str, Any] | None = None,
    ) -> Reserva:
        # Verifica que no exista ya una reserva con el mismo ID.
        if any(
            r.id == reserva_id.strip().upper()
            for r in self._reservas
            if isinstance(reserva_id, str)
        ):
            # Lanza ValidacionError si el ID esta duplicado.
            raise ValidacionError(
                f"Ya existe una reserva con el ID '{reserva_id}'.", campo="id"
            )

        # Busca el cliente por su ID.
        cliente = self.buscar_cliente(cliente_id)
        # Busca el servicio por su ID.
        servicio = self.buscar_servicio(servicio_id)
        # Instancia la reserva validando todos sus parametros.
        reserva = Reserva(
            id_entidad=reserva_id,
            cliente=cliente,
            servicio=servicio,
            duracion=duracion,
            parametros_servicio=parametros_servicio,
        )
        # Agrega la reserva a la lista interna.
        self._reservas.append(reserva)
        # Registra la creacion en el archivo de logs.
        self.logger.info(f"Reserva creada: {reserva.resumen()}")
        # Retorna la reserva creada.
        return reserva

    # Busca una reserva por ID y la confirma.
    def confirmar_reserva(self, reserva_id: str) -> Reserva:
        # Busca la reserva.
        reserva = self.buscar_reserva(reserva_id)
        # Ejecuta el metodo confirmar() de la reserva.
        reserva.confirmar()
        # Registra la confirmacion en el archivo de logs.
        self.logger.info(f"Reserva confirmada: {reserva.resumen()}")
        # Retorna la reserva confirmada.
        return reserva

    # Busca una reserva por ID y la cancela con el motivo indicado.
    def cancelar_reserva(
        self, reserva_id: str, motivo: str = "Cancelada por el usuario"
    ) -> Reserva:
        # Busca la reserva.
        reserva = self.buscar_reserva(reserva_id)
        # Ejecuta el metodo cancelar() de la reserva.
        reserva.cancelar(motivo=motivo)
        # Registra una advertencia en el archivo de logs.
        self.logger.warning(f"Reserva cancelada ({motivo}): {reserva.resumen()}")
        # Retorna la reserva cancelada.
        return reserva

    # Calcula el costo con sobrecarga y procesa financieramente la reserva.
    def procesar_reserva(
        self,
        reserva_id: str,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
    ) -> float:
        # Busca la reserva.
        reserva = self.buscar_reserva(reserva_id)
        # Calcula el monto usando la variante sobrecargada para Reserva.
        monto = self.calcular_costo_sobrecargado(
            reserva,
            descuento_pct=descuento_pct,
            impuesto_pct=impuesto_pct,
        )
        # Cierra la reserva con el monto calculado.
        total_procesado = reserva.procesar(monto)
        # Registra el procesamiento en el archivo de logs.
        self.logger.info(
            f"Reserva procesada por ${total_procesado:,.2f}: {reserva.resumen()}"
        )
        # Retorna el total procesado.
        return total_procesado

    # Registra cualquier excepcion en el archivo de logs sin detener la ejecucion.
    def registrar_error(self, operacion: str, exc: Exception) -> None:
        # Si es un error propio del sistema, registra codigo, mensaje y detalles.
        if isinstance(exc, ErrorSistemaFJ):
            # Escribe el error en el log.
            self.logger.error(
                f"[{operacion}] {exc.codigo} -> {exc.mensaje} | Detalles: {exc.detalles}"
            )
        # Si es una excepcion inesperada, registra el error y su traza.
        else:
            # Escribe la excepcion con traceback en el log.
            self.logger.exception(f"[{operacion}] Error inesperado: {exc}")
