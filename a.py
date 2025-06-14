import meshtastic
from meshtastic.serial_interface import SerialInterface
import serial.tools.list_ports
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='meshtastic.log')

# Listar portas seriais disponíveis
print("Portas seriais disponíveis:")
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

# Conectar ao dispositivo Meshtastic via serial
port = "COM3"  # Ajuste para a porta correta após verificar
try:
    device = SerialInterface(port)
    print(f"Conectado ao dispositivo Meshtastic na porta {port}")
except Exception as e:
    print(f"Erro ao conectar ao dispositivo: {e}")
    logging.error(f"Erro ao conectar ao dispositivo: {e}")
    exit(1)

# Função para enviar mensagem
def send_message(device, message, channel=0):
    try:
        device.sendText(message, channelIndex=channel)
        print(f"Mensagem enviada: {message}")
        logging.info(f"Mensagem enviada: {message}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        logging.error(f"Erro ao enviar mensagem: {e}")

# Função para receber mensagens
def on_receive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            sender = packet.get('fromId', 'Unknown')
            message = packet['decoded'].get('text', '')
            if not message:
                try:
                    message = packet['decoded']['payload'].decode('utf-8', errors='ignore')
                except:
                    logging.error("Erro ao decodificar payload")
                    return
            print(f"{sender}: {message}", flush=True)
            logging.info(f"Mensagem recebida de {sender}: {message}")
    except Exception as e:
        logging.error(f"Erro ao processar pacote: {e}")

# Registrar callback para receber mensagens
try:
    device.onReceive = on_receive
    print("Escutando mensagens da rede mesh...")
    print("Digite mensagens para enviar ou 'sair' para encerrar.")
except Exception as e:
    print(f"Erro ao registrar callback: {e}")
    logging.error(f"Erro ao registrar callback: {e}")
    try:
        device.close()
    except:
        pass
    exit(1)

try:
    while True:
        message = input("Mensagem: ")
        if message.lower() == 'sair':
            break
        send_message(device, message)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nPrograma interrompido pelo usuário")
    logging.info("Programa interrompido pelo usuário")
finally:
    try:
        device.close()
        print("Comunicação encerrada.")
        logging.info("Comunicação encerrada.")
    except Exception as e:
        print(f"Erro ao fechar a conexão: {e}")
        logging.error(f"Erro ao fechar a conexão: {e}")