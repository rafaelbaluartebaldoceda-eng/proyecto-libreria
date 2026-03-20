from database.connection import get_connection
from models.libro import Libro

class LibroRepository:
    """Repositorio que maneja la persistencia de libros en PostgreSQL."""

    def guardar(self, libro):
        """Guarda o actualiza un libro en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
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
        conn.commit()
        cursor.close()
        conn.close()