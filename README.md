# 📚 Sistema de Gestión de Librería

## 📋 Descripción
Sistema de gestión de librería desarrollado en Python aplicando programación orientada a objetos, validaciones y arquitectura limpia. Incluye interfaz CLI funcional con persistencia completa en PostgreSQL y arquitectura por capas profesional.

## 🛠️ Tecnologías
- Python 3
- PostgreSQL 17+
- psycopg2-binary

## 🧠 Conceptos aplicados
- Encapsulamiento con atributos privados
- Properties y setters
- Validaciones con manejo de errores
- Métodos de dominio (`reducir_stock`, `aumentar_stock`, `marcar_como_frecuente`)
- Arquitectura modular (models / services / repositories / database)
- Composición de objetos (Venta y Pedido usan Libro y Cliente)
- Generación automática de IDs con SERIAL en PostgreSQL
- Registro de fechas con `datetime`
- Separación de capas profesional
- Lógica de negocio en services
- Persistencia en PostgreSQL con `psycopg2`
- Context managers para manejo seguro de conexiones
- Patrón Repository para acceso a datos
- Queries SQL con JOIN, ON CONFLICT, RETURNING
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
├── repositories/
│   ├── libro_repository.py
│   ├── cliente_repository.py
│   ├── venta_repository.py
│   └── pedido_repository.py
├── database/
│   └── connection.py
├── main.py
└── README.md
```

## ⚙️ Requisitos
- Python 3.x
- PostgreSQL 17+
- psycopg2-binary

## 🗄️ Configuración de base de datos
```sql
CREATE DATABASE libreria;

CREATE TABLE libros (
    id INTEGER PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio INTEGER NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE clientes (
    dni CHAR(8) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    frecuente BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    libro_id INTEGER NOT NULL REFERENCES libros(id),
    cliente_dni CHAR(8) NOT NULL REFERENCES clientes(dni),
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    libro_id INTEGER NOT NULL REFERENCES libros(id),
    cliente_dni CHAR(8) NOT NULL REFERENCES clientes(dni),
    cantidad INTEGER NOT NULL,
    metodo_entrega VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## ▶️ Cómo ejecutar
```bash
pip install psycopg2-binary
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
✅ Fase 1 — Sistema CLI con persistencia en JSON
✅ Fase 2 — Migración a PostgreSQL completada

**Próxima fase:**
🔜 Fase 3 — API REST con FastAPI

## 🎯 Objetivo del proyecto
Este proyecto forma parte de mi proceso de aprendizaje para convertirme en desarrollador backend, aplicando buenas prácticas y diseño de software escalable.
```