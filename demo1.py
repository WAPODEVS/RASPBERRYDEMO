# Librerías
import time
from pymodbus.client import ModbusSerialClient
import asyncio
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import ModbusRtuFramer

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
        self.client = ModbusSerialClient(self.port,self.framer,self.baudrate,self.bytesize,self.parity,self.stopbits,)
    
    def leer_registros(self, registro_inicio, num_registros,esclavo):
        try:
            self.rr =self.client.read_holding_registers(address = registro_inicio, count = num_registros, slave=esclavo)
        except Exception as exc:
            print(f"Error: {exc}")
            
        if self.rr.isError():
            print(f"Received Modbus library error({self.rr})")
        elif isinstance(self.rr, ExceptionResponse):
            print(f"Received Modbus library exception ({self.rr})")
        else:
            return self.rr.registers
        
    def leer_coils(self, coil_inicio, num_coils, esclavo):
        try:
            self.coils =self.client.read_coils(address = coil_inicio, count = num_coils, slave = esclavo)        
        except Exception as exc:
            print(f"Error: {exc}")
            
        if self.coils.isError():
            print(f"Received Modbus library error({self.coils})")
        elif isinstance(self.coils, ExceptionResponse):
            print(f"Received Modbus library exception ({self.coils})")
        else:
            return self.coils.registers

    def escribir_register(self, registro, valor, esclavo):
        try:
            self.client.write_register(address = registro,value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicación Modbus: {exc}")

    def escribir_coil(self,coil,valor,esclavo):
        try:
            self.client.write_coil(address = coil,value = valor, slave = esclavo)
        except Exception as exc:
            print(f"Error de comunicacion modbus:{exc}")
                
#programa principal   
if __name__ == "__main__":

    escritura_registros_flag = True

    # Creacion del objeto modbus
    modbus0 = Modbus(port = "RR", timeout = 10, baudrate = 9600, bytesize = 8, parity = "N", stopbits = 1)

    # Prueba de escritura de registros

    while escritura_registros_flag:
        registro = int(input("Ingrese la dirección del registro al que quiere escribir un valor"))
        value = int(input("Ingrese el valor que quiere enviar al esclavo"))
        slaveID = int(input("Ingresar el ID del esclavo al que desea enviar el dato"))

        modbus0.escribir_register(registro = registro, value = value, slave = slaveID)

        repeat = input("Desea seguir escribiendo registros? (Y\N)").lower()

        escritura_registros_flag = True if repeat == 'Y' else False

    # Prueba de lectura de registros
    
    registers_slave = modbus0.leer_registros()
