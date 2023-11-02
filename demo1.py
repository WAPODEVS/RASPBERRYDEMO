# Librerías
from prettytable import PrettyTable
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.pdu import ExceptionResponse

# Clase Principal
class Modbus:
    def __init__(self, port, timeout, baudrate, bytesize, parity, stopbits):
        self.port=port
        self.framer=ModbusRtuFramer
        self.timeout=timeout
        self.baudrate=baudrate
        self.bytesize=bytesize
        self.parity=parity
        self.stopbits=stopbits
        self.client = ModbusSerialClient(self.port,self.framer,self.baudrate,self.bytesize,self.parity,self.stopbits)

        if self.client.connect():
            print("################")
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

    def escribir_register(self, registro, valor, esclavo):
        try:
            self.client.write_register(address = registro, value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicación Modbus: {exc}")

    def escribir_coil(self,coil,valor,esclavo):
        try:
            self.client.write_coil(address = coil,value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicacion Modbus: {exc}")
                
#programa principal   
if __name__ == "__main__":

    escritura_registros_flag = True
    lectura_registros_flag = True

    # Creacion del objeto modbus
    modbus0 = Modbus(port = "COM4", timeout = 10, baudrate = 9600, bytesize = 8, parity = "N", stopbits = 1)

    # Prueba de escritura de registros

    print("================================")
    print("Prueba de escritura de registros")
    print("================================")

    while escritura_registros_flag:

        registro = int(input("Ingrese la dirección del registro al que quiere escribir un valor : "))
        valor = int(input("Ingrese el valor que quiere enviar al esclavo : "))
        slaveID = int(input("Ingresar el ID del esclavo al que desea enviar el dato : "))

        modbus0.escribir_register(registro = registro, valor = valor, esclavo = slaveID)

        repeat = input("Desea seguir escribiendo registros? (Y/N) : ").upper()

        escritura_registros_flag = True if repeat == 'Y' else False

    # Prueba de lectura de registros

    print("================================")
    print("Prueba de lectura de registros")
    print("================================")

    while lectura_registros_flag:

        registro_inicio = int(input("Ingrese la dirección del registro donde se iniciará la lectura : "))
        num_registros = int(input("Ingrese la cantidad de registros que desea leer : "))
        slaveID = int(input("Ingresar el ID del esclavo al que desea enviar el dato : "))

        registros_esclavo = modbus0.leer_registros(registro_inicio = registro_inicio, num_registros = num_registros, esclavo = slaveID)

        print("\nSe leyeron los siguientes registros : \n")
        table = PrettyTable()
        table.field_names = ["Registro", "Valor"]
        for i, v in enumerate(registros_esclavo):
            table.add_row([i, v])
        print(table)
        
        repeat = input("Desea seguir leyendo registros? (Y/N) : ").upper()

        lectura_registros_flag = True if repeat == 'Y' else False