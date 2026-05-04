import tkinter as tk
from tkinter import ttk, messagebox

from base_datos.repositorios import listar_productos


# ==============================
# VENTANA DE STOCK
# ==============================

class VentanaStock(tk.Toplevel):
    """
    Muestra el inventario completo con todos sus atributos.
    Permite filtrar por categoría y nombre.
    """

    def __init__(self, master):
        super().__init__(master)
        self.title("Inventario — Stock Actual")
        self.geometry("760x480")
        self.minsize(640, 380)
        self.configure(bg="#1e1e2e")

        self.productos = listar_productos()

        self._construir_ui()
        self._centrar_ventana()
        self.grab_set()

    # ------------------------------------------------------------------
    # INTERFAZ
    # ------------------------------------------------------------------

    def _construir_ui(self):
        # Encabezado
        frame_header = tk.Frame(self, bg="#181825", pady=10)
        frame_header.pack(fill="x")
        tk.Label(
            frame_header, text="📊  Stock Actual",
            font=("Courier New", 16, "bold"),
            bg="#181825", fg="#89b4fa"
        ).pack()
        tk.Label(
            frame_header,
            text=f"{len(self.productos)} productos registrados",
            font=("Courier New", 9), bg="#181825", fg="#6c7086"
        ).pack(pady=(2, 0))

        # Buscador y filtros
        frame_filtros = tk.Frame(self, bg="#1e1e2e")
        frame_filtros.pack(fill="x", padx=12, pady=8)

        tk.Label(frame_filtros, text="🔍 Buscar:", font=("Courier New", 10),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *_: self._filtrar())
        tk.Entry(
            frame_filtros, textvariable=self.var_buscar,
            font=("Courier New", 10), bg="#313244", fg="#cdd6f4",
            insertbackground="#89b4fa", relief="flat", bd=4, width=20
        ).pack(side="left", padx=(4, 14), ipady=3)

        tk.Label(frame_filtros, text="Categoría:", font=("Courier New", 10),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        categorias = ["Todas"] + sorted(set(p.categoria for p in self.productos))
        self.var_categoria = tk.StringVar(value="Todas")
        self.var_categoria.trace_add("write", lambda *_: self._filtrar())
        combo = ttk.Combobox(
            frame_filtros, textvariable=self.var_categoria,
            values=categorias, state="readonly", width=16,
            font=("Courier New", 10)
        )
        combo.pack(side="left", padx=4)

        tk.Button(
            frame_filtros, text="↺ Actualizar",
            font=("Courier New", 9), bg="#45475a", fg="#cdd6f4",
            relief="flat", cursor="hand2",
            command=self._recargar
        ).pack(side="right", ipadx=6, ipady=3)

        # Tabla
        cols = ("ID", "Nombre", "Categoría", "Precio", "Stock", "Stock Mín.", "Estado")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=16)
        _estilizar_tabla(self.tabla)
        anchos = (40, 180, 110, 90, 70, 80, 80)
        for col, w in zip(cols, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=w, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 12))
        scroll.pack(side="left", fill="y", pady=(0, 12))

        self._cargar_tabla(self.productos)

    def _cargar_tabla(self, productos):
        self.tabla.delete(*self.tabla.get_children())
        for p in productos:
            estado = "Activo" if p.activo else "Inactivo"
            tag = ""
            if not p.activo:
                tag = "inactivo"
            elif p.alerta_stock_minimo():
                tag = "bajo"

            self.tabla.insert(
                "", "end",
                values=(p.id, p.nombre, p.categoria, f"${p.precio:.2f}",
                        p.stock, p.stock_minimo, estado),
                tags=(tag,)
            )

        self.tabla.tag_configure("bajo", foreground="#f38ba8")
        self.tabla.tag_configure("inactivo", foreground="#6c7086")

    def _filtrar(self):
        texto = self.var_buscar.get().lower()
        cat = self.var_categoria.get()
        filtrados = [
            p for p in self.productos
            if (texto in p.nombre.lower() or texto in p.categoria.lower())
            and (cat == "Todas" or p.categoria == cat)
        ]
        self._cargar_tabla(filtrados)

    def _recargar(self):
        self.productos = listar_productos()
        self._filtrar()
        messagebox.showinfo("Actualizado", "Stock actualizado desde la base de datos.", parent=self)

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ==============================
# VENTANA DE ALERTAS DE STOCK
# ==============================

class VentanaAlertas(tk.Toplevel):
    """
    Muestra solo los productos con stock en o por debajo del stock mínimo.
    """

    def __init__(self, master):
        super().__init__(master)
        self.title("⚠️ Alertas de Stock Mínimo")
        self.geometry("640x400")
        self.configure(bg="#1e1e2e")

        productos = listar_productos()
        self.alertas = [p for p in productos if p.alerta_stock_minimo() and p.activo]

        self._construir_ui()
        self._centrar_ventana()
        self.grab_set()

    def _construir_ui(self):
        frame_header = tk.Frame(self, bg="#181825", pady=10)
        frame_header.pack(fill="x")
        tk.Label(
            frame_header, text="⚠️  Productos con Stock Bajo",
            font=("Courier New", 15, "bold"),
            bg="#181825", fg="#f38ba8"
        ).pack()
        tk.Label(
            frame_header,
            text=f"{len(self.alertas)} producto(s) requieren reposición",
            font=("Courier New", 9), bg="#181825", fg="#6c7086"
        ).pack(pady=(2, 0))

        if not self.alertas:
            tk.Label(
                self, text="✅ Todos los productos tienen stock suficiente.",
                font=("Courier New", 12), bg="#1e1e2e", fg="#a6e3a1"
            ).pack(expand=True)
            return

        cols = ("ID", "Nombre", "Categoría", "Stock Actual", "Stock Mínimo", "Faltante")
        tabla = ttk.Treeview(self, columns=cols, show="headings", height=14)
        _estilizar_tabla(tabla)
        for col, w in zip(cols, (40, 180, 110, 90, 90, 80)):
            tabla.heading(col, text=col)
            tabla.column(col, width=w, anchor="center")

        for p in self.alertas:
            faltante = max(0, p.stock_minimo - p.stock)
            tabla.insert(
                "", "end",
                values=(p.id, p.nombre, p.categoria, p.stock, p.stock_minimo, faltante),
                tags=("alerta",)
            )
        tabla.tag_configure("alerta", foreground="#f38ba8")
        tabla.pack(fill="both", expand=True, padx=12, pady=12)

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ==============================
# HELPER COMPARTIDO
# ==============================

def _estilizar_tabla(tabla):
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Treeview",
        background="#313244", fieldbackground="#313244",
        foreground="#cdd6f4", rowheight=24,
        font=("Courier New", 9)
    )
    estilo.configure(
        "Treeview.Heading",
        background="#45475a", foreground="#89b4fa",
        font=("Courier New", 9, "bold")
    )
    estilo.map("Treeview", background=[("selected", "#585b70")])
