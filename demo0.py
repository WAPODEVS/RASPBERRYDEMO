# Librerías
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer

# Programa principal

if __name__ == "__main__":

    print("======================")
    print("        DEMO 0       ")
    print("======================")

    # Creación del objeto modbus
    modbusConnection = ModbusSerialClient(port = "/dev/ttyUSB0", framer = ModbusRtuFramer, baudrate = 9600, bytesize = 8, 
                        parity = "N", stopbits = 1)
    
    # Verificar la conexión
    if modbusConnection.connect():
        print("\n----CONEXION EXITOSA----\n")

    # Escritura de datos (0x06)
    registro = int(input("Ingrese la dirección del registro al que quiere escribir un valor : "))
    valor = int(input("Ingrese el valor que quiere enviar al esclavo : "))
    slaveID = int(input("Ingresar el ID del esclavo al que desea enviar el dato : "))
    modbusConnection.write_register(address = registro, value = valor, slave = slaveID)