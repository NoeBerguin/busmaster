import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.MainWindow import Ui_LOGconverter
from ALLinterpreter import CANLogProcessor

class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LOGconverter()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.start_conversion)

    def start_conversion(self):
        dbc_path = self.ui.lineEdit.text()
        log_path = self.ui.lineEdit_2.text()
        csv_final_output_path = "./output_final.csv"

        if dbc_path and log_path:
            processor = CANLogProcessor(log_path, dbc_path, csv_final_output_path, self.update_progress_bar)
            messages_can = processor.log_to_messages()
            processor.messages_to_csv(messages_can)
        else:
            print("Les chemins des fichiers sont nécessaires pour commencer la conversion.")

    def update_progress_bar(self, value):
        self.ui.progressBar.setValue(int(value))



def main():
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
