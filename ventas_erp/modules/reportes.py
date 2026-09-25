import tkinter as tk
from tkinter import ttk
from config import COLOR_FONDO, COLOR_BLANCO
from database import total_productos, total_clientes, total_proveedores, total_ventas


class ReportesFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()

    def obtener_conteo_seguro(self, funcion):
        try:
            return funcion()
        except Exception:
            return 0

    def crear_interfaz(self):
        tk.Label(
            self,
            text="REPORTES Y ESTADÍSTICAS DEL SISTEMA",
            bg=COLOR_FONDO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # RESUMEN DE TARJETAS
        resumen_frame = tk.LabelFrame(
            self,
            text="RESUMEN EJECUTIVO",
            bg=COLOR_BLANCO,
            padx=15,
            pady=15
        )
        resumen_frame.pack(fill="x", padx=10, pady=5)

        tarjetas = [
            ("Total Productos", self.obtener_conteo_seguro(total_productos), "#2563EB"),
            ("Total Clientes", self.obtener_conteo_seguro(total_clientes), "#16A34A"),
            ("Total Proveedores", self.obtener_conteo_seguro(total_proveedores), "#EA580C"),
            ("Total Ventas", self.obtener_conteo_seguro(total_ventas), "#7C3AED")
        ]

        for i, (titulo, val, color) in enumerate(tarjetas):
            card = tk.Frame(resumen_frame, bg=color, width=200, height=80)
            card.pack_propagate(False)
            card.grid(row=0, column=i, padx=10, pady=5)

            tk.Label(card, text=titulo, bg=color, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
            tk.Label(card, text=str(val), bg=color, fg="white", font=("Segoe UI", 18, "bold")).pack()

        # TABLA DE DETALLES
        detalle_frame = tk.LabelFrame(
            self,
            text="DETALLE DE MOVIMIENTOS RECIENTES",
            bg=COLOR_BLANCO,
            padx=10,
            pady=10
        )
        detalle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("tipo", "descripcion", "monto", "estado")
        self.tree = ttk.Treeview(detalle_frame, columns=columnas, show="headings", height=8)
        self.tree.heading("tipo", text="TIPO DE MOVIMIENTO")
        self.tree.heading("descripcion", text="DESCRIPCIÓN")
        self.tree.heading("monto", text="MONTO / CANTIDAD")
        self.tree.heading("estado", text="ESTADO")

        self.tree.column("tipo", width=150, anchor="center")
        self.tree.column("descripcion", width=300)
        self.tree.column("monto", width=150, anchor="e")
        self.tree.column("estado", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.cargar_reporte()

    def cargar_reporte(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        prod = self.obtener_conteo_seguro(total_productos)
        cli = self.obtener_conteo_seguro(total_clientes)
        prov = self.obtener_conteo_seguro(total_proveedores)
        vta = self.obtener_conteo_seguro(total_ventas)

        self.tree.insert("", "end", values=("Venta", "Registro de ventas acumuladas", f"{vta} transacciones", "Completado"))
        self.tree.insert("", "end", values=("Inventario", "Productos en stock activo", f"{prod} registros", "Activo"))
        self.tree.insert("", "end", values=("Clientes", "Directorio de clientes", f"{cli} registrados", "Activo"))
        self.tree.insert("", "end", values=("Proveedores", "Red de proveedores", f"{prov} proveedores", "Activo"))


# Alias de compatibilidad
ReportesView = ReportesFrame