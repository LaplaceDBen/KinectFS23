import sys
import datetime
#from calibrate import detect_area
#get testmacth from Detewction klass
from detection_func import QRCodeDetector
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QScrollArea, QInputDialog,QMessageBox
from PySide6.QtQuickControls2 import QQuickStyle


#help by chatgpt
class GUI_Azure_Kinect(QWidget):

    def __init__(self):
        super().__init__()

        self.num_obj = None

        self.setWindowTitle('GUI_Azure_Kinect')
        self.setWindowIcon(QIcon('images\FHGR.jpg'))
        self.resize(800, 600)

        self.layout = QVBoxLayout(self)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start)

        self.calibrate_button = QPushButton('Calibrate')
        self.calibrate_button.clicked.connect(self.calibrate)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)

        self.log_window = QTextEdit()
        self.log_window.setPlaceholderText('Log')
        self.log_window.setFontWeight(QFont.Bold)
        self.log_window.setFontPointSize(12)
        self.log_window.setFontFamily('Courier')
        self.log_window.setReadOnly(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.log_window)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.calibrate_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.log_window)

                # set stylesheet

        stylesheet = QFile('style.css')
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
    # Set the stylesheet for the application
            self.setStyleSheet(stylesheet.readAll().data().decode('utf-8'))
        

    def start(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if self.max_area is None:
            self.log_window.append(f"{current_time} - Could no start - Object Size is not calibrated")
        else:
            self.log_window.append(f"{current_time} - Programm is started - Object Size= {self.max_area}")
            QRCodeDetector.detect_qr_codes( num_obj=5)


    def calibrate(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        try:
            num_obj, ok = QInputDialog.getInt(self, "Calibration", "Enter the number of objects:", 1, 1)
            if ok:
                self.log_window.append(f"{current_time} - Calibration is started")
                self.num_obj = num_obj
                self.log_window.append(f"{current_time} - Number of objects: {self.num_obj}")
                self.setWindowTitle(f"GUI_Azure_Kinect - {num_obj} objects")
                self.log_window.append(f"{current_time} - Calibration is done")
            else:
                return 
            
        except: 
            self.log_window.append(f"{current_time} - Calibration is not possible")
            

    def stop(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.log_window.append(f"{current_time} - Programm is stopped")
        self.max_area = None
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.log_window.append(f"{current_time} - Calibration is reset")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QQuickStyle.setStyle('Material')

    gui = GUI_Azure_Kinect()
    gui.show()

    sys.exit(app.exec())
