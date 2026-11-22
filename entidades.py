# Módulo de Entidades para Gestion de Clientes y Servicios.
# Este módulo contiene las entidades y la clase cliente.

# Importa ABC y abstractmethod para definir clases y metodos abstractos.
from abc import ABC, abstractmethod

# Importa datetime para registrar la fecha y hora de creacion de cada entidad.
from datetime import datetime

# Importa re para validar formatos mediante expresiones regulares.
import re

# Importa la excepcion de validacion personalizada.
from excepciones import ValidacionError


# Clase abstracta base que representa cualquier entidad general dentro del sistema.
class EntidadBase(ABC):
    # Inicializa el identificador validado, la fecha de creacion y el estado activo.
    def __init__(self, id_entidad: str):
        # Valida y normaliza el ID recibido.
        self._id = self._validar_id(id_entidad)
        # Guarda la marca de tiempo actual de creacion.
        self._fecha_creacion = datetime.now()
        # Marca la entidad como activa por defecto.
        self._activo = True

    # Metodo estatico que valida que el ID sea un texto no vacio y lo normaliza.
    @staticmethod
    def _validar_id(valor: str) -> str:
        # Comprueba que sea string y que tras quitar espacios no quede vacio.
        if not isinstance(valor, str) or not valor.strip():
            # Lanza ValidacionError si el ID no es valido.
            raise ValidacionError(
                "El identificador de la entidad no puede estar vacio.", campo="id"
            )
        # Retorna el ID limpio y en mayusculas.
        return valor.strip().upper()

    # Propiedad de solo lectura para consultar el ID de la entidad.
    @property
    def id(self) -> str:
        # Devuelve el atributo protegido _id.
        return self._id

    # Propiedad de solo lectura para consultar la fecha de creacion.
    @property
    def fecha_creacion(self) -> datetime:
        # Devuelve el atributo protegido _fecha_creacion.
        return self._fecha_creacion

    # Propiedad de solo lectura para consultar si la entidad esta activa.
    @property
    def activo(self) -> bool:
        # Devuelve el atributo protegido _activo.
        return self._activo

    # Activa la entidad cambiando su estado a True.
    def activar(self) -> None:
        # Establece _activo en True.
        self._activo = True

    # Desactiva la entidad cambiando su estado a False.
    def desactivar(self) -> None:
        # Establece _activo en False.
        self._activo = False

    # Metodo abstracto que cada subclase debe implementar para devolver un resumen.
    @abstractmethod
    def resumen(self) -> str:
        # Cuerpo vacio porque es un metodo abstracto.
        pass

    # Metodo abstracto que cada subclase debe implementar para validar su estado interno.
    @abstractmethod
    def validar_estado(self) -> bool:
        # Cuerpo vacio porque es un metodo abstracto.
        pass


# Clase Cliente que hereda de EntidadBase e implementa encapsulacion y validaciones estrictas.
class Cliente(EntidadBase):
    # Patron regular para validar direcciones de correo electronico.
    _EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    # Constructor de Cliente con datos personales y empresa opcional.
    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        email: str,
        telefono: str,
        empresa: str = "Particular",
    ):
        # Inicializa los atributos heredados de EntidadBase.
        super().__init__(id_entidad)
        # Inicializa los campos internos protegidos antes de asignar via setters.
        self._nombre = ""
        # Inicializa el correo interno.
        self._email = ""
        # Inicializa el telefono interno.
        self._telefono = ""
        # Inicializa la empresa interna.
        self._empresa = ""

        # Asigna el nombre usando su setter para ejecutar validaciones.
        self.nombre = nombre
        # Asigna el correo usando su setter para ejecutar validaciones.
        self.email = email
        # Asigna el telefono usando su setter para ejecutar validaciones.
        self.telefono = telefono
        # Asigna la empresa usando su setter para ejecutar validaciones.
        self.empresa = empresa

    # Getter de la propiedad nombre.
    @property
    def nombre(self) -> str:
        # Retorna el nombre almacenado.
        return self._nombre

    # Setter de la propiedad nombre con validacion de longitud minima.
    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Verifica que sea texto y tenga al menos 2 caracteres utiles.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            # Lanza ValidacionError si el nombre es invalido.
            raise ValidacionError(
                "El nombre del cliente debe ser un texto de al menos 2 caracteres.",
                campo="nombre",
            )
        # Guarda el nombre sin espacios sobrantes en los extremos.
        self._nombre = valor.strip()

    # Getter de la propiedad email.
    @property
    def email(self) -> str:
        # Retorna el correo almacenado.
        return self._email

    # Setter de la propiedad email con validacion de formato.
    @email.setter
    def email(self, valor: str) -> None:
        # Verifica que sea texto y cumpla con _EMAIL_REGEX.
        if not isinstance(valor, str) or not self._EMAIL_REGEX.match(valor.strip()):
            # Lanza ValidacionError si el correo no es valido.
            raise ValidacionError(
                f"El correo electronico '{valor}' no tiene un formato valido.",
                campo="email",
            )
        # Normaliza el correo a minusculas y sin espacios.
        self._email = valor.strip().lower()

    # Getter de la propiedad telefono.
    @property
    def telefono(self) -> str:
        # Retorna el telefono almacenado.
        return self._telefono

    # Setter de la propiedad telefono con validacion de cantidad de digitos.
    @telefono.setter
    def telefono(self, valor: str) -> None:
        # Verifica que el valor sea una cadena de texto.
        if not isinstance(valor, str):
            # Lanza ValidacionError si no es string.
            raise ValidacionError(
                "El telefono debe ser una cadena de texto.", campo="telefono"
            )
        # Elimina espacios, guiones, signo mas y parentesis para contar solo digitos.
        digitos = re.sub(r"[\s\-\+\(\)]", "", valor)
        # Comprueba que todos los caracteres restantes sean digitos y longitud entre 7 y 15.
        if not digitos.isdigit() or not (7 <= len(digitos) <= 15):
            # Lanza ValidacionError si el telefono no cumple.
            raise ValidacionError(
                f"El telefono '{valor}' debe contener entre 7 y 15 digitos numericos.",
                campo="telefono",
            )
        # Guarda el telefono limpio de espacios en los extremos.
        self._telefono = valor.strip()

    # Getter de la propiedad empresa.
    @property
    def empresa(self) -> str:
        # Retorna la empresa almacenada.
        return self._empresa

    # Setter de la propiedad empresa con validacion de no vacio.
    @empresa.setter
    def empresa(self, valor: str) -> None:
        # Verifica que sea un string no vacio.
        if not isinstance(valor, str) or not valor.strip():
            # Lanza ValidacionError si esta vacio o no es texto.
            raise ValidacionError(
                "La empresa o tipo de cliente no puede estar vacio.", campo="empresa"
            )
        # Guarda el nombre de empresa sin espacios extremos.
        self._empresa = valor.strip()

    # Valida que el cliente tenga datos completos y este activo.
    def validar_estado(self) -> bool:
        # Retorna True solo si todos los campos requeridos existen y _activo es True.
        return bool(
            self._id
            and self._nombre
            and self._email
            and self._telefono
            and self._activo
        )

    # Genera una descripcion legible del cliente.
    def resumen(self) -> str:
        # Determina la etiqueta textual del estado.
        estado = "Activo" if self._activo else "Inactivo"
        # Construye y retorna la cadena de resumen.
        return (
            f"[{self._id}] {self._nombre} ({self._empresa}) | "
            f"Email: {self._email} | Tel: {self._telefono} | Estado: {estado}"
        )
