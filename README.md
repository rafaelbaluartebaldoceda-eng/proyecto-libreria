# Sistema de Gestion de Libreria

## Descripcion
Proyecto backend desarrollado en Python para gestionar libros, clientes, ventas, pedidos y usuarios autenticables en una libreria. El sistema mantiene una interfaz CLI y una API REST construida con FastAPI, trabajando sobre PostgreSQL, validaciones de dominio, autenticacion con JWT, persistencia con SQLAlchemy y versionado de esquema con Alembic.

## Tecnologias
- Python 3
- PostgreSQL 17+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Alembic
- psycopg2-binary
- python-jose
- pwdlib + argon2-cffi
- Pydantic

## Arquitectura actual
- `models/`: entidades del dominio y validaciones
- `services/`: logica de negocio reutilizable
- `repositories/`: acceso a datos con SQLAlchemy ORM
- `database/`: engine, sesiones SQLAlchemy y metadata ORM
- `alembic/`: migraciones versionadas del esquema
- `main.py`: interfaz CLI y flujo de consola
- `app/`: capa HTTP con FastAPI, routers, schemas, dependencias y seguridad
- `tests/`: pruebas automaticas de dominio, servicios y API

## Estado del proyecto
- Fase 1 completada: CLI con persistencia inicial
- Fase 2 completada: migracion a PostgreSQL y cierre tecnico del backend base
- Fase 3 completada: integracion base de FastAPI reutilizando la capa de servicios
- Fase 4A completada: autenticacion, autorizacion por rol y proteccion de rutas con JWT
- Fase 4B completada: migracion de persistencia a SQLAlchemy ORM y gobierno del esquema con Alembic

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
```

El esquema ya no se recomienda mantener a mano. A partir de esta fase, la fuente oficial del esquema es Alembic.

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

## Migraciones con Alembic
Aplicar la ultima migracion:

```bash
alembic upgrade head
```

Ver historial de migraciones:

```bash
alembic history
```

Crear una nueva migracion:

```bash
alembic revision -m "descripcion_del_cambio"
```

La migracion inicial ya fue validada contra PostgreSQL local y deja el esquema alineado con los modelos ORM del proyecto.

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
- La capa ORM conserva transacciones explicitas por operacion para evitar escrituras parciales.

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
- Constraints a nivel de base de datos modelados con SQLAlchemy y versionados con Alembic
- Repositories migrados a SQLAlchemy ORM sin romper la capa de servicios existente

## Ejecutar pruebas
```bash
python -m unittest discover -s tests -v
```

## Objetivo de aprendizaje
Este proyecto forma parte de mi proceso de crecimiento como desarrollador backend. Con la Fase 4 ya integrada a nivel de seguridad, ORM y migraciones, la siguiente etapa prevista es profundizar la evolucion del producto con relaciones de dominio mas finas, ownership entre usuarios y clientes, y mejoras de observabilidad o despliegue.
