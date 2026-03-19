# 📚 Sistema de Gestión de Librería

## 📋 Descripción
Sistema de gestión de librería desarrollado en Python aplicando programación orientada a objetos, validaciones y arquitectura limpia.

## 🛠️ Tecnologías
- Python 3

## 🧠 Conceptos aplicados
- Encapsulamiento con atributos privados
- Properties y setters
- Validaciones con manejo de errores
- Métodos de dominio (`reducir_stock`, `aumentar_stock`, `marcar_como_frecuente`)
- Arquitectura modular (models, services, storage, utils)
- Composición de objetos (Venta y Pedido usan Libro y Cliente)
- Generación automática de IDs
- Registro de fechas con `datetime`
- Separación de capas (models vs services)

## 📁 Estructura
```
proyecto-libreria/
├── models/
│   ├── libro.py
│   ├── cliente.py
│   ├── venta.py
│   └── pedido.py
├── services/
│   └── venta_service.py
├── storage/
├── utils/
├── main.py
└── README.md
```

## ▶️ Ejemplo de uso
```python
libro = Libro(1, "1984", "George Orwell", "Distopia", 50, 10)
cliente = Cliente("12345678", "Ana Torres", "ana@gmail.com", "Lima")

# Registrar una venta
service = VentaService()
venta = service.registrar_venta(libro, cliente, 2)
print(venta)

# Registrar un pedido
pedido = Pedido(libro, cliente, 1, "domicilio")
print(pedido)
```

## 📈 Estado
🚧 En desarrollo — Fase 2: Services

## 🎯 Objetivo del proyecto
Este proyecto forma parte de mi proceso de aprendizaje para convertirme en desarrollador backend, aplicando buenas prácticas y diseño de software escalable.