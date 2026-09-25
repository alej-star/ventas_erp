import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar


class ComprasFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.compra_id = None
        self.crear_interfaz()
        self.asegurar_tabla()
        self.cargar_compras()

    def asegurar_tabla(self):
        """Crea o ajusta la tabla compras para evitar errores de columnas."""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(compras)")
            columnas = [col[1] for col in cursor.fetchall()]

            if "proveedor" not in columnas:
                cursor.execute("DROP TABLE IF EXISTS compras")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proveedor TEXT NOT NULL,
                    concepto TEXT,
                    total REAL NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al asegurar tabla compras: {e}")

    def crear_interfaz(self):
        # TÍTULO
        tk.Label(
            self,
            text="GESTIÓN DE COMPRAS",
            bg=COLOR_FONDO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # FORMULARIO
        form = tk.LabelFrame(
            self,
            text="REGISTRAR NUEVA COMPRA / ORDEN",
            bg=COLOR_BLANCO,
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Proveedor", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_proveedor = tk.Entry(form, width=30)
        self.ent_proveedor.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Concepto / Insumos", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_concepto = tk.Entry(form, width=35)
        self.ent_concepto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Monto Total ($)", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_total = tk.Entry(form, width=20)
        self.ent_total.grid(row=1, column=2, padx=5, pady=5)

        # BOTONES DE ACCIÓN
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(
            barra, text="Registrar Compra", bg="#16A34A", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.registrar_compra
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text="Limpiar", bg="#64748B", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.limpiar_formulario
        ).pack(side="left", padx=5)

        # TABLA DE HISTORIAL DE COMPRAS
        columnas = ("id", "proveedor", "concepto", "total")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        self.tree.heading("id", text="Nº ORDEN / ID")
        self.tree.heading("proveedor", text="PROVEEDOR")
        self.tree.heading("concepto", text="CONCEPTO / INSUMOS")
        self.tree.heading("total", text="TOTAL ($)")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("proveedor", width=200)
        self.tree.column("concepto", width=300)
        self.tree.column("total", width=150, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def registrar_compra(self):
        proveedor = self.ent_proveedor.get().strip()
        concepto = self.ent_concepto.get().strip()
        monto_str = self.ent_total.get().strip()

        if not proveedor:
            messagebox.showwarning("Validación", "El campo Proveedor es obligatorio.")
            return

        try:
            total = float(monto_str)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto total numérico válido.")
            return

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO compras (proveedor, concepto, total) VALUES (?, ?, ?)",
                (proveedor, concepto, total)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Orden de compra registrada correctamente.")
            self.limpiar_formulario()
            self.cargar_compras()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la compra:\n{e}")

    def cargar_compras(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, proveedor, concepto, total FROM compras ORDER BY id DESC")
            registros = cursor.fetchall()
            conn.close()

            for fila in registros:
                self.tree.insert("", "end", values=(fila[0], fila[1], fila[2], f"${fila[3]:,.2f}"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las compras:\n{e}")

    def limpiar_formulario(self):
        self.ent_proveedor.delete(0, tk.END)
        self.ent_concepto.delete(0, tk.END)
        self.ent_total.delete(0, tk.END)


# Alias de compatibilidad
ComprasView = ComprasFrame