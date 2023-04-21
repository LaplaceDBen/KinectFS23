import sys
import os
import datetime
from detection_func import QRCodeDetector,QR_Detector_3, QR_Detector_4
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit,QPushButton, QScrollArea, QInputDialog,QMessageBox,QCheckBox,QComboBox,QDialog,QDialogButtonBox,QFormLayout,QLabel,QLineEdit,QSpinBox,QVBoxLayout

from PySide6.QtQuickControls2 import QQuickStyle
import threading
from config import camera_config
import pyk4a
from pyk4a import Config, PyK4A





#help by chatgpt
class GUI_Azure_Kinect(QWidget):

    def __init__(self):
        super().__init__()

        self.num_obj = None
        self.detector = None
        self.camera_config = camera_config

        self.setWindowTitle('GUI_Azure_Kinect')
        self.setWindowIcon(QIcon('images\FHGR.jpg'))
        self.resize(800, 600)

        self.layout = QVBoxLayout(self)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start)
        self.start_button.setEnabled(False)

        self.calibrate_button = QPushButton('Calibrate')
        self.calibrate_button.clicked.connect(self.calibrate)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        
        self.config_button = QPushButton('Config')
        self.config_button.clicked.connect(self.config)
        
        self.checkbox = QCheckBox('Display QR codes')
        self.checkbox.setChecked(True)
        #make space
        

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
        self.layout.addWidget(self.config_button)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.log_window)



                # set stylesheet

        stylesheet = QFile('style.css')
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
    # Set the stylesheet for the application
            self.setStyleSheet(stylesheet.readAll().data().decode('utf-8'))

    def start(self):
        self.config_button.setEnabled(False)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if self.num_obj is None:
            self.log_window.append(f"{current_time} - Could no start - number off objects is not calibrated")
        else:
            self.log_window.append(f"{current_time} - Programm is started - Number of objects: {self.num_obj}")
            self.calibrate_button.setEnabled(False)
            
            self.detector.run(self.camera_config,display=self.checkbox.isChecked())
            #disable calibration button
            
            
        
        


    def calibrate(self):
        self.config_button.setEnabled(False)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        try:
            num_obj, ok = QInputDialog.getInt(self, "Calibration", "Enter the number of objects:", 1, 1)
            if ok:
                self.detector = QR_Detector_4(num_objects=5)
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(True)
                self.log_window.append(f"{current_time} - Calibration is started")
                self.num_obj = num_obj
                self.log_window.append(f"{current_time} - Number of objects: {self.num_obj}")
                self.setWindowTitle(f"GUI_Azure_Kinect - {num_obj} objects")
                self.active = True
                self.log_window.append(f"{current_time} - Calibration is done")
            else:
                return 
            
        except: 
            self.log_window.append(f"{current_time} - Calibration is not possible")
            

    def stop(self):
        self.config_button.setEnabled(True)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.log_window.append(f"{current_time} - Programm is stopped")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.log_window.append(f"{current_time} - Calibration is reset")
        #enable calibration button
        self.calibrate_button.setEnabled(True)
        #if detector is running
        try:
             self.detector.stop()
        except:
            pass
           

    def config(self):
            # create dialog
            dialog = QDialog(self)
            dialog.setWindowTitle('Config')

            # create form layout
            layout = QFormLayout(dialog)

            # create dropdowns
            label = QLabel('Resolution')
            dropdown1 = QComboBox()
            dropdown1.addItems(['720P','1080P','2160P'])
            layout.addRow(label, dropdown1)

            label = QLabel('Synchronized images only')
            dropdown2 = QComboBox()
            dropdown2.addItems(['True', 'False'])
            layout.addRow(label, dropdown2)

            # create buttons
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            

            # show dialog and wait for result
            result = dialog.exec()
            
            resolutions = {"720P": pyk4a.ColorResolution.RES_720P,
               "1080P": pyk4a.ColorResolution.RES_1080P,
               "2160P": pyk4a.ColorResolution.RES_2160P}
            
            

            # handle result
            if result == QDialog.Accepted:
                # retrieve selected options from dropdowns
                res = dropdown1.currentText()
                syn = dropdown2.currentText()
                resolution = resolutions[res]
                # print selected options
                print(f'Resolution: {res}, synchronized: {syn}')
                
                self.camera_config = PyK4A(Config(color_resolution=resolution,
                             depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                             synchronized_images_only=syn,))


   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QQuickStyle.setStyle('Material')

    gui = GUI_Azure_Kinect()
    gui.show()

    sys.exit(app.exec())
