from sqlalchemy.exc import SQLAlchemyError

from repositories.cliente_repository import ClienteRepository
from repositories.libro_repository import LibroRepository
from repositories.pedido_repository import PedidoRepository
from repositories.venta_repository import VentaRepository
from services.libreria_service import LibreriaService
from services.pedido_service import PedidoService
from services.venta_service import VentaService


def crear_aplicacion():
    """Construye los services principales de la aplicacion."""
    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    libreria_service = LibreriaService(libro_repo, cliente_repo)
    libreria_service.inicializar_datos_base()
    venta_service = VentaService(VentaRepository(), libro_repo, cliente_repo)
    pedido_service = PedidoService(PedidoRepository(), libro_repo, cliente_repo)
    return libreria_service, venta_service, pedido_service


def registrar_libro(libreria_service):
    """Lee datos del usuario y registra un nuevo libro."""
    print("\n--- REGISTRAR LIBRO ---")
    try:
        libro_id = int(input("ID: "))
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        categoria = input("Categoria: ")
        precio = int(input("Precio (S/.): "))
        stock = int(input("Stock: "))
        libreria_service.registrar_libro(libro_id, titulo, autor, categoria, precio, stock)
        print("Libro registrado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")


def registrar_cliente(libreria_service):
    """Lee datos del usuario y registra un nuevo cliente."""
    print("\n--- REGISTRAR CLIENTE ---")
    try:
        dni = input("DNI (8 digitos): ")
        nombre = input("Nombre completo: ")
        correo = input("Correo: ")
        direccion = input("Direccion: ")
        frecuente = input("Cliente frecuente? (s/n): ").lower() == "s"
        libreria_service.registrar_cliente(dni, nombre, correo, direccion, frecuente)
        print("Cliente registrado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")


def registrar_venta(libreria_service, venta_service):
    """Registra una nueva venta en el sistema."""
    print("\n--- REGISTRAR VENTA ---")
    try:
        reporte_stock(libreria_service)
        id_libro = int(input("ID del libro: "))
        libro = libreria_service.buscar_libro(id_libro)
        if not libro:
            print("Libro no encontrado.")
            return
        if not libro.disponible:
            print("El libro no esta disponible.")
            return
        dni_cliente = input("DNI del cliente: ")
        cantidad = int(input("Cantidad: "))
        venta = venta_service.registrar_venta(id_libro, dni_cliente, cantidad)
        print("Venta registrada correctamente.")
        print(venta)
    except ValueError as error:
        print(f"Error: {error}")


def realizar_pedido(libreria_service, pedido_service):
    """Realiza un pedido para un cliente."""
    print("\n--- REALIZAR PEDIDO ---")
    try:
        reporte_stock(libreria_service)
        id_libro = int(input("ID del libro: "))
        libro = libreria_service.buscar_libro(id_libro)
        if not libro:
            print("Libro no encontrado.")
            return
        if not libro.disponible:
            print("El libro no esta disponible.")
            return
        dni_cliente = input("DNI del cliente: ")
        cantidad = int(input("Cantidad: "))
        metodo = input("Metodo de entrega (tienda/domicilio): ").lower()
        pedido = pedido_service.registrar_pedido(id_libro, dni_cliente, cantidad, metodo)
        print("Pedido registrado correctamente.")
        print(pedido)
    except ValueError as error:
        print(f"Error: {error}")


def reporte_stock(libreria_service):
    """Muestra el reporte de stock de todos los libros."""
    print("\n--- REPORTE DE STOCK ---")
    libros = libreria_service.listar_libros()
    if not libros:
        print("No hay libros registrados.")
        return
    for libro in libros:
        print(f"[{libro.id}] {libro}")


def reporte_clientes_frecuentes(libreria_service):
    """Muestra el reporte de clientes frecuentes."""
    print("\n--- CLIENTES FRECUENTES ---")
    frecuentes = libreria_service.listar_clientes_frecuentes()
    if not frecuentes:
        print("No hay clientes frecuentes registrados.")
        return
    for cliente in frecuentes:
        print(cliente)


def reporte_ventas(venta_service):
    """Muestra el reporte de todas las ventas."""
    print("\n--- REPORTE DE VENTAS ---")
    ventas = venta_service.listar_ventas()
    if not ventas:
        print("No hay ventas registradas.")
        return
    for venta in ventas:
        print(venta)


def reporte_pedidos(pedido_service):
    """Muestra el reporte de todos los pedidos."""
    print("\n--- REPORTE DE PEDIDOS ---")
    pedidos = pedido_service.listar_pedidos()
    if not pedidos:
        print("No hay pedidos registrados.")
        return
    for pedido in pedidos:
        print(pedido)


def menu_administrador(libreria_service, venta_service, pedido_service):
    """Muestra el menu del administrador y gestiona sus opciones."""
    while True:
        print("\n--- MENU ADMINISTRADOR ---")
        print("1. Registrar libro")
        print("2. Registrar venta")
        print("3. Reporte de stock")
        print("4. Reporte de clientes frecuentes")
        print("5. Reporte de ventas")
        print("6. Reporte de pedidos")
        print("0. Volver")
        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_libro(libreria_service)
        elif opcion == "2":
            registrar_venta(libreria_service, venta_service)
        elif opcion == "3":
            reporte_stock(libreria_service)
        elif opcion == "4":
            reporte_clientes_frecuentes(libreria_service)
        elif opcion == "5":
            reporte_ventas(venta_service)
        elif opcion == "6":
            reporte_pedidos(pedido_service)
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def menu_usuario(libreria_service, pedido_service):
    """Muestra el menu del usuario y gestiona sus opciones."""
    while True:
        print("\n--- MENU USUARIO ---")
        print("1. Registrar cliente")
        print("2. Realizar pedido")
        print("3. Ver stock de libros")
        print("0. Volver")
        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_cliente(libreria_service)
        elif opcion == "2":
            realizar_pedido(libreria_service, pedido_service)
        elif opcion == "3":
            reporte_stock(libreria_service)
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def main():
    """Funcion principal del sistema."""
    print("""
 L       III  M   M   AAAAA    BBBBB   OOO   OOO     K   K
 L        I   MM MM  A     A   B    B  O   O  O   O  K  K
 L        I   M M M  AAAAAAA   BBBBB   O   O  O   O  KKK
 L        I   M   M  A     A   B    B  O   O  O   O  K  K
 LLLLL   III  M   M  A     A   BBBBB   OOO   OOO     K   K
    """)

    try:
        libreria_service, venta_service, pedido_service = crear_aplicacion()
    except ValueError as error:
        print(f"Error de configuracion: {error}")
        return
    except SQLAlchemyError as error:
        print(f"Error de base de datos: {error}")
        return

    while True:
        print("\n        M E N U        ")
        print("  SISTEMA DE LIBRERIA  ")
        print("1. Administrador")
        print("2. Usuario")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_administrador(libreria_service, venta_service, pedido_service)
        elif opcion == "2":
            menu_usuario(libreria_service, pedido_service)
        elif opcion == "0":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
