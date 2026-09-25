import tkinter as tk
from tkinter import messagebox
from config import APP_TITLE, VERSION, COMPANY_NAME, COMPANY_NIT
from database import init_db

from modules.dashboard import DashboardFrame
from modules.inventario import InventarioFrame
from modules.clientes import ClientesFrame
from modules.compras import ComprasFrame
from modules.proveedores import ProveedoresFrame
from modules.reportes import ReportesFrame
from modules.ventas import VentasFrame

class ERPEmpresarialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1050x680")
        self.configure(bg="#f0f4f8")

        init_db()

        self.setup_sidebar()

        self.container = tk.Frame(self, bg="#f0f4f8")
        self.container.pack(side="right", fill="both", expand=True)

        self.views = {}
        self.init_views()

        self.show_view("Dashboard")

    def setup_sidebar(self):
        sidebar = tk.Frame(self, bg="#1e293b", width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text=f"🛒 {APP_TITLE}", font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#1e293b").pack(anchor="w", padx=15, pady=(20, 2))
        tk.Label(sidebar, text=f"Versión {VERSION}", font=("Helvetica", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=15, pady=(0, 15))

        menu_items = [
            ("Dashboard", lambda: self.show_view("Dashboard")),
            ("Ventas", lambda: self.show_view("Ventas")),
            ("Inventario", lambda: self.show_view("Inventario")),
            ("Clientes", lambda: self.show_view("Clientes")),
            ("Proveedores", lambda: self.show_view("Proveedores")),
            ("Compras", lambda: self.show_view("Compras")),
            ("Reportes", lambda: self.show_view("Reportes")),
            ("Cerrar Sesión", self.cerrar_sesion)
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar, text=text, font=("Helvetica", 10),
                fg="#cbd5e1", bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
                bd=0, anchor="w", padx=15, pady=7, cursor="hand2", command=command
            )
            btn.pack(fill="x")

        footer = tk.Frame(sidebar, bg="#1e293b")
        footer.pack(side="bottom", fill="x", padx=15, pady=20)
        tk.Label(footer, text=COMPANY_NAME, font=("Helvetica", 8, "bold"), fg="#94a3b8", bg="#1e293b", anchor="w").pack(fill="x")
        tk.Label(footer, text=f"NIT: {COMPANY_NIT}", font=("Helvetica", 8), fg="#64748b", bg="#1e293b", anchor="w").pack(fill="x")

    def init_views(self):
        self.views["Dashboard"] = DashboardFrame(self.container)
        self.views["Inventario"] = InventarioFrame(self.container)
        self.views["Clientes"] = ClientesFrame(self.container)
        self.views["Compras"] = ComprasFrame(self.container)
        self.views["Proveedores"] = ProveedoresFrame(self.container)
        self.views["Reportes"] = ReportesFrame(self.container)
        self.views["Ventas"] = VentasFrame (self.container)

        for view in self.views.values():
            view.place(x=0, y=0, relwidth=1, relheight=1)

    def show_view(self, name):
        view = self.views[name]
        if hasattr(view, 'cargar_tabla'):
            view.cargar_tabla()
        view.tkraise()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Deseas salir del ERP Empresarial?"):
            self.destroy()

if __name__ == "__main__":
    app = ERPEmpresarialApp()
    app.mainloop()
