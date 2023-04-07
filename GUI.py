# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:05:01 2023

@author: valen
"""

from Sistema import *
from PyQt5 import QtWidgets, uic


sistema = Sistema()



# Carga el archivo .ui
app = QtWidgets.QApplication([])
window = uic.loadUi("test.ui")

window.sendInstru.clicked.connect(sistema.ejecutarHilos)

dato = window.dataInput.text()
procesa = window.pInput.currentText()
direccion = window.dirInput.currentText()
operacion = window.opInput.currentText()

def inputData():
    print(dato + " " + procesa + " " + direccion + " " + operacion)

#window.sendInstru.clicked.connect(inputData)


# Muestra la ventana
window.show()
app.exec_()