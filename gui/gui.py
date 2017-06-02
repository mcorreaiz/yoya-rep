# from PyQt4 import QtCore, QtGui, uic
# import os
#
# def get_absolute_path(relative_path):
#     return os.path.join(os.path.dirname(__file__), relative_path)
#
# pantalla_ui    = uic.loadUiType(get_absolute_path("pantalla.ui"))
#
# class GUI:
#     def __init__(self):
#         #self.pantalla    = Pantalla()
#
#         self.__bind_signals()
#         self.pantalla_inicial.show()
#         self.pantalla_inicial.raise_()
#
#     def __bind_signals(self):
#
#         self.pantalla.boton_ingresar.clicked.connect(
#             self.__pantalla_boton_ingresar_click
#         )
#
#     def __pantalla_boton_ingresar_click(self):
#         self.__toggle_windows(self.pantalla_ingresar, self.pantalla_inicial)
#
# class Pantalla(*pantalla_ui):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.statusbar.showMessage("YOYA", 2000)
