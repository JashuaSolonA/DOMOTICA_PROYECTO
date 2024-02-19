import sys
import numpy as np
from INTERFAZ_ui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer, QDate, Qt, QTime
from PyQt5.QtGui import QPixmap, QIcon
import serial
import time

arduino = serial.Serial('COM2',2400)
time.sleep(2)

class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)

        #update the date every 1 second
        self.refreshDate()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshDate)
        self.timer.start(1000)

        #Connect/Disconnect the interface
        self.ui.connect_bt.clicked.connect(self.startConection)

        #Serial connection date
        self.refreshDate()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshAll)
        self.timer.start(2000)

    def refreshAll(self):
        data = str(arduino.readline().decode().replace("\n", ""))
        temperatura = data[0:2]
        humedad = data[2:4]
        sala = data[4:5]
        pasadizo = data[5:6]
        cortinas = data[6:7]
        ventilador = data[7:8]
        riego = data[8:9]
        fuego = data[9:10]
        llave = data[10:11]

        self.ui.temperature_value.setText(temperatura + " °C" + "  " + humedad +" %")
        if sala == "1":
            self.ui.living_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.dining_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.kitchen_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.bedroom_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.lamp_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.hall_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
            self.ui.bathroom_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
        else:
            self.ui.living_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.dining_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.kitchen_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.bedroom_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.lamp_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.hall_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))
            self.ui.bathroom_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))

        if pasadizo == "1":
            self.ui.passage_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_on.png"))
        else:
            self.ui.passage_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\light_off.png"))

        if cortinas == "1":
            self.ui.blind_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\blind_on.png"))
        else:
            self.ui.blind_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\blind.png"))

        if ventilador == "1":
            self.ui.fan_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\fan_on.png"))
        else:
            self.ui.fan_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\fan.png"))
        
        if riego == "1":
            self.ui.pump_bt.setIcon(QIcon(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\pump_off.png"))
        else:
            self.ui.pump_bt.setIcon(QIcon(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\pump_on.png"))
        
        if fuego == "1":
            self.ui.alarm_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\alarm_on.png"))
            self.ui.fire_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\fire_on.png"))
        else:
            self.ui.fire_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\fire_off.png"))
            self.ui.alarm_data.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\alarm_off.png"))
        
        if llave == "1":
            self.ui.lock_bt.setIcon(QIcon(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\door_open.png"))
        else:
            self.ui.lock_bt.setIcon(QIcon(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\door_close.png"))


    def startConection(self):
        enabled = not self.ui.pump_bt.isEnabled()
        #LABEL
        self.ui.living_label.setEnabled(enabled)
        self.ui.dining_label.setEnabled(enabled)
        self.ui.kitchen_label.setEnabled(enabled)
        self.ui.passage_label.setEnabled(enabled)
        self.ui.bedroom_label.setEnabled(enabled)
        self.ui.lamp_label.setEnabled(enabled)
        self.ui.hall_label.setEnabled(enabled)
        self.ui.bathroom_label.setEnabled(enabled)
        #DATA
        self.ui.living_data.setEnabled(enabled)
        self.ui.dining_data.setEnabled(enabled)
        self.ui.kitchen_data.setEnabled(enabled)
        self.ui.passage_data.setEnabled(enabled)
        self.ui.bedroom_data.setEnabled(enabled)
        self.ui.lamp_data.setEnabled(enabled)
        self.ui.hall_data.setEnabled(enabled)
        self.ui.bathroom_data.setEnabled(enabled)
        self.ui.fan_data.setEnabled(enabled)
        self.ui.blind_data.setEnabled(enabled)
        self.ui.alarm_data.setEnabled(enabled)
        self.ui.fire_data.setEnabled(enabled)
        #BT
        self.ui.pump_bt.setEnabled(enabled)
        self.ui.lock_bt.setEnabled(enabled)

        if enabled:
            self.ui.connect_bt.setText('DESCONECTAR')
        else:
            self.ui.connect_bt.setText('CONECTAR')

    def refreshDate(self):
        seleccion = str(QTime.currentTime().toString(Qt.DefaultLocaleLongDate))
        self.ui.date_value.setText(QDate.currentDate().toString(Qt.DefaultLocaleLongDate))
        self.ui.time_value.setText(seleccion)
        select = int(seleccion[:2])
        if  19 >= select >= 6:
            self.ui.DN_icon.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\sun.png"))
        else:
            self.ui.DN_icon.setPixmap(QPixmap(r"C:\UNT\VI CICLO\DOMOTICA\JTT\INTERFAZ\IMAGENES\moon.png"))
        if 12 <= select < 19:
            self.ui.greet_value.setText('Buenas tardes...')
        elif 5 <= select < 12:
            self.ui.greet_value.setText('Buenos días...')
        else:
            self.ui.greet_value.setText('Buenas noches...')


if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     mi_app = MiApp()
     mi_app.show()
     sys.exit(app.exec_())  