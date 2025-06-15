import meshtastic
import time
import threading
import logging
from meshtastic.serial_interface import SerialInterface
import platform

sistem = platform.system()

# CONFIGURAÇÃO DO LOGGING
logging.basicConfig(
    filename="meshtastic_log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# CONFIGURAÇÃO DA PORTA SERIAL
if sistem == "Windows":
    PORTA_SERIAL = "COM3"
else:
    PORTA_SERIAL = "/dev/ttyACM0"

# CONECTAR AO DISPOSITIVO
device = SerialInterface(PORTA_SERIAL)

# FUNÇÃO DE ENVIO DE MENSAGEM
def send_message(device, message, channel=0):
    device.sendText(message, channelIndex=channel)
    print(f"[ENVIADO] {message}")
    logging.info(f"[ENVIADO] {message}")

# CALLBACK PARA RECEBER MENSAGENS
def on_receive(packet, interface):
    try:
        logging.info(f"Pacote recebido {packet}")
        
        msg = packet['decoded']['text']
        print(f"[RECEBIDO] {msg}")
        logging.info(f"[RECEBIDO] {msg} | RAW: {packet}")
    except Exception as e:
        logging.error(f"Erro ao processar pacote recebido: {e}")

# REGISTRA O CALLBACK
device.onReceive = on_receive
print("✅ Comunicação Meshtastic iniciada.")
print("Digite mensagens para enviar. Digite 'sair' para encerrar.\n")

# VARIÁVEL DE CONTROLE PARA ENCERRAMENTO
running = True

# LOOP DE ENTRADA DO USUÁRIO EM UMA THREAD
def input_loop():
    global running
    while running:
        try:
            msg = input("Mensagem: ")
            if msg.lower() == 'sair':
                print("Encerrando comunicação...")
                running = False
                device.close()
                break
            send_message(device, msg)
        except Exception as e:
            logging.error(f"Erro na entrada de mensagem: {e}")

# INICIA THREAD DE ENTRADA
input_thread = threading.Thread(target=input_loop)
input_thread.daemon = True
input_thread.start()

# LOOP PRINCIPAL PARA MANTER O SCRIPT RODANDO
try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    device.close()
    running = False
    print("\nInterrompido manualmente.")
    logging.info("Encerrado por KeyboardInterrupt.")

print("🔒 Comunicação encerrada.")
logging.info("Comunicação finalizada.")
