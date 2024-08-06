import subprocess
import time
import signal
import sys
import logging

# Configuración del logging
logging.basicConfig(filename='pairing_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Variable para controlar el estado del bucle
running = True

def signal_handler(sig, frame):
    global running
    logging.info("Interrupción recibida. Terminando...")
    running = False

def send_pairing_requests(interval):
    while running:
        try:
            # Ejecuta el comando y captura la salida
            result = subprocess.run(["hcitool", "-i", "hci0", "scan"], capture_output=True, text=True, check=True)
            logging.info(f"Escaneo realizado con éxito:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error en la ejecución del comando: {e}")
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    # Intervalo de escaneo (en segundos)
    scan_interval = 1
    
    # Configura el manejador de señales para permitir la terminación del script con Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    logging.info("Iniciando el proceso de escaneo de emparejamiento.")
    send_pairing_requests(scan_interval)
    logging.info("Proceso terminado.")
