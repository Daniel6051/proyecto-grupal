from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from base_datos.conexion import Base


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    total = Column(Float, default=0)

    # relación con usuario
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<Venta(id={self.id}, total={self.total})>"