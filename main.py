from models.libro import Libro
from models.cliente import Cliente
from services.venta_service import VentaService
from services.pedido_service import PedidoService
from repositories.libro_repository import LibroRepository
from repositories.cliente_repository import ClienteRepository
from repositories.venta_repository import VentaRepository
from repositories.pedido_repository import PedidoRepository


def inicializar_datos(libro_repo, cliente_repo):
    """Carga o inicializa los datos del sistema desde PostgreSQL."""
    libros = libro_repo.obtener_todos()
    if not libros:
        libros_precargados = [
            Libro(101, "El Principito", "Antoine de Saint-Exupery", "Ficcion", 35, 10),
            Libro(102, "Cien Anios de Soledad", "Gabriel Garcia Marquez", "Realismo Magico", 45, 8),
            Libro(103, "1984", "George Orwell", "Distopia", 50, 6),
        ]
        for libro in libros_precargados:
            libro_repo.guardar(libro)
        libros = libros_precargados

    clientes = cliente_repo.obtener_todos()
    if not clientes:
        clientes_precargados = [
            Cliente("12345678", "Ana Torres", "ana@gmail.com", "Lima"),
            Cliente("23456789", "Carlos Ruiz", "carlos@gmail.com", "Cusco"),
            Cliente("34567890", "Lucia Vega", "lucia@gmail.com", "Arequipa"),
            Cliente("45678901", "Marco Rios", "marco@gmail.com", "Piura"),
        ]
        for cliente in clientes_precargados:
            cliente_repo.guardar(cliente)
        clientes = clientes_precargados

    return libros, clientes


def inicializar_services(libro_repo, cliente_repo):
    """Inicializa los services con sus repositories."""
    venta_service = VentaService(VentaRepository(), libro_repo, cliente_repo)
    pedido_service = PedidoService(PedidoRepository(), libro_repo, cliente_repo)
    return venta_service, pedido_service


def registrar_libro(libro_repo):
    """Registra un nuevo libro en el sistema."""
    print("\n--- REGISTRAR LIBRO ---")
    try:
        id = int(input("ID: "))
        if libro_repo.buscar_por_id(id):
            print("Ya existe un libro con ese ID.")
            return
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        categoria = input("Categoria: ")
        precio = int(input("Precio (S/.): "))
        stock = int(input("Stock: "))
        libro = Libro(id, titulo, autor, categoria, precio, stock)
        libro_repo.guardar(libro)
        print("Libro registrado correctamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_cliente(cliente_repo):
    """Registra un nuevo cliente en el sistema."""
    print("\n--- REGISTRAR CLIENTE ---")
    try:
        dni = input("DNI (8 digitos): ")
        if cliente_repo.buscar_por_dni(dni):
            print("Ya existe un cliente con ese DNI.")
            return
        nombre = input("Nombre completo: ")
        correo = input("Correo: ")
        direccion = input("Direccion: ")
        frecuente = input("Cliente frecuente? (s/n): ").lower() == "s"
        cliente = Cliente(dni, nombre, correo, direccion, frecuente)
        cliente_repo.guardar(cliente)
        print("Cliente registrado correctamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_venta(libro_repo, venta_service):
    """Registra una nueva venta en el sistema."""
    print("\n--- REGISTRAR VENTA ---")
    try:
        reporte_stock(libro_repo)
        id_libro = int(input("ID del libro: "))
        libro = libro_repo.buscar_por_id(id_libro)
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
    except ValueError as e:
        print(f"Error: {e}")


def realizar_pedido(libro_repo, pedido_service):
    """Realiza un pedido para un cliente."""
    print("\n--- REALIZAR PEDIDO ---")
    try:
        reporte_stock(libro_repo)
        id_libro = int(input("ID del libro: "))
        libro = libro_repo.buscar_por_id(id_libro)
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
    except ValueError as e:
        print(f"Error: {e}")


def reporte_stock(libro_repo):
    """Muestra el reporte de stock de todos los libros."""
    print("\n--- REPORTE DE STOCK ---")
    libros = libro_repo.obtener_todos()
    if not libros:
        print("No hay libros registrados.")
        return
    for libro in libros:
        print(f"[{libro.id}] {libro}")


def reporte_clientes_frecuentes(cliente_repo):
    """Muestra el reporte de clientes frecuentes."""
    print("\n--- CLIENTES FRECUENTES ---")
    frecuentes = [c for c in cliente_repo.obtener_todos() if c.frecuente]
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


def menu_administrador(libro_repo, cliente_repo, venta_service, pedido_service):
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
            registrar_libro(libro_repo)
        elif opcion == "2":
            registrar_venta(libro_repo, venta_service)
        elif opcion == "3":
            reporte_stock(libro_repo)
        elif opcion == "4":
            reporte_clientes_frecuentes(cliente_repo)
        elif opcion == "5":
            reporte_ventas(venta_service)
        elif opcion == "6":
            reporte_pedidos(pedido_service)
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def menu_usuario(libro_repo, cliente_repo, pedido_service):
    """Muestra el menu del usuario y gestiona sus opciones."""
    while True:
        print("\n--- MENU USUARIO ---")
        print("1. Registrar cliente")
        print("2. Realizar pedido")
        print("3. Ver stock de libros")
        print("0. Volver")
        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_cliente(cliente_repo)
        elif opcion == "2":
            realizar_pedido(libro_repo, pedido_service)
        elif opcion == "3":
            reporte_stock(libro_repo)
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

    libro_repo = LibroRepository()
    cliente_repo = ClienteRepository()
    inicializar_datos(libro_repo, cliente_repo)
    venta_service, pedido_service = inicializar_services(libro_repo, cliente_repo)

    while True:
        print("\n        M E N U        ")
        print("  SISTEMA DE LIBRERIA  ")
        print("1. Administrador")
        print("2. Usuario")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_administrador(libro_repo, cliente_repo, venta_service, pedido_service)
        elif opcion == "2":
            menu_usuario(libro_repo, cliente_repo, pedido_service)
        elif opcion == "0":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()