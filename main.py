"""
main.py — Punto de entrada del Sistema de Stock y Ventas
=========================================================
Flujo de arranque:
  1. Se crea la base de datos (si no existe).
  2. Se muestra la pantalla de login.
  3. Si la autenticación es exitosa, se abre la ventana principal.
  4. La ventana principal adapta su menú según el rol del usuario.
"""

import tkinter as tk

from backend.base_datos.conexion import crear_base_datos
import backend.modelos.producto
import backend.modelos.usuario
import backend.modelos.venta
import backend.modelos.proveedor

from interfaz.login import VentanaLogin
from interfaz.ventana_principal import VentanaPrincipal


def main():
    crear_base_datos()
    _crear_usuario_demo()

    root = tk.Tk()
    root.withdraw()

    login = VentanaLogin(root)
    root.wait_window(login)

    if login.usuario_autenticado is None:
        root.destroy()
        return

    root.destroy()
    app = VentanaPrincipal(login.usuario_autenticado)
    app.mainloop()


def _crear_usuario_demo():
    from backend.base_datos.repositorios import buscar_usuario, crear_usuario

    if buscar_usuario("admin") is None:
        crear_usuario("admin", "admin123", "administrador")
        print("[demo] Usuario 'admin' creado con contraseña 'admin123'")

    if buscar_usuario("vendedor") is None:
        crear_usuario("vendedor", "venta123", "vendedor")
        print("[demo] Usuario 'vendedor' creado con contraseña 'venta123'")


if __name__ == "__main__":
    main()