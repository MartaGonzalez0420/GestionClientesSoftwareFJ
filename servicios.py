# Módulo de Servicios para Gestion de Clientes y Servicios de dominio de Software FJ.
# Este módulo contiene la clase abstracta servicio y tres subclases especializadas para salas, equipos y asesorias.

# Importa ABC y abstractmethod para definir la clase abstracta Servicio.
from abc import ABC, abstractmethod

# Importa Any para tipar argumentos variables y valores genericos.
from typing import Any

# Importa EntidadBase como clase padre.
from entidades import EntidadBase

# Importa las excepciones de calculo y validacion.
from excepciones import CalculoFinancieroError, ValidacionError


# Clase abstracta que representa un servicio ofrecido por Software FJ.
class Servicio(EntidadBase, ABC):
    # Inicializa un servicio con ID, nombre, tarifa base y unidad de tiempo.
    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        unidad_tiempo: str = "hora",
    ):
        # Llama al constructor de EntidadBase.
        super().__init__(id_entidad)
        # Valida que el nombre del servicio tenga al menos 3 caracteres.
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            # Lanza ValidacionError si el nombre es invalido.
            raise ValidacionError(
                "El nombre del servicio debe tener al menos 3 caracteres.",
                campo="nombre",
            )
        # Valida que la unidad de tiempo sea una cadena no vacia.
        if not isinstance(unidad_tiempo, str) or not unidad_tiempo.strip():
            # Lanza ValidacionError si falta unidad de tiempo.
            raise ValidacionError(
                "La unidad de tiempo del servicio es obligatoria.",
                campo="unidad_tiempo",
            )

        # Guarda el nombre limpio.
        self._nombre = nombre.strip()
        # Guarda la unidad de tiempo en minusculas.
        self._unidad_tiempo = unidad_tiempo.strip().lower()
        # Inicializa la tarifa base temporalmente antes de pasar por el setter.
        self._tarifa_base = 0.0
        # Asigna la tarifa base usando su setter para validar.
        self.tarifa_base = tarifa_base

    # Propiedad de solo lectura para obtener el nombre del servicio.
    @property
    def nombre(self) -> str:
        # Retorna _nombre.
        return self._nombre

    # Propiedad de solo lectura para obtener la unidad de tiempo.
    @property
    def unidad_tiempo(self) -> str:
        # Retorna _unidad_tiempo.
        return self._unidad_tiempo

    # Getter de la propiedad tarifa_base.
    @property
    def tarifa_base(self) -> float:
        # Retorna _tarifa_base.
        return self._tarifa_base

    # Setter de tarifa_base que exige un numero positivo (excluyendo booleanos).
    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        # Verifica que no sea bool, que sea int o float y que sea mayor que 0.
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            # Lanza ValidacionError si la tarifa es invalida.
            raise ValidacionError(
                "La tarifa base del servicio debe ser un numero mayor que cero.",
                campo="tarifa_base",
            )
        # Guarda la tarifa como flotante.
        self._tarifa_base = float(valor)

    # Metodo abstracto para calcular el costo del servicio segun duracion y parametros.
    @abstractmethod
    def calcular_costo(self, duracion: float, **kwargs: Any) -> float:
        # Implementado en cada subclase.
        pass

    # Metodo abstracto para describir el servicio.
    @abstractmethod
    def describir(self) -> str:
        # Implementado en cada subclase.
        pass

    # Metodo abstracto para validar parametros antes de reservar el servicio.
    @abstractmethod
    def validar_parametros_reserva(self, duracion: float, **kwargs: Any) -> bool:
        # Implementado en cada subclase.
        pass

    # Valida que el servicio tenga datos validos y este activo.
    def validar_estado(self) -> bool:
        # Retorna True si cumple todas las condiciones.
        return bool(
            self._id and self._nombre and self._tarifa_base > 0 and self._activo
        )

    # Devuelve un resumen combinando la descripcion y la tarifa base.
    def resumen(self) -> str:
        # Retorna la cadena formateada.
        return f"{self.describir()} | Tarifa base: ${self._tarifa_base:,.2f}/{self._unidad_tiempo}"


# Subclase especializada para la reserva de salas.
class ReservaSala(Servicio):
    # Inicializa la sala con capacidad maxima y opcion de proyector.
    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        capacidad_maxima: int,
        incluye_proyector: bool = True,
    ):
        # Inicializa la clase padre Servicio con unidad de tiempo "hora".
        super().__init__(id_entidad, nombre, tarifa_base, unidad_tiempo="hora")
        # Valida que capacidad_maxima sea un entero positivo y no un booleano.
        if (
            isinstance(capacidad_maxima, bool)
            or not isinstance(capacidad_maxima, int)
            or capacidad_maxima <= 0
        ):
            # Lanza ValidacionError si la capacidad es invalida.
            raise ValidacionError(
                "La capacidad maxima de la sala debe ser un entero positivo.",
                campo="capacidad_maxima",
            )
        # Guarda la capacidad maxima.
        self._capacidad_maxima = capacidad_maxima
        # Guarda si incluye proyector como booleano.
        self._incluye_proyector = bool(incluye_proyector)

    # Propiedad de solo lectura para consultar la capacidad maxima.
    @property
    def capacidad_maxima(self) -> int:
        # Retorna _capacidad_maxima.
        return self._capacidad_maxima

    # Valida duracion y numero de asistentes contra la capacidad de la sala.
    def validar_parametros_reserva(self, duracion: float, **kwargs: Any) -> bool:
        # Extrae el parametro 'asistentes' de los argumentos opcionales.
        asistentes = kwargs.get("asistentes")
        # Valida que la duracion sea numerica y mayor que cero.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            # Lanza ValidacionError si la duracion es invalida.
            raise ValidacionError(
                "La duracion de la reserva de sala debe ser mayor a 0 horas.",
                campo="duracion",
            )
        # Verifica que se haya enviado el parametro 'asistentes'.
        if asistentes is None:
            # Lanza ValidacionError si falta 'asistentes'.
            raise ValidacionError(
                "Debe especificar el numero de 'asistentes' para reservar una sala.",
                campo="asistentes",
            )
        # Verifica que 'asistentes' sea un entero positivo.
        if (
            isinstance(asistentes, bool)
            or not isinstance(asistentes, int)
            or asistentes <= 0
        ):
            # Lanza ValidacionError si el numero de asistentes es invalido.
            raise ValidacionError(
                "El numero de asistentes debe ser un entero positivo.",
                campo="asistentes",
            )
        # Verifica que no exceda la capacidad maxima de la sala.
        if asistentes > self._capacidad_maxima:
            # Lanza ValidacionError si se supera el limite de personas.
            raise ValidacionError(
                f"Los asistentes ({asistentes}) superan la capacidad maxima de la sala ({self._capacidad_maxima}).",
                campo="asistentes",
            )
        # Retorna True si todas las validaciones pasan.
        return True

    # Calcula el costo de la sala aplicando recargo del 15% si supera el 75% de ocupacion.
    def calcular_costo(self, duracion: float, **kwargs: Any) -> float:
        # Valida primero los parametros de reserva.
        self.validar_parametros_reserva(duracion, **kwargs)
        # Obtiene la cantidad de asistentes ya validada.
        asistentes = kwargs["asistentes"]
        # Calcula el subtotal base multiplicando duracion por tarifa base.
        subtotal = float(duracion) * self._tarifa_base

        # Si los asistentes superan el 75% de la capacidad maxima, aplica recargo del 15%.
        if asistentes > self._capacidad_maxima * 0.75:
            # Multiplica el subtotal por 1.15.
            subtotal *= 1.15

        # Verifica que el subtotal resultante sea positivo.
        if subtotal <= 0:
            # Lanza CalculoFinancieroError si el resultado es inconsistente.
            raise CalculoFinancieroError(
                "El costo calculado para la reserva de sala no es valido."
            )
        # Redondea a 2 decimales y retorna.
        return round(subtotal, 2)

    # Describe la sala con su ID, nombre, capacidad y disponibilidad de proyector.
    def describir(self) -> str:
        # Define texto descriptivo del proyector.
        proyector = "con proyector" if self._incluye_proyector else "sin proyector"
        # Retorna la descripcion formateada.
        return (
            f"[Sala {self._id}] {self._nombre} "
            f"(Cap. max: {self._capacidad_maxima} personas, {proyector})"
        )


# Subclase especializada para el alquiler de equipos tecnologicos.
class AlquilerEquipo(Servicio):
    # Inicializa el alquiler con stock disponible y deposito de garantia opcional.
    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        stock_disponible: int,
        deposito_garantia: float = 0.0,
    ):
        # Inicializa Servicio con unidad de tiempo "dia".
        super().__init__(id_entidad, nombre, tarifa_base, unidad_tiempo="dia")
        # Valida que stock_disponible sea entero mayor o igual a 0.
        if (
            isinstance(stock_disponible, bool)
            or not isinstance(stock_disponible, int)
            or stock_disponible < 0
        ):
            # Lanza ValidacionError si el stock es invalido.
            raise ValidacionError(
                "El stock disponible debe ser un entero mayor o igual a cero.",
                campo="stock_disponible",
            )
        # Valida que deposito_garantia sea numerico y no negativo.
        if (
            isinstance(deposito_garantia, bool)
            or not isinstance(deposito_garantia, (int, float))
            or deposito_garantia < 0
        ):
            # Lanza ValidacionError si el deposito es negativo.
            raise ValidacionError(
                "El deposito de garantia no puede ser negativo.",
                campo="deposito_garantia",
            )
        # Guarda el stock disponible.
        self._stock_disponible = stock_disponible
        # Guarda el deposito de garantia como flotante.
        self._deposito_garantia = float(deposito_garantia)

    # Propiedad de solo lectura para consultar el stock actual.
    @property
    def stock_disponible(self) -> int:
        # Retorna _stock_disponible.
        return self._stock_disponible

    # Descuenta unidades del stock disponible si hay suficiente existencia.
    def consumir_stock(self, cantidad: int) -> None:
        # Comprueba si la cantidad solicitada supera el stock actual.
        if cantidad > self._stock_disponible:
            # Lanza ValidacionError si no hay suficiente stock.
            raise ValidacionError(
                f"Stock insuficiente para '{self._nombre}': solicitado {cantidad}, disponible {self._stock_disponible}.",
                campo="cantidad",
            )
        # Resta la cantidad al stock disponible.
        self._stock_disponible -= cantidad

    # Devuelve unidades al stock disponible cuando se cancela una reserva confirmada.
    def devolver_stock(self, cantidad: int) -> None:
        # Solo suma si la cantidad es positiva.
        if cantidad > 0:
            # Incrementa _stock_disponible.
            self._stock_disponible += cantidad

    # Valida duracion y cantidad de equipos solicitados frente al stock.
    def validar_parametros_reserva(self, duracion: float, **kwargs: Any) -> bool:
        # Obtiene la cantidad solicitada (por defecto 1).
        cantidad = kwargs.get("cantidad", 1)
        # Valida que la duracion sea positiva.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            # Lanza ValidacionError si la duracion no es valida.
            raise ValidacionError(
                "La duracion del alquiler debe ser mayor a 0 dias.", campo="duracion"
            )
        # Valida que cantidad sea un entero positivo.
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            # Lanza ValidacionError si la cantidad es invalida.
            raise ValidacionError(
                "La cantidad de equipos debe ser un entero positivo.", campo="cantidad"
            )
        # Valida que exista stock suficiente para cubrir la solicitud.
        if cantidad > self._stock_disponible:
            # Lanza ValidacionError si no alcanza el stock.
            raise ValidacionError(
                f"No hay suficiente stock de '{self._nombre}' ({cantidad} solicitados, {self._stock_disponible} disponibles).",
                campo="cantidad",
            )
        # Retorna True si la validacion es exitosa.
        return True

    # Calcula el costo del alquiler: (duracion * tarifa_base * cantidad) + deposito_garantia.
    def calcular_costo(self, duracion: float, **kwargs: Any) -> float:
        # Obtiene la cantidad solicitada (por defecto 1).
        cantidad = kwargs.get("cantidad", 1)
        # Valida los parametros de reserva.
        self.validar_parametros_reserva(duracion, cantidad=cantidad)
        # Calcula el subtotal sumando el deposito de garantia.
        subtotal = (
            float(duracion) * self._tarifa_base * cantidad
        ) + self._deposito_garantia
        # Verifica que el subtotal sea mayor que cero.
        if subtotal <= 0:
            # Lanza CalculoFinancieroError si el monto es invalido.
            raise CalculoFinancieroError(
                "El costo calculado para el alquiler de equipo no es valido."
            )
        # Redondea a 2 decimales y retorna.
        return round(subtotal, 2)

    # Describe el equipo con su ID, nombre, stock y deposito de garantia.
    def describir(self) -> str:
        # Retorna la cadena formateada.
        return (
            f"[Equipo {self._id}] {self._nombre} "
            f"(Stock: {self._stock_disponible}, Garantia: ${self._deposito_garantia:,.2f})"
        )


# Subclase especializada para asesorias tecnicas o profesionales.
class AsesoriaEspecializada(Servicio):
    # Inicializa la asesoria con su especialidad y horas minimas requeridas.
    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        horas_minimas: int = 1,
    ):
        # Inicializa Servicio con unidad de tiempo "hora".
        super().__init__(id_entidad, nombre, tarifa_base, unidad_tiempo="hora")
        # Valida que especialidad sea un texto de al menos 3 caracteres.
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            # Lanza ValidacionError si la especialidad es invalida.
            raise ValidacionError(
                "La especialidad de la asesoria es obligatoria.", campo="especialidad"
            )
        # Valida que horas_minimas sea un entero positivo.
        if (
            isinstance(horas_minimas, bool)
            or not isinstance(horas_minimas, int)
            or horas_minimas <= 0
        ):
            # Lanza ValidacionError si horas_minimas es invalido.
            raise ValidacionError(
                "Las horas minimas deben ser un entero positivo.", campo="horas_minimas"
            )
        # Guarda la especialidad limpia.
        self._especialidad = especialidad.strip()
        # Guarda las horas minimas.
        self._horas_minimas = horas_minimas

    # Propiedad de solo lectura para obtener la especialidad.
    @property
    def especialidad(self) -> str:
        # Retorna _especialidad.
        return self._especialidad

    # Valida que la duracion sea positiva y cumpla con las horas minimas.
    def validar_parametros_reserva(self, duracion: float, **kwargs: Any) -> bool:
        # Valida que duracion sea numerica y mayor que cero.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            # Lanza ValidacionError si la duracion es invalida.
            raise ValidacionError(
                "La duracion de la asesoria debe ser mayor a 0 horas.", campo="duracion"
            )
        # Verifica que la duracion no sea inferior a las horas minimas exigidas.
        if duracion < self._horas_minimas:
            # Lanza ValidacionError si no cumple el minimo.
            raise ValidacionError(
                f"La asesoria en '{self._especialidad}' requiere al menos {self._horas_minimas} hora(s); se solicito {duracion}.",
                campo="duracion",
            )
        # Retorna True si todo es valido.
        return True

    # Calcula el costo de la asesoria multiplicando duracion por tarifa base.
    def calcular_costo(self, duracion: float, **kwargs: Any) -> float:
        # Valida los parametros antes de calcular.
        self.validar_parametros_reserva(duracion, **kwargs)
        # Calcula el subtotal.
        subtotal = float(duracion) * self._tarifa_base
        # Verifica que el subtotal sea mayor que cero.
        if subtotal <= 0:
            # Lanza CalculoFinancieroError si el calculo es invalido.
            raise CalculoFinancieroError(
                "El costo calculado para la asesoria no es valido."
            )
        # Redondea a 2 decimales y retorna.
        return round(subtotal, 2)

    # Describe la asesoria con su ID, nombre, especialidad y horas minimas.
    def describir(self) -> str:
        # Retorna la cadena formateada.
        return (
            f"[Asesoria {self._id}] {self._nombre} "
            f"(Especialidad: {self._especialidad}, Min: {self._horas_minimas}h)"
        )
