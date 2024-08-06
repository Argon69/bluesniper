import subprocess
import time
import argparse
import re

def scan_devices():
    """Escanea dispositivos Bluetooth cercanos y los muestra."""
    try:
        result = subprocess.run(
            ["hcitool", "scan"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("\nDispositivos encontrados:\n")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error al escanear dispositivos: {e}")

def flood_data(interface, device_address, interval):
    """Envía paquetes a un dispositivo Bluetooth específico."""
    try:
        while True:
            # El comando para enviar datos podría variar dependiendo del uso
            command = ["hcitool", "-i", interface, "leadv", device_address]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(result.stdout.decode())
            time.sleep(interval)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except KeyboardInterrupt:
        print("\nInterrupción por el usuario. Terminando...")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

def get_device_address():
    """Solicita la dirección del dispositivo Bluetooth al usuario."""
    address_pattern = re.compile(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}")
    while True:
        address = input("Introduce la dirección del dispositivo Bluetooth (formato XX:XX:XX:XX:XX:XX): ")
        if address_pattern.fullmatch(address):
            return address
        print("Dirección inválida. Por favor, usa el formato XX:XX:XX:XX:XX:XX.")

def main():
    print("Bienvenido al script de gestión de Bluetooth")
    print("Seleccione una opción:")
    print("1. Escanear dispositivos Bluetooth cercanos")
    print("2. Enviar paquetes a un dispositivo específico")
    print("3. Salir")

    while True:
        choice = input("\nIntroduce el número de la opción deseada: ")

        if choice == '1':
            scan_devices()
        elif choice == '2':
            interface = input("Introduce la interfaz Bluetooth (por ejemplo, hci0): ")
            device_address = get_device_address()
            interval = float(input("Introduce el intervalo en segundos entre comandos (por defecto 1.0): ") or "1.0")
            flood_data(interface, device_address, interval)
        elif choice == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 3.")

if __name__ == "__main__":
    main()
