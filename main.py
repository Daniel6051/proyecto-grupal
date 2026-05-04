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
from base_datos.conexion import crear_base_datos
import modelos.producto
import modelos.usuario
import modelos.venta
import modelos.proveedor

from interfaz.login import VentanaLogin
from interfaz.ventana_principal import VentanaPrincipal


def main():
    # ── 1. Inicializar base de datos ──────────────────────────────────
    crear_base_datos()

    # Crear un usuario de prueba si no existe (solo para desarrollo)
    _crear_usuario_demo()

    # ── 2. Ventana raíz oculta (necesaria para el Toplevel del login) ─
    root = tk.Tk()
    root.withdraw()  # ocultamos la raíz mientras está el login

    # ── 3. Pantalla de login ──────────────────────────────────────────
    login = VentanaLogin(root)
    root.wait_window(login)  # espera a que el login se cierre

    # ── 4. Verificar autenticación ────────────────────────────────────
    if login.usuario_autenticado is None:
        # El usuario cerró el login sin autenticarse
        root.destroy()
        return

    # ── 5. Abrir ventana principal ────────────────────────────────────
    root.destroy()  # destruimos la raíz temporal
    app = VentanaPrincipal(login.usuario_autenticado)
    app.mainloop()


def _crear_usuario_demo():
    """
    Crea un usuario administrador de prueba si la tabla está vacía.
    Contraseña: admin123 (guardada en texto plano para desarrollo).
    En producción reemplazar por un hash bcrypt.
    """
    from base_datos.repositorios import buscar_usuario, crear_usuario

    if buscar_usuario("admin") is None:
        crear_usuario("admin", "admin123", "administrador")
        print("[demo] Usuario 'admin' creado con contraseña 'admin123'")

    if buscar_usuario("vendedor") is None:
        crear_usuario("vendedor", "venta123", "vendedor")
        print("[demo] Usuario 'vendedor' creado con contraseña 'venta123'")


if __name__ == "__main__":
    main()
