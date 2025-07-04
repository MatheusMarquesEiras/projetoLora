from app import app
from flask import request, jsonify
from db.functions import create_user, create_record, get_records
import meshtastic
import datetime, time
from pubsub import pub
import threading
import datetime
from db.configs import Base, DBConnectionHandler

interface = None  # vai ser inicializado em uma função

import json

if False:  # Mudar para True quando for usar o Lora
    import meshtastic.serial_interface

    def onReceive(packet, interface):
        print("Mensagem recebida:")
        try:
            data = packet['decoded']['text']
            print(data)
            data_dict = json.loads(data.replace("'", '"'))
            date_str = data_dict['date']
            date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
            create_record(hash=data_dict['hash'], date=date_obj)
        except KeyError:
            pass
            # print("Pacote recebido, mas sem texto")
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
        except Exception as e:
            print(f"erro: {e}")


    def iniciar_lora():
        global interface
        try:
            interface = meshtastic.serial_interface.SerialInterface()
            pub.subscribe(onReceive, "meshtastic.receive")
            print("Lora ligado")
        except Exception as e:
            print("Erro ao iniciar o Lora:", e)

    # Inicia o Lora em uma thread separada, para não travar o Flask
    threading.Thread(target=iniciar_lora, daemon=True).start()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        create_user(username=username, password=password)

        return jsonify({'message': 'deu boa', "username": username, "password": password})
    
    except Exception as e:
        return jsonify({"message": "deu ruim", "error": str(e)})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        return jsonify({'message': 'deu boa', "username": username, "password": password})
    
    except Exception as e:
        return jsonify({"message": "deu ruim", "error": str(e)})

@app.route('/get_data', methods=['GET'])
def get_data():
    records = get_records()
    records_dict = [record.to_dict() for record in records]
    return jsonify(records_dict)

if __name__ == "__main__":
    with DBConnectionHandler() as db: 
        engine = db.get_engine()
        Base.metadata.create_all(engine)
        for i in range(5):
            now = datetime.datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")
            create_record(hash=i, date=now)
            print(f"Data e hora atual: {date}")
            time.sleep(1)
    app.run( host='0.0.0.0', port=8890)
