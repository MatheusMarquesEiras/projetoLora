from datetime import datetime

agora = datetime.now()

# Formatar data e hora
formatado = agora.strftime("%d/%m/%Y %H:%M:%S")

print("Data e hora atual formatada: " + formatado)
