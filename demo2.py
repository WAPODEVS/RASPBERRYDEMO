# Librerías
import time
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.pdu import ExceptionResponse

# Clase Principal
class Modbus:
    def __init__(self, port, baudrate, bytesize, parity, stopbits):
        self.port = port
        self.framer = ModbusRtuFramer
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.client = ModbusSerialClient(self.port, self.framer, self.baudrate, self.bytesize, self.parity, self.stopbits)
    
    def leer_registros(self, registro_inicio, num_registros,esclavo):

        rr = self.client.read_holding_registers(address = registro_inicio, count = num_registros, slave = esclavo)
            
        if rr.isError():
            print(f"Received Modbus library error({rr})")
        elif isinstance(rr, ExceptionResponse):
            print(f"Received Modbus library exception ({rr})")
        else:
            return rr.registers
        
    def leer_coils(self, coil_inicio, num_coils, esclavo):
        
        coils = self.client.read_coils(address = coil_inicio, count = num_coils, slave = esclavo)        
            
        if coils.isError():
            print(f"Received Modbus library error({coils})")
        elif isinstance(coils, ExceptionResponse):
            print(f"Received Modbus library exception ({coils})")
        else:
            return coils.registers

    def escribir_registro(self, registro, valor, esclavo):
        try:
            self.client.write_register(address = registro, value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicación Modbus: {exc}")

    def escribir_coil(self, coil, valor, esclavo):
        try:
            self.client.write_coil(address = coil,value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicacion Modbus: {exc}")

# Comprobando la conexión
def verificar_conexion(modbus_object):
    if modbus_object.client.connect():
        print("\n----CONEXION EXITOSA----\n")

# Creación del gráfico tiempo vs nivel
def plot_time_water_level(tiempo, nivel_agua):

    # Crear figura y ejes
    fig, ax = plt.subplots()

    # Configuración del formato de fecha
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    # Configuración formato del gráfico
    ax.plot(tiempo, nivel_agua, color = 'blue', marker = 'o', linestyle = '-', markersize = 6, linewidth = 2, markerfacecolor = 'black')
    plt.xticks(rotation = 45)

    # Etiquetas y título
    plt.xlabel("Tiempo")
    plt.ylabel("Nivel de agua (cm)")
    plt.title("Gráfico tiempo vs nivel de agua (cm)")

    # Mostrar gráfico
    plt.tight_layout()
    plt.show()

# Programa principal   
if __name__ == "__main__":

    print("======================")
    print("        DEMO 2       ")
    print("======================") 

    # Creación del objeto modbus
    modbus0 = Modbus(port = "/dev/ttyUSB0", baudrate = 9600, bytesize = 8, parity = "N", stopbits = 1)
    verificar_conexion(modbus0)
    
    # Variables para guardar los valores que se plotearán
    niveles = []
    horas = []

    # Prueba de lectura del sensor de nivel de agua 
    try:
        while True:
            # registros_sensor = modbus0.leer_registros(registro_inicio = 0, num_registros = 10, esclavo = 1)
            # nivel_agua = registros_sensor[4]
            nivel_agua = random.randint(20, 30)
            niveles.append(nivel_agua)
            hora_actual = datetime.now()
            horas.append(hora_actual)
            print(f"El nivel de agua actualmente es de {nivel_agua} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        plot_time_water_level(horas, niveles)
        print("Programa finalizado por el usuario")