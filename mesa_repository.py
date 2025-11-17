from models import Mesa
from db import Database

class MesaRepository:
    def __init__(self, db: Database):
        self.db = db

    def obtener_todas(self) -> list[Mesa]:
        filas = self.db.obtener_mesas()
        return [Mesa.from_db_row(row) for row in filas]

    def obtener_por_id(self, id_mesa: int) -> Mesa | None:
        row = self.db.obtener_mesa_por_id(id_mesa)
        return Mesa.from_db_row(row) if row else None
