# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:05:01 2023

@author: valen
"""

from Sistema import *
from PyQt5 import QtWidgets, uic


sistema = Sistema()

def inputData():
    print(window.dataInput.text())

# Carga el archivo .ui
app = QtWidgets.QApplication([])
window = uic.loadUi("test.ui")

window.sendInstru.clicked.connect(sistema.ejecutarHilos)

# Muestra la ventana
window.show()
app.exec_()