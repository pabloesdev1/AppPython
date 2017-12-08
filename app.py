import sys
import sqlite3
from PyQt5 import uic, QtWidgets #importamos uic y QtWidgets desde el modulo PyQt5


qtCreatorFile = "design.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # usammos loadUiType para cargar el diseño de qt creator

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):  # Creamos nuestra clase con sus parametros (QtWidgets.QMainWindow y el diseño de qt creator

	def __init__(self):             # Metodos init para iniciar la aplicacion
		QtWidgets.QMainWindow.__init__(self) # Preparamos una ventana principal
		Ui_MainWindow.__init__(self) # Iniciar el diseño de qt creator
		self.setupUi(self)  # Inicializamos la configuracion de la interfaz
		self.btnGuardar.clicked.connect(self.guardarCliente) # Id del boton conectado a la funcion guardarCliente
		self.btnMostrar.clicked.connect(self.mostrarClientes) # Id del boton conectado a la funcion guardarCliente
		self.btnNuevo.clicked.connect(self.borrarCampos) # Id del boton conectado a la funcion guardarCliente
		self.btnEliminar.clicked.connect(self.eliminarCliente) # Id del boton conectado a la funcion guardarCliente
		self.listaClientes2.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) # seleccionar solo filas
		self.listaClientes2.setSelectionMode(QtWidgets.QTableWidget.SingleSelection) # usar seleccion simple, una fila a la vez
		self.listaClientes2.itemPressed.connect(self.seleccionarFila) # evento producido cuando se selecciona un elemento
		self.txtId.setEnabled(False)
		self.btnEliminar.setEnabled(False)
		self.conexionDB() # Al iniciar la aplicacion se crea la base de datos

	def conexionDB(self):
		self.con = sqlite3.connect("./database/clientes.bd") # Conexion a la base de datos
		self.cursor = self.con.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS cliente(id INTEGER PRIMARY KEY AUTOINCREMENT, nombres text not null, apellidos text not null, correo text not null, telefono text not null, direccion text not null)")
		self.con.commit()

	def guardarCliente(self):
		self.con = sqlite3.connect("./database/clientes.bd")
		self.cursor = self.con.cursor()
		self.id = self.txtId.text()
		self.nombre = str(self.txtNombre.text())
		self.apellido = str(self.txtApellido.text())
		self.correo = str(self.txtCorreo.text())
		self.telefono = str(self.txtTelefono.text())
		self.direccion = str(self.txtDireccion.text())
		if 	self.btnGuardar.text() == 'Guardar':
			self.datos = (self.nombre, self.apellido, self.correo, self.telefono, self.direccion)
			self.cursor.execute("INSERT INTO cliente (nombres, apellidos, correo, telefono, direccion) VALUES (?,?,?,?,?)", self.datos)
			print('Cliente registrado')
		elif self.btnGuardar.text() == 'Modificar':
			self.datos = (self.nombre, self.apellido, self.correo, self.telefono, self.direccion, self.id)
			self.cursor.execute("UPDATE cliente set nombres = ?, apellidos = ?, correo = ?, telefono = ?, direccion = ? where id = ?", self.datos)
			print('Cliente actualizado')
		self.borrarCampos()
		self.con.commit()
		self.con.close()
		self.mostrarClientes()

	def mostrarClientes(self):
		self.con = sqlite3.connect("./database/clientes.bd")
		self.cursor = self.con.cursor()
		self.cursor.execute("SELECT * FROM cliente")
		self.listaClientes2.clear() # Se vacia la lista
		self.listaClientes2.setColumnCount(6)
		self.listaClientes2.setHorizontalHeaderLabels(['Id', 'Nombre', 'Apellido', 'Correo', 'Teléfono', 'Dirección'])
		self.cur = self.cursor.fetchall()
		self.listaClientes2.setRowCount(len(self.cur))
		for i, row in enumerate(self.cur):
			for j, val in enumerate(row):
				self.listaClientes2.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

	def eliminarCliente(self):
		self.con = sqlite3.connect("./database/clientes.bd")
		self.cursor = self.con.cursor()
		self.cursor.execute("delete from cliente where id = (?)", [self.txtId.text()])
		print("Cliente eliminado")
		self.con.commit()
		self.con.close()
		self.mostrarClientes()
		self.borrarCampos()

	def seleccionarFila(self):
		identificador, nombre, apellido, correo, telefono, direccion = self.listaClientes2.selectedItems()
		self.txtId.setText(identificador.text())
		self.txtNombre.setText(nombre.text())
		self.txtApellido.setText(apellido.text())
		self.txtCorreo.setText(correo.text())
		self.txtTelefono.setText(telefono.text())
		self.txtDireccion.setText(direccion.text())
		self.btnEliminar.setEnabled(True)
		self.btnGuardar.setText("Modificar")

	def borrarCampos(self):
		self.txtId.setText("")
		self.txtNombre.setText("")
		self.txtApellido.setText("")
		self.txtCorreo.setText("")
		self.txtTelefono.setText("")
		self.txtDireccion.setText("")
		self.btnEliminar.setEnabled(False)
		self.btnGuardar.setText("Guardar")

if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())