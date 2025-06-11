import meshtastic
import time
from meshtastic.serial_interface import SerialInterface

# Conectar ao dispositivo Meshtastic via porta USB
device1 = SerialInterface("/dev/ttyACM1")  # Porta identificada para o dispositivo Meshtastic

# Função para enviar mensagem
def send_message(device, message, channel=0):
    device.sendText(message, channelIndex=channel)
    print(f"Mensagem enviada: {message}")

# Função para receber mensagens
def on_receive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        print(f"Mensagem recebida em {interface}: {packet['decoded']['text']}")

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
        time.sleep(0.5)  # Pequena pausa para evitar sobrecarga
finally:
    # Fechar a conexão
    device1.close()
    print("Comunicação encerrada.")