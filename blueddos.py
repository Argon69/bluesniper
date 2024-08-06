import subprocess
import time
import argparse

def flood_data(interface, interval):
    try:
        while True:
            # Usa subprocess para ejecutar el comando y captura su salida
            result = subprocess.run(
                ["hcitool", "-i", interface, "leadv"],
                check=True,  # Lanza una excepción si el comando falla
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Imprime la salida del comando, si es necesario
            print(result.stdout.decode())
            time.sleep(interval)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except KeyboardInterrupt:
        print("\nInterrupción por el usuario. Terminando...")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envía comandos a un dispositivo Bluetooth repetidamente.")
    parser.add_argument("interface", type=str, help="La interfaz Bluetooth a usar (por ejemplo, hci0).")
    parser.add_argument("--interval", type=float, default=1.0, help="Intervalo en segundos entre comandos.")

    args = parser.parse_args()
    flood_data(args.interface, args.interval)
