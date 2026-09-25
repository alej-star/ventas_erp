import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar


class VentasFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()
        self.asegurar_tabla()
        self.cargar_ventas()

    def asegurar_tabla(self):
        """Verifica que la tabla ventas tenga las columnas correctas; si no, la reconstruye."""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(ventas)")
            columnas = [col[1] for col in cursor.fetchall()]

            # Si la tabla vieja no tiene la columna id o cliente, se elimina
            if "id" not in columnas or "cliente" not in columnas:
                cursor.execute("DROP TABLE IF EXISTS ventas")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT,
                    concepto TEXT,
                    total REAL NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al asegurar tabla ventas: {e}")

    def crear_interfaz(self):
        tk.Label(
            self,
            text="GESTIÓN DE VENTAS",
            bg=COLOR_FONDO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # FORMULARIO
        form = tk.LabelFrame(
            self,
            text="REGISTRAR NUEVA VENTA",
            bg=COLOR_BLANCO,
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Cliente", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_cliente = tk.Entry(form, width=30)
        self.ent_cliente.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Producto / Concepto", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_concepto = tk.Entry(form, width=35)
        self.ent_concepto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Monto Total ($)", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_total = tk.Entry(form, width=20)
        self.ent_total.grid(row=1, column=2, padx=5, pady=5)

        # BOTONES
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(
            barra, text="Registrar Venta", bg="#16A34A", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.registrar_venta
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text="Limpiar", bg="#64748B", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.limpiar_formulario
        ).pack(side="left", padx=5)

        # TABLA DE VENTAS
        columnas = ("id", "cliente", "concepto", "total")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        self.tree.heading("id", text="Nº FACTURA / ID")
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("concepto", text="CONCEPTO / PRODUCTO")
        self.tree.heading("total", text="TOTAL ($)")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("cliente", width=200)
        self.tree.column("concepto", width=300)
        self.tree.column("total", width=150, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def registrar_venta(self):
        cliente = self.ent_cliente.get().strip()
        concepto = self.ent_concepto.get().strip()
        monto_str = self.ent_total.get().strip()

        try:
            total = float(monto_str)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto total numérico válido.")
            return

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ventas (cliente, concepto, total) VALUES (?, ?, ?)", (cliente, concepto, total))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self.limpiar_formulario()
            self.cargar_ventas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")

    def cargar_ventas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, cliente, concepto, total FROM ventas ORDER BY id DESC")
            registros = cursor.fetchall()
            conn.close()

            for fila in registros:
                cli = fila[1] if fila[1] else "General"
                con = fila[2] if fila[2] else "Venta Directa"
                self.tree.insert("", "end", values=(fila[0], cli, con, f"${fila[3]:,.2f}"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas:\n{e}")

    def limpiar_formulario(self):
        self.ent_cliente.delete(0, tk.END)
        self.ent_concepto.delete(0, tk.END)
        self.ent_total.delete(0, tk.END)


# Aliases de compatibilidad por si main los invoca con otro nombre
VentasView = VentasFrame