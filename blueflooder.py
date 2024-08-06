import subprocess
import time
import threading
import logging

# Configuración del logging
logging.basicConfig(filename='flood_messages.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Flooder:
    def __init__(self, command, interval=1):
        self.command = command
        self.interval = interval
        self._stop_event = threading.Event()

    def _send_command(self):
        try:
            # Ejecutar el comando usando subprocess para mayor control
            result = subprocess.run(self.command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info(f"Comando ejecutado con éxito: {result.stdout.decode().strip()}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al ejecutar el comando: {e.stderr.decode().strip()}")

    def start(self):
        logging.info("Iniciando el flooder...")
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while not self._stop_event.is_set():
            self._send_command()
            time.sleep(self.interval)

    def stop(self):
        logging.info("Deteniendo el flooder...")
        self._stop_event.set()
        self.thread.join()
        logging.info("Flooder detenido.")

def main():
    # Configuración del comando y el intervalo
    command = ["hcitool", "-i", "hci0", "cmd", "0x08", "0x0004", "01", "00"]
    interval = 1  # Intervalo en segundos

    flooder = Flooder(command, interval)
    
    try:
        flooder.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupción del usuario. Terminando...")
    finally:
        flooder.stop()

if __name__ == "__main__":
    main()
