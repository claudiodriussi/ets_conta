#!/usr/bin/python3
import sys
import tkinter as tk
from tkinter import filedialog as fd
import pathlib
import pygubu

import ets_conta

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "conta_gui.ui"


class ContaTkApp:
    def __init__(self, master=None, primanota_file=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)

        self.primanota_file = None
        self.do_giornale = None
        self.do_bilancio = None
        self.do_schede = None
        self.do_eventi = None
        self.do_anag = None
        builder.import_variables(self,
                                 ['primanota_file',
                                  'do_bilancio',
                                  'do_schede',
                                  'do_eventi',
                                  'do_anag',
                                  'do_giornale'])
        self.do_bilancio.set(True)
        self.do_schede.set(True)
        self.do_eventi.set(False)
        self.do_anag.set(False)
        self.do_giornale.set(False)
        if primanota_file:
            self.primanota_file.set(primanota_file)

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def open_file(self):
        filetypes = (
            ('Excel files', '*.xlsx'),
            ('All files', '*.*')
        )
        file = fd.askopenfilename(filetypes=filetypes)
        self.primanota_file.set(file)

    def cancel(self):
        self.mainwindow.quit()

    def confirm(self):
        conta = ets_conta.EtsConta()
        try:
            conta.read_prima(self.primanota_file.get())
        except Exception as e:
            tk.messagebox.showwarning(message="Errore: " + e.__repr__())
            return

        if self.do_giornale.get():
            conta.write_giornale('GIORNALE.xlsx')
        if self.do_bilancio.get():
            conta.write_bilancio('BILANCIO.xlsx')
        if self.do_schede.get():
            conta.write_schede()
        if self.do_anag.get():
            conta.write_anag()
        if self.do_eventi.get():
            conta.write_eventi()
        tk.messagebox.showinfo(message="Fatto")


if __name__ == "__main__":
    filename = None if len(sys.argv) < 2 else sys.argv[1]
    app = ContaTkApp(primanota_file=filename)
    app.run()
