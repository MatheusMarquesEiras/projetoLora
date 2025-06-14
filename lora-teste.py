import meshtastic
import time
import logging
from meshtastic.serial_interface import SerialInterface

# Configurar o logging
logging.basicConfig(
    filename="meshtastic_log.txt",
    filemode="a",  # "a" para adicionar, "w" para sobrescrever a cada execução
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Conectar ao dispositivo Meshtastic via porta USB
device1 = SerialInterface("/dev/ttyACM0")  # Altere conforme a porta correta

# Função para enviar mensagem
def send_message(device, message, channel=0):
    device.sendText(message, channelIndex=channel)
    print(f"Mensagem enviada: {message}")
    logging.info(f"Mensagem enviada: {message}")

# Função para receber mensagens
def on_receive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        received_msg = packet['decoded']['text']
        print(f"Mensagem recebida em {interface}: {received_msg}")
        logging.info(f"Mensagem recebida em {interface}: {received_msg} | Raw: {packet}")

# Registrar callback para receber mensagens
device1.onReceive = on_receive

print("Comunicação Meshtastic iniciada!")
print("Digite mensagens para enviar ou 'sair' para encerrar.")

try:
    while True:
        message = input("Mensagem: ")
        if message.lower() == 'sair':
            break
        send_message(device1, message)
        time.sleep(0.5)  # Pausa para evitar sobrecarga
finally:
    device1.close()
    print("Comunicação encerrada.")
    logging.info("Comunicação encerrada.")
