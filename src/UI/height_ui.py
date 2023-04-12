"""
    Interfaz gráfica para seleccionar de manera más fácil los argumentos necesarios
    para la ejecución del script "height.py"
"""


# BIBLIOTECAS
#_______________________________________________________________________________
from os.path import join as pj
import tkinter as tk
from tkinter import W, END, StringVar, BooleanVar
from tkinter import ttk
from tkinter import filedialog as fd


# CLASES
#_______________________________________________________________________________
class UI(ttk.Frame):
    """
    Clase para crear la interfaz gráfica del programa para medir la altura de
    los cactus.

    Args:
        ttk.Frame (class): clase de la que hereda.
    """


    # Constructor
    #___________________________________________________________________________
    def __init__(self, main_function):
        self.parent = tk.Tk()
        self.parent.title("Altura de cactus")
        self.parent.resizable(0,0)
        self.parent.iconbitmap("src/ico/height.ico")

        super().__init__(self.parent)


        # Variables
        #_______________________________________________________________________
        self.bbox_file = StringVar(value=pj('src','results','bboxes','bbox_file.csv'))
        self.heights_dir = StringVar(value=pj('src','results','heights'))
        self.overwrite = BooleanVar(value=False)
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
        self.label_res = ttk.Label(
            self.marco,
            text="Directorio de resultados:"
        )

        self.label_bbox = ttk.Label(
            self.marco,
            text="Archivo de bboxes:"
        )


        # Entries
        #_______________________________________________________________________
        standard_width = 70

        self.entry_res = ttk.Entry(
            self.marco,
            textvariable=self.heights_dir,
            width=standard_width
        )

        self.entry_bbox = ttk.Entry(
            self.marco,
            textvariable=self.bbox_file,
            width=standard_width
        )


        # Buttons
        #_______________________________________________________________________

        self.button_res = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_res,
                selection_function=fd.askdirectory()
                )
        )

        self.button_bbox = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_bbox,
                selection_function=fd.askopenfilename()
                )
        )

        self.button_run = ttk.Button(
            self.marco,
            text='Ejecutar',
            command=lambda : self.run_button()
        )


        # Checkboxes
        #_______________________________________________________________________
        self.check_save_imgs = ttk.Checkbutton(
            self.marco,
            variable=self.overwrite,
            text='Sobreescribir .csv'
        )


        # Grid
        #_______________________________________________________________________
        ## marco
        row_ = 0
        self.marco.grid(row=row_, column=0)

        ## archivo de bboxes
        row_ += 1
        self.label_bbox.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_bbox.grid(
            row=row_,
            column=0,
            columnspan=2,
            sticky=W,
            padx=(0,10),
            pady=(0,15)
        )
        self.button_bbox.grid(row=row_, column=2, pady=(0,15))

        ## resultados de imágenes
        row_ += 1
        self.label_res.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_res.grid(
            row=row_,
            column=0,
            columnspan=2,
            sticky=W,
            padx=(0,10),
            pady=(0,15)
        )
        self.button_res.grid(row=row_, column=2, pady=(0,15))

        ## guardar imágenes
        row_ += 1
        self.check_save_imgs.grid(row=row_, column=0, sticky=W, pady=(0,0))

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
        self.main_function(self.bbox_file.get(), self.heights_dir.get(),
                           self.overwrite.get())
        self.parent.destroy()
