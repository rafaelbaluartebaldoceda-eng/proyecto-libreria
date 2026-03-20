from database.connection import get_connection
from models.libro import Libro

class LibroRepository:
    """Repositorio que maneja la persistencia de libros en PostgreSQL."""

    def guardar(self, libro):
        """Guarda o actualiza un libro en la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO libros (id, titulo, autor, categoria, precio, stock)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        titulo = EXCLUDED.titulo,
                        autor = EXCLUDED.autor,
                        categoria = EXCLUDED.categoria,
                        precio = EXCLUDED.precio,
                        stock = EXCLUDED.stock
                """, (libro.id, libro.titulo, libro.autor, libro.categoria, libro.precio, libro.stock))

    def obtener_todos(self):
        """Retorna una lista de todos los libros de la base de datos."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, titulo, autor, categoria, precio, stock FROM libros")
                filas = cursor.fetchall()
        return [Libro(f[0], f[1], f[2], f[3], f[4], f[5]) for f in filas]

    def buscar_por_id(self, id):
        """Busca y retorna un libro por su id, o None si no existe."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, titulo, autor, categoria, precio, stock FROM libros WHERE id = %s", (id,))
                fila = cursor.fetchone()
        if fila:
            return Libro(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
        return None