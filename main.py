import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Transporte")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f9")

        # Crear contenedor principal
        self.main_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Caja de texto para mostrar archivos cargados
        self.loaded_files_text = tk.Text(self.main_frame, height=10, width=70, bg="#ffffff", fg="#333", font=("Arial", 12), state=tk.DISABLED)
        self.loaded_files_text.pack(pady=10)

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Sistema de Gestión de Transporte", font=("Arial", 22, "bold"), bg="#f4f4f9", fg="#333").pack(pady=20)

        button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049", "bd": 0, "width": 30, "height": 2}

        ttk.Style().configure("TButton", padding=6, font=("Arial", 12))

        tk.Button(self.main_frame, text="Cargar Archivo de Rutas", command=self.load_routes, **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Gestión de Clientes", command=self.manage_clients, **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Gestión de Vehículos", command=self.manage_vehicles, **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Gestión de Viajes", command=self.manage_trips, **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Generar Reportes", command=self.generate_reports, **button_style).pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Restaurar la caja de texto para mostrar archivos cargados
        self.loaded_files_text = tk.Text(self.main_frame, height=10, width=70, bg="#ffffff", fg="#333", font=("Arial", 8), state=tk.DISABLED)
        self.loaded_files_text.pack(pady=10)

    def load_routes(self):
        filepath = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                self.update_loaded_files(f"Contenido del archivo:\n{content}\n")
                messagebox.showinfo("Cargar Archivo", f"Archivo cargado: {filepath}")
                # Aquí se generará el grafo
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def update_loaded_files(self, text):
        self.loaded_files_text.config(state=tk.NORMAL)
        self.loaded_files_text.insert(tk.END, text)
        self.loaded_files_text.config(state=tk.DISABLED)

    def manage_clients(self):
        self.manage_entity("Clientes")

    def manage_vehicles(self):
        self.manage_entity("Vehículos")

    def manage_trips(self):
        self.manage_entity("Viajes", trips=True)

    def generate_reports(self):
        messagebox.showinfo("Reportes", "Generar reportes no implementado aún.")

    def manage_entity(self, entity_name, trips=False):
        self.clear_frame()

        tk.Label(self.main_frame, text=f"Gestión de {entity_name}", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333").pack(pady=20)

        button_style = {"font": ("Arial", 14), "bg": "#2196F3", "fg": "white", "activebackground": "#1e88e5", "bd": 0, "width": 30, "height": 2}

        tk.Button(self.main_frame, text="Crear", command=lambda: self.entity_action(entity_name, "Crear"), **button_style).pack(pady=5)
        
        if not trips:
            tk.Button(self.main_frame, text="Modificar", command=lambda: self.entity_action(entity_name, "Modificar"), **button_style).pack(pady=5)
            tk.Button(self.main_frame, text="Eliminar", command=lambda: self.entity_action(entity_name, "Eliminar"), **button_style).pack(pady=5)
            tk.Button(self.main_frame, text="Mostrar Información", command=lambda: self.entity_action(entity_name, "Mostrar Información"), **button_style).pack(pady=5)

        tk.Button(self.main_frame, text="Mostrar Estructura de Datos", command=lambda: self.entity_action(entity_name, "Mostrar Estructura de Datos"), **button_style).pack(pady=5)

        tk.Button(self.main_frame, text="Volver al Menú Principal", command=self.create_main_menu, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", bd=0, width=30, height=2).pack(pady=20)

    def entity_action(self, entity_name, action):
        messagebox.showinfo("Acción", f"{action} en {entity_name} no implementado aún.")

# Inicialización de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()
