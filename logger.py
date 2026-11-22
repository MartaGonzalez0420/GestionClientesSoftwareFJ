# Módulo de logger para Gestion de Clientes y Servicios de dominio de Software FJ.
# Este módulo contiene los logs del sistema y la configuración del logger.

# Importa el modulo estandar logging para registrar eventos y errores.
import logging

# Importa Path para manejar rutas de archivos de forma segura.
from pathlib import Path


# Configura y devuelve un logger que escribe eventos y errores en un archivo de texto.
def configurar_logger(
    nombre: str = "SoftwareFJ", archivo_log: str = "software_fj.log"
) -> logging.Logger:
    # Obtiene o crea la instancia del logger identificada por 'nombre'.
    logger = logging.getLogger(nombre)
    # Establece el nivel minimo de registro en DEBUG para capturar todo el detalle.
    logger.setLevel(logging.DEBUG)

    # Verifica si el logger aun no tiene manejadores para evitar duplicar registros.
    if not logger.handlers:
        # Convierte la ruta del archivo log en un objeto Path.
        ruta_log = Path(archivo_log)
        # Crea las carpetas padre si no existen en la ruta indicada.
        ruta_log.parent.mkdir(parents=True, exist_ok=True)

        # Crea un manejador que escribe en el archivo en modo 'a' (anadir al final).
        file_handler = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        # Define el nivel minimo que aceptara el manejador de archivo.
        file_handler.setLevel(logging.DEBUG)

        # Define el formato de cada linea del log con fecha, nivel, origen y mensaje.
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        # Aplica el formato al manejador de archivo.
        file_handler.setFormatter(formato)
        # Asocia el manejador al logger.
        logger.addHandler(file_handler)

    # Retorna el logger listo para usar.
    return logger
