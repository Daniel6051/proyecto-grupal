import tkinter as tk
from tkinter import messagebox
import bcrypt

from backend.base_datos.repositorios import buscar_usuario


# ==============================
# VENTANA DE LOGIN
# ==============================

class VentanaLogin(tk.Toplevel):
    """
    Pantalla de inicio de sesión.
    Valida usuario y contraseña contra la base de datos usando bcrypt.
    Al autenticarse con éxito, abre la ventana principal según el rol.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Iniciar sesión — Sistema de Stock y Ventas")
        self.resizable(False, False)
        self.geometry("380x340")
        self.configure(bg="#1e1e2e")

        # Resultado de la autenticación
        self.usuario_autenticado = None

        self._construir_ui()
        self._centrar_ventana()

        # Bloquea la ventana padre hasta que se cierre el login
        self.grab_set()
        self.focus_force()

    # ------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ------------------------------------------------------------------

    def _construir_ui(self):
        # ---- Encabezado ----
        tk.Label(
            self,
            text="📦 Stock & Ventas",
            font=("Courier New", 18, "bold"),
            bg="#1e1e2e",
            fg="#cba6f7",
        ).pack(pady=(30, 4))

        tk.Label(
            self,
            text="Ingrese sus credenciales para continuar",
            font=("Courier New", 9),
            bg="#1e1e2e",
            fg="#6c7086",
        ).pack(pady=(0, 20))

        # ---- Formulario ----
        frame_form = tk.Frame(self, bg="#1e1e2e")
        frame_form.pack(padx=40, fill="x")

        # Usuario
        tk.Label(
            frame_form, text="Usuario", font=("Courier New", 10),
            bg="#1e1e2e", fg="#cdd6f4", anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.entry_usuario = tk.Entry(
            frame_form,
            font=("Courier New", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cba6f7",
            relief="flat",
            bd=6,
        )
        self.entry_usuario.pack(fill="x", ipady=4)

        tk.Label(frame_form, bg="#1e1e2e", height=1).pack()  # espaciado

        # Contraseña
        tk.Label(
            frame_form, text="Contraseña", font=("Courier New", 10),
            bg="#1e1e2e", fg="#cdd6f4", anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.entry_password = tk.Entry(
            frame_form,
            show="●",
            font=("Courier New", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cba6f7",
            relief="flat",
            bd=6,
        )
        self.entry_password.pack(fill="x", ipady=4)

        # ---- Botón ----
        tk.Button(
            self,
            text="INGRESAR",
            font=("Courier New", 11, "bold"),
            bg="#cba6f7",
            fg="#1e1e2e",
            activebackground="#b4befe",
            activeforeground="#1e1e2e",
            relief="flat",
            cursor="hand2",
            command=self._intentar_login,
        ).pack(pady=24, ipadx=20, ipady=6)

        # Enter dispara el login
        self.bind("<Return>", lambda e: self._intentar_login())

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    # ------------------------------------------------------------------
    # LÓGICA DE AUTENTICACIÓN
    # ------------------------------------------------------------------

    def _intentar_login(self):
        nombre = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not nombre or not password:
            messagebox.showwarning("Campos vacíos", "Complete usuario y contraseña.", parent=self)
            return

        usuario = buscar_usuario(nombre)

        if usuario is None:
            messagebox.showerror("Error", "Usuario no encontrado.", parent=self)
            return

        if not self._verificar_password(password, usuario.password):
            messagebox.showerror("Error", "Contraseña incorrecta.", parent=self)
            return

        if not usuario.activo:
            messagebox.showerror("Error", "El usuario está inactivo.", parent=self)
            return

        self.usuario_autenticado = usuario
        self.destroy()

    @staticmethod
    def _verificar_password(password_plana: str, hash_guardado: str) -> bool:
        """
        Verifica la contraseña contra el hash bcrypt almacenado.
        También acepta contraseñas guardadas en texto plano (modo desarrollo).
        """
        try:
            return bcrypt.checkpw(
                password_plana.encode("utf-8"),
                hash_guardado.encode("utf-8"),
            )
        except Exception:
            # Fallback para desarrollo: comparación directa
            return password_plana == hash_guardado
