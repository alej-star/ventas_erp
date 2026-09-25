import sys
import os

# Permite encontrar config.py y database.py al ejecutarse de forma independiente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from config import COLOR_FONDO, COLOR_BLANCO
from database import total_productos, total_clientes, total_proveedores, total_ventas


class DashboardFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_dashboard()

    def obtener_conteo_seguro(self, funcion):
        try:
            return funcion()
        except Exception:
            return 0

    def crear_tarjeta(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, width=180, height=120)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=titulo,
            bg=color,
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(20, 10))

        tk.Label(
            card,
            text=str(valor),
            bg=color,
            fg="white",
            font=("Segoe UI", 26, "bold")
        ).pack()

        return card

    def crear_dashboard(self):
        # TÍTULO PRINCIPAL
        tk.Label(
            self,
            text="DASHBOARD",
            bg=COLOR_FONDO,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(40, 25))

        # CONTENEDOR HORIZONTAL EN 1 SOLA FILA
        row_frame = tk.Frame(self, bg=COLOR_FONDO)
        row_frame.pack(pady=10)

        tarjetas_data = [
            ("PRODUCTOS", self.obtener_conteo_seguro(total_productos), "#2563EB"),   # Azul
            ("CLIENTES", self.obtener_conteo_seguro(total_clientes), "#16A34A"),    # Verde
            ("PROVEEDORES", self.obtener_conteo_seguro(total_proveedores), "#EA580C"), # Naranja
            ("VENTAS", self.obtener_conteo_seguro(total_ventas), "#8B5CF6")         # Púrpura
        ]

        for i, (titulo, valor, color) in enumerate(tarjetas_data):
            t = self.crear_tarjeta(row_frame, titulo, valor, color)
            t.grid(row=0, column=i, padx=10, pady=10)

        # MENSAJE INFERIOR
        tk.Label(
            self,
            text="Bienvenido al ERP Empresarial",
            bg=COLOR_FONDO,
            fg="#334155",
            font=("Segoe UI", 11)
        ).pack(pady=(40, 0))


# Alias de compatibilidad
DashboardView = DashboardFrame


# ==============================================================================
# EJECUCIÓN AUTÓNOMA COMO VENTANA COMPLETA (IGUAL A LA IMAGEN)
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ERP EMPRESARIAL")
    root.geometry("1050x680")
    root.configure(bg=COLOR_FONDO)

    # BARRA LATERAL SIMULADA
    sidebar = tk.Frame(root, bg="#1E293B", width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Encabezado Sidebar
    tk.Label(sidebar, text="🛒 ERP EMPRESARIAL", bg="#1E293B", fg="white", font=("Segoe UI", 12, "bold")).pack(pady=(20, 2))
    tk.Label(sidebar, text="Versión 1.0", bg="#1E293B", fg="#94A3B8", font=("Segoe UI", 9)).pack(pady=(0, 20))

    # Opciones de Menú
    opciones = [
        ("Dashboard", True),
        ("Ventas", False),
        ("Inventario", False),
        ("Clientes", False),
        ("Proveedores", False),
        ("Cuentas por Cobrar", False),
        ("Cuentas por Pagar", False),
        ("ReportesAuditoría", False),
        ("Cerrar Sesión", False)
    ]

    for texto, activo in opciones:
        fg_col = "white" if activo else "#94A3B8"
        tk.Label(sidebar, text=texto, bg="#1E293B", fg=fg_col, font=("Segoe UI", 10), anchor="w", padx=25).pack(fill="x", pady=5)

    # Pie de página Sidebar
    footer = tk.Frame(sidebar, bg="#1E293B")
    footer.pack(side="bottom", fill="x", pady=15, padx=15)
    tk.Label(footer, text="Mi Empresa JURM S.A.S", bg="#1E293B", fg="#94A3B8", font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x")
    tk.Label(footer, text="NIT: 900.123.456-7", bg="#1E293B", fg="#64748B", font=("Segoe UI", 8), anchor="w").pack(fill="x")

    # PANEL DEL DASHBOARD A LA DERECHA
    dash_panel = DashboardFrame(root)
    dash_panel.pack(side="right", fill="both", expand=True)

    root.mainloop()