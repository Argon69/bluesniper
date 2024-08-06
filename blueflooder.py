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
        print("Dispositivos encontrados:")
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
    parser = argparse.ArgumentParser(description="Envía comandos a un dispositivo Bluetooth repetidamente.")
    parser.add_argument("interface", type=str, help="La interfaz Bluetooth a usar (por ejemplo, hci0).")
    parser.add_argument("--scan", action="store_true", help="Escanea dispositivos Bluetooth cercanos.")
    parser.add_argument("--interval", type=float, default=1.0, help="Intervalo en segundos entre comandos.")
    
    args = parser.parse_args()
    
    if args.scan:
        scan_devices()
        return
    
    device_address = get_device_address()
    flood_data(args.interface, device_address, args.interval)

if __name__ == "__main__":
    main()
