import sys
import os  # Import os module for path manipulations
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
        
        # Generating the output CSV filename based on the input log file
        if log_path:
            base_name = os.path.basename(log_path)  # Get the base name of the log file
            output_filename = base_name.replace('.log', '_converted.csv')  # Replace .log with _converted.csv
            csv_final_output_path = os.path.join('./', output_filename)  # Create the full path for the CSV output
        else:
            csv_final_output_path = "./output_final.csv"  # Default output filename if no log path is provided

        if dbc_path and log_path:
            self.update_debug_message("Démarrage de la conversion...")
            processor = CANLogProcessor(log_path, dbc_path, csv_final_output_path, self.update_progress_bar)
            self.update_debug_message("Conversion des logs en messages CAN...")
            messages_can = processor.log_to_messages()
            self.update_debug_message("Écriture des messages CAN dans le fichier CSV...")
            processor.messages_to_csv(messages_can)
            self.update_debug_message(f"Conversion terminée avec succès. Fichier enregistré sous : {csv_final_output_path}")
        else:
            self.update_debug_message("Les chemins des fichiers sont nécessaires pour commencer la conversion.")

    def update_debug_message(self, message):
        self.ui.debugView.appendPlainText(message)  # Update the text display with new message
        
    def update_progress_bar(self, value):
        self.ui.progressBar.setValue(int(value))


def main():
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
