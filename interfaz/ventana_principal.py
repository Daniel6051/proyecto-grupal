import tkinter as tk
from tkinter import messagebox

from backend.config import NOMBRE_SISTEMA, ROLES_VALIDOS


# ==============================
# VENTANA PRINCIPAL CON MENÚ
# ==============================

class VentanaPrincipal(tk.Tk):
    """
    Ventana raíz de la aplicación.
    Muestra el menú principal adaptado al rol del usuario autenticado.
    Opciones: Registrar venta | Ver stock | Reportes | Salir
    """

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"{NOMBRE_SISTEMA} — {usuario.nombre_usuario} ({usuario.rol})")
        self.geometry("700x480")
        self.minsize(600, 420)
        self.configure(bg="#1e1e2e")

        self._construir_menu()
        self._construir_ui()
        self._centrar_ventana()

    # ------------------------------------------------------------------
    # MENÚ NATIVO DE LA VENTANA
    # ------------------------------------------------------------------

    def _construir_menu(self):
        barra = tk.Menu(self, bg="#313244", fg="#cdd6f4", activebackground="#cba6f7")

        # Menú Ventas
        menu_ventas = tk.Menu(barra, tearoff=0, bg="#313244", fg="#cdd6f4")
        menu_ventas.add_command(label="Registrar venta", command=self._abrir_venta)
        menu_ventas.add_separator()
        menu_ventas.add_command(label="Salir", command=self._salir)
        barra.add_cascade(label="Ventas", menu=menu_ventas)

        # Menú Stock (solo admin y repositor)
        if self.usuario.rol in ("administrador", "repositor"):
            menu_stock = tk.Menu(barra, tearoff=0, bg="#313244", fg="#cdd6f4")
            menu_stock.add_command(label="Ver stock actual", command=self._abrir_stock)
            menu_stock.add_command(label="Alertas de stock mínimo", command=self._abrir_alertas)
            barra.add_cascade(label="Stock", menu=menu_stock)

        # Menú Reportes (solo admin)
        if self.usuario.rol == "administrador":
            menu_reportes = tk.Menu(barra, tearoff=0, bg="#313244", fg="#cdd6f4")
            menu_reportes.add_command(label="Reporte de ventas", command=self._abrir_reportes)
            barra.add_cascade(label="Reportes", menu=menu_reportes)

        self.config(menu=barra)

    # ------------------------------------------------------------------
    # INTERFAZ PRINCIPAL (DASHBOARD)
    # ------------------------------------------------------------------

    def _construir_ui(self):
        # Encabezado
        frame_header = tk.Frame(self, bg="#181825", pady=16)
        frame_header.pack(fill="x")

        tk.Label(
            frame_header,
            text=f"📦 {NOMBRE_SISTEMA}",
            font=("Courier New", 20, "bold"),
            bg="#181825",
            fg="#cba6f7",
        ).pack()

        tk.Label(
            frame_header,
            text=f"Bienvenido, {self.usuario.nombre_usuario}  •  Rol: {self.usuario.rol.upper()}",
            font=("Courier New", 10),
            bg="#181825",
            fg="#6c7086",
        ).pack(pady=(4, 0))

        # Área de botones de acceso rápido
        frame_botones = tk.Frame(self, bg="#1e1e2e")
        frame_botones.pack(expand=True)

        botones = self._obtener_botones_por_rol()

        for i, (icono, texto, comando) in enumerate(botones):
            col = i % 2
            row = i // 2
            self._crear_boton_card(frame_botones, icono, texto, comando).grid(
                row=row, column=col, padx=20, pady=16, sticky="nsew"
            )

        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)

        # Pie de página
        tk.Label(
            self,
            text="Autómatas y Lenguajes — Universidad del Aconcagua — 2026",
            font=("Courier New", 8),
            bg="#1e1e2e",
            fg="#45475a",
        ).pack(side="bottom", pady=8)

    def _crear_boton_card(self, parent, icono, texto, comando):
        """Crea una tarjeta-botón grande para el dashboard."""
        frame = tk.Frame(
            parent,
            bg="#313244",
            cursor="hand2",
            width=220,
            height=110,
        )
        frame.pack_propagate(False)

        tk.Label(frame, text=icono, font=("Segoe UI Emoji", 28), bg="#313244").pack(pady=(14, 4))
        tk.Label(
            frame, text=texto, font=("Courier New", 11, "bold"),
            bg="#313244", fg="#cdd6f4"
        ).pack()

        # Hover effects
        def on_enter(e): frame.configure(bg="#45475a"); [w.configure(bg="#45475a") for w in frame.winfo_children()]
        def on_leave(e): frame.configure(bg="#313244"); [w.configure(bg="#313244") for w in frame.winfo_children()]
        def on_click(e): comando()

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        frame.bind("<Button-1>", on_click)
        for child in frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            child.bind("<Button-1>", on_click)

        return frame

    def _obtener_botones_por_rol(self):
        """Devuelve los botones disponibles según el rol del usuario."""
        botones = [("🛒", "Registrar Venta", self._abrir_venta)]

        if self.usuario.rol in ("administrador", "repositor"):
            botones.append(("📊", "Ver Stock", self._abrir_stock))
            botones.append(("⚠️", "Alertas de Stock", self._abrir_alertas))

        if self.usuario.rol == "administrador":
            botones.append(("📄", "Reportes", self._abrir_reportes))

        botones.append(("🚪", "Salir", self._salir))
        return botones

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    # ------------------------------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------------------------------

    def _abrir_venta(self):
        from interfaz.ventana_venta import VentanaVenta
        VentanaVenta(self, self.usuario)

    def _abrir_stock(self):
        from interfaz.ventana_stock import VentanaStock
        VentanaStock(self)

    def _abrir_alertas(self):
        from interfaz.ventana_stock import VentanaAlertas
        VentanaAlertas(self)

    def _abrir_reportes(self):
        messagebox.showinfo(
            "Reportes",
            "El módulo de reportes será implementado por el Subgrupo C.",
            parent=self,
        )

    def _salir(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar el sistema?", parent=self):
            self.destroy()
