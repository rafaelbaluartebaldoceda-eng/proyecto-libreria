# Sistema de Gestion de Libreria

## Descripcion
Proyecto backend desarrollado en Python para gestionar libros, clientes, ventas, pedidos y usuarios autenticables en una libreria. El sistema mantiene una interfaz CLI y una API REST construida con FastAPI, trabajando sobre PostgreSQL, validaciones de dominio, autenticacion con JWT y separacion por capas.

## Tecnologias
- Python 3
- PostgreSQL 17+
- FastAPI
- Uvicorn
- psycopg2-binary
- python-jose
- pwdlib + argon2-cffi
- Pydantic

## Arquitectura actual
- `models/`: entidades del dominio y validaciones
- `services/`: logica de negocio reutilizable
- `repositories/`: acceso a datos con SQL
- `database/`: manejo de conexiones y transacciones
- `main.py`: interfaz CLI y flujo de consola
- `app/`: capa HTTP con FastAPI, routers, schemas, dependencias y seguridad
- `tests/`: pruebas automaticas de dominio, servicios y API

## Estado del proyecto
- Fase 1 completada: CLI con persistencia inicial
- Fase 2 completada: migracion a PostgreSQL y cierre tecnico del backend base
- Fase 3 completada: integracion base de FastAPI reutilizando la capa de servicios
- Fase 4A completada: autenticacion, autorizacion por rol y proteccion de rutas con JWT

La version actual fue validada localmente con **49 pruebas automaticas en estado OK**.

## Configuracion
1. Crear y activar un entorno virtual.
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
SECRET_KEY=tu_clave_super_secreta_y_larga_de_al_menos_32_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_BOOTSTRAP_TOKEN=crea_un_token_unico_y_largo_para_el_primer_admin
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

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
```

## Como ejecutar la CLI
```bash
python main.py
```

## Como ejecutar la API
```bash
python -m uvicorn app.main:app --reload
```

Una vez levantada la API, la documentacion interactiva estara disponible en:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Flujo de seguridad
- `POST /auth/bootstrap-admin`: crea el primer administrador usando `ADMIN_BOOTSTRAP_TOKEN`. Solo funciona si aun no existe un admin activo.
- `POST /auth/register`: registra un usuario comun con rol `user`.
- `POST /auth/users`: permite a un admin crear usuarios con rol explicito.
- `POST /token`: autentica un usuario y retorna un JWT Bearer.
- `GET /users/me`: devuelve el perfil del usuario autenticado.

### Consideraciones de seguridad
- Las contrasenas se almacenan hasheadas, nunca en texto plano.
- El JWT usa `sub` como identificador principal y `role` para autorizacion por rol.
- Las rutas protegidas devuelven `401` si el token falta o es invalido.
- Las rutas administrativas devuelven `403` si el usuario autenticado no es admin.
- El bootstrap del primer admin se bloquea automaticamente cuando ya existe un administrador activo.

## Recursos API disponibles

### Publicos
- `GET /`
- `GET /libros/`
- `GET /libros/{id}`
- `POST /clientes/`
- `POST /pedidos/`
- `POST /auth/bootstrap-admin`
- `POST /auth/register`
- `POST /token`

### Autenticados
- `GET /users/me`

### Solo admin
- `POST /auth/users`
- `POST /libros/`
- `GET /clientes/frecuentes`
- `GET /ventas/`
- `GET /ventas/{id}`
- `POST /ventas/`
- `GET /pedidos/`
- `GET /pedidos/{id}`
- `PATCH /pedidos/{id}/estado`

## Validaciones implementadas
- Modelos de dominio con reglas de negocio para libros, clientes, ventas, pedidos y usuarios
- Schemas Pydantic para validar cuerpos HTTP y tipos de respuesta
- Validacion de `dni` con 8 digitos
- Validacion de usernames con letras, numeros y guion bajo
- Validacion de correo con `EmailStr` y normalizacion del email en el servicio
- Validacion de contrasenas con longitud minima, letras y numeros
- Validacion de tokens JWT firmados y con expiracion
- Proteccion de rutas con dependencias de FastAPI (`get_current_user`, `require_admin`)

## Ejecutar pruebas
```bash
python -m unittest discover -s tests -v
```

## Objetivo de aprendizaje
Este proyecto forma parte de mi proceso de crecimiento como desarrollador backend. Con la Fase 4A cerrada, la siguiente etapa prevista es profundizar la capa de persistencia y evolucionar el acceso a datos con herramientas mas avanzadas como ORM y migraciones.
