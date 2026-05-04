# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

NOMBRE_SISTEMA = "Sistema de Stock y Ventas"

# Base de datos
NOMBRE_BD = "stock_ventas.db"

# URL para SQLAlchemy
DATABASE_URL = f"sqlite:///{NOMBRE_BD}"

# IVA
IVA = 0.21

# Stock mínimo
STOCK_MINIMO_DEFAULT = 5

# Roles
ROLES_VALIDOS = ("administrador", "vendedor", "repositor")