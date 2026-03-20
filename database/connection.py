import psycopg2

def get_connection():
    """Retorna una conexion activa a la base de datos PostgreSQL."""
    return psycopg2.connect(
        host="localhost",
        database="libreria",
        user="postgres",
        password="holass123"
    )