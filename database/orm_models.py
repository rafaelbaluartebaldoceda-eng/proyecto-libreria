"""Modelos ORM SQLAlchemy que representan el esquema persistente."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base declarativa compartida por los modelos ORM."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class LibroORM(Base):
    """Tabla persistente de libros."""

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    autor: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    ventas: Mapped[list["VentaORM"]] = relationship(back_populates="libro")
    pedidos: Mapped[list["PedidoORM"]] = relationship(back_populates="libro")

    __table_args__ = (
        CheckConstraint("precio > 0", name="precio_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )


class ClienteORM(Base):
    """Tabla persistente de clientes."""

    __tablename__ = "clientes"

    dni: Mapped[str] = mapped_column(String(8), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(150), nullable=False)
    frecuente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ventas: Mapped[list["VentaORM"]] = relationship(back_populates="cliente")
    pedidos: Mapped[list["PedidoORM"]] = relationship(back_populates="cliente")

    __table_args__ = (
        CheckConstraint("char_length(dni) = 8", name="dni_len_8"),
    )


class VentaORM(Base):
    """Tabla persistente de ventas."""

    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"), nullable=False)
    cliente_dni: Mapped[str] = mapped_column(
        ForeignKey("clientes.dni"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.now,
        server_default=func.now(),
    )

    libro: Mapped["LibroORM"] = relationship(back_populates="ventas")
    cliente: Mapped["ClienteORM"] = relationship(back_populates="ventas")

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="cantidad_positive"),
    )


class PedidoORM(Base):
    """Tabla persistente de pedidos."""

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"), nullable=False)
    cliente_dni: Mapped[str] = mapped_column(
        ForeignKey("clientes.dni"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    metodo_entrega: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="pendiente")
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.now,
        server_default=func.now(),
    )

    libro: Mapped["LibroORM"] = relationship(back_populates="pedidos")
    cliente: Mapped["ClienteORM"] = relationship(back_populates="pedidos")

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="cantidad_positive"),
        CheckConstraint(
            "metodo_entrega IN ('tienda', 'domicilio')",
            name="metodo_entrega_valid",
        ),
        CheckConstraint(
            "estado IN ('pendiente', 'entregado', 'cancelado')",
            name="estado_valid",
        ),
    )


class UsuarioORM(Base):
    """Tabla persistente de usuarios autenticables."""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="role_valid"),
    )
