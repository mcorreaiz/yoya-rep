from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox
import os
import pickle

def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

pantalla_inicial_ui    = uic.loadUiType(get_absolute_path("pantalla_inicial.ui"))
pantalla_menu_ui    = uic.loadUiType(get_absolute_path("pantalla_menu.ui"))
pantalla_pedido_ui    = uic.loadUiType(get_absolute_path("pantalla_pedido.ui"))
pantalla_estadisticas_ui    = uic.loadUiType(get_absolute_path("pantalla_estadisticas.ui"))
pantalla_programacion_ui    = uic.loadUiType(get_absolute_path("pantalla_programacion.ui"))

dialogo_agregar_producto_ui    = uic.loadUiType(get_absolute_path("dialogo_agregar_producto.ui"))

class GUI:
    def __init__(self):
        self.version = "1.0"
        self.nombre = "Yoya v" + self.version

        self.pantalla_inicial         = Pantalla_Inicial()
        self.pantalla_menu            = Pantalla_Menu()
        self.pantalla_pedido          = Pantalla_Pedido()
        self.pantalla_estadisticas    = Pantalla_Estadisticas()
        self.pantalla_programacion    = Pantalla_Programacion()

        self.__bind_signals()
        self.pantalla_inicial.show()
        self.pantalla_inicial.raise_()

    def __bind_signals(self):

        self.pantalla_inicial.boton_menu.clicked.connect(
            self.__pantalla_inicial_boton_menu_click
        )

        self.pantalla_inicial.boton_pedido.clicked.connect(
            self.__pantalla_inicial_boton_pedido_click
        )

        self.pantalla_inicial.boton_estadisticas.clicked.connect(
            self.__pantalla_inicial_boton_estadisticas_click
        )

        self.pantalla_inicial.boton_programacion.clicked.connect(
            self.__pantalla_inicial_boton_programacion_click
        )

        self.pantalla_menu.boton_volver.clicked.connect(
            lambda: self.__boton_volver_click(self.pantalla_menu)
        )

        self.pantalla_pedido.boton_volver.clicked.connect(
            lambda: self.__boton_volver_click(self.pantalla_pedido)
        )

        self.pantalla_estadisticas.boton_volver.clicked.connect(
            lambda: self.__boton_volver_click(self.pantalla_estadisticas)
        )

        self.pantalla_programacion.boton_volver.clicked.connect(
            lambda: self.__boton_volver_click(self.pantalla_programacion)
        )

    def __pantalla_inicial_boton_menu_click(self):
        self.__toggle_windows(self.pantalla_menu, self.pantalla_inicial)

    def __pantalla_inicial_boton_pedido_click(self):
        self.__toggle_windows(self.pantalla_pedido, self.pantalla_inicial)

    def __pantalla_inicial_boton_estadisticas_click(self):
        self.__toggle_windows(self.pantalla_estadisticas, self.pantalla_inicial)

    def __pantalla_inicial_boton_programacion_click(self):
        self.__toggle_windows(self.pantalla_programacion, self.pantalla_inicial)

    def __boton_volver_click(self, pantalla):
        self.__toggle_windows(self.pantalla_inicial, pantalla)

    def __toggle_windows(self, incoming, outgoing):
        outgoing.close()
        text_fields = getattr(outgoing, "text_fields", None)
        if text_fields is not None:
            self.__reset_text_fields(text_fields)
        incoming.show()
        incoming.raise_()

    def __mostrar_mensaje_critico(self, parent, msg):
        QtGui.QMessageBox.critical(parent, self.nombre, msg)

    def __mostrar_mensaje_info(self, parent, msg):
        QtGui.QMessageBox.information(parent, self.nombre, msg)


class Pantalla_Inicial(*pantalla_inicial_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Pantalla_Menu(*pantalla_menu_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.dialogo_agregar_producto = Dialogo_Agregar_Producto()
        self.menu_file = "../db/menu"
        self.menu = {}
        self.producto_nuevo = False
        self.nombre_viejo = ""
        self.precio_viejo = ""

        self.leer_menu()
        self.actualizar_tabla_menu()
        self.__bind_signals()

    def __bind_signals(self):
        self.boton_agregar_producto.clicked.connect(
            self.__boton_agregar_producto_click
        )

        self.tabla_menu.cellChanged.connect(
            self.__tabla_menu_change
        )

        self.tabla_menu.cellDoubleClicked.connect(
            self.__tabla_menu_dobleclick
        )

        self.dialogo_agregar_producto.buttonBox.accepted.connect(
            self.__dialogo_agregar_producto_accept
        )

    def __boton_agregar_producto_click(self):
        self.dialogo_agregar_producto.show()

    def __dialogo_agregar_producto_accept(self):
        nombre = self.dialogo_agregar_producto.edit_nombre.text()
        precio = self.dialogo_agregar_producto.edit_precio.text()
        if nombre in self.menu:
            QMessageBox.critical(self, "Yoya", "Ese producto ya esta en el menu.\nPara editar un producto, haz doble click sobre el.")
            return
        if precio and nombre:
            if precio.isdigit():
                self.agregar_producto(nombre, precio)
                self.producto_nuevo = True
                self.actualizar_tabla_menu()
                [i.setText("") for i in self.dialogo_agregar_producto.text_fields]
            else:
                QMessageBox.critical(self, "Yoya", "El precio debe ser un numero.")
        else:
            QMessageBox.critical(self, "Yoya", "No pueden haber espacios vacios.")

    def __tabla_menu_dobleclick(self, row, col):
        self.nombre_viejo = self.tabla_menu.item(row, 0).data(0)
        self.precio_viejo = self.tabla_menu.item(row, 1).data(0)

    def __tabla_menu_change(self, row, col):
        if not self.producto_nuevo:
            nombre = self.tabla_menu.item(row, 0).data(0)
            precio = self.tabla_menu.item(row, 1).data(0)
            if nombre and precio:
                self.menu[nombre] = precio
                if not col: # cambio un nombre
                    del self.menu[self.nombre_viejo]
                self.guardar_menu()
            else:
                QMessageBox.critical(self, "Yoya", "No pueden haber espacios vacios.")
                if col:
                    self.tabla_menu.setItem(row, col, QtWidgets.QTableWidgetItem(self.precio_viejo))
                else:
                    self.tabla_menu.setItem(row, col, QtWidgets.QTableWidgetItem(self.nombre_viejo))

    def leer_menu(self):
        if not os.path.isfile(self.menu_file):
            self.menu = {}
            with open(self.menu_file, "wb") as arch:
                pickle.dump(self.menu, arch)
        with open(self.menu_file, "rb") as arch:
            try:
                self.menu = pickle.load(arch)
            except:
                self.menu = {}

    def guardar_menu(self):
        with open(self.menu_file, "wb") as arch:
            pickle.dump(self.menu, arch)

    def agregar_producto(self, nombre, precio):
        self.menu[nombre] = precio

    def actualizar_tabla_menu(self):
        filas = self.tabla_menu.rowCount()
        self.tabla_menu.clearContents()
        k = 0
        for i in self.menu:
            if k >= filas:
                self.tabla_menu.insertRow(k)
            self.tabla_menu.setItem(k, 0, QtWidgets.QTableWidgetItem(i))
            self.tabla_menu.setItem(k, 1, QtWidgets.QTableWidgetItem(self.menu[i]))
            k += 1
        self.producto_nuevo = False
        self.guardar_menu()


class Pantalla_Pedido(*pantalla_pedido_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Pantalla_Estadisticas(*pantalla_estadisticas_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Pantalla_Programacion(*pantalla_programacion_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Dialogo_Agregar_Producto(*dialogo_agregar_producto_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text_fields = (
            self.edit_nombre,
            self.edit_precio
        )


if __name__ == "__main__":

    app = QApplication([])
    gui = GUI()
    app.exec_()
