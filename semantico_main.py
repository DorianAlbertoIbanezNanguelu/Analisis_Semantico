from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMessageBox, QFileDialog

import sys

from semantico_visual import Ui_MainWindow

from semantico_clase import Clase_Semantica

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        mywindow.setWindowTitle(self,"Analizador Semántico")
        self.ui.pushButton_iniciar.clicked.connect(self.button_iniciar)
        self.ui.pushButton_importar.clicked.connect(self.button_importar)
        self.ui.textEdit_2.setReadOnly(True)
        self.dialog = QFileDialog

    def button_iniciar(self):
        self.ui.textEdit_2.clear()
        a = self.ui.textEdit.toPlainText()
        clase = Clase_Semantica(a.splitlines())
        clase.iniciar()
        lista = clase.getValor()
        for x in lista:
            self.ui.textEdit_2.append(str(x))

    def button_importar(self):
        self.ui.textEdit.clear()
        options = QFileDialog.Options()
        self.dialog, _ = QFileDialog.getOpenFileName(self,"Selecciona un archivo .TXT", "","Archivo txt (*.txt)", options=options)
        f = open(self.dialog, mode='r', encoding='utf-8')
        #self.estado.append(f.read())
        self.ui.textEdit.setText(f.read())


app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())