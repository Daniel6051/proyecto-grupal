"""
interfaz/ventana_reportes.py
============================
Módulo de reportes — Subgrupo C
Permite al administrador generar:
  • PDF de ventas
  • Excel del inventario actual
  • Listado de alertas de stock crítico
"""

import tkinter as tk
from tkinter import messagebox, filedialog

from backend.base_datos.repositorios import listar_productos, listar_ventas
from reportes.pdf_ventas import generar_pdf_ventas
from reportes.excel_inventario import exportar_excel_inventario
from reportes.alertas import generar_reporte_alertas


# ════════════════════════════════════════════════════════════════════════
# Paleta de colores (consistente con el resto de la app)
# ════════════════════════════════════════════════════════════════════════
BG_DARK    = "#1e1e2e"
BG_PANEL   = "#181825"
BG_CARD    = "#313244"
FG_MAIN    = "#cdd6f4"
FG_PURPLE  = "#cba6f7"
FG_MUTED   = "#6c7086"
FG_GREEN   = "#a6e3a1"
FG_RED     = "#f38ba8"
FG_YELLOW  = "#f9e2af"
FONT_TITLE = ("Courier New", 16, "bold")
FONT_LABEL = ("Courier New", 10)
FONT_BTN   = ("Courier New", 10, "bold")


class VentanaReportes(tk.Toplevel):
    """
    Ventana secundaria con las opciones de reporte.
    Se abre desde VentanaPrincipal._abrir_reportes().
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("📄 Módulo de Reportes")
        self.geometry("640x520")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.grab_set()   # modal

        self._construir_ui()
        self._centrar()

    # ──────────────────────────────────────────────────────────────────
    # UI
    # ──────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # Encabezado
        frame_header = tk.Frame(self, bg=BG_PANEL, pady=14)
        frame_header.pack(fill="x")

        tk.Label(frame_header, text="📄 Módulo de Reportes",
                 font=FONT_TITLE, bg=BG_PANEL, fg=FG_PURPLE).pack()
        tk.Label(frame_header, text="Generá reportes del sistema en PDF y Excel",
                 font=FONT_LABEL, bg=BG_PANEL, fg=FG_MUTED).pack(pady=(4, 0))

        # ── Sección 1: PDF de ventas ───────────────────────────────────
        self._seccion(
            icono="📊",
            titulo="Reporte de Ventas (PDF)",
            descripcion="Genera un PDF con todas las ventas registradas y el total recaudado.",
            color_btn=FG_PURPLE,
            comando=self._generar_pdf_ventas,
        )

        # ── Sección 2: Excel inventario ────────────────────────────────
        self._seccion(
            icono="📋",
            titulo="Inventario Actual (Excel)",
            descripcion="Exporta el stock de todos los productos a un archivo .xlsx con formato.",
            color_btn=FG_GREEN,
            comando=self._exportar_excel,
        )

        # ── Sección 3: Alertas de stock ────────────────────────────────
        self._seccion(
            icono="⚠️",
            titulo="Alertas de Stock Mínimo",
            descripcion="Muestra los productos con stock igual o menor al mínimo configurado.",
            color_btn=FG_YELLOW,
            comando=self._ver_alertas,
        )

        # Botón cerrar
        tk.Button(
            self, text="Cerrar", font=FONT_BTN,
            bg=BG_CARD, fg=FG_MUTED, activebackground=BG_PANEL,
            relief="flat", cursor="hand2", pady=6,
            command=self.destroy,
        ).pack(pady=(8, 16), ipadx=20)

    def _seccion(self, icono, titulo, descripcion, color_btn, comando):
        frame = tk.Frame(self, bg=BG_CARD, pady=12, padx=16)
        frame.pack(fill="x", padx=24, pady=8)

        # Fila icono + título
        frame_top = tk.Frame(frame, bg=BG_CARD)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text=icono, font=("Courier New", 14),
                 bg=BG_CARD, fg=color_btn).pack(side="left")
        tk.Label(frame_top, text=f"  {titulo}", font=("Courier New", 11, "bold"),
                 bg=BG_CARD, fg=FG_MAIN).pack(side="left")

        tk.Label(frame, text=descripcion, font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED, wraplength=520, justify="left").pack(
            anchor="w", pady=(4, 8))

        tk.Button(
            frame, text="Generar", font=FONT_BTN,
            bg=color_btn, fg=BG_DARK, activebackground=FG_MAIN,
            relief="flat", cursor="hand2", pady=4, padx=14,
            command=comando,
        ).pack(anchor="e")

    # ──────────────────────────────────────────────────────────────────
    # Acciones
    # ──────────────────────────────────────────────────────────────────

    def _generar_pdf_ventas(self):
        try:
            ventas = listar_ventas()
            if not ventas:
                messagebox.showinfo("Sin datos", "No hay ventas registradas aún.", parent=self)
                return

            ruta = filedialog.asksaveasfilename(
                parent=self,
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile="reporte_ventas.pdf",
                title="Guardar reporte de ventas",
            )
            if not ruta:
                return  # usuario canceló

            generar_pdf_ventas(ventas, ruta)
            messagebox.showinfo(
                "✅ Éxito",
                f"PDF generado correctamente:\n{ruta}",
                parent=self,
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}", parent=self)

    def _exportar_excel(self):
        try:
            productos = listar_productos()
            if not productos:
                messagebox.showinfo("Sin datos", "No hay productos en el inventario.", parent=self)
                return

            ruta = filedialog.asksaveasfilename(
                parent=self,
                defaultextension=".xlsx",
                filetypes=[("Excel", "*.xlsx")],
                initialfile="inventario.xlsx",
                title="Guardar inventario en Excel",
            )
            if not ruta:
                return

            exportar_excel_inventario(productos, ruta)
            messagebox.showinfo(
                "✅ Éxito",
                f"Excel generado correctamente:\n{ruta}",
                parent=self,
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el Excel:\n{e}", parent=self)

    def _ver_alertas(self):
        try:
            productos = listar_productos()

            # Convertir objetos SQLAlchemy a dict para alertas.py
            inventario_dict = [
                {
                    "nombre": p.nombre,
                    "stock": p.stock,
                    "stock_minimo": p.stock_minimo,
                }
                for p in productos
            ]

            alertas = generar_reporte_alertas(inventario_dict)

            ventana_alertas = tk.Toplevel(self)
            ventana_alertas.title("⚠️ Alertas de Stock Mínimo")
            ventana_alertas.configure(bg=BG_DARK)
            ventana_alertas.geometry("520x400")
            ventana_alertas.grab_set()

            tk.Label(ventana_alertas, text="⚠️ Alertas de Stock Mínimo",
                     font=FONT_TITLE, bg=BG_DARK, fg=FG_YELLOW).pack(pady=12)

            frame_lista = tk.Frame(ventana_alertas, bg=BG_DARK)
            frame_lista.pack(fill="both", expand=True, padx=16, pady=4)

            scrollbar = tk.Scrollbar(frame_lista)
            scrollbar.pack(side="right", fill="y")

            listbox = tk.Listbox(
                frame_lista, bg=BG_CARD, fg=FG_MAIN, font=FONT_LABEL,
                selectbackground=FG_PURPLE, relief="flat", bd=0,
                yscrollcommand=scrollbar.set,
            )
            scrollbar.config(command=listbox.yview)
            listbox.pack(fill="both", expand=True)

            if not alertas:
                listbox.insert(tk.END, "✅ Todos los productos tienen stock suficiente.")
            else:
                for a in alertas:
                    listbox.insert(tk.END, a["mensaje"])

            tk.Button(
                ventana_alertas, text="Cerrar", font=FONT_BTN,
                bg=BG_CARD, fg=FG_MUTED, relief="flat",
                cursor="hand2", pady=5, command=ventana_alertas.destroy,
            ).pack(pady=10, ipadx=16)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las alertas:\n{e}", parent=self)

    # ──────────────────────────────────────────────────────────────────

    def _centrar(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - self.winfo_width())  // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
