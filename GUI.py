import sys
import datetime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtQuickControls2 import QQuickStyle

def start():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.append(f"{current_time} - start")

def calibrate():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.append(f"{current_time} - calibrate")

def stop():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.append(f"{current_time} - stop")

app = QApplication(sys.argv)
QQuickStyle.setStyle('Material')

window = QWidget()
window.setWindowTitle('Button Example')
window.setWindowIcon(QIcon('images\FHGR.jpg'))
window.resize(500, 400)

layout = QVBoxLayout(window)

start_button = QPushButton('Start')
start_button.clicked.connect(start)

calibrate_button = QPushButton('Calibrate')
calibrate_button.clicked.connect(calibrate)

stop_button = QPushButton('Stop')
stop_button.clicked.connect(stop)

log_window = QTextEdit()
log_window.setReadOnly(True)

layout.addWidget(start_button)
layout.addWidget(calibrate_button)
layout.addWidget(stop_button)
layout.addWidget(log_window)

window.show()
sys.exit(app.exec_())
