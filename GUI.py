# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:05:01 2023

@author: valen
"""

from PyQt5 import QtWidgets, uic
from Sistema import *

class Ventana(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Carga el archivo .ui
        uic.loadUi("test.ui", self)

        self.sistema = Sistema()

        self.sendInstru.clicked.connect(self.ejecutarHilos)

    def ejecutarHilos(self):
        self.sistema.ejecutarHilos()
        self.instruccion1.setText(self.sistema.instrucciones_procesadores[0])
        self.instruccion2.setText(self.sistema.instrucciones_procesadores[1])
        self.instruccion3.setText(self.sistema.instrucciones_procesadores[2])
        self.instruccion4.setText(self.sistema.instrucciones_procesadores[3])
        

app = QtWidgets.QApplication([])
ventana = Ventana()
ventana.show()
app.exec_()
