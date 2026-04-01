# Sistema de Gestion de Libreria

## Descripcion
Proyecto backend desarrollado en Python para gestionar libros, clientes, ventas y pedidos en una libreria. Esta fase mantiene una interfaz CLI, pero ya trabaja con persistencia completa en PostgreSQL, validaciones de dominio y separacion por capas para preparar la siguiente etapa con FastAPI.

## Tecnologias
- Python 3
- PostgreSQL 17+
- FastAPI
- Uvicorn
- psycopg2-binary

## Arquitectura actual
- `models/`: entidades del dominio y validaciones
- `services/`: logica de negocio reutilizable
- `repositories/`: acceso a datos con SQL
- `database/`: configuracion y manejo de conexiones/transacciones
- `main.py`: interfaz CLI y flujo de consola
- `app/`: capa HTTP de FastAPI con routers, schemas y dependencias
- `tests/`: pruebas automaticas base

## Estado del proyecto
- Fase 1 completada: CLI con persistencia en JSON
- Fase 2 completada: migracion a PostgreSQL y cierre tecnico del backend base
- Fase 3 completada: integracion base de FastAPI reutilizando la capa de servicios

La persistencia JSON de la Fase 1 ya no forma parte del flujo principal y se conserva solo como parte del historial del proyecto.

## Configuracion
1. Crear un entorno virtual opcional.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` tomando como referencia `.env.example`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=libreria
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
```

## Esquema de base de datos
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

## Como ejecutar
```bash
python main.py
```

Al iniciar, el sistema precarga libros y clientes si la base de datos aun esta vacia.
En Windows, si `python` no esta disponible en PATH, puedes usar `py -3 main.py`.

## Como ejecutar la API
```bash
python -m uvicorn app.main:app --reload
```

En Windows, si `python` no esta disponible en PATH, puedes usar:

```bash
py -3 -m uvicorn app.main:app --reload
```

Una vez levantada la API, la documentacion interactiva estara disponible en:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Funcionalidades CLI
### Menu Administrador
- Registrar libro
- Registrar venta
- Ver reporte de stock
- Ver clientes frecuentes
- Ver reporte de ventas
- Ver reporte de pedidos

### Menu Usuario
- Registrar cliente
- Realizar pedido
- Ver stock de libros

## Mejoras cerradas en esta fase
- Configuracion de base de datos por variables de entorno
- Manejo de transacciones para ventas y entrega de pedidos
- Eliminacion de dependencias activas de la fase JSON
- Separacion mas clara entre CLI y logica reutilizable
- Pruebas automaticas minimas para dominio, servicios y conexion

## Avance actual de la Fase 3
- Integracion de FastAPI sin reemplazar la CLI existente
- Creacion de la capa `app/` con `main.py`, `dependencies.py`, `routers/` y `schemas/`
- Routers funcionales para `libros`, `clientes`, `ventas` y `pedidos`
- Schemas Pydantic de entrada y salida para libros, clientes, ventas y pedidos
- Manejo de respuestas HTTP con `response_model`, `status_code` y `HTTPException`
- Pruebas automaticas para endpoints de libros, clientes, ventas y pedidos
- Documentacion interactiva activa en `/docs` para validar endpoints durante el desarrollo

## Recursos API disponibles
- `GET /`
- `GET /libros/`
- `GET /libros/{id}`
- `POST /libros/`
- `GET /clientes/frecuentes`
- `POST /clientes/`
- `GET /ventas/`
- `GET /ventas/{id}`
- `POST /ventas/`
- `GET /pedidos/`
- `GET /pedidos/{id}`
- `POST /pedidos/`
- `PATCH /pedidos/{id}/estado`

## Validacion final de la Fase 2
Antes de dar por cerrada esta fase, el proyecto paso por una etapa final de revision tecnica y fortalecimiento del codigo. Esta validacion incluyo pruebas manuales de funcionamiento del sistema y una revision asistida por herramientas de IA enfocada en detectar puntos debiles de la implementacion.

La asistencia de IA se utilizo como herramienta de apoyo para auditoria y mejora tecnica, no como sustituto del desarrollo del proyecto. Su uso estuvo orientado a:
- revisar validaciones y restricciones del dominio
- identificar riesgos de consistencia en operaciones con PostgreSQL
- detectar posibles errores de configuracion y conexion con la base de datos
- revisar compatibilidad de ejecucion en entornos virtuales y escenarios distintos al entorno local original
- limpiar artefactos, carpetas y archivos residuales dentro de la arquitectura del proyecto
- mejorar la separacion entre la capa CLI, la logica de negocio y la persistencia
- reforzar la documentacion final y dejar una base mas preparada para la siguiente fase con FastAPI

Como resultado, la Fase 2 queda cerrada con una base mas consistente, portable y mantenible, manteniendo el proyecto como un trabajo de aprendizaje progresivo construido por etapas.

## Ejecutar pruebas
```bash
python -m unittest discover -s tests -v
```

En Windows, si `python` no esta disponible en PATH, puedes usar `py -3 -m unittest discover -s tests -v`.

## Objetivo de aprendizaje
Este proyecto forma parte de mi proceso de crecimiento como desarrollador backend. La meta de esta fase es cerrar una base funcional y consistente antes de evolucionar el sistema a una API REST con FastAPI.
