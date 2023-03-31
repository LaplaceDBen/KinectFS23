import sys
import datetime
from calibrate import detect_area
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QScrollArea
from PySide6.QtQuickControls2 import QQuickStyle


max_area = None  # Declare global variable

def start():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.append(f"{current_time} - start")
    

def calibrate():
    #change global value
    global max_area
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    max_area = detect_area()
    if max_area is not None:
        log_window.append(f"{current_time} - calibrated - Object Size= {max_area}")
    else:
        log_window.append(f"{current_time} - calibration failed")
    return max_area

def stop():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.append(f"{current_time} - Programm is stopped")
    global max_area
    max_area = None
    log_window.append(f"{current_time} - Calibration is reset")

app = QApplication(sys.argv)
QQuickStyle.setStyle('Material')

window = QWidget()
window.setWindowTitle('GUI_Azure_Kinect')
window.setWindowIcon(QIcon('images\FHGR.jpg'))
window.resize(800, 600)

layout = QVBoxLayout(window)

start_button = QPushButton('Start')
start_button.clicked.connect(start)

calibrate_button = QPushButton('Calibrate')
calibrate_button.clicked.connect(calibrate)

stop_button = QPushButton('Stop')
stop_button.clicked.connect(stop)

log_window = QTextEdit()
log_window.setPlaceholderText('Log')
log_window.setFontWeight(QFont.Bold)
log_window.setFontPointSize(12)
log_window.setFontFamily('Courier')


log_window.setReadOnly(True)

scroll_area = QScrollArea()
scroll_area.setWidget(log_window)

layout.addWidget(start_button)
layout.addWidget(calibrate_button)
layout.addWidget(stop_button)
layout.addWidget(log_window)

window.show()
sys.exit(app.exec())
