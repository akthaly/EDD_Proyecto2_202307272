import datetime
import os
import tkinter as tk
from tkinter import Image, ttk, filedialog, messagebox, font 
from PIL import Image, ImageTk
from datetime import datetime


from Clases.Clientes import Cliente
from Clases.GestorViajes import GestorViajes
from Clases.Rutas import Ruta
from Clases.Vehiculos import Vehiculo
from Clases.Viajes import Viaje
from arbol.ArbolB import ArbolB
from Estructuras.rutas_lista_de_adyacencia.ListaDeAdyacencia import GrafoRutas
from Estructuras.clientes_lista_circular_doble.ListaCircularDoble import ListaCircularDoblementeEnlazada

lista_clientes = ListaCircularDoblementeEnlazada()
arbol_vehiculos = ArbolB(5)
grafo_rutas = GrafoRutas()
gestor_viajes = GestorViajes(lista_clientes, arbol_vehiculos, grafo_rutas)

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Transporte")
        self.root.geometry("800x600")
        self.root.configure(bg="#BCCCDC")
        #messagebox.showinfo("AVISO.", "Antes de todo, cargar el archivo con las rutas.")

        # principal
        self.main_frame = tk.Frame(self.root, bg="#BCCCDC")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # text to show info
        self.text_frame = tk.Frame(self.root, bg="#BCCCDC")
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        image = tk.PhotoImage(file="imagenes/imagen.png")
        image = image.subsample(4, 4)
        
        tk.Label(self.main_frame, text="Llega Rapidito", font=("Consolas", 22, "bold"), bg="#BCCCDC", fg="#3B3030", image=image, compound="left").pack(pady=20)
        tk.image = image
        button_style = {
            "font": ("Consolas", 14),
            "bg": "#66785F",
            "fg": "white",
            "activebackground": "#91AC8F",
            "bd": 2,
            "relief": tk.RAISED,
            "highlightthickness": 0,
            "overrelief": tk.GROOVE,
            "width": 25,
            "height": 2
        }

        button_frame = tk.Frame(self.main_frame, bg="#9AA6B2")
        button_frame.pack(pady=7)

        tk.Button(button_frame, text="Cargar Archivo de Rutas", command=self.load_routes, **button_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Gestión de Clientes", command=self.manage_clients, **button_style).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Gestión de Vehículos", command=self.manage_vehicles, **button_style).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Gestión de Viajes", command=self.manage_trips, **button_style).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Carga Masiva Clientes", command=self.manage_massive_clients, **button_style).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Carga Masiva Vehículos", command=self.manage_massive_autos, **button_style).grid(row=2, column=1, padx=10, pady=10)


        tk.Button(self.main_frame, text="Generar Reportes", command=self.generate_reports, **button_style).pack(pady=20)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def load_routes(self):
        filepath = filedialog.askopenfilename(filetypes=[("cs Files", "*.cs"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.readlines()

                    for line in content:
                        data = line.strip().split("/")
                        if len(data) == 3:
                            origen = data[0].strip()
                            destino = data[1].strip()
                            tiempo_de_ruta_str = data[2].strip().replace("%", "")

                            # Verificación de tipos
                            if not isinstance(origen, str):
                                raise ValueError(f"El origen debe ser de tipo string, pero se encontró {type(origen)}.")
                            if not isinstance(destino, str):
                                raise ValueError(f"El destino debe ser de tipo string, pero se encontró {type(destino)}.")

                            try:
                                tiempo_de_ruta = int(tiempo_de_ruta_str)  # Convertir tiempo_de_ruta a entero
                            except ValueError:
                                raise ValueError(f"El tiempo de ruta '{tiempo_de_ruta_str}' no es un número válido.")
                            
                            # Verificación de tipo de tiempo_de_ruta
                            if not isinstance(tiempo_de_ruta, int):
                                raise ValueError(f"El tiempo de ruta debe ser de tipo int, pero se encontró {type(tiempo_de_ruta)}.")

                            # Crear el objeto Ruta y agregar la ruta
                            ruta = Ruta(origen, destino, tiempo_de_ruta)
                            print(ruta.getOrigen() + " " + ruta.getDestino() + " " + str(ruta.getTiempoDeRuta()))
                            grafo_rutas.agregar_ruta(origen, destino, tiempo_de_ruta)

                
                self.update_loaded_files(f"Contenido del archivo:\n{content}\n")
                grafo_rutas.mostrar_grafo()
                grafo_rutas.generar_grafo_graphviz()
                messagebox.showinfo("Cargar Archivo", "Archivo de rutas cargado con éxito")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")


    def update_loaded_files(self, text):
        # show info in console
        print(text)

    def manage_clients(self):
        self.open_entity_window("Clientes")

    def manage_vehicles(self):
        self.open_entity_window("Vehículos", vehicles=True)

    def manage_trips(self):
        self.open_entity_window("Viajes", trips=True)
    
    def manage_massive_clients(self):
        window = tk.Toplevel(self.root)
        window.title("Carga Masiva de Clientes")
        window.geometry("400x250")
        window.configure(bg="#e3f2fd")

        tk.Label(window, text="Cargar Clientes Masivos", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

        def load_clients_from_file():
            filepath = filedialog.askopenfilename(filetypes=[("cs Files", "*.cs"), ("All Files", "*.*")])
            if filepath:
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.readlines()



                    for line in content:
                        data = line.strip().split(",")
                        if len(data) == 6:
                            dpi, nombre, apellido, genero, telefono, direccion = data
                            cliente = Cliente(dpi, nombre, apellido, genero, telefono, direccion)
                            lista_clientes.insertar(cliente)
                            print(cliente.getDPI())

                    messagebox.showinfo("Carga Completa", "Clientes cargados correctamente.")
                    lista_clientes.imprimir()
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

        tk.Button(window, text="Cargar Clientes", command=load_clients_from_file, font=("Arial", 14), bg="#1976d2", fg="white", activebackground="#0d47a1", bd=2, relief=tk.RAISED).pack(pady=20)

        tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", bd=2, relief=tk.RAISED).pack(pady=20)

    
    def manage_massive_autos(self):
        window = tk.Toplevel(self.root)
        window.title("Carga Masiva de Vehículos")
        window.geometry("400x250")
        window.configure(bg="#e3f2fd")

        tk.Label(window, text="Cargar Vehículos Masivos", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

        def load_vehicles_from_file():
            filepath = filedialog.askopenfilename(filetypes=[("cs Files", "*.cs"), ("All Files", "*.*")])
            if filepath:
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.readlines()

                    for line in content:
                        data = line.strip().split(":")
                        if len(data) == 4:
                            placa, marca, modelo, precio = data
                            vehiculo = Vehiculo(placa, marca, modelo, precio)
                            arbol_vehiculos.insertar_vehiculo(vehiculo)
                            print(vehiculo.getPlaca())  

                    messagebox.showinfo("Carga Completa", "Vehículos cargados correctamente.")
                    
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

        tk.Button(window, text="Cargar Vehículos", command=load_vehicles_from_file, font=("Arial", 14), bg="#1976d2", fg="white", activebackground="#0d47a1", bd=2, relief=tk.RAISED).pack(pady=20)

        tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", bd=2, relief=tk.RAISED).pack(pady=20)


    def generate_reports(self):
        window = tk.Toplevel(self.root)
        window.title("Generar Reportes")
        window.geometry("400x350")
        window.configure(bg="#FFF0D1")

        tk.Label(window, text="Generar Reportes", font=("Arial", 18, "bold"), bg="#FFF0D1", fg="#3B3030").pack(pady=20)

        button_style = {
            "font": ("Arial", 14),
            "bg": "#795757",
            "fg": "white",
            "activebackground": "#664343",
            "bd": 2,
            "relief": tk.RAISED,
            "highlightthickness": 0,
            "overrelief": tk.GROOVE,
            "width": 25,
            "height": 2
        }

        # tk.Button(window, text="Top Viajes", command=self.report_top_travels, **button_style).pack(pady=5)
        # tk.Button(window, text="Top Ganancia", command=self.report_top_gains, **button_style).pack(pady=5)
        # tk.Button(window, text="Top Clientes", command=self.report_top_customers, **button_style).pack(pady=5)
        # tk.Button(window, text="Top Vehiculos", command=self.report_top_vehicles, **button_style).pack(pady=5)
        tk.Button(window, text="Ruta de Viaje", command=self.report_travel_route, **button_style).pack(pady=5)

    def report_travel_route(self):
        window = tk.Toplevel(self.root)
        window.title("Ruta de Viaje")
        window.geometry("500x400")
        window.configure(bg="#FFF0D1")

        tk.Label(window, text="Ruta de Viaje", font=("Arial", 18, "bold"), bg="#FFF0D1", fg="#3B3030").pack(pady=20)

        tk.Label(window, text="Ingresa la llave:", bg="#FFF0D1").pack(pady=5)
        origen_entry = tk.Entry(window, font=("Arial", 14))
        origen_entry.pack(pady=5)

        # Caja de texto para mostrar la ruta
        route_text = tk.Text(window, height=8, width=50, font=("Arial", 12), bg="#F4F4F4", fg="#3B3030")
        route_text.pack(pady=10)

        def show_route():
            try:
                llave = int(origen_entry.get())  # Convertir la entrada a entero
                ruta = gestor_viajes.obtener_ruta_por_id(llave)
                route_text.delete(1.0, tk.END)  # Limpiar texto anterior
                route_text.insert(tk.END, ruta)  # Insertar nueva ruta
            except ValueError:
                messagebox.showerror("Error", "La llave debe ser un número entero.")  # Manejar error si no es un entero

        tk.Button(window, text="Mostrar Ruta", command=show_route, font=("Arial", 14), bg="#795757", fg="white", activebackground="#664343").pack(pady=20)


    def open_entity_window(self, entity_name, vehicles=False, trips=False):
        window = tk.Toplevel(self.root)
        window.title(f"Gestión de {entity_name}")
        window.geometry("400x550")
        window.configure(bg="#FFF0D1")

        tk.Label(window, text=f"Gestión de {entity_name}", font=("Arial", 18, "bold"), bg="#FFF0D1", fg="#3B3030").pack(pady=20)

        button_style = {
            "font": ("Arial", 14),
            "bg": "#795757",
            "fg": "white",
            "activebackground": "#664343",
            "bd": 2,
            "relief": tk.RAISED,
            "highlightthickness": 0,
            "overrelief": tk.GROOVE,
            "width": 25,
            "height": 2
        }

        if not vehicles and not trips:
            tk.Button(window, text="Crear Cliente", command=self.create_customer, **button_style).pack(pady=5)
            tk.Button(window, text="Modificar", command=self.modify_customer, **button_style).pack(pady=5)
            tk.Button(window, text="Eliminar", command=self.delete_customer, **button_style).pack(pady=5)
            tk.Button(window, text="Mostrar Información", command=self.info_customer, **button_style).pack(pady=5)
            tk.Button(window, text="Mostrar Estructura de Datos", command=self.structure_customer, **button_style).pack(pady=5)

        if vehicles:
            tk.Button(window, text="Crear Vehículo", command=self.create_vehicle, **button_style).pack(pady=5)
            tk.Button(window, text="Modificar", command=self.modify_vehicle, **button_style).pack(pady=5)
            tk.Button(window, text="Eliminar", command=self.delete_vehicle, **button_style).pack(pady=5)
            tk.Button(window, text="Mostrar Información", command=self.info_vehicle, **button_style).pack(pady=5)
            tk.Button(window, text="Mostrar Estructura de Datos", command=self.structure_vehicle, **button_style).pack(pady=5)
        if trips:
            tk.Button(window, text="Crear Viaje", command=self.create_trip, **button_style).pack(pady=5)

        tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#C5705D", fg="white", activebackground="#d32f2f", bd=2, relief=tk.RAISED, width=25, height=2).pack(pady=20)


    # functions for customers
    def modify_customer(self):
        global lista_clientes

        if not lista_clientes.head: 
            messagebox.showinfo("Información", "La lista de clientes está vacía.")
            return

        # create a new window
        window = tk.Toplevel(self.root)
        window.title("Seleccionar Cliente para Modificar")
        window.geometry("500x400")
        window.configure(bg="#FFF0D1")

        # listbox for clients
        listbox = tk.Listbox(window, font=("Arial", 12), bg="#FFF8E1", width=50, height=10)
        listbox.pack(pady=20)

        # insert client into listbox
        actual = lista_clientes.head
        while True:
            cliente_info = f"{actual.cliente.getDPI()} - {actual.cliente.getNombre()} {actual.cliente.getApellido()}"
            listbox.insert(tk.END, cliente_info)

            actual = actual.siguiente
            if actual == lista_clientes.head:
                break

        # select client to modify
        def select_customer():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Información", "Seleccione un cliente.")
                return
            selected_cliente_str = listbox.get(selected_index)
            selected_dpi = selected_cliente_str.split(' - ')[0]  

            cliente = lista_clientes.buscar(selected_dpi)

            if cliente:
                open_edit_window(cliente)

        def open_edit_window(cliente):

            edit_window = tk.Toplevel(window)
            edit_window.title(f"Modificar Cliente: {cliente.getNombre()} {cliente.getApellido()}")
            edit_window.geometry("400x400")
            edit_window.configure(bg="#FFF0D1")

            tk.Label(edit_window, text="Nombre", bg="#FFF0D1").pack(pady=5)
            nombre_entry = tk.Entry(edit_window, font=("Arial", 12))
            nombre_entry.insert(tk.END, cliente.getNombre())
            nombre_entry.pack(pady=5)

            tk.Label(edit_window, text="Apellido", bg="#FFF0D1").pack(pady=5)
            apellido_entry = tk.Entry(edit_window, font=("Arial", 12))
            apellido_entry.insert(tk.END, cliente.getApellido())
            apellido_entry.pack(pady=5)

            tk.Label(edit_window, text="Género", bg="#FFF0D1").pack(pady=5)
            genero_entry = tk.Entry(edit_window, font=("Arial", 12))
            genero_entry.insert(tk.END, cliente.getGenero())
            genero_entry.pack(pady=5)

            tk.Label(edit_window, text="Teléfono", bg="#FFF0D1").pack(pady=5)
            telefono_entry = tk.Entry(edit_window, font=("Arial", 12))
            telefono_entry.insert(tk.END, cliente.getTelefono())
            telefono_entry.pack(pady=5)

            tk.Label(edit_window, text="Dirección", bg="#FFF0D1").pack(pady=5)
            direccion_entry = tk.Entry(edit_window, font=("Arial", 12))
            direccion_entry.insert(tk.END, cliente.getDireccion())
            direccion_entry.pack(pady=5)

            def save_changes():
                cliente.setNombre(nombre_entry.get())
                cliente.setApellido(apellido_entry.get())
                cliente.setGenero(genero_entry.get())
                cliente.setTelefono(telefono_entry.get())
                cliente.setDireccion(direccion_entry.get())

                messagebox.showinfo("Información", "Cliente actualizado con éxito.")
                edit_window.destroy()

            # save chanegs
            save_button = tk.Button(edit_window, text="Guardar Cambios", command=save_changes, font=("Arial", 14), bg="#795757", fg="white")
            save_button.pack(pady=20)

        # select client button
        select_button = tk.Button(window, text="Seleccionar Cliente", command=select_customer, font=("Arial", 14), bg="#795757", fg="white")
        select_button.pack(pady=20)

        
        close_button = tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#C5705D", fg="white")
        close_button.pack(pady=10)

    def delete_customer(self):

        if lista_clientes.head is None:
            messagebox.showinfo("Información", "La lista de clientes está vacía.")
            return

        
        window = tk.Toplevel(self.root)
        window.title("Eliminar Cliente")
        window.geometry("500x400")
        window.configure(bg="#FFF0D1")

        listbox = tk.Listbox(window, font=("Arial", 12), bg="#FFF8E1", width=50, height=10)
        listbox.pack(pady=20)

        # insert clients into listbox
        actual = lista_clientes.head
        while True:
            cliente_info = f"{actual.cliente.getDPI()} - {actual.cliente.getNombre()} {actual.cliente.getApellido()}"
            listbox.insert(tk.END, cliente_info)
            actual = actual.siguiente
            if actual == lista_clientes.head:
                break

        def delete_selected_customer():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Información", "Seleccione un cliente.")
                return

            selected_cliente_str = listbox.get(selected_index)
            selected_dpi = selected_cliente_str.split(' - ')[0]

            # delete cliente by dpi
            success = lista_clientes.eliminar_cliente_por_dpi(selected_dpi)
            lista_clientes.imprimir()

            if success:
                messagebox.showinfo("Información", f"Cliente con DPI {selected_dpi} eliminado correctamente.")
                window.destroy()  # close window after deleting
            else:
                messagebox.showinfo("Error", "No se encontró el cliente.")

        delete_button = tk.Button(window, text="Eliminar Cliente", command=delete_selected_customer, font=("Arial", 14), bg="#795757", fg="white")
        delete_button.pack(pady=20)

        close_button = tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#C5705D", fg="white")
        close_button.pack(pady=10)

    def info_customer(self):
        global lista_clientes
        self.contador = 1

        if lista_clientes.head is None:
            messagebox.showinfo("Información", "La lista de clientes está vacía.")
            return

        window = tk.Toplevel(self.root)
        window.title("Lista de Clientes")
        window.geometry("600x400")
        window.configure(bg="#FFF0D1")

        text_area = tk.Text(window, wrap=tk.WORD, font=("Arial", 12), bg="#FFF8E1")
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        actual = lista_clientes.head
        while True:
            cliente_info = f"""
            Cliente {self.contador}
            DPI: {actual.cliente.getDPI()}
            Nombre: {actual.cliente.getNombre()}
            Apellido: {actual.cliente.getApellido()}
            Género: {actual.cliente.getGenero()}
            Teléfono: {actual.cliente.getTelefono()}
            Dirección: {actual.cliente.getDireccion()}
            ----------------------------------------------------------------------------------
            """
            text_area.insert(tk.END, cliente_info)
            self.contador += 1

            actual = actual.siguiente
            if actual == lista_clientes.head:
                break

        text_area.config(state=tk.DISABLED)

    def structure_customer(self):
        global lista_clientes

        lista_clientes.estructura_cliente_graphviz()
        messagebox.showinfo("Estructura de Datos", "Estructura de clientes generada con éxito.")

    def modify_vehicle(self):
        global arbol_vehiculos

        if not arbol_vehiculos.raizPricipal.llave:
            messagebox.showinfo("Información", "No hay vehículos disponibles para modificar.")
            return

        window = tk.Toplevel(self.root)
        window.title("Seleccionar Vehículo para Modificar")
        window.geometry("500x400")
        window.configure(bg="#FFF0D1")

        listbox = tk.Listbox(window, font=("Arial", 12), bg="#FFF8E1", width=50, height=10)
        listbox.pack(pady=20)

        def cargar_vehiculos(nodo):
            for vehiculo in nodo.llave:
                vehiculo_info = f"{vehiculo.getPlaca()} - {vehiculo.getMarca()} {vehiculo.getModelo()}"
                listbox.insert(tk.END, vehiculo_info)
            for hijo in nodo.hijo:
                cargar_vehiculos(hijo)

        cargar_vehiculos(arbol_vehiculos.raizPricipal)

        def select_vehicle():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Información", "Seleccione un vehículo.")
                return
            selected_vehicle_str = listbox.get(selected_index)
            selected_placa = selected_vehicle_str.split(' - ')[0]  

            vehiculo = arbol_vehiculos.buscar_vehiculo(selected_placa)

            if vehiculo:
                open_edit_window(vehiculo)

        def open_edit_window(vehiculo):
            edit_window = tk.Toplevel(window)
            edit_window.title(f"Modificar Vehículo: {vehiculo.getPlaca()}")
            edit_window.geometry("400x400")
            edit_window.configure(bg="#FFF0D1")

            tk.Label(edit_window, text="Placa", bg="#FFF0D1").pack(pady=5)
            placa_entry = tk.Entry(edit_window, font=("Arial", 12))
            placa_entry.insert(tk.END, vehiculo.getPlaca())
            placa_entry.pack(pady=5)

            tk.Label(edit_window, text="Marca", bg="#FFF0D1").pack(pady=5)
            marca_entry = tk.Entry(edit_window, font=("Arial", 12))
            marca_entry.insert(tk.END, vehiculo.getMarca())
            marca_entry.pack(pady=5)

            tk.Label(edit_window, text="Modelo", bg="#FFF0D1").pack(pady=5)
            modelo_entry = tk.Entry(edit_window, font=("Arial", 12))
            modelo_entry.insert(tk.END, vehiculo.getModelo())
            modelo_entry.pack(pady=5)

            tk.Label(edit_window, text="Precio por Segundo", bg="#FFF0D1").pack(pady=5)
            precio_entry = tk.Entry(edit_window, font=("Arial", 12))
            precio_entry.insert(tk.END, vehiculo.getPrecioPorSegundo())
            precio_entry.pack(pady=5)

            def save_changes():
                vehiculo.setPlaca(placa_entry.get())
                vehiculo.setMarca(marca_entry.get())
                vehiculo.setModelo(modelo_entry.get())
                vehiculo.setPrecioPorSegundo(precio_entry.get())

                messagebox.showinfo("Información", "Vehículo actualizado con éxito.")
                edit_window.destroy()

            save_button = tk.Button(edit_window, text="Guardar Cambios", command=save_changes, font=("Arial", 14), bg="#795757", fg="white")
            save_button.pack(pady=20)

        select_button = tk.Button(window, text="Seleccionar Vehículo", command=select_vehicle, font=("Arial", 14), bg="#795757", fg="white")
        select_button.pack(pady=20)

        close_button = tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#C5705D", fg="white")
        close_button.pack(pady=10)

    def delete_vehicle(self):
        global arbol_vehiculos

        if not arbol_vehiculos.raizPricipal.llave:
            messagebox.showinfo("Información", "No hay vehículos disponibles para eliminar.")
            return

        window = tk.Toplevel(self.root)
        window.title("Eliminar Vehículo")
        window.geometry("500x400")
        window.configure(bg="#FFF0D1")

        listbox = tk.Listbox(window, font=("Arial", 12), bg="#FFF8E1", width=50, height=10)
        listbox.pack(pady=20)

        def cargar_vehiculos(nodo):
            for vehiculo in nodo.llave:
                vehiculo_info = f"{vehiculo.getPlaca()} - {vehiculo.getMarca()} {vehiculo.getModelo()}"
                listbox.insert(tk.END, vehiculo_info)
            for hijo in nodo.hijo:
                cargar_vehiculos(hijo)

        cargar_vehiculos(arbol_vehiculos.raizPricipal)

        def delete_selected_vehicle():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Información", "Seleccione un vehículo.")
                return

            selected_vehicle_str = listbox.get(selected_index)
            selected_placa = selected_vehicle_str.split(' - ')[0] 

            success = arbol_vehiculos.eliminar_vehiculo_por_placa(selected_placa)

            if success:
                messagebox.showinfo("Información", f"Vehículo con placa {selected_placa} eliminado correctamente.")
                window.destroy() 
            else:
                messagebox.showinfo("Error", "No se encontró el vehículo.")

        delete_button = tk.Button(window, text="Eliminar Vehículo", command=delete_selected_vehicle, font=("Arial", 14), bg="#795757", fg="white")
        delete_button.pack(pady=20)

        close_button = tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#C5705D", fg="white")
        close_button.pack(pady=10)


    def info_vehicle(self):
        global arbol_vehiculos
        self.contador = 1

        if not arbol_vehiculos.raizPricipal.llave:
            messagebox.showinfo("Información", "El árbol de vehículos está vacío.")
            return

        window = tk.Toplevel(self.root)
        window.title("Lista de Vehículos")
        window.geometry("600x400")
        window.configure(bg="#FFF0D1")

        text_area = tk.Text(window, wrap=tk.WORD, font=("Arial", 12), bg="#FFF8E1")
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def recorrer_arbol(nodo):
            
            for vehiculo in nodo.llave:
                vehiculo_info = f"""
                Vehiculo {self.contador}
                Placa: {vehiculo.getPlaca()}
                Marca: {vehiculo.getMarca()}
                Modelo: {vehiculo.getModelo()}
                Precio por segundo: Q. {vehiculo.getPrecioPorSegundo()} .00
                ----------------------------------------------------------------------------------
                """
                text_area.insert(tk.END, vehiculo_info)
                self.contador += 1
            
            

            for hijo in nodo.hijo:
                recorrer_arbol(hijo)

        recorrer_arbol(arbol_vehiculos.raizPricipal)
        text_area.config(state=tk.DISABLED)
    
    def structure_vehicle(self):
        global arbol_vehiculos

        arbol_vehiculos.imprimir_grafica()
        messagebox.showinfo("Estructura de Datos", "Estructura de vehículos generada con éxito.")


    def create_customer(self):
        window = tk.Toplevel(self.root)
        window.title("Crear Cliente")
        window.geometry("400x650")
        window.configure(bg="#e3f2fd")

        tk.Label(window, text="Crear Cliente", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

        tk.Label(window, text="DPI:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        dpi_entry = tk.Entry(window, font=("Arial", 14))
        dpi_entry.pack(pady=5)

        tk.Label(window, text="Nombres:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        nombres_entry = tk.Entry(window, font=("Arial", 14))
        nombres_entry.pack(pady=5)

        tk.Label(window, text="Apellidos:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        apellidos_entry = tk.Entry(window, font=("Arial", 14))
        apellidos_entry.pack(pady=5)

        tk.Label(window, text="Género:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        genero_entry = tk.Entry(window, font=("Arial", 14))
        genero_entry.pack(pady=5)

        tk.Label(window, text="Teléfono:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        telefono_entry = tk.Entry(window, font=("Arial", 14))
        telefono_entry.pack(pady=5)

        tk.Label(window, text="Dirección:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        direccion_entry = tk.Entry(window, font=("Arial", 14))
        direccion_entry.pack(pady=5)

        def create_client():
            dpi = dpi_entry.get()
            nombres = nombres_entry.get()
            apellidos = apellidos_entry.get()
            genero = genero_entry.get()
            telefono = telefono_entry.get()
            direccion = direccion_entry.get()

            if dpi and nombres and apellidos and genero and telefono and direccion:
                cliente = Cliente(dpi, nombres, apellidos, genero, telefono, direccion)
                lista_clientes.insertar(cliente)
                messagebox.showinfo("Cliente Creado", f"Cliente creado con éxito: {cliente.nombre} {cliente.apellido}")
                window.destroy()
            else:
                messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")

        tk.Button(window, text="Crear Cliente", command=create_client, font=("Arial", 14), bg="#1976d2", fg="white", activebackground="#0d47a1", bd=2, relief=tk.RAISED).pack(pady=20)

        tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", bd=2, relief=tk.RAISED).pack(pady=20)

    def create_vehicle(self):
        window = tk.Toplevel(self.root)
        window.title("Crear Vehículo")
        window.geometry("400x600")
        window.configure(bg="#e3f2fd")

        tk.Label(window, text="Crear Vehículo", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

        tk.Label(window, text="Placa:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        placa_entry = tk.Entry(window, font=("Arial", 14))
        placa_entry.pack(pady=5)

        tk.Label(window, text="Marca:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        marca_entry = tk.Entry(window, font=("Arial", 14))
        marca_entry.pack(pady=5)

        tk.Label(window, text="Modelo:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        modelo_entry = tk.Entry(window, font=("Arial", 14))
        modelo_entry.pack(pady=5)

        tk.Label(window, text="Precio por Segundo:", bg="#e3f2fd", fg="#0d47a1").pack(pady=5)
        precio_entry = tk.Entry(window, font=("Arial", 14))
        precio_entry.pack(pady=5)

        def create_vehicle():
            placa = placa_entry.get()
            marca = marca_entry.get()
            modelo = modelo_entry.get()
            precio = precio_entry.get()

            if placa and marca and modelo and precio:
                vehiculo = Vehiculo(placa, marca, modelo, precio)
                arbol_vehiculos.insertar_vehiculo(vehiculo)
                messagebox.showinfo("Vehículo Creado", f"Vehículo creado con éxito: {vehiculo.marca} {vehiculo.modelo}")
                window.destroy()
            else:
                messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")

        tk.Button(window, text="Crear Vehículo", command=create_vehicle, font=("Arial", 14), bg="#1976d2", fg="white", activebackground="#0d47a1", bd=2, relief=tk.RAISED).pack(pady=20)

        tk.Button(window, text="Cerrar", command=window.destroy, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", bd=2, relief=tk.RAISED).pack(pady=20)

    def create_trip(self):

        def crear_viaje():
            cliente_dpi = entry_cliente_dpi.get()
            placa_vehiculo = entry_placa_vehiculo.get()
            origen = entry_origen.get()
            destino = entry_destino.get()
            fecha_hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not cliente_dpi or not placa_vehiculo or not origen or not destino:
                messagebox.showerror("Error", "Todos los campos deben ser llenados")
                return

            # Llamada al gestor de viajes para crear el viaje
            gestor_viajes.crear_viaje(cliente_dpi, placa_vehiculo, origen, destino, fecha_hora_inicio)
            print(f"Viaje creado con los siguientes datos:\nDPI: {cliente_dpi}\nPlaca: {placa_vehiculo}\nOrigen: {origen}\nDestino: {destino}\nFecha y Hora: {fecha_hora_inicio} ")

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Viaje creado exitosamente.")

        # Crear la ventana principal de tkinter
        ventana = tk.Tk()
        ventana.title("Formulario de Viaje")
        ventana.geometry("400x300")
        ventana.configure(bg="#F1F1F1")  # Fondo suave para la ventana

        # Título con una fuente agradable
        title_label = tk.Label(ventana, text="Formulario de Viaje", font=("Arial", 18, "bold"), bg="#F1F1F1", fg="#4A4A4A")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiquetas y campos de texto con margen y centrado
        tk.Label(ventana, text="Cliente DPI:", font=("Arial", 12), bg="#F1F1F1").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_cliente_dpi = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
        entry_cliente_dpi.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Placa Vehículo:", font=("Arial", 12), bg="#F1F1F1").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_placa_vehiculo = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
        entry_placa_vehiculo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Origen:", font=("Arial", 12), bg="#F1F1F1").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        entry_origen = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
        entry_origen.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Destino:", font=("Arial", 12), bg="#F1F1F1").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_destino = tk.Entry(ventana, font=("Arial", 12), bd=2, relief="solid")
        entry_destino.grid(row=4, column=1, padx=10, pady=5)

        # Botón con color de fondo y texto personalizado
        crear_button = tk.Button(ventana, text="Crear Viaje", font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#45a049", command=crear_viaje)
        crear_button.grid(row=5, columnspan=2, pady=20)

        # Iniciar la ventana
        ventana.mainloop()

        # gestor_viajes.crear_viaje(cliente_dpi, placa_vehiculo, origen, destino, fecha_hora_inicio)
        # print(gestor_viajes.obtener_ruta_por_id(1))

if __name__ == "__main__":
    root = tk.Tk()
    # available_fonts = list(font.families())
    # print("Fuentes disponibles:", available_fonts)
    app = TransportApp(root)
    root.mainloop()
    # Crear el gestor de viajes
    

    # Agregar datos de prueba
    # cliente = Cliente("3060396800308", "CARLOS", "LOPEZ", "M", "34567890", "Dirección 1")
    # lista_clientes.insertar(cliente)
    # vehiculo = Vehiculo("765MCR", "Toyota", "Corolla", 28500)
    # arbol_vehiculos.insertar_vehiculo(vehiculo)
    # grafo_rutas.agregar_ruta("Oviedo", "Bilbao", 304)
    # grafo_rutas.agregar_ruta("Bilbao", "Zaragoza", 324)


    # # Crear un viaje con una fecha y hora específicas
    # fecha_hora_inicio = "2024-12-30 14:00:00"
    # gestor_viajes.crear_viaje("3060396800308", "765MCR", "Oviedo", "Zaragoza", fecha_hora_inicio)
    # print(gestor_viajes.obtener_ruta_por_id(1))
