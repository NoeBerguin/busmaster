from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog

class Ui_LOGconverter(object):
    def setupUi(self, LOGconverter):
        LOGconverter.setObjectName("LOGconverter")
        LOGconverter.resize(864, 477)
        self.centralwidget = QtWidgets.QWidget(parent=LOGconverter)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 841, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.undoView = QtWidgets.QUndoView(parent=self.verticalLayoutWidget)
        self.undoView.setObjectName("undoView")
        self.verticalLayout.addWidget(self.undoView)
        self.progressBar = QtWidgets.QProgressBar(parent=self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        LOGconverter.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=LOGconverter)
        self.statusbar.setObjectName("statusbar")
        LOGconverter.setStatusBar(self.statusbar)

        self.retranslateUi(LOGconverter)
        QtCore.QMetaObject.connectSlotsByName(LOGconverter)

        # Connect button signals to their respective slot functions
        self.pushButton_5.clicked.connect(self.openDbcFileDialog)
        self.pushButton.clicked.connect(self.openLogFileDialog)

    def retranslateUi(self, LOGconverter):
        _translate = QtCore.QCoreApplication.translate
        LOGconverter.setWindowTitle(_translate("LOGconverter", "MainWindow"))
        self.label_3.setText(_translate("LOGconverter", "DBC file :"))
        self.pushButton_5.setText(_translate("LOGconverter", "..."))
        self.label.setText(_translate("LOGconverter", "BUSMASTER file to convert : "))
        self.pushButton_2.setText(_translate("LOGconverter", "Convert"))
        self.pushButton.setText(_translate("LOGconverter", "..."))
        self.label_2.setText(_translate("LOGconverter", "Debug"))

    def openDbcFileDialog(self):
        # Aucune option spéciale n'est nécessaire, on peut donc omettre l'argument des options
        fileName, _ = QFileDialog.getOpenFileName(None, "Ouvrir un fichier DBC", "", "Fichiers DBC (*.dbc);;Tous les fichiers (*)")
        if fileName:
            self.lineEdit.setText(fileName)

    def openLogFileDialog(self):
        # Aucune option spéciale n'est nécessaire, on peut donc omettre l'argument des options
        fileName, _ = QFileDialog.getOpenFileName(None, "Ouvrir un fichier Log", "", "Fichiers Log (*.log);;Tous les fichiers (*)")
        if fileName:
            self.lineEdit_2.setText(fileName)