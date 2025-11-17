# models.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import IntEnum
from typing import Optional, Any, Dict


# -------------------------------------------------------------------
# Clase base para todas las entidades (para herencia)
# -------------------------------------------------------------------
@dataclass
class BaseEntity:
    """
    Clase base para representar entidades de la base de datos.

    Más adelante, si quieres, aquí podemos agregar:
    - validaciones genéricas
    - lógica común de serialización
    - métodos para comparar cambios, etc.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un dict (útil para inserts/updates)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        """
        Crea una entidad a partir de un diccionario.
        Útil si en el futuro usamos cursor tipo dict (RealDictCursor).
        """
        return cls(**data)


# -------------------------------------------------------------------
# Enumeración para el estado de la mesa: 0, 1, 2 -> más legible
# -------------------------------------------------------------------
class EstadoMesa(IntEnum):
    LIBRE = 0
    OCUPADA = 1
    RESERVADA = 2


# -------------------------------------------------------------------
# Entidad: mesas
# -------------------------------------------------------------------
@dataclass
class Mesa(BaseEntity):
    """
    Representa un registro de la tabla 'mesas'.

    CREATE TABLE mesas (
        id INT PRIMARY KEY,
        sillas INT NOT NULL,
        estado INT NOT NULL CHECK (estado IN (0, 1, 2)),
        pos_x INT NOT NULL,
        pos_y INT NOT NULL,
        ancho INT NOT NULL,
        alto INT NOT NULL,
        forma VARCHAR(20) NOT NULL
    );
    """
    id: int
    sillas: int
    estado: EstadoMesa
    pos_x: int
    pos_y: int
    ancho: int
    alto: int
    forma: str  # ej. "rectangulo", "circulo"

    @classmethod
    def from_db_row(cls, row: tuple) -> "Mesa":
        """
        Crea una Mesa a partir de una tupla devuelta por psycopg2
        con el SELECT en el orden:
        (id, sillas, estado, pos_x, pos_y, ancho, alto, forma)
        """
        return cls(
            id=row[0],
            sillas=row[1],
            estado=EstadoMesa(row[2]),
            pos_x=row[3],
            pos_y=row[4],
            ancho=row[5],
            alto=row[6],
            forma=row[7],
        )

    def cambiar_estado(self, nuevo_estado: EstadoMesa) -> None:
        """Cambia el estado de la mesa (libre, ocupada, reservada)."""
        self.estado = nuevo_estado

    def esta_libre(self) -> bool:
        return self.estado == EstadoMesa.LIBRE

    def esta_ocupada(self) -> bool:
        return self.estado == EstadoMesa.OCUPADA


# -------------------------------------------------------------------
# Entidad: producto
# -------------------------------------------------------------------
@dataclass
class Producto(BaseEntity):
    """
    Representa un registro de la tabla 'producto'.

    CREATE TABLE producto (
        id_pro SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        id_rec INT,
        disponible BOOLEAN,
        FOREIGN KEY (id_rec) REFERENCES receta(id)
    );
    ALTER TABLE producto
    ADD COLUMN precio NUMERIC(10, 2);
    """
    id_pro: int
    nombre: str
    id_rec: Optional[int]
    disponible: bool
    precio: float

    @classmethod
    def from_db_row(cls, row: tuple) -> "Producto":
        """
        Espera un SELECT en el orden:
        (id_pro, nombre, id_rec, disponible, precio)
        """
        return cls(
            id_pro=row[0],
            nombre=row[1],
            id_rec=row[2],
            disponible=row[3],
            precio=float(row[4]),
        )

    def marcar_disponible(self) -> None:
        self.disponible = True

    def marcar_no_disponible(self) -> None:
        self.disponible = False


# -------------------------------------------------------------------
# Entidad: cuenta  (cada renglón de la tabla cuenta)
# -------------------------------------------------------------------
@dataclass
class Cuenta(BaseEntity):
    """
    Representa un registro de la tabla 'cuenta'.

    CREATE TABLE cuenta (
        id SERIAL PRIMARY KEY,
        id_mesa INT NOT NULL REFERENCES mesas(id),
        num_id_producto VARCHAR(13) NOT NULL REFERENCES inventario(num_id),
        valor_articulo FLOAT NOT NULL,
        cantidad INT NOT NULL,
        subtotal FLOAT NOT NULL,
        id_folio INT,
        observaciones TEXT
    );
    """
    id: int
    id_mesa: int
    num_id_producto: str
    valor_articulo: float
    cantidad: int
    subtotal: float
    id_folio: Optional[int] = None
    observaciones: Optional[str] = None

    @classmethod
    def from_db_row(cls, row: tuple) -> "Cuenta":
        """
        Espera un SELECT en el orden:
        (id, id_mesa, num_id_producto, valor_articulo,
         cantidad, subtotal, id_folio, observaciones)
        """
        return cls(
            id=row[0],
            id_mesa=row[1],
            num_id_producto=row[2],
            valor_articulo=row[3],
            cantidad=row[4],
            subtotal=row[5],
            id_folio=row[6],
            observaciones=row[7],
        )

    def recalcular_subtotal(self) -> None:
        """Recalcula el subtotal según valor_articulo * cantidad."""
        self.subtotal = self.valor_articulo * self.cantidad
