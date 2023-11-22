import smbus
import time
import csv

# Dirección del dispositivo ADXL345
ADXL345_ADDRESS = 0x53

# Registros del ADXL345
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATA_REGISTER = 0x32

# Configuración del bus I2C
bus = smbus.SMBus(1)

def init_adxl345():
    # Activar el acelerómetro (Poner en modo de medición)
    bus.write_byte_data(ADXL345_ADDRESS, POWER_CTL, 0x08)

    # Configurar el rango de medición a ±2g
    bus.write_byte_data(ADXL345_ADDRESS, DATA_FORMAT, 0x08)

def read_adxl345_data():
    # Leer datos de los registros X, Y, Z
    data = bus.read_i2c_block_data(ADXL345_ADDRESS, DATA_REGISTER, 6)
    
    # Convertir los datos a valores de aceleración
    x = data[1] << 8 | data[0]
    y = data[3] << 8 | data[2]
    z = data[5] << 8 | data[4]

    x = x if x < 32768 else x - 65536
    y = y if y < 32768 else y - 65536
    z = z if z < 32768 else z - 65536

    return x, y, z

def main():
    try:
        # Inicializar el ADXL345
        init_adxl345()

        # Crear archivo CSV para almacenar datos
        with open('sensor_data.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'X', 'Y', 'Z'])

            while True:
                # Leer datos del acelerómetro
                x, y, z = read_adxl345_data()

                # Obtener la marca de tiempo actual
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                # Imprimir datos en la consola
                print(f'Timestamp: {timestamp}, X: {x}, Y: {y}, Z: {z}')

                # Escribir datos en el archivo CSV
                csv_writer.writerow([timestamp, x, y, z])

                time.sleep(1)

    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")

if __name__ == "__main__":
    main()
