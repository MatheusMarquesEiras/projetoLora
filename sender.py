
from meshtastic.serial_interface import SerialInterface
import platform
from datetime import datetime

sistem = platform.system()

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

print("✅ Comunicação Meshtastic iniciada.")
print("Digite mensagens para enviar. Digite 'sair' para encerrar.\n")

# LOOP PRINCIPAL PARA MANTER O SCRIPT RODANDO
try:
    while True:
        try:
            msg = input("Mensagem: ")
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")
            msg = f"{{'hash': '{msg}', 'date': '{date}'}}"
            if msg.lower() == 'sair':
                print("Encerrando comunicação...")
                device.close()
                break
            send_message(device, msg)
        except Exception as e:
            print(f"Erro na entrada de mensagem: {e}")
except KeyboardInterrupt:
    device.close()
    print("\nInterrompido manualmente.")

print("🔒 Comunicação encerrada.")
