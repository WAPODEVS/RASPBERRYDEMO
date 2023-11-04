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

        if self.client.connect():
            print("\n################")
            print("Conexión exitosa")
            print("################\n")
    
    def leer_registros(self, registro_inicio, num_registros,esclavo):

        rr = self.client.read_holding_registers(address = registro_inicio, count = num_registros, slave=esclavo)
            
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
                
#programa principal   
if __name__ == "__main__":

    # Creacion del objeto modbus
    modbus0 = Modbus(port = "COM4", timeout = 10, baudrate = 9600, bytesize = 8, parity = "N", stopbits = 1)

    # Verificando la conexión
    if modbus0.client.connect():
        print("================")
        print("Conexión exitosa")
        print("================\n")       








