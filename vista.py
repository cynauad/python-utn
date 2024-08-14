"""
vista.py:
    En el patron MVC, esta clase es la Vista con interfaz gráfica realizada en Tkinter

    -	Contiene el menú superior desplegable.
    -	Botones con las opciones de Alta, Baja, Modificar y Buscar.
    -	Visualización de la base de datos en formato tabla (treeview).
    -	Toma la solicitud de usuario y ejecuta la acción correspondiente.
    -   Consulta al modelo y disponibiliza la información.
    -   Implementa el patron observador para informar cambios en Alta y Baja

"""

from tkinter import LabelFrame, Label, StringVar, Entry, Frame, Button
from tkinter import Menu, Spinbox
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showwarning, askyesno, showerror
from tkcalendar import DateEntry
import os
from valid import Validation
from model import Abmc
from observador_vista import SujetoV
from observador_model import ConcreteObserverMetodo
import threading
import server


# ##############################################
#        VISTA
# ##############################################

# VARIABLES GLOBALES
mi_id = ""
theproc = ""


class Vista(SujetoV):
    def __init__(self, window):    # todo sucede dentro del constructor
        """
        Configuración de la interfaz gráfica con Tkinter.
        Se generan labels y entrys para el ingreso de datos.
        Buttons que generan la accion de alta, baja, modificación y consulta.
        Finalmente el treeview para mostrar la informacion almacenada.
        """

        self.master = window
        # self.objeto_con = Abmc("SQLite3")

        base_dir = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(base_dir, "icono.ico")
        # print(ruta)

        self.master.title("CRUD para Agenda de Eventos Quirúrgicos")
        self.master.iconbitmap(ruta)
        # master.iconbitmap('icono.ico')

        # ----  Frame para SELECCION DE DDBB  --------------------------
        self.sel_db = LabelFrame(self.master)
        self.sel_db.config(borderwidth=0,
                           relief="flat")  # quito los bordes del frame
        self.sel_db.pack(padx=5, pady=5)  # uso pack

        self.select_base = Label(self.sel_db,
                                 text='Seleccione la base de datos >>',
                                 background="#7FFFD4")
        self.select_base.pack(side="left", padx=5)

        self.opciones = ['SQLite3', 'PostgreSQL']
        self.combobox = ttk.Combobox(self.sel_db, state="readonly",
                                     values=self.opciones)
        # self.combobox.current(0)
        self.combobox.pack(side="left", padx=5)

        # Vincular el evento de selección del combobox a la función
        # obtener_seleccion
        self.combobox.bind("<<ComboboxSelected>>", self.obtener_seleccion)

        # ----  Frame para la entrada de datos  --------------------------
        ''' Utilizo pack para definir los frames y luego grid dentro de cada
        frame para ubicar las cajas entry y botones'''
        self.frame_grilla = LabelFrame(self.master, text='Formulario',
                                       padx=5, pady=5)
        self.frame_grilla.pack(padx=5, pady=5)  # uso pack

        # nombre, centrado, color del texto, color de fondo
        self.ingreso_datos = Label(
            self.frame_grilla, text="Ingrese sus datos:", anchor="center",
            fg="#ffffff", background="#A569BD")
        self.ingreso_datos.grid(row=0, column=0, columnspan=5, sticky="nswe")
        # centrado en todas las direcciones

        self.id_pac = Label(self.frame_grilla,
                            text="ID Paciente", width=20, anchor='w')
        self.id_pac.grid(row=1, column=0, sticky='w')
        self.name = Label(self.frame_grilla,
                          text="Nombre y Apellido", width=20, anchor='w')
        self.name.grid(row=2, column=0, sticky='w')
        self.surgeon = Label(self.frame_grilla,
                             text="Cirujano", width=20, anchor='w')
        self.surgeon.grid(row=3, column=0, sticky='w')
        self.procedure = Label(self.frame_grilla,
                               text="Procedimiento", width=20, anchor='w')
        self.procedure.grid(row=4, column=0, sticky='w')
        self.date = Label(self.frame_grilla,
                          text="Fecha", width=15, anchor='w')
        self.date.grid(row=1, column=2, sticky='w')
        self.hour = Label(self.frame_grilla,
                          text="Horario [h:m]", width=15, anchor='w')
        self.hour.grid(row=2, column=2, sticky='w')
        self.duration = Label(self.frame_grilla,
                              text="Duracion [min]", width=15, anchor='w')
        self.duration.grid(row=3, column=2, sticky='w')

        # ------------VARIABLES---------------------------------------
        self.var_id_pac = StringVar()
        self.var_name = StringVar()
        self.var_procedure = StringVar()
        self.var_surgeon = StringVar()
        self.var_date = StringVar()
        self.var_hour_ = StringVar()
        self.var_min = StringVar()
        self.var_duration = StringVar()  # minutes

        self.var_id_pac.set("")   # aparecian con un 0
        # ----------------------------------------------------------

        self.entry_id = Entry(self.frame_grilla,
                              textvariable=self.var_id_pac, width=30)
        self.entry_id.grid(row=1, column=1)
        self.entry_name = Entry(self.frame_grilla,
                                textvariable=self.var_name, width=30)
        self.entry_name.grid(row=2, column=1)
        self.entry_surgeon = Entry(self.frame_grilla,
                                   textvariable=self.var_surgeon, width=30)
        self.entry_surgeon.grid(row=3, column=1)
        self.entry_procedure = Entry(self.frame_grilla,
                                     textvariable=self.var_procedure, width=30)
        self.entry_procedure.grid(row=4, column=1)
        self.entry_date = DateEntry(self.frame_grilla, selectmode='day',
                                    date_pattern="dd/mm/yyyy",
                                    textvariable=self.var_date, width=12)
        self.entry_date.grid(row=1, column=3)
        # self.entry_hour = Entry(self.frame_grilla,
        #                         textvariable=self.var_hour, width=20)
        # self.entry_hour.grid(row=2, column=3)
        self.frame_grilla3 = Frame(self.frame_grilla)
        self.frame_grilla3.grid(row=2, column=3)
        self.entry_hour = Spinbox(self.frame_grilla3, from_=0, to=23,
                                  wrap=True, textvariable=self.var_hour_,
                                  width=5)
        self.entry_hour.grid(row=0, column=0)
        self.entry_min = Spinbox(self.frame_grilla3, from_=0, to=59,
                                 wrap=True, textvariable=self.var_min,
                                 width=5)
        self.entry_min.grid(row=0, column=1)
        self.entry_duration = Entry(self.frame_grilla,
                                    textvariable=self.var_duration, width=15)
        self.entry_duration.grid(row=3, column=3)

        self.entrys = [self.entry_id, self.entry_name, self.entry_surgeon,
                       self.entry_procedure, self.entry_date, self.entry_hour,
                       self.entry_min, self.entry_duration]
        # ----- otro frame para separar botones
        self.frame_grilla2 = Frame(self.master)
        self.frame_grilla2.pack(padx=5, pady=5)

        # ------------ Línea divisoria ---------------
        self.separator = Frame(self.master, height=2, bd=1, relief='sunken')
        self.separator.pack(fill="x", padx=5, pady=5)
        # ----------------------------------------------------------

        # Crear el Frame para el Treeview
        self.frame_treeview = Frame(self.master)
        self.frame_treeview.pack(fill='both', expand=True)

        # difino el treeview  --> es una tabla
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5",
                                "col6", "col7", "col8")
        # lista de columnas
        self.tree.column("#0", width=70, minwidth=70, anchor='w')
        self.tree.column("col1", width=70, minwidth=70, anchor='w')
        self.tree.column("col2", width=150, minwidth=150, anchor='w')
        self.tree.column("col3", width=150, minwidth=150, anchor='w')
        self.tree.column("col4", width=200, minwidth=200, anchor='w')
        self.tree.column("col5", width=70, minwidth=70, anchor='w')
        self.tree.column("col6", width=70, minwidth=70, anchor='w')
        self.tree.column("col7", width=70, minwidth=70, anchor='w')
        self.tree.column("col8", width=200, minwidth=200, anchor='w')

        # Agregar encabezados a las columnas
        self.tree.heading("#0", text="ID cirugia", anchor='center')
        self.tree.heading("col1", text="ID paciente", anchor='center')
        self.tree.heading("col2", text="Nombre", anchor='center')
        self.tree.heading("col3", text="Cirujano", anchor='center')
        self.tree.heading("col4", text="Procedimiento", anchor='center')
        self.tree.heading("col5", text="Fecha", anchor='center')
        self.tree.heading("col6", text="Horario", anchor='center')
        self.tree.heading("col7", text="Duracion", anchor='center')
        self.tree.heading("col8", text="Descripcion", anchor='center')

        # aca digo donde lo voy a motrar, en que posicion
        # tree.grid(row=6, column=0, columnspan=4)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # ------------- botones dentro de alta ----------------
        self.boton_alta = Button(self.frame_grilla,
                                 text="Alta",
                                 command=lambda:
                                 self.vista_alta(self.var_id_pac,
                                                 self.var_name,
                                                 self.var_surgeon,
                                                 self.var_procedure,
                                                 self.var_date,
                                                 self.var_hour_,
                                                 self.var_min,
                                                 self.var_duration,
                                                 self.tree),
                                 width=10)
        self.boton_alta.grid(row=1, column=4, padx=15)
        self.boton_alta['state'] = "disable"

        self.boton_cancel = Button(self.frame_grilla, text="Cancelar",
                                   width=10,
                                   command=lambda: self.cancelar(self.entrys))
        self.boton_cancel.grid(row=4, column=4, padx=15)
        self.boton_cancel['state'] = "disable"

        # ------------Botones otra grilla ---------
        self.boton_borrar = Button(self.frame_grilla2, text="Baja",
                                   width=10,
                                   command=lambda:
                                   self.vista_borrar(self.tree,
                                                     self.var_id_pac))
        self.boton_borrar.grid(row=1, column=0, padx=10, pady=5)
        self.boton_borrar['state'] = "disable"

        self.boton_edit = Button(self.frame_grilla2, text="Modificar",
                                 command=lambda:
                                 self.vista_modificar(self.tree,
                                                      self.entrys),  width=10)
        self.boton_edit.grid(row=1, column=1, padx=10, pady=5)
        self.boton_edit['state'] = "disable"

        self.boton_buscar = Button(self.frame_grilla2, text="Buscar", width=10,
                                   command=lambda:
                                   self.vista_consulta(self.var_id_pac,
                                                       self.tree))
        self.boton_buscar.grid(row=1, column=2, padx=10, pady=5)
        self.boton_buscar['state'] = "disable"

        self.boton_mostrar = Button(self.frame_grilla2, text="Mostrar todo",
                                    width=10,
                                    command=lambda:
                                    self.actualizar_treeview(self.tree))
        self.boton_mostrar.grid(row=1, column=3, padx=10, pady=5)
        self.boton_mostrar['state'] = "disable"

        # El siguiente boton solo se habilita si presiono Modificar
        self.boton_save = Button(self.frame_grilla, text="Guardar", width=10,
                                 command=lambda:
                                 self.vista_guardar(
                                     self.var_id_pac, self.var_name,
                                     self.var_surgeon, self.var_procedure,
                                     self.var_date, self.var_hour_,
                                     self.var_min, self.var_duration,
                                     self.tree, self.entrys))
        self.boton_save.grid(row=2, column=4, padx=15)
        self.boton_save.grid_forget()  # lo oculto
        # ------------ MENU ---------------------------------------
        self.menubar = Menu(self.master)

        self.menu_archivo = Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(label="Mostar tabla",
                                      command=lambda: self.actualizar_treeview(
                                          self.tree))
        self.menu_archivo.add_command(label="Exportar base",
                                      command=self.vista_export)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.master.quit)
        # estos en Archivo
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        self.menu_config = Menu(self.menubar, tearoff=0)
        self.menu_config.add_command(label="Color fondo", command=self.color)
        # estos en Configurar
        self.menubar.add_cascade(label="Configuracion", menu=self.menu_config)

        self.menu_srv = Menu(self.menubar, tearoff=0)
        self.menu_srv.add_command(label="Iniciar SRV", command=self.try_connection)
        self.menu_srv.add_command(label="Stop SRV", command=self.stop_server)
        # estos en Servidor
        self.menubar.add_cascade(label="Servidor", menu=self.menu_srv)

        self.master.config(menu=self.menubar)  # muestra el menu dise;ado
        # ----------------------------------------------------------
        # Al ejecutar el programa, consulto la BBDD y actualizo treeview
        # self.actualizar_treeview(self.tree)

    def try_connection(self, ):
        if theproc != "":
            theproc.kill()
            threading.Thread(target=server.lanzar_server, daemon=True).start()
        else:
            threading.Thread(target=server.lanzar_server, daemon=True).start()

    def stop_server(self, ):
        global theproc
        if theproc != "":
            theproc.kill()
        print("El servidor esta apagado")

    def obtener_seleccion(self, event):
        """
        Acción del combobox:

        - Captura la selección de la base de datos con la que se quiere trabajar

        :selección: Se puede elegir entre <Sqlite3> y <Postgres>.
        """
        self.seleccion = self.combobox.get()  # capturar el valor del combobox
        print(self.seleccion)
        if self.seleccion == "SQLite3":
            # Conectar a SQLite
            database = "SQLite3"
            self.objeto_con = Abmc(database)
            # select_database(database)
            print("Conectado a SQLite")
        elif self.seleccion == "PostgreSQL":
            # Conectar a PostgreSQL
            database = "PostgreSQL"
            self.objeto_con = Abmc(database)
            print("Conectado a PostgreSQL")
        else:
            print("Error: Base de datos no válida")
        # self.objeto_con = Abmc(database)
        self.notificar(database)
        self.boton_alta['state'] = "normal"
        self.boton_cancel['state'] = "normal"
        self.boton_edit['state'] = "normal"
        self.boton_buscar['state'] = "normal"
        self.boton_mostrar['state'] = "normal"
        self.boton_borrar['state'] = "normal"
        self.objeto_observador_metodo = ConcreteObserverMetodo(self.objeto_con)
        self.actualizar_treeview(self.tree)

    def color(self,):
        """Permite seleccionar y cambiar el color de fondo de la aplicación"""
        color_fondo = askcolor(color="#00ff00",
                               title="Seleccione un color de fondo")
        self.configure(background=color_fondo[1])

    def actualizar_treeview(self, treeview):
        """Permite la consulta a la BBDD y actualiza la tabla, mostrando toda la
        información almacenada"""
        self.limpiar_treeview(treeview)

        resultado = self.objeto_con.update_tree()
        for fila in resultado:  # print(fila)
            treeview.insert("", 0, text=fila.id_cx,
                            values=(fila.id_pac, fila.name, fila.surgeon,
                                    fila.procedure, fila.date, fila.hour,
                                    fila.duration, fila))

    def limpiar_treeview(self, treeview):
        """Limpia todos los elementos de la tabla"""
        for i in treeview.get_children():
            treeview.delete(i)

    def limpiar_entry(self, entrys):
        """Limpia/borra el contenido de los entrys"""
        entrys[0].delete(0, 'end')     # si tiene algo lo borro
        entrys[1].delete(0, 'end')
        entrys[2].delete(0, 'end')
        entrys[3].delete(0, 'end')
        entrys[4].delete(0, 'end')
        entrys[5].delete(0, 'end')
        entrys[6].delete(0, 'end')
        entrys[7].delete(0, 'end')

    def vista_alta(self, id_pac, name, surgeon, procedure, date, hour_, min,
                   duration, tree,):
        '''Acción del botón "Alta":

            - Captura la informacion ingresada en los entrys.
            - Llama a la funcion de validación de algunos campos obligatorios.
            - Llama a la funcion que guarda los elementos en la tabla.
            - Finalmente, muestra la tabla actualizada'''
        hour = hour_.get()+":"+min.get()
        dato = (id_pac.get(), name.get(), surgeon.get(),
                procedure.get(), date.get(), hour, duration.get())
        dni = id_pac.get()
        nombre = name.get()
        medico = surgeon.get()
        self.numero = Validation()
        self.texto = Validation()
        if self.numero.valid_numero(dni) is False:
            showwarning("ERROR", """Debe completar el campo ID Paciente.\n
                        Solo se permiten numeros""")
        elif self.texto.valid_text(nombre) is False:
            showwarning("ERROR", '''El campo "Nombre y Apellido" no puede
                         contener\nnúmeros ni caracteres especiales''')
        elif self.texto.valid_text(medico) is False:
            showwarning("ERROR", '''El campo "Cirujano" no puede contener
                        \nnúmeros ni caracteres especiales''')
        else:
            self.objeto_con.alta(dato)
            self.actualizar_treeview(tree)
            showinfo("REGISTRO CORRECTO",
                     "Registro de cirugia realizado correctamente")
            id_pac.set("")
            name.set("")
            procedure.set("")
            surgeon.set("")
            date.set("")
            hour_.set("")
            min.set("")
            duration.set("")

    def vista_borrar(self, tree, var_id_pac):
        '''Acción del botón "Baja":

            - Obtiene el elemento seleccionado del treeview, su id.
            - Llama a la funcion de borrar de la BBDD
            - Finalmente, muestra la tabla actualizada'''
        try:
            valor = tree.selection()  # obtengo seleccion del treeview
            item = tree.item(valor)
            print(item["text"])
            mi_id = item["text"]
            # print(type(mi_id))
            if askyesno("Eliminar", "Desea eliminar el registro?"):
                showinfo("Si", "Se ha eliminado la cirugia programada")
                self.objeto_con.borrar(mi_id)
                tree.delete(valor)
                var_id_pac.set("")
                # si NO -> no hago nada
        except Exception:
            showwarning("ERROR", "Debe seleccionar un elemento a borrar")

    def vista_consulta(self, var_id_pac, tree):
        '''Acción del botón "Buscar":

            - Se selecciona un elemento del treeview y se realiza la búsqueda.
            - Llama a la funcion de consulta de la BBDD.
            - Mediante el manejo de excepciones, si el registro fue encontrado, actualiza el treeview, sino muestra un mensaje de error.'''
        try:
            id_pac = int(var_id_pac.get())
            print(id_pac, type(id_pac))
            # data = (id_pac,)
            # print(data)
            try:
                resultado = self.objeto_con.consulta(id_pac)
            # if resultado:
                print(resultado)
                self.limpiar_treeview(tree)
                tree.insert("", 0, text=resultado.id_cx,
                            values=(resultado.id_pac, resultado.name,
                                    resultado.surgeon, resultado.procedure,
                                    resultado.date, resultado.hour,
                                    resultado.duration))
            except Exception:
                showwarning("Consulta", f"No se encuentra el ID: {id_pac}")
                var_id_pac.set("")
        except ValueError:
            showwarning("Error", "No se ha seleccionado ningun ID Paciente")

    def cancelar(self, entrys):
        '''Acción del botón "Cancelar":

            - Mensaje de consulta
            - Resetea los entrys y los botones que se hayan ocultado
            '''
        if askyesno("Cancelar", "Desea cancelar?"):
            showinfo("Si", "No se realizo ningun cambio")
            entrys[0].delete(0, 'end')     # si tiene algo lo borro
            entrys[1].delete(0, 'end')
            entrys[2].delete(0, 'end')
            entrys[3].delete(0, 'end')
            entrys[4].delete(0, 'end')
            entrys[5].delete(0, 'end')
            entrys[6].delete(0, 'end')
            entrys[7].delete(0, 'end')
            self.boton_alta['state'] = "normal"
            self.boton_borrar['state'] = "normal"
            self.boton_edit['state'] = "normal"
            self.boton_save.grid_forget()  # lo oculto

    def vista_modificar(self, tree, entrys):
        '''Acción del botón "Modificar":

            - Se selecciona un elemento y captura el contenido
            - Completa los entrys para realizar modificaciones
            - Se bloquean algunos botones y se habilita el boton "Guardar
            - Mediante el manejo de excepciones se intenta guardar, sino muestra mensaje de error"'''
        # En esta funcion leo el evento seleccionado
        valor = tree.selection()  # obtengo seleccion del treeview
        item = tree.item(valor)
        global mi_id
        mi_id = item["text"]
        mi_column = item["values"]   # lista de registro seleccionado
        print(mi_column)
        # if mi_id == '':                  # verifico que haya una seleccion
        #     showwarning("Modificar",
        #                 "Debe seleccionar un elemento en la tabla.")
        # else:
        try:
            self.limpiar_entry(entrys)
            # cambio estado de botones, los deshabilito
            self.boton_alta['state'] = "disable"
            self.boton_borrar['state'] = "disable"
            self.boton_edit['state'] = "disable"
            self.boton_save.grid(row=2, column=4, padx=15)  # lo hago visible
            # entry=[entry_id, entry_name, entry_surgeon, entry_procedure,
            #       entry_date, entry_hour, entry_duration]
            # capturo en entry el dato de la seleccion:
            entrys[0].insert(0, mi_column[0])
            entrys[1].insert(0, mi_column[1])
            entrys[3].insert(0, mi_column[3])
            entrys[2].insert(0, mi_column[2])
            entrys[4].insert(0, mi_column[4])
            entrys[5].insert(0, mi_column[5].split(":")[0])
            entrys[6].insert(0, mi_column[5].split(":")[-1])
            entrys[7].insert(0, mi_column[6])
            # Espera la accion de un boton -> Guardar / Cancelar
        except IndexError:
            showwarning("Modificar",
                        "Debe seleccionar un elemento en la tabla.")

    def vista_guardar(self, id_pac, name, surgeon, procedure, date, hour_, min,
                      duration, tree, entrys):
        '''Acción del botón "Guardar":

            - Captura los cambios en los entrys.
            - Llama a la funcion de validación de los campos.
            - Llama a la funcion que guarda los elementos en la tabla.
            - Finalmente, muestra la tabla actualizada
            - Habilita nuevamente los botones deshabilitados'''
        hour = hour_.get()+":"+min.get()
        dato = (id_pac.get(), name.get(), surgeon.get(),
                procedure.get(), date.get(), hour, duration.get())
        print(mi_id)
        dni = id_pac.get()
        nombre = name.get()
        medico = surgeon.get()
        self.numero = Validation()
        self.texto = Validation()
        if self.numero.valid_numero(dni) is False:
            showwarning("ERROR", """Debe completar el campo ID Paciente.
                        \nSolo se permiten numeros""")
        elif self.texto.valid_text(nombre) is False:
            showwarning("ERROR", '''El campo "Nombre y Apellido" no puede
                         contener\nnúmeros ni caracteres especiales''')
        elif self.texto.valid_text(medico) is False:
            showwarning("ERROR", '''El campo "Cirujano" no puede contener
                        \nnúmeros ni caracteres especiales''')
        else:
            self.objeto_con.guardar(dato, mi_id)
            showinfo("REGISTRO CORRECTO",
                     "Registro de cirugia modificado correctamente")
            self.limpiar_entry(entrys)
            self.actualizar_treeview(tree)

            self.boton_save.grid_forget()  # lo oculto
            self.boton_alta['state'] = "normal"
            self.boton_borrar['state'] = "normal"
            self.boton_buscar['state'] = "normal"
            self.boton_edit['state'] = "normal"

    def vista_export(self, ):
        ''''Codigo para exportar a .txt, funciona correctamente.'''
        # archivo = open('mi_base_qx.txt', 'w')
        # archivo.write("Nueva alta de datos\n")
        # resultado = datos.fetchall()
        # archivo.write('lis=%s\n'%resultado+'\n')
        # archivo.close()
        try:
            self.objeto_con.export()
            showinfo("EXPORTAR", "Se ha exportado el archivo correctamente")
        except Exception:
            showerror("EXPORTAR", "Ocurrió un error")
