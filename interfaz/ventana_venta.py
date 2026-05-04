import tkinter as tk
from tkinter import ttk, messagebox

from backend.base_datos.repositorios import listar_productos, crear_venta, actualizar_stock
from backend.config import IVA


# ==============================
# VENTANA DE VENTA CON CARRITO
# ==============================

class VentanaVenta(tk.Toplevel):
    """
    Ventana para registrar una venta.
    Permite:
      - Buscar y agregar productos al carrito
      - Ver subtotales, IVA y total en tiempo real
      - Quitar ítems del carrito
      - Cerrar la venta (descuenta stock y persiste en BD)
    """

    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.title("Registrar Venta")
        self.geometry("820x560")
        self.minsize(700, 480)
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        # Estado interno
        self.carrito: list[dict] = []          # ítems en el carrito
        self.productos_bd: list = listar_productos()  # todos los productos

        self._construir_ui()
        self._centrar_ventana()
        self.grab_set()

    # ------------------------------------------------------------------
    # INTERFAZ
    # ------------------------------------------------------------------

    def _construir_ui(self):
        # ── Encabezado ────────────────────────────────────────────────
        frame_header = tk.Frame(self, bg="#181825", pady=10)
        frame_header.pack(fill="x")
        tk.Label(
            frame_header, text="🛒  Nueva Venta",
            font=("Courier New", 16, "bold"),
            bg="#181825", fg="#a6e3a1"
        ).pack()
        tk.Label(
            frame_header,
            text=f"Vendedor: {self.usuario.nombre_usuario}",
            font=("Courier New", 9), bg="#181825", fg="#6c7086"
        ).pack()

        # ── Cuerpo: dos columnas ──────────────────────────────────────
        frame_cuerpo = tk.Frame(self, bg="#1e1e2e")
        frame_cuerpo.pack(fill="both", expand=True, padx=12, pady=8)
        frame_cuerpo.columnconfigure(0, weight=1)
        frame_cuerpo.columnconfigure(1, weight=1)
        frame_cuerpo.rowconfigure(0, weight=1)

        # Columna izquierda: catálogo de productos
        self._construir_catalogo(frame_cuerpo)

        # Columna derecha: carrito
        self._construir_carrito(frame_cuerpo)

        # ── Pie: totales y botones ────────────────────────────────────
        self._construir_pie()

    def _construir_catalogo(self, parent):
        frame = tk.LabelFrame(
            parent, text=" Catálogo de Productos ",
            font=("Courier New", 10, "bold"),
            bg="#1e1e2e", fg="#cba6f7", bd=1, relief="solid"
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        # Buscador
        frame_buscar = tk.Frame(frame, bg="#1e1e2e")
        frame_buscar.pack(fill="x", padx=8, pady=(8, 4))
        tk.Label(frame_buscar, text="🔍", bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *_: self._filtrar_productos())
        tk.Entry(
            frame_buscar, textvariable=self.var_buscar,
            font=("Courier New", 10), bg="#313244", fg="#cdd6f4",
            insertbackground="#cba6f7", relief="flat", bd=4
        ).pack(side="left", fill="x", expand=True, ipady=3)

        # Tabla de productos
        cols = ("ID", "Nombre", "Categoría", "Precio", "Stock")
        self.tabla_productos = ttk.Treeview(
            frame, columns=cols, show="headings", height=12
        )
        self._estilizar_tabla(self.tabla_productos)
        for col, w in zip(cols, (40, 160, 100, 80, 60)):
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=w, anchor="center")
        self.tabla_productos.pack(fill="both", expand=True, padx=8, pady=4)

        # Cantidad + Agregar
        frame_agregar = tk.Frame(frame, bg="#1e1e2e")
        frame_agregar.pack(fill="x", padx=8, pady=(4, 8))
        tk.Label(frame_agregar, text="Cantidad:", font=("Courier New", 10),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.spin_cantidad = tk.Spinbox(
            frame_agregar, from_=1, to=9999, width=5,
            font=("Courier New", 10), bg="#313244", fg="#cdd6f4",
            buttonbackground="#45475a", relief="flat"
        )
        self.spin_cantidad.pack(side="left", padx=6)
        tk.Button(
            frame_agregar, text="Agregar al carrito →",
            font=("Courier New", 10, "bold"),
            bg="#a6e3a1", fg="#1e1e2e",
            activebackground="#94e2d5", relief="flat", cursor="hand2",
            command=self._agregar_al_carrito
        ).pack(side="left", ipady=3, ipadx=8)

        self._cargar_productos()

    def _construir_carrito(self, parent):
        frame = tk.LabelFrame(
            parent, text=" Carrito de Venta ",
            font=("Courier New", 10, "bold"),
            bg="#1e1e2e", fg="#a6e3a1", bd=1, relief="solid"
        )
        frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        cols = ("Producto", "Cant.", "Precio u.", "Subtotal")
        self.tabla_carrito = ttk.Treeview(
            frame, columns=cols, show="headings", height=14
        )
        self._estilizar_tabla(self.tabla_carrito)
        for col, w in zip(cols, (160, 50, 80, 90)):
            self.tabla_carrito.heading(col, text=col)
            self.tabla_carrito.column(col, width=w, anchor="center")
        self.tabla_carrito.pack(fill="both", expand=True, padx=8, pady=(8, 4))

        tk.Button(
            frame, text="✖ Quitar ítem seleccionado",
            font=("Courier New", 9),
            bg="#f38ba8", fg="#1e1e2e",
            activebackground="#eba0ac", relief="flat", cursor="hand2",
            command=self._quitar_del_carrito
        ).pack(pady=(0, 8), ipadx=6, ipady=3)

    def _construir_pie(self):
        frame_pie = tk.Frame(self, bg="#181825", pady=10)
        frame_pie.pack(fill="x", padx=12)

        # Totales (izquierda)
        frame_totales = tk.Frame(frame_pie, bg="#181825")
        frame_totales.pack(side="left")

        self.lbl_subtotal = tk.Label(
            frame_totales, text="Subtotal:    $0.00",
            font=("Courier New", 11), bg="#181825", fg="#cdd6f4"
        )
        self.lbl_subtotal.pack(anchor="w")

        self.lbl_iva = tk.Label(
            frame_totales, text=f"IVA ({int(IVA*100)}%):   $0.00",
            font=("Courier New", 11), bg="#181825", fg="#fab387"
        )
        self.lbl_iva.pack(anchor="w")

        self.lbl_total = tk.Label(
            frame_totales, text="TOTAL:       $0.00",
            font=("Courier New", 14, "bold"), bg="#181825", fg="#a6e3a1"
        )
        self.lbl_total.pack(anchor="w", pady=(4, 0))

        # Botones (derecha)
        frame_botones = tk.Frame(frame_pie, bg="#181825")
        frame_botones.pack(side="right")

        tk.Button(
            frame_botones, text="🗑 Limpiar carrito",
            font=("Courier New", 10),
            bg="#45475a", fg="#cdd6f4",
            activebackground="#585b70", relief="flat", cursor="hand2",
            command=self._limpiar_carrito
        ).pack(side="left", padx=(0, 8), ipadx=6, ipady=4)

        tk.Button(
            frame_botones, text="✔ Cerrar Venta",
            font=("Courier New", 12, "bold"),
            bg="#cba6f7", fg="#1e1e2e",
            activebackground="#b4befe", relief="flat", cursor="hand2",
            command=self._cerrar_venta
        ).pack(side="left", ipadx=12, ipady=6)

    # ------------------------------------------------------------------
    # LÓGICA DEL CATÁLOGO
    # ------------------------------------------------------------------

    def _cargar_productos(self):
        """Carga todos los productos activos en la tabla del catálogo."""
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        for p in self.productos_bd:
            if p.activo:
                tag = "bajo_stock" if p.alerta_stock_minimo() else ""
                self.tabla_productos.insert(
                    "", "end",
                    values=(p.id, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock),
                    tags=(tag,)
                )
        self.tabla_productos.tag_configure("bajo_stock", foreground="#f38ba8")

    def _filtrar_productos(self):
        """Filtra el catálogo según el texto del buscador."""
        texto = self.var_buscar.get().lower()
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        for p in self.productos_bd:
            if p.activo and (texto in p.nombre.lower() or texto in p.categoria.lower()):
                tag = "bajo_stock" if p.alerta_stock_minimo() else ""
                self.tabla_productos.insert(
                    "", "end",
                    values=(p.id, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock),
                    tags=(tag,)
                )
        self.tabla_productos.tag_configure("bajo_stock", foreground="#f38ba8")

    # ------------------------------------------------------------------
    # LÓGICA DEL CARRITO
    # ------------------------------------------------------------------

    def _agregar_al_carrito(self):
        seleccion = self.tabla_productos.focus()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccioná un producto del catálogo.", parent=self)
            return

        try:
            cantidad = int(self.spin_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Ingresá una cantidad válida (número entero positivo).", parent=self)
            return

        valores = self.tabla_productos.item(seleccion, "values")
        id_prod = int(valores[0])

        # Buscar producto en memoria
        producto = next((p for p in self.productos_bd if p.id == id_prod), None)
        if producto is None:
            return

        # Verificar stock suficiente considerando lo ya en carrito
        en_carrito = sum(i["cantidad"] for i in self.carrito if i["id"] == id_prod)
        if producto.stock < en_carrito + cantidad:
            messagebox.showerror(
                "Stock insuficiente",
                f"Stock disponible: {producto.stock - en_carrito} unidades.",
                parent=self
            )
            return

        # Si ya existe en el carrito, acumular
        existente = next((i for i in self.carrito if i["id"] == id_prod), None)
        if existente:
            existente["cantidad"] += cantidad
        else:
            self.carrito.append({
                "id": id_prod,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "cantidad": cantidad,
            })

        self._actualizar_tabla_carrito()
        self._actualizar_totales()

    def _quitar_del_carrito(self):
        seleccion = self.tabla_carrito.focus()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccioná un ítem del carrito.", parent=self)
            return
        idx = self.tabla_carrito.index(seleccion)
        self.carrito.pop(idx)
        self._actualizar_tabla_carrito()
        self._actualizar_totales()

    def _limpiar_carrito(self):
        if self.carrito and messagebox.askyesno("Limpiar", "¿Vaciar el carrito?", parent=self):
            self.carrito.clear()
            self._actualizar_tabla_carrito()
            self._actualizar_totales()

    def _actualizar_tabla_carrito(self):
        self.tabla_carrito.delete(*self.tabla_carrito.get_children())
        for item in self.carrito:
            subtotal = item["precio"] * item["cantidad"]
            self.tabla_carrito.insert(
                "", "end",
                values=(item["nombre"], item["cantidad"],
                        f"${item['precio']:.2f}", f"${subtotal:.2f}")
            )

    def _actualizar_totales(self):
        subtotal = sum(i["precio"] * i["cantidad"] for i in self.carrito)
        iva_monto = subtotal * IVA
        total = subtotal + iva_monto
        self.lbl_subtotal.config(text=f"Subtotal:    ${subtotal:,.2f}")
        self.lbl_iva.config(text=f"IVA ({int(IVA*100)}%):   ${iva_monto:,.2f}")
        self.lbl_total.config(text=f"TOTAL:       ${total:,.2f}")

    # ------------------------------------------------------------------
    # CERRAR VENTA
    # ------------------------------------------------------------------

    def _cerrar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "Agregá productos antes de cerrar la venta.", parent=self)
            return

        subtotal = sum(i["precio"] * i["cantidad"] for i in self.carrito)
        total_con_iva = subtotal * (1 + IVA)

        confirmacion = messagebox.askyesno(
            "Confirmar venta",
            f"¿Confirmar la venta por un total de ${total_con_iva:,.2f}?",
            parent=self
        )
        if not confirmacion:
            return

        try:
            # Persistir venta en BD
            venta = crear_venta(self.usuario.id, total_con_iva)

            # Descontar stock de cada producto
            for item in self.carrito:
                producto = next((p for p in self.productos_bd if p.id == item["id"]), None)
                if producto:
                    nuevo_stock = producto.stock - item["cantidad"]
                    actualizar_stock(producto.id, nuevo_stock)
                    producto.stock = nuevo_stock  # actualizar en memoria

            messagebox.showinfo(
                "Venta registrada ✔",
                f"Venta #{venta.id} registrada exitosamente.\nTotal: ${total_con_iva:,.2f}",
                parent=self
            )
            self.carrito.clear()
            self._actualizar_tabla_carrito()
            self._actualizar_totales()
            self._cargar_productos()  # refrescar stock en catálogo

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}", parent=self)

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    @staticmethod
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
            background="#45475a", foreground="#cba6f7",
            font=("Courier New", 9, "bold")
        )
        estilo.map("Treeview", background=[("selected", "#585b70")])

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
