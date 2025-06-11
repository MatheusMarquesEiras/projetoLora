import meshtastic
import time
from meshtastic.serial_interface import SerialInterface

# Conectar aos dispositivos via serial (ajuste as portas conforme necessário)
device1 = SerialInterface("COM6")
#
# Função para enviar mensagem
def send_message(device, message, channel=0):
    device.sendText(message, channelIndex=channel)
    print(f"Mensagem enviada: {message}")

# Função para receber mensagens
def on_receive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        print(f"Mensagem recebida em {interface}: {packet['decoded']['text']}")

# Registrar callbacks para receber mensagens
device1.onReceive = on_receive
#device2.onReceive = on_receive

print("Comunicação Meshtastic iniciada!")
print("Digite mensagens para enviar de Device1 para Device2 ou 'sair' para encerrar.")

try:
    while True:
        message = input("Mensagem: ")
        if message.lower() == 'sair':
            break
        send_message(device1, message)
        time.sleep(0.5)  # Pequena pausa para evitar sobrecarga
finally:
    # Fechar as conexões
    device1.close()
    #device2.close()
    print("Comunicação encerrada.")