"""
    Interfaz gráfica para seleccionar de manera más fácil los argumentos necesarios
    para la ejecución del script "count_cacti.py"
"""


# BIBLIOTECAS
#_______________________________________________________________________________
from os.path import join as pj
import tkinter as tk
from tkinter import E,W, DoubleVar, StringVar, BooleanVar, HORIZONTAL, END
from tkinter import ttk
from tkinter import filedialog as fd
from dataclasses import dataclass
import matplotlib


# CLASES
#_______________________________________________________________________________
class UI(ttk.Frame):
    """
    Clase para crear la interfaz gráfica del programa para contar cactus.

    Args:
        ttk.Frame (class): clase de la que hereda.
    """


    # Constructor
    #___________________________________________________________________________
    def __init__(self, main_function):
        matplotlib.use('Agg')
        self.parent = tk.Tk()
        self.parent.title("Detección y conteo de cactus")
        self.parent.resizable(0,0)
        self.parent.iconbitmap("src/ico/cactus.ico")

        super().__init__(self.parent)


        # Variables
        #_______________________________________________________________________
        self.threshold = DoubleVar(value=0.5)
        self.imgs_dir = StringVar(value=pj('src','imgs_prueba'))
        self.res_dir = StringVar(value=pj('src','results'))
        self.config_file = StringVar(
            value=pj(
                'mmdetection',
                'configs',
                'cactus',
                'faster_rcnn_r50_fpn_1x_saguaro.py'
            )
        )
        self.checkpoint_file = StringVar(
            value=pj(
                'mmdetection',
                'work_dirs',
                'faster_rcnn_r50_fpn_1x_saguaro',
                'latest.pth'
            )
        )
        self.save_imgs = BooleanVar(value=True)
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
        self.label_imgs = ttk.Label(
            self.marco,
            text="Directorio de imágenes:"
        )

        self.label_res = ttk.Label(
            self.marco,
            text="Directorio de resultados:"
        )

        self.label_config = ttk.Label(
            self.marco,
            text="Archivo de configuración:"
        )

        self.label_checkpoint = ttk.Label(
            self.marco,
            text="Archivo de control:"
        )

        self.label_thres = ttk.Label(
            self.marco,
            text="Threshold:"
        )


        # Entries
        #_______________________________________________________________________
        standard_width = 70
        self.entry_imgs = ttk.Entry(
            self.marco,
            textvariable=self.imgs_dir,
            width=standard_width
        )

        self.entry_res = ttk.Entry(
            self.marco,
            textvariable=self.res_dir,
            width=standard_width
        )

        self.entry_config = ttk.Entry(
            self.marco,
            textvariable=self.config_file,
            width=standard_width
        )

        self.entry_checkpoint = ttk.Entry(
            self.marco,
            textvariable=self.checkpoint_file,
            width=standard_width
        )

        self.entry_thres = ttk.Entry(
            self.marco,
            textvariable=self.threshold,
            width=10
        )


        # Buttons
        #_______________________________________________________________________
        self.button_imgs = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_imgs,
                selection_function=fd.askdirectory(
                    initialdir='data/imgs'
                )
            )
        )

        self.button_res = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_res,
                selection_function=fd.askdirectory(
                    initialdir='src/results'
                )
            )
        )

        self.button_config = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_config,
                selection_function=fd.askopenfilename(
                    initialdir='mmdetection/configs'
                )
            )
        )

        self.button_checkpoint = ttk.Button(
            self.marco,
            text='Seleccionar',
            command=lambda : self.update_entry_directory(
                self.entry_checkpoint,
                selection_function=fd.askopenfilename(
                    initialdir='mmdetection/work_dirs'
                )
            )
        )

        self.button_run = ttk.Button(
            self.marco,
            text='Ejecutar',
            command=lambda : self.run_button()
        )


        # Scales
        #_______________________________________________________________________
        self.threshold_scale = ttk.Scale(
            self.marco,
            variable=self.threshold,
            from_=0.0,
            to=1.0,
            orient=HORIZONTAL,
            length=270
        )


        # Checkboxes
        #_______________________________________________________________________
        self.check_save_imgs = ttk.Checkbutton(
            self.marco,
            variable=self.save_imgs,
            text='Guardar imágenes'
        )


        # Grid
        #_______________________________________________________________________
        ## marco
        row_ = 0
        self.marco.grid(row=row_, column=0)

        ## guardar imágenes
        self.check_save_imgs.grid(row=row_, column=0, sticky=W, pady=(0,15))
        row_ += 1

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

        ## configuración
        row_ += 1
        self.label_config.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_config.grid(row=row_, column=0, columnspan=2, sticky=W,
                               padx=(0,10), pady=(0,15))
        self.button_config.grid(row=row_, column=2, pady=(0,15))

        ## archivo de control
        row_ += 1
        self.label_checkpoint.grid(row=row_, column=0, sticky=W)
        row_ += 1
        self.entry_checkpoint.grid(row=row_, column=0, columnspan=2, sticky=W,
                                   padx=(0,10), pady=(0,15))
        self.button_checkpoint.grid(row=row_, column=2, pady=(0,15))

        ## threshold
        row_ += 1
        self.label_thres.grid(row=row_, column=0, sticky=(E), padx=(0,20))
        self.threshold_scale.grid(row=row_, column=1, padx=(0,20), pady=(15,15))
        self.entry_thres.grid(row=row_, column=2, columnspan=2, pady=(15,15))

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
        @dataclass
        class Args:
            """
            Struct para formatear los argumentos que se le pasarán a la
            main_function.
            """
            imgs_path = self.imgs_dir.get()
            res_path = self.res_dir.get()
            threshold = self.threshold.get()
            config_file = self.config_file.get()
            checkpoint_file = self.checkpoint_file.get()
            save_imgs = self.save_imgs.get()

        args = Args()
        to_print = self.main_function(args)[:-1]

        for i, txt in enumerate(to_print):
            label_aux = ttk.Label(
                self.parent,
                text=txt
            )
            label_aux.grid(row=i+1, column=0, padx=(20,20), pady=(10,0), sticky=W)
