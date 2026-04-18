"""Baseline schema with ORM-managed tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260417_0001"
down_revision = None
branch_labels = None
depends_on = None


def _has_table(bind, table_name):
    """Indica si una tabla ya existe en el esquema actual."""
    return inspect(bind).has_table(table_name)


def upgrade():
    """Crea las tablas base del proyecto si aun no existen."""
    bind = op.get_bind()

    if not _has_table(bind, "libros"):
        op.create_table(
            "libros",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("titulo", sa.String(length=100), nullable=False),
            sa.Column("autor", sa.String(length=100), nullable=False),
            sa.Column("categoria", sa.String(length=50), nullable=False),
            sa.Column("precio", sa.Integer(), nullable=False),
            sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
            sa.CheckConstraint("precio > 0", name="ck_libros_precio_positive"),
            sa.CheckConstraint("stock >= 0", name="ck_libros_stock_non_negative"),
            sa.PrimaryKeyConstraint("id", name="pk_libros"),
        )

    if not _has_table(bind, "clientes"):
        op.create_table(
            "clientes",
            sa.Column("dni", sa.String(length=8), nullable=False),
            sa.Column("nombre", sa.String(length=100), nullable=False),
            sa.Column("correo", sa.String(length=100), nullable=False),
            sa.Column("direccion", sa.String(length=150), nullable=False),
            sa.Column("frecuente", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.CheckConstraint("char_length(dni) = 8", name="ck_clientes_dni_len_8"),
            sa.PrimaryKeyConstraint("dni", name="pk_clientes"),
        )

    if not _has_table(bind, "ventas"):
        op.create_table(
            "ventas",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("libro_id", sa.Integer(), nullable=False),
            sa.Column("cliente_dni", sa.String(length=8), nullable=False),
            sa.Column("cantidad", sa.Integer(), nullable=False),
            sa.Column(
                "fecha",
                sa.DateTime(timezone=False),
                nullable=False,
                server_default=sa.text("NOW()"),
            ),
            sa.CheckConstraint("cantidad > 0", name="ck_ventas_cantidad_positive"),
            sa.ForeignKeyConstraint(["cliente_dni"], ["clientes.dni"], name="fk_ventas_cliente_dni_clientes"),
            sa.ForeignKeyConstraint(["libro_id"], ["libros.id"], name="fk_ventas_libro_id_libros"),
            sa.PrimaryKeyConstraint("id", name="pk_ventas"),
        )

    if not _has_table(bind, "pedidos"):
        op.create_table(
            "pedidos",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("libro_id", sa.Integer(), nullable=False),
            sa.Column("cliente_dni", sa.String(length=8), nullable=False),
            sa.Column("cantidad", sa.Integer(), nullable=False),
            sa.Column("metodo_entrega", sa.String(length=20), nullable=False),
            sa.Column("estado", sa.String(length=20), nullable=False, server_default="pendiente"),
            sa.Column(
                "fecha",
                sa.DateTime(timezone=False),
                nullable=False,
                server_default=sa.text("NOW()"),
            ),
            sa.CheckConstraint("cantidad > 0", name="ck_pedidos_cantidad_positive"),
            sa.CheckConstraint(
                "metodo_entrega IN ('tienda', 'domicilio')",
                name="ck_pedidos_metodo_entrega_valid",
            ),
            sa.CheckConstraint(
                "estado IN ('pendiente', 'entregado', 'cancelado')",
                name="ck_pedidos_estado_valid",
            ),
            sa.ForeignKeyConstraint(["cliente_dni"], ["clientes.dni"], name="fk_pedidos_cliente_dni_clientes"),
            sa.ForeignKeyConstraint(["libro_id"], ["libros.id"], name="fk_pedidos_libro_id_libros"),
            sa.PrimaryKeyConstraint("id", name="pk_pedidos"),
        )

    if not _has_table(bind, "usuarios"):
        op.create_table(
            "usuarios",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("username", sa.String(length=50), nullable=False),
            sa.Column("email", sa.String(length=100), nullable=False),
            sa.Column("hashed_password", sa.String(length=255), nullable=False),
            sa.Column("role", sa.String(length=20), nullable=False, server_default="user"),
            sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.CheckConstraint("role IN ('admin', 'user')", name="ck_usuarios_role_valid"),
            sa.PrimaryKeyConstraint("id", name="pk_usuarios"),
            sa.UniqueConstraint("username", name="uq_usuarios_username"),
            sa.UniqueConstraint("email", name="uq_usuarios_email"),
        )


def downgrade():
    """Elimina las tablas del proyecto si existen."""
    bind = op.get_bind()
    inspector = inspect(bind)

    for table_name in ("usuarios", "pedidos", "ventas", "clientes", "libros"):
        if inspector.has_table(table_name):
            op.drop_table(table_name)
