# 📚 Sistema de Gestión de Librería

## 📋 Descripción
Sistema de gestión de librería desarrollado en Python aplicando programación orientada a objetos, validaciones y arquitectura limpia. Incluye interfaz CLI funcional con persistencia completa en JSON.

## 🛠️ Tecnologías
- Python 3

## 🧠 Conceptos aplicados
- Encapsulamiento con atributos privados
- Properties y setters
- Validaciones con manejo de errores
- Métodos de dominio (`reducir_stock`, `aumentar_stock`, `marcar_como_frecuente`)
- Arquitectura modular (models, services, storage)
- Composición de objetos (Venta y Pedido usan Libro y Cliente)
- Generación automática de IDs
- Registro de fechas con `datetime`
- Separación de capas (models vs services)
- Lógica de negocio en services (cambio de estado, filtros)
- Persistencia completa en JSON (`to_dict`, `from_dict`)
- Reconstrucción de objetos desde almacenamiento
- Interfaz CLI con menú de administrador y usuario

## 📁 Estructura
```
proyecto-libreria/
├── models/
│   ├── libro.py
│   ├── cliente.py
│   ├── venta.py
│   └── pedido.py
├── services/
│   ├── venta_service.py
│   └── pedido_service.py
├── storage/
│   └── json_storage.py
├── data/
│   ├── libros.json
│   ├── clientes.json
│   ├── ventas.json
│   └── pedidos.json
├── main.py
└── README.md
```

## ▶️ Cómo ejecutar
```bash
python main.py
```

## 🖥️ Funcionalidades
**Menú Administrador:**
- Registrar libro
- Registrar venta
- Reporte de stock
- Reporte de clientes frecuentes
- Reporte de ventas
- Reporte de pedidos

**Menú Usuario:**
- Registrar cliente
- Realizar pedido
- Ver stock de libros

## 📈 Estado
✅ Fase 1 completada — Sistema CLI con persistencia en JSON

**Próxima fase:**
🔜 Fase 2 — Migración a PostgreSQL

## 🎯 Objetivo del proyecto
Este proyecto forma parte de mi proceso de aprendizaje para convertirme en desarrollador backend, aplicando buenas prácticas y diseño de software escalable.
```