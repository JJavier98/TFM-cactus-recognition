"""
    Interfaz gráfica para seleccionar de manera más fácil los argumentos necesarios
    para la ejecución del script "train.py"
"""


# BIBLIOTECAS
#_______________________________________________________________________________
from os.path import join as pj
import tkinter as tk
from tkinter import W, END, StringVar
from tkinter import ttk
from tkinter import filedialog as fd


# CLASES
#_______________________________________________________________________________
class UI(ttk.Frame):
    """
    Clase para crear la interfaz gráfica del programa para entrenar el modelo
    de detección de cactus.

    Args:
        ttk.Frame (class): clase de la que hereda.
    """


    # Constructor
    #___________________________________________________________________________
    def __init__(self, main_function):
        self.parent = tk.Tk()
        self.parent.title("Training")
        self.parent.resizable(0,0)
        self.parent.iconbitmap("src/ico/train.ico")

        super().__init__(self.parent)


        # Variables
        #_______________________________________________________________________
        self.train_file = StringVar(value=pj('mmdetection','tools','train.py'))
        self.config_file = StringVar(value=pj('mmdetection', 'configs', 'cactus',
                                              'faster_rcnn_r50_fpn_1x_google_saguaro.py'))
        self.main_function = main_function


        # Frames
        #_______________________________________________________________________
        self.marco = ttk.Frame(
            self.parent,
            borderwidth=2,
            relief='raised',
            padding=(20,20)
        )


        # Labels
        #_______________________________________________________________________
        self.label_conf = ttk.Label(
            self.marco,
            text="Archivo de configuración:"
        )

        # self.label_train = ttk.Label(
        #     self.marco,
        #     text="Script de train:"
        # )


        # Entries
        #_______________________________________________________________________
        standard_width = 70

        self.entry_conf = ttk.Entry(
            self.marco,
            textvariable=self.config_file,
            width=standard_width
        )

        # self.entry_train = ttk.Entry(
        #     self.marco,
        #     textvariable=self.train_file,
        #     width=standard_width
        # )


        # Buttons
        #_______________________________________________________________________

        self.button_conf = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_conf,
                selection_function=fd.askopenfilename(
                    initialdir=pj('mmdetection','configs','cactus')
                )
            )
        )

        # self.button_train = ttk.Button(
        #     self.marco,
        #     text='Seleccionar',
        #     command=lambda : self.update_entry_directory(
        #         # self.entry_train,
        #         selection_function=fd.askopenfilename(
        #             initialdir=pj('mmdetection','tools')
        #         )
        #     )
        # )

        self.button_run = ttk.Button(
            self.marco,
            text='Ejecutar',
            command=lambda : self.run_button()
        )


        # Grid
        #_______________________________________________________________________
        ## marco
        row_ = 0
        self.marco.grid(row=row_, column=0)

        ## archivo de bboxes
        # row_ += 1
        # self.label_train.grid(row=row_, column=0, sticky=W)
        # row_ += 1
        # self.entry_train.grid(
        #     row=row_,
        #     column=0,
        #     columnspan=2,
        #     sticky=W,
        #     padx=(0,10),
        #     pady=(0,15)
        # )
        # self.button_train.grid(row=row_, column=2, pady=(0,15))

        ## resultados de imágenes
        row_ += 1
        self.label_conf.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_conf.grid(
            row=row_,
            column=0,
            columnspan=2,
            sticky=W,
            padx=(0,10),
            pady=(0,15)
        )
        self.button_conf.grid(row=row_, column=2, pady=(0,15))

        ## ejecutar
        row_ += 1
        self.button_run.grid(row=row_, column=2, pady=(15,0))


        # Loop
        #_______________________________________________________________________
        self.parent.mainloop()


    # Methods
    #_______________________________________________________________________
    def update_entry_directory(self, entry, selection_function):
        """
        
        Actualiza el texto de un campo de entrada mediante un método de selección

        Args:
            entry (tkk.Entry): campo de entrada a actualizar
            selection_function (function): función o método mediante el que
            se selecciona el nuevo valor del campo
        """
        entry.delete(0,END)
        entry.insert(0,selection_function)

    def run_button(self):
        """
        Tras darle al botón "Ejecutar" se ejecutará la main_function que se haya
        pasado en el constructor.
        """
        self.marco.destroy()
        self.main_function(self.train_file.get(), self.config_file.get())
        self.parent.destroy()
