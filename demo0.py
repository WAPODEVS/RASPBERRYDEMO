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
    modbusConnection.write_register(address = 4, value = 10, slave = 5)