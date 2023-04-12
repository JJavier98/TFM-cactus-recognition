"""
    Interfaz gráfica para seleccionar de manera más fácil los argumentos necesarios
    para la ejecución del script auxiliar "compare_mAP.py"
"""


# BIBLIOTECAS
#_______________________________________________________________________________
from os.path import join as pj
import tkinter as tk
from tkinter import W, StringVar, END
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib


# CLASES
#_______________________________________________________________________________
class UI(ttk.Frame):
    """
    Clase para crear la interfaz gráfica del programa para comparar gráficas.

    Args:
        ttk.Frame (class): clase de la que hereda.
    """


    # Constructor
    #___________________________________________________________________________
    def __init__(self, main_function):
        matplotlib.use('Agg')
        self.parent = tk.Tk()
        self.parent.title("Comparativa de mAPs")
        self.parent.resizable(0,0)
        self.parent.iconbitmap("src/ico/versus.ico")

        super().__init__(self.parent)


        # Variables
        #_______________________________________________________________________
        self.workdir1 = StringVar(value=pj('work_dirs'))
        self.workdir2 = StringVar(value=pj('work_dirs'))
        self.main_function = main_function
        self.comparation_img = None


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
        self.label_imgs = ttk.Label(
            self.marco,
            text="Workdir 1:"
        )

        self.label_res = ttk.Label(
            self.marco,
            text="Workdir 2:"
        )


        # Entries
        #_______________________________________________________________________
        standard_width = 70
        self.entry_imgs = ttk.Entry(
            self.marco,
            textvariable=self.workdir1,
            width=standard_width
        )

        self.entry_res = ttk.Entry(
            self.marco,
            textvariable=self.workdir2,
            width=standard_width
        )


        # Buttons
        #_______________________________________________________________________
        self.button_imgs = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_imgs,
                selection_function=fd.askdirectory(
                    initialdir='work_dirs'
                )
            )
        )

        self.button_res = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_res,
                selection_function=fd.askdirectory(
                    initialdir='work_dirs'
                )
            )
        )

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

        ## imagenes
        self.label_imgs.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_imgs.grid(row=row_, column=0, columnspan=2, sticky=W,
                             padx=(0,10), pady=(0,15))
        self.button_imgs.grid(row=row_, column=2, pady=(0,15))

        ## resultados de imágenes
        row_ += 1
        self.label_res.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_res.grid(row=row_, column=0, columnspan=2, sticky=W,
                            padx=(0,10), pady=(0,15))
        self.button_res.grid(row=row_, column=2, pady=(0,15))

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
        workdir1 = self.workdir1.get()
        workdir2 = self.workdir2.get()

        self.comparation_img = self.main_function(workdir1, workdir2)
