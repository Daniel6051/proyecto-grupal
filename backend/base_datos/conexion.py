from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import DATABASE_URL

# ==============================
# MOTOR DE BASE DE DATOS
# ==============================

engine = create_engine(DATABASE_URL, echo=True)

# ==============================
# SESIONES
# ==============================

SessionLocal = sessionmaker(bind=engine)

# ==============================
# BASE DE MODELOS
# ==============================

Base = declarative_base()

# ==============================
# CREAR BASE DE DATOS
# ==============================

def crear_base_datos():
    Base.metadata.create_all(bind=engine)
