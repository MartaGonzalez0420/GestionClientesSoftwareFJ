# Módulo de excepciones para Gestion de Clientes y Servicios de dominio de Software FJ.
# Este módulo contiene la jerarquía de excepciones.


# Excepcion base
class ErrorGestionClientes(Exception):
    """Excepción base para todos los errores de dominio de Software FJ."""

    # Inicializa la excepcion con un mensaje, un codigo de error y un diccionario de detalles opcional.
    def __init__(
        self, mensaje: str, codigo: str = "ERR_GENERAL", detalles: dict | None = None
    ):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo
        self.detalles = detalles or {}


# Define una excepcion para para datos invalidos , formatos incorrectos o prarámetros fuera de regla.
class ValidacionError(ErrorGestionClientes):
    """Error lanzado cuando un dato o parámetro no cumple con las reglas de validación."""

    # Inicializa el error de validación ndicando opcionalmente el campon afectado.
    def __init__(
        self, mensaje: str, campo: str | None = None, detalles: dict | None = None
    ):
        info = dict(detalles or {})
        if campo:
            info["campo"] = campo
        super().__init__(mensaje, codigo="ERR_VALIDACION", detalles=info)
        self.campo = campo


# Define una excepcion cuando no se encuentra un cliente, servicio o reserva solicitada.
class EntidadNoEncontradaError(ErrorGestionClientes):
    """Error lanzado cuando no se encuentra un cliente, servicio o reserva solicitada."""

    # Inicializa la excepcion con el tipo de entidad y el identificador buscado.
    def __init__(
        self, mensaje: str, tipo_entidad: str = "Entidad", identificador: str = ""
    ):
        super().__init__(
            mensaje,
            codigo="ERR_NO_ENCONTRADO",
            detalles={"tipo_entidad": tipo_entidad, "identificador": identificador},
        )


# Define una excepcion cuando un cliente, servicio o reserva ya existe y no se puede duplicar.
class ServicioNoDisponibleError(ErrorGestionClientes):
    """Error lanzado cuando un servicio está inactivo, sin cupo o no disponible."""

    # Inicializa la excepcion con el nombre del servicio afectado.
    def __init__(self, mensaje: str, servicio_id: str = ""):
        super().__init__(
            mensaje,
            codigo="ERR_SERVICIO_NO_DISPONIBLE",
            detalles={"servicio_id": servicio_id},
        )


# Define una excepcion cuando se intenta una operación o transiciones de estado no permitida en una reserva.
class OperacionReservaError(ErrorGestionClientes):
    """Error lanzado ante transiciones de estado inválidas o fallos al procesar reservas."""

    # Inicializa el error con el id de la reserva y su estado actual.
    def __init__(self, mensaje: str, reserva_id: str = "", estado_actual: str = ""):
        super().__init__(
            mensaje,
            codigo="ERR_OPERACION_RESERVA",
            detalles={"reserva_id": reserva_id, "estado_actual": estado_actual},
        )


# Define una excepcion para cálculos financieros inconsistentes, negativos o fuera de rango.
class CalculoFinancieroError(ErrorGestionClientes):
    """Error lanzado cuando ocurre un cálculo inconsistente, negativo o inválido."""

    # Inicializa el error con un mensaje y detalles numéricos opcionales.
    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_CALCULO_FINANCIERO", detalles=detalles)
