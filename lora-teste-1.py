import meshtastic
from meshtastic.serial_interface import SerialInterface
import time
import logging
import platform

sistem = platform.system()

# Configurar logging para depuração detalhada
logging.basicConfig(
    filename="meshtastic_log.txt",
    filemode="a",
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Conectar ao dispositivo Meshtastic via serial

if sistem == "Windows":
    PORTA_SERIAL = "COM3"
else:
    PORTA_SERIAL = "/dev/ttyACM0"

try:
    device = SerialInterface(PORTA_SERIAL)  # Ajuste a porta serial se necessário
    logging.info("Conectado ao dispositivo Meshtastic na porta COM5")
except Exception as e:
    logging.error(f"Erro ao conectar ao dispositivo: {e}")
    exit(1)

# Função para receber mensagens
def on_receive(packet, interface):
    try:
        # Log detalhado de todos os pacotes recebidos
        logging.debug(f"Pacote recebido: {packet}")
        # Verificar se é uma mensagem de texto
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            sender = packet.get('from', 'Unknown')  # ID do nó remetente
            message = packet['decoded']['text']
            # Tentar obter o nome do remetente, se disponível
            try:
                node_info = interface.getNode(sender)
                sender_name = node_info.get('user', {}).get('longName', sender)
            except Exception as e:
                logging.warning(f"Erro ao obter nome do remetente {sender}: {e}")
                sender_name = sender
            print(f"Mensagem recebida de {sender_name}: {message}")
            logging.info(f"Mensagem recebida de {sender_name}: {message}")
        else:
            logging.debug(f"Pacote ignorado (não é mensagem de texto): {packet.get('decoded', {}).get('portnum', 'N/A')}")
    except Exception as e:
        logging.error(f"Erro ao processar pacote: {e}")

# Registrar callback para receber mensagens
try:
    device.onReceive = on_receive
    logging.info("Callback de recebimento registrado com sucesso")
except Exception as e:
    logging.error(f"Erro ao registrar callback: {e}")
    try:
        device.close()
    except:
        pass
    exit(1)

print("Escutando mensagens da rede mesh... (Pressione Ctrl+C para encerrar)")

try:
    while True:
        time.sleep(0.05)  # Pausa curta para manter a escuta sem sobrecarga
except KeyboardInterrupt:
    print("\nPrograma interrompido pelo usuário")
    logging.info("Programa interrompido pelo usuário")
finally:
    try:
        device.close()
        print("Comunicação encerrada.")
        logging.info("Comunicação encerrada.")
    except Exception as e:
        logging.error(f"Erro ao fechar a conexão: {e}")