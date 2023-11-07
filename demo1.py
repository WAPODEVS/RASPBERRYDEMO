# Librerías
from prettytable import PrettyTable
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.pdu import ExceptionResponse

# Clase Principal
class Modbus:
    def __init__(self, port, timeout, baudrate, bytesize, parity, stopbits):
        self.port = port
        self.framer = ModbusRtuFramer
        self.timeout = timeout
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

# Tabla menu
def print_menu_table():
    tabla_menu = PrettyTable()
    tabla_menu.field_names = ["Opcion", "Descripcion"]
    tabla_menu.add_row(["1", "Escribir registros"])
    tabla_menu.add_row(["2", "Leer registros"])
    tabla_menu.add_row(["3", "Salir"])
    print(tabla_menu)

# Prueba de escritura de registros
def escribir_registros_demo():
    registro = int(input("Ingrese la dirección del registro al que quiere escribir un valor : "))
    valor = int(input("Ingrese el valor que quiere enviar al esclavo : "))
    slaveID = int(input("Ingresar el ID del esclavo al que desea enviar el dato : "))
    modbus0.escribir_registro(registro = registro, valor = valor, esclavo = slaveID)

# Prueba de lectura de registros
def leer_registros_demo():
    registro_inicio = int(input("Ingrese la dirección del registro donde se iniciará la lectura : "))
    num_registros = int(input("Ingrese la cantidad de registros que desea leer : "))
    slaveID = int(input("Ingresar el ID del esclavo al cual desea leer los registros : "))

    registros_esclavo = modbus0.leer_registros(registro_inicio = registro_inicio, num_registros = num_registros, esclavo = slaveID)

    print("\nSe leyeron los siguientes registros : \n")
    table = PrettyTable()
    table.field_names = ["Registro", "Valor"]
    for i, v in enumerate(registros_esclavo):
        table.add_row([i + registro_inicio, v])
    print(table)   

# Comprando la conexión
def verificar_conexion():
    if modbus0.client.connect():
        print("\n----CONEXION EXITOSA----\n")

# Programa principal   
if __name__ == "__main__":

    print("======================")
    print("        DEMO 1       ")
    print("======================")

    # Creacion del objeto modbus
    modbus0 = Modbus(port = "/dev/ttyUSB0", timeout = 10, baudrate = 9600, bytesize = 8, parity = "N", stopbits = 1)
    verificar_conexion()

    while True:
        print_menu_table()
        opcion = input("Ingrese una opcion : ")

        if opcion not in ["1", "2", "3"]:
            print("Esta opcion no existe. Vuelva a intentarlo.")
        elif opcion == '1':
            escribir_registros_demo()
        elif opcion == '2':
            leer_registros_demo()
        else:
            print("Programa terminado")
            break