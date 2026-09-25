import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar


class ProveedoresFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.proveedor_id = None
        self.crear_interfaz()
        self.asegurar_tabla()
        self.cargar_proveedores()

    def asegurar_tabla(self):
        """Verifica que la tabla tenga la columna id y si no, la recrea limpia."""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(proveedores)")
            columnas = [col[1] for col in cursor.fetchall()]

            if "id" not in columnas:
                cursor.execute("DROP TABLE IF EXISTS proveedores")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nit TEXT,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al asegurar tabla proveedores: {e}")

    def crear_interfaz(self):
        tk.Label(
            self,
            text="GESTIÓN DE PROVEEDORES",
            bg=COLOR_FONDO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # FORMULARIO
        form = tk.LabelFrame(
            self,
            text="DATOS DEL PROVEEDOR",
            bg=COLOR_BLANCO,
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Nombre / Razón Social", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_nombre = tk.Entry(form, width=35)
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="NIT / RUC", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_nit = tk.Entry(form, width=20)
        self.ent_nit.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Teléfono", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_telefono = tk.Entry(form, width=20)
        self.ent_telefono.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(form, text="Email", bg=COLOR_BLANCO).grid(row=2, column=0, sticky="w")
        self.ent_email = tk.Entry(form, width=35)
        self.ent_email.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(form, text="Dirección", bg=COLOR_BLANCO).grid(row=2, column=1, sticky="w")
        self.ent_direccion = tk.Entry(form, width=35)
        self.ent_direccion.grid(row=3, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        # BOTONES
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(
            barra, text="Guardar", bg="#16A34A", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.guardar_proveedor
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text="Actualizar", bg="#2563EB", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.actualizar_proveedor
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text="Eliminar", bg="#DC2626", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.eliminar_proveedor
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text="Limpiar", bg="#64748B", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.limpiar_formulario
        ).pack(side="left", padx=5)

        # TABLA
        columnas = ("id", "nombre", "nit", "telefono", "email", "direccion")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="NOMBRE / RAZÓN SOCIAL")
        self.tree.heading("nit", text="NIT / RUC")
        self.tree.heading("telefono", text="TELÉFONO")
        self.tree.heading("email", text="EMAIL")
        self.tree.heading("direccion", text="DIRECCIÓN")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("nit", width=120)
        self.tree.column("telefono", width=120)
        self.tree.column("email", width=180)
        self.tree.column("direccion", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def guardar_proveedor(self):
        nombre = self.ent_nombre.get().strip()
        nit = self.ent_nit.get().strip()
        telefono = self.ent_telefono.get().strip()
        email = self.ent_email.get().strip()
        direccion = self.ent_direccion.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre del proveedor es obligatorio.")
            return

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proveedores (nombre, nit, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, nit, telefono, email, direccion))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el proveedor:\n{e}")

    def actualizar_proveedor(self):
        if self.proveedor_id is None:
            messagebox.showwarning("Actualizar", "Seleccione un proveedor de la tabla.")
            return

        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE proveedores
                SET nombre = ?, nit = ?, telefono = ?, email = ?, direccion = ?
                WHERE id = ?
            """, (
                nombre,
                self.ent_nit.get().strip(),
                self.ent_telefono.get().strip(),
                self.ent_email.get().strip(),
                self.ent_direccion.get().strip(),
                self.proveedor_id
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor:\n{e}")

    def eliminar_proveedor(self):
        if self.proveedor_id is None:
            messagebox.showwarning("Eliminar", "Seleccione un proveedor de la tabla.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM proveedores WHERE id = ?", (self.proveedor_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_proveedores()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el proveedor:\n{e}")

    def cargar_proveedores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            self.asegurar_tabla()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, nit, telefono, email, direccion FROM proveedores ORDER BY nombre")
            registros = cursor.fetchall()
            conn.close()

            for fila in registros:
                self.tree.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proveedores:\n{e}")

    def seleccionar_proveedor(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos = self.tree.item(seleccion[0], "values")
        self.limpiar_formulario()
        self.proveedor_id = datos[0]
        self.ent_nombre.insert(0, datos[1] if datos[1] else "")
        self.ent_nit.insert(0, datos[2] if datos[2] else "")
        self.ent_telefono.insert(0, datos[3] if datos[3] else "")
        self.ent_email.insert(0, datos[4] if datos[4] else "")
        self.ent_direccion.insert(0, datos[5] if datos[5] else "")

    def limpiar_formulario(self):
        self.proveedor_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_nit.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

# Aliases de compatibilidad por si main los invoca con otro nombre
ProveedoresView = ProveedoresFrame