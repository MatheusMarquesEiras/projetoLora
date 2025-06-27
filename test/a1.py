import datetime

while True:
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"Data e hora atual: {date}")
    input("Pressione Enter para continuar...")
    