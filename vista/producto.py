import tkinter as tk
from tkinter import ttk, messagebox
from logica.producto import ProductoLogica
from modelo.producto import ProductoModel

class ProductoVista(tk.Tk):

    def __init__(self):
        super().__init__() # Llamar el constructor del padre

        self.__logica = ProductoLogica()

        self.geometry("640x480")
        self.title("Productos en U-Coltis")
        self.iconbitmap("coltis.ico")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        izquierda = tk.Frame(self)
        self.__construir_frame_izquierdo(izquierda)
        izquierda.grid(column=0, row=0)

        derecha = tk.Frame(self)
        self.__construir_frame_derecho(derecha)
        derecha.grid(column=1, row=0)

        self.__cargar_tabla()

    def __construir_frame_izquierdo(self, frame: tk.Frame):
        self.__tabla = ttk.Treeview(frame)
        self.__tabla.grid(column=0, row=0, columnspan=2)
        self.__tabla['columns'] = ('Código', 'Nombre', 'Precio')

        self.__tabla.heading('#0',text="", anchor=tk.CENTER)
        self.__tabla.heading('Código', text="Código", anchor=tk.CENTER)
        self.__tabla.heading('Nombre', text="Nombre", anchor=tk.CENTER)
        self.__tabla.heading('Precio', text="Precio", anchor=tk.CENTER)

        self.__tabla.column('#0', width=0, stretch=tk.NO)
        self.__tabla.column('Código', anchor=tk.E, width=80)
        self.__tabla.column('Nombre', anchor=tk.W, width=250)
        self.__tabla.column('Precio', anchor=tk.E, width=80)

        def seleccionar_elemento(event):
                for item_selected in self.__tabla.selection():
                    item = self.__tabla.item(item_selected)
                    self.__codigo.set(item['values'][0])
                    self.__nombre.set(item['values'][1])
                    self.__precio.set(item['values'][2])

        self.__tabla.bind('<<TreeviewSelect>>', seleccionar_elemento)

        def nuevo():
            #TODO Limpiar la seleccion de la tabla
            self.__codigo.set(0)
            self.__nombre.set("")
            self.__precio.set(0.0)

        def eliminar():
            opcion = messagebox.askquestion('Eliminar producto', '¿Esta seguro en eliminar este producto?')
            if opcion == 'yes':
                # TODO Seleccionar el codigo del elemento seleccionado en la tabla
                codigo = int(self.__codigo.get())

                # Enviar a eliminar el producto con ese id
                self.__logica.eliminar(codigo)
                messagebox.showinfo("Eliminar producto", "Se eliminó de forma existosa")

                self.__cargar_tabla()


        boton1 = ttk.Button(frame, text="Nuevo", command=nuevo)
        boton1.grid(column=0, row=1)

        boton2 = ttk.Button(frame, text="Eliminar", command=eliminar)
        boton2.grid(column=1, row=1)

    def __construir_frame_derecho(self, frame):

        ttk.Label(frame, text="Datos del producto").grid(column=0, row=0, columnspan=2)

        ttk.Label(frame, text="Código").grid(column=0, row=1)
        self.__codigo = tk.IntVar(); 
        ttk.Entry(frame, textvariable=self.__codigo).grid(column=1, row=1)

        ttk.Label(frame, text="Nombre").grid(column=0, row=2)
        self.__nombre = tk.StringVar(); 
        ttk.Entry(frame, textvariable=self.__nombre).grid(column=1, row=2)

        ttk.Label(frame, text="Precio").grid(column=0, row=3)
        self.__precio = tk.DoubleVar(); 
        ttk.Entry(frame, textvariable=self.__precio).grid(column=1, row=3, sticky=tk.E)

        def insertar():
            # TODO Validar los campos llenos
            producto = ProductoModel()
            producto.set_nombre(self.__nombre.get())
            producto.set_precio(self.__precio.get())

            try:
                # Envio a guardar a la base de datos
                self.__logica.insertar(producto)
                self.__cargar_tabla()

                messagebox.showinfo("Guardado de producto", "Se guardó de forma existosa")
            except Exception as ex:
                messagebox.showerror("Error guardando el producto", str(ex))

        ttk.Button(frame, text="Ingresar", command=insertar).grid(column=0,row=4)

        def actualizar():
            # TODO Validar los campos llenos
            producto = ProductoModel()
            producto.set_codigo(self.__codigo.get())
            producto.set_nombre(self.__nombre.get())
            producto.set_precio(self.__precio.get())

            try:
                # Envio a guardar a la base de datos
                self.__logica.actualizar(producto)
                self.__cargar_tabla()

                messagebox.showinfo("Actualizar de producto", "Se actualizó de forma existosa")
            except:
                messagebox.showerror("Actualizar de producto", "Error al actualizar el producto")

        ttk.Button(frame, text="Actualizar", command=actualizar).grid(column=1,row=4)

    def __cargar_tabla(self):
        productos = self.__logica.listar()

        # Eliminar los valores anteriores
        for item in self.__tabla.get_children(""):
            self.__tabla.delete(item)

        for producto in productos:
            identificador = producto.get_codigo()
            self.__tabla.insert(parent='', index=identificador, iid=identificador, text="",
                values=(identificador, producto.get_nombre(), producto.get_precio()))


    def iniciar_ejecucion(self):
        self.mainloop()