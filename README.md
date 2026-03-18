# 📚 Sistema de Gestión de Librería

## 📋 Descripción
Sistema de gestión de librería desarrollado en Python aplicando programación orientada a objetos, validaciones y arquitectura limpia.

## 🛠️ Tecnologías
- Python 3

## 🧠 Conceptos aplicados
- Encapsulamiento con atributos privados
- Properties y setters
- Validaciones con manejo de errores
- Métodos de dominio (reducir_stock, aumentar_stock)
- Arquitectura modular (models, services, storage, utils)

## 📁 Estructura
```
proyecto-libreria/
├── models/
│   ├── libro.py
│   ├── cliente.py
│   └── venta.py
├── services/
├── storage/
├── utils/
├── main.py
└── README.md
```

## ▶️ Ejemplo de uso
```python
libro = Libro(1, "1984", "George Orwell", "Distopia", 50, 10)
libro.reducir_stock(2)
print(libro)
```

## 📈 Estado
🚧 En desarrollo — Fase 1: Modelos

## 🎯 Objetivo del proyecto
Este proyecto forma parte de mi proceso de aprendizaje para convertirme en desarrollador backend, aplicando buenas prácticas y diseño de software escalable.
```
