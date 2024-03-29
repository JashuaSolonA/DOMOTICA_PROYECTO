from tkinter import Tk, Button, Label
import serial
import time
from datetime import datetime
import struct

arduino = serial.Serial('COM2',  2400)
time.sleep(2)

def encender_luces():
    arduino.write('1'.encode())

def apagar_luces():
    arduino.write('0'.encode())

def actualizar_fecha():
    fecha_actual = datetime.now()
    fecha_texto = fecha_actual.strftime("%d/%m/%Y %H:%M:%S")  # Formatear la fecha como una cadena
    label_fecha.config(text=fecha_texto)
    root.after(1000, actualizar_fecha)

def actualizar_temperatura():
    data = str(arduino.readline().decode().replace("\n", ""))
    temperatura = "T(°C): " + data[:5]
    humedad = "H(%): " + data[6:11]
    label_temperatura.config(text=temperatura)
    label_humedad.config(text=humedad)
    root.after(500, actualizar_temperatura)

root = Tk()
root.title("AVANCE")
root.geometry("220x150")

label_fecha = Label(root)
label_fecha.pack()
actualizar_fecha()

label_temperatura = Label(root)
label_temperatura.pack()
label_humedad = Label(root)
label_humedad.pack()
actualizar_temperatura()

label_insano = Label(root, text="COMING SOON")
label_insano.pack()

control_led1 = Button(root, text="ENCENDER LEDS", command=encender_luces)
control_led1.config(fg = "black", bg = "light blue")
control_led1.pack()

control_led2 = Button(root, text="APAGAR LEDS", command=apagar_luces)
control_led2.config(fg = "black", bg = "light blue")
control_led2.pack()

root.mainloop()