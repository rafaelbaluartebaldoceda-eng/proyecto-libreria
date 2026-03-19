from models.libro import Libro
from models.cliente import Cliente
from services.venta_service import VentaService
from services.pedido_service import PedidoService
from storage.json_storage import JsonStorage


def inicializar_datos(storage_libros, storage_clientes):
    """Inicializa los datos del sistema."""
    libros_precargados = [
        Libro(101, "El Principito", "Antoine de Saint-Exupery", "Ficcion", 35, 10),
        Libro(102, "Cien Anios de Soledad", "Gabriel Garcia Marquez", "Realismo Magico", 45, 8),
        Libro(103, "1984", "George Orwell", "Distopia", 50, 6),
    ]
    clientes_precargados = [
        Cliente("12345678", "Ana Torres", "ana@gmail.com", "Lima"),
        Cliente("23456789", "Carlos Ruiz", "carlos@gmail.com", "Cusco"),
        Cliente("34567890", "Lucia Vega", "lucia@gmail.com", "Arequipa"),
        Cliente("45678901", "Marco Rios", "marco@gmail.com", "Piura"),
    ]
    datos_libros = storage_libros.cargar()
    if datos_libros:
        libros = [Libro.from_dict(l) for l in datos_libros]
    else:
        libros = libros_precargados
        storage_libros.guardar([l.to_dict() for l in libros])

    datos_clientes = storage_clientes.cargar()
    if datos_clientes:
        clientes = [Cliente.from_dict(c) for c in datos_clientes]
    else:
        clientes = clientes_precargados
        storage_clientes.guardar([c.to_dict() for c in clientes])

    return libros, clientes


def inicializar_services(libros, clientes):
    """Inicializa los services con su storage correspondiente."""
    storage_ventas = JsonStorage("data/ventas.json")
    storage_pedidos = JsonStorage("data/pedidos.json")
    venta_service = VentaService(storage_ventas, libros, clientes)
    pedido_service = PedidoService(storage_pedidos, libros, clientes)
    return venta_service, pedido_service


def registrar_libro(libros, storage_libros):
    """Registra un nuevo libro en el sistema."""
    print("\n--- REGISTRAR LIBRO ---")
    try:
        id = int(input("ID: "))
        if any(l.id == id for l in libros):
            print("Ya existe un libro con ese ID.")
            return
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        categoria = input("Categoria: ")
        precio = int(input("Precio (S/.): "))
        stock = int(input("Stock: "))
        libro = Libro(id, titulo, autor, categoria, precio, stock)
        libros.append(libro)
        storage_libros.guardar([l.to_dict() for l in libros])
        print("Libro registrado correctamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_cliente(clientes, storage_clientes):
    """Registra un nuevo cliente en el sistema."""
    print("\n--- REGISTRAR CLIENTE ---")
    try:
        dni = input("DNI (8 digitos): ")
        if any(c.dni == dni for c in clientes):
            print("Ya existe un cliente con ese DNI.")
            return
        nombre = input("Nombre completo: ")
        correo = input("Correo: ")
        direccion = input("Direccion: ")
        frecuente = input("Cliente frecuente? (s/n): ").lower() == "s"
        cliente = Cliente(dni, nombre, correo, direccion, frecuente)
        clientes.append(cliente)
        storage_clientes.guardar([c.to_dict() for c in clientes])
        print("Cliente registrado correctamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_venta(libros, clientes, venta_service, storage_libros):
    """Registra una nueva venta en el sistema."""
    print("\n--- REGISTRAR VENTA ---")
    try:
        reporte_stock(libros)
        id_libro = int(input("ID del libro: "))
        libro = next((l for l in libros if l.id == id_libro), None)
        if not libro:
            print("Libro no encontrado.")
            return
        if not libro.disponible:
            print("El libro no esta disponible.")
            return
        dni_cliente = input("DNI del cliente: ")
        cliente = next((c for c in clientes if c.dni == dni_cliente), None)
        if not cliente:
            print("Cliente no encontrado.")
            return
        cantidad = int(input("Cantidad: "))
        venta = venta_service.registrar_venta(libro, cliente, cantidad)
        storage_libros.guardar([l.to_dict() for l in libros])
        print("Venta registrada correctamente.")
        print(venta)
    except ValueError as e:
        print(f"Error: {e}")


def realizar_pedido(libros, clientes, pedido_service):
    """Realiza un pedido para un cliente."""
    print("\n--- REALIZAR PEDIDO ---")
    try:
        reporte_stock(libros)
        id_libro = int(input("ID del libro: "))
        libro = next((l for l in libros if l.id == id_libro), None)
        if not libro:
            print("Libro no encontrado.")
            return
        if not libro.disponible:
            print("El libro no esta disponible.")
            return
        dni_cliente = input("DNI del cliente: ")
        cliente = next((c for c in clientes if c.dni == dni_cliente), None)
        if not cliente:
            print("Cliente no encontrado.")
            return
        cantidad = int(input("Cantidad: "))
        metodo = input("Metodo de entrega (tienda/domicilio): ").lower()
        pedido = pedido_service.registrar_pedido(libro, cliente, cantidad, metodo)
        print("Pedido registrado correctamente.")
        print(pedido)
    except ValueError as e:
        print(f"Error: {e}")


def reporte_stock(libros):
    """Muestra el reporte de stock de todos los libros."""
    print("\n--- REPORTE DE STOCK ---")
    if not libros:
        print("No hay libros registrados.")
        return
    for libro in libros:
        print(f"[{libro.id}] {libro}")


def reporte_clientes_frecuentes(clientes):
    """Muestra el reporte de clientes frecuentes."""
    print("\n--- CLIENTES FRECUENTES ---")
    frecuentes = [c for c in clientes if c.frecuente]
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


def menu_administrador(libros, clientes, venta_service, pedido_service, storage_libros):
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
            registrar_libro(libros, storage_libros)
        elif opcion == "2":
            registrar_venta(libros, clientes, venta_service, storage_libros)
        elif opcion == "3":
            reporte_stock(libros)
        elif opcion == "4":
            reporte_clientes_frecuentes(clientes)
        elif opcion == "5":
            reporte_ventas(venta_service)
        elif opcion == "6":
            reporte_pedidos(pedido_service)
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def menu_usuario(libros, clientes, pedido_service, storage_clientes):
    """Muestra el menu del usuario y gestiona sus opciones."""
    while True:
        print("\n--- MENU USUARIO ---")
        print("1. Registrar cliente")
        print("2. Realizar pedido")
        print("3. Ver stock de libros")
        print("0. Volver")
        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_cliente(clientes, storage_clientes)
        elif opcion == "2":
            realizar_pedido(libros, clientes, pedido_service)
        elif opcion == "3":
            reporte_stock(libros)
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

    storage_libros = JsonStorage("data/libros.json")
    storage_clientes = JsonStorage("data/clientes.json")
    libros, clientes = inicializar_datos(storage_libros, storage_clientes)
    venta_service, pedido_service = inicializar_services(libros, clientes)

    while True:
        print("\n        M E N U        ")
        print("  SISTEMA DE LIBRERIA  ")
        print("1. Administrador")
        print("2. Usuario")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_administrador(libros, clientes, venta_service, pedido_service, storage_libros)
        elif opcion == "2":
            menu_usuario(libros, clientes, pedido_service, storage_clientes)
        elif opcion == "0":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()