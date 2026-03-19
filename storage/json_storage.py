import json
import os

class JsonStorage:
    """Maneja la persistencia de datos en archivos JSON."""
    def __init__(self, filepath):
        """Inicializa el storage con la ruta del archivo JSON."""
        self._filepath = filepath
    def guardar(self, datos):
        """Guarda una lista de diccionarios en el archivo JSON."""
        if not isinstance(datos, list):
            raise ValueError("Los datos deben ser una lista")
        dirpath = os.path.dirname(self._filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    def cargar(self):
        """Carga y retorna los datos del archivo JSON."""
        if not os.path.exists(self._filepath):
            return []
        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    def existe(self):
        """Retorna True si el archivo de almacenamiento existe."""
        return os.path.exists(self._filepath)