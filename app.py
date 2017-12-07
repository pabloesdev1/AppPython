import sys
import sqlite3
from PyQt5 import uic, QtWidgets #importamos uic y QtWidgets desde el modulo PyQt5


qtCreatorFile = "design.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # usammos loadUiType para cargar el diseño de qt creator

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):  # Creamos nuestra clase con sus parametros (QtWidgets.QMainWindow y el diseño de qt creator

    def __init__(self):				# Metodos init para iniciar la aplicacion
        QtWidgets.QMainWindow.__init__(self) # Preparamos una ventana principal
        Ui_MainWindow.__init__(self) # Iniciar el diseño de qt creator
        self.setupUi(self)	# Inicializamos la configuracion de la interfaz
        self.btnGuardar.clicked.connect(self.guardarCliente) # Id del boton conectado a la funcion guardarCliente
        self.btnMostrar.clicked.connect(self.mostrarClientes) # Id del boton conectado a la funcion guardarCliente
        self.listaClientes2.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) # seleccionar solo filas
        self.listaClientes2.setSelectionMode(QtWidgets.QTableWidget.SingleSelection) # usar seleccion simple, una fila a la vez
        self.listaClientes2.itemPressed.connect(self.seleccionarFila) # evento producido cuando se selecciona un elemento
        #self.listaClientes2.setColumnCount(4)
        #self.listaClientes2.setRowCount(4)
        self.conexionDB() # Al iniciar la aplicacion se crea la base de datos

    def conexionDB(self):
    	self.con = sqlite3.connect("./database/clientes.bd") # Conexion a la base de datos
    	self.cursor = self.con.cursor()
    	self.cursor.execute ("CREATE TABLE IF NOT EXISTS cliente(id INTEGER PRIMARY KEY AUTOINCREMENT, nombres text not null, apellidos text not null, correo text not null, telefono text not null)")
    	self.con.commit()

    def guardarCliente(self):
    	print('Cliente registrado')
    	self.con = sqlite3.connect("./database/clientes.bd")
    	self.cursor = self.con.cursor()
    	self.nombre = str(self.txtNombre.text())
    	self.apellido = str(self.txtApellido.text())
    	self.correo = str(self.txtCorreo.text())
    	self.telefono = str(self.txtTelefono.text())
    	self.datos = (self.nombre, self.apellido, self.correo, self.telefono)
    	self.cursor.execute("INSERT INTO cliente (nombres, apellidos, correo, telefono) VALUES (?,?,?,?)", self.datos)
    	self.con.commit()
    	self.con.close()

    def mostrarClientes(self):
        self.con = sqlite3.connect("./database/clientes.bd")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT * FROM cliente")
        self.listaClientes2.clear() # Se vacia la lista
        self.listaClientes2.setColumnCount(5)
        self.listaClientes2.setHorizontalHeaderLabels(['Id', 'Nombre', 'Apellido', 'Correo', 'Teléfono'])
        self.cur = self.cursor.fetchall()   
        self.listaClientes2.setRowCount(len(self.cur))
        for i, row in enumerate(self.cur):
            for j, val in enumerate(row):
                self.listaClientes2.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))


    def seleccionarFila(self):
        identificador, nombre, apellido, correo, telefono = self.listaClientes2.selectedItems()
        self.txtNombre.setText(nombre.text())
        self.txtApellido.setText(apellido.text())
        self.txtCorreo.setText(correo.text())
        self.txtTelefono.setText(telefono.text())
        self.listaClientes2.selectedItems()

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())