# Módulo main para Gestion de Clientes y Servicios de dominio de Software FJ
# Este módulo contiene la simulación de operaciones completas del sistema Software FJ,
# ejecutando 12 operaciones con manejo de errores y registro en logs.

# Importa Callable para usar funciones como argumentos en la simulación.
from typing import Callable

# Importa la clase Cliente.
from entidades import Cliente

# Importa la excepcion base del sistema.
from excepciones import ErrorGestionClientes

# Importa el gestor principal.
from gestor import GestorSistemaFJ

# Importa las tres subclases de servicios especializados.
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


# Ejecuta una operacion usando try / except / else / finally y registra su resultado.
def ejecutar_operacion(
    numero: int, descripcion: str, gestor: GestorSistemaFJ, accion: Callable[[], str]
) -> None:
    # Imprime el encabezado de la operacion en consola.
    print(f"\n--- Operacion #{numero:02d}: {descripcion} ---")
    # Inicializa el indicador de estado de la operacion.
    estado_op = "COMPLETADA"
    # Inicia bloque try para ejecutar la accion.
    try:
        # Ejecuta la funcion 'accion' y guarda su resultado en texto.
        resultado = accion()
    # Captura errores controlados del dominio Software FJ.
    except ErrorGestionClientes as exc:
        # Actualiza el estado de la operacion.
        estado_op = "RECHAZADA (Error controlado)"
        # Registra el error en el archivo de logs.
        gestor.registrar_error(f"OP-{numero:02d} ({descripcion})", exc)
        # Informa el error controlado por consola.
        print(f"  [ERROR CONTROLADO | {exc.codigo}] {exc.mensaje}")
    # Captura cualquier otra excepcion inesperada para mantener el sistema activo.
    except Exception as exc:
        # Actualiza el estado de la operacion.
        estado_op = "FALLIDA (Error inesperado)"
        # Registra el error inesperado en el archivo de logs.
        gestor.registrar_error(f"OP-{numero:02d} ({descripcion})", exc)
        # Informa el error inesperado por consola.
        print(f"  [ERROR INESPERADO] {exc}")
    # El bloque 'else' se ejecuta solo si 'try' termino sin lanzar excepciones.
    else:
        # Registra el exito de la operacion en el log.
        gestor.logger.info(f"[OP-{numero:02d}] Exito: {resultado}")
        # Muestra el resultado exitoso por consola.
        print(f"  [EXITO] {resultado}")
    # El bloque 'finally' se ejecuta siempre, haya habido error o no.
    finally:
        # Imprime el cierre de la operacion y su estado final.
        print(f"  [FIN OP #{numero:02d}] Estado de ejecucion: {estado_op}")


# Ejecuta la simulacion de 12 operaciones completas en memoria.
def simular_sistema() -> None:
    # Crea el gestor apuntando al archivo 'software_fj.log'.
    gestor = GestorSistemaFJ(archivo_log="software_fj.log")
    # Imprime el titulo general de la simulacion.
    print("=== SISTEMA INTEGRAL SOFTWARE FJ (MODO EN MEMORIA / SIN BD) ===")

    # Operacion 1: Registro valido de un cliente corporativo.
    ejecutar_operacion(
        1,
        "Registro valido de cliente corporativo",
        gestor,
        lambda: gestor.registrar_cliente(
            Cliente(
                "CLI-01",
                "Laura Gomez",
                "laura.gomez@acme.com",
                "+57 310 555 0192",
                "Acme Corp",
            )
        ).resumen(),
    )

    # Operacion 2: Registro invalido de un cliente por correo mal formado.
    ejecutar_operacion(
        2,
        "Registro invalido de cliente por correo electronico incorrecto",
        gestor,
        lambda: gestor.registrar_cliente(
            Cliente(
                "CLI-02",
                "Carlos Ruiz",
                "carlos.ruiz_sin_arroba",
                "3114445566",
                "Soluciones Norte",
            )
        ).resumen(),
    )

    # Operacion 3: Registro valido de un segundo cliente (particular).
    ejecutar_operacion(
        3,
        "Registro valido de cliente particular",
        gestor,
        lambda: gestor.registrar_cliente(
            Cliente("CLI-03", "Sofia Mendoza", "sofia.mendoza@correo.co", "3009876543")
        ).resumen(),
    )

    # Operacion 4: Creacion de tres servicios especializados (Sala, Equipo y Asesoria).
    ejecutar_operacion(
        4,
        "Creacion de servicios especializados (Sala, Equipo, Asesoria)",
        gestor,
        lambda: "\n    * ".join(
            [
                gestor.registrar_servicio(
                    ReservaSala(
                        "SRV-SAL-1",
                        "Sala Ejecutiva Andes",
                        80.0,
                        capacidad_maxima=12,
                        incluye_proyector=True,
                    )
                ).resumen(),
                gestor.registrar_servicio(
                    AlquilerEquipo(
                        "SRV-EQ-1",
                        "Laptop Workstation i7",
                        45.0,
                        stock_disponible=5,
                        deposito_garantia=100.0,
                    )
                ).resumen(),
                gestor.registrar_servicio(
                    AsesoriaEspecializada(
                        "SRV-ASE-1",
                        "Arquitectura Cloud y DevOps",
                        120.0,
                        "Cloud AWS",
                        horas_minimas=2,
                    )
                ).resumen(),
            ]
        ),
    )

    # Operacion 5: Intento invalido de crear un servicio con tarifa base negativa.
    ejecutar_operacion(
        5,
        "Intento de creacion de servicio con tarifa base invalida (-50.0)",
        gestor,
        lambda: gestor.registrar_servicio(
            ReservaSala("SRV-SAL-ERR", "Sala Beta", -50.0, capacidad_maxima=8)
        ).resumen(),
    )

    # Funcion auxiliar para la Operacion 6: crea, confirma y procesa una reserva de sala.
    def op_6() -> str:
        # Crea la reserva de sala por 3 horas para 8 asistentes.
        reserva = gestor.crear_reserva(
            "RES-01",
            "CLI-01",
            "SRV-SAL-1",
            duracion=3.0,
            parametros_servicio={"asistentes": 8},
        )
        # Confirma la reserva.
        gestor.confirmar_reserva("RES-01")
        # Procesa la reserva con 10% de descuento y 19% de impuesto.
        total = gestor.procesar_reserva("RES-01", descuento_pct=10.0, impuesto_pct=19.0)
        # Retorna el resumen y el total final.
        return f"{reserva.resumen()} | Total con desc/imp: ${total:,.2f}"

    # Ejecuta la Operacion 6.
    ejecutar_operacion(
        6,
        "Reserva de sala confirmada y procesada con sobrecarga financiera",
        gestor,
        op_6,
    )

    # Operacion 7: Reserva fallida por exceder la capacidad maxima de la sala.
    ejecutar_operacion(
        7,
        "Intento de reserva de sala superando capacidad maxima (20 > 12)",
        gestor,
        lambda: gestor.crear_reserva(
            "RES-02",
            "CLI-03",
            "SRV-SAL-1",
            duracion=2.0,
            parametros_servicio={"asistentes": 20},
        ).resumen(),
    )

    # Funcion auxiliar para la Operacion 8: reserva equipo, confirma, cancela y verifica devolucion de stock.
    def op_8() -> str:
        # Crea reserva de 2 laptops por 2 dias.
        gestor.crear_reserva(
            "RES-03",
            "CLI-03",
            "SRV-EQ-1",
            duracion=2.0,
            parametros_servicio={"cantidad": 2},
        )
        # Confirma la reserva (descuenta 2 unidades del stock).
        gestor.confirmar_reserva("RES-03")
        # Consulta el stock tras confirmar.
        stock_tras_confirmar = gestor.buscar_servicio("SRV-EQ-1").stock_disponible
        # Cancela la reserva (devuelve las 2 unidades al stock).
        gestor.cancelar_reserva("RES-03", motivo="Cambio de cronograma del cliente")
        # Consulta el stock tras cancelar.
        stock_tras_cancelar = gestor.buscar_servicio("SRV-EQ-1").stock_disponible
        # Retorna ambos valores para verificar.
        return (
            f"Stock tras confirmar: {stock_tras_confirmar} | "
            f"Stock tras cancelar: {stock_tras_cancelar}"
        )

    # Ejecuta la Operacion 8.
    ejecutar_operacion(
        8,
        "Reserva de equipo confirmada y luego cancelada con liberacion de stock",
        gestor,
        op_8,
    )

    # Operacion 9: Reserva fallida por solicitar menos horas que el minimo de la asesoria.
    ejecutar_operacion(
        9,
        "Intento de reserva de asesoria por debajo de horas minimas",
        gestor,
        lambda: gestor.crear_reserva(
            "RES-04", "CLI-01", "SRV-ASE-1", duracion=1.0
        ).resumen(),
    )

    # Funcion auxiliar para la Operacion 10: reserva asesoria, confirma y procesa.
    def op_10() -> str:
        # Crea reserva de asesoria por 4 horas.
        gestor.crear_reserva("RES-05", "CLI-01", "SRV-ASE-1", duracion=4.0)
        # Confirma la reserva.
        gestor.confirmar_reserva("RES-05")
        # Procesa con 5% de descuento y 0% de impuesto.
        monto = gestor.procesar_reserva("RES-05", descuento_pct=5.0, impuesto_pct=0.0)
        # Retorna el monto procesado.
        return f"Asesoria procesada por ${monto:,.2f}"

    # Ejecuta la Operacion 10.
    ejecutar_operacion(
        10, "Reserva de asesoria especializada confirmada y procesada", gestor, op_10
    )

    # Operacion 11: Operacion invalida al intentar confirmar una reserva ya PROCESADA.
    ejecutar_operacion(
        11,
        "Intento de confirmar una reserva ya PROCESADA (RES-05)",
        gestor,
        lambda: gestor.confirmar_reserva("RES-05").resumen(),
    )

    # Operacion 12: Calculo financiero invalido con porcentaje de descuento fuera de rango (150%).
    ejecutar_operacion(
        12,
        "Calculo sobrecargado invalido con descuento del 150%",
        gestor,
        lambda: str(
            gestor.calcular_costo_sobrecargado(
                gestor.buscar_servicio("SRV-ASE-1"),
                duracion=2.0,
                descuento_pct=150.0,
            )
        ),
    )

    # Imprime el resumen final de las listas almacenadas en memoria.
    print("\n=== ESTADO FINAL EN MEMORIA ===")
    # Muestra total de clientes y cada uno.
    print(f"Clientes registrados: {len(gestor.clientes)}")
    # Recorre clientes registrados.
    for c in gestor.clientes:
        # Imprime resumen del cliente.
        print("  -", c.resumen())

    # Muestra total de servicios y cada uno.
    print(f"Servicios registrados: {len(gestor.servicios)}")
    # Recorre servicios registrados.
    for s in gestor.servicios:
        # Imprime resumen del servicio.
        print("  -", s.resumen())

    # Muestra total de reservas y cada una.
    print(f"Reservas registradas: {len(gestor.reservas)}")
    # Recorre reservas registradas.
    for r in gestor.reservas:
        # Imprime resumen de la reserva.
        print("  -", r.resumen())

    # Indica donde consultar el archivo de logs.
    print(
        "\nRevisa el archivo 'software_fj.log' para consultar el historial completo de eventos y errores."
    )


# Punto de entrada del programa cuando se ejecuta main.py directamente.
if __name__ == "__main__":
    # Llama a la funcion principal de simulacion.
    simular_sistema()
