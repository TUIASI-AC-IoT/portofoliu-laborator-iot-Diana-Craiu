import io
from flask import Flask, send_file,jsonify,request
import os.path
import random
import socket

app = Flask(__name__)

CONFIG_DIR = "config_files"
ESP32_IP = "192.168.89.14"
ESP32_PORT = 10001

director = "directory"

if not os.path.exists(director):
    os.makedirs(director)

def send_udp_command(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ESP32_IP, ESP32_PORT))
    sock.close()

@app.route('/firmware.bin')
def firm():
    with open(".pio\\build\\esp-wrover-kit\\firmware.bin", 'rb') as bites:
        print(bites)
        return send_file(
                     io.BytesIO(bites.read()),
                     mimetype='application/octet-stream'
               )

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/sensor/<sensor_id>', methods=['GET'])
def citire_senzor(sensor_id):
    valoare = round(random.uniform(15.0, 40.0), 2)
    return jsonify({'sensor_id': sensor_id, 'valoare_masurata': valoare})


@app.route('/sensor/<sensor_id>', methods=['POST'])
def creare_config_senzor(sensor_id):
    nume_fisier = f"config_{sensor_id}.txt"
    cale = os.path.join(director, nume_fisier)

    if os.path.exists(cale):
        return jsonify({
            'error': 'Configurarea exista deja!',
            'details': 'Foloseste PUT pentru a modifica configuratia.'
        }), 409

    continut = request.json.get("continut", "")
    with open(cale, 'w', encoding='utf-8') as f:
        f.write(continut)

    return jsonify({'mesaj': 'Configurarea a fost creata.', 'fisier': nume_fisier})


@app.route('/sensor/<sensor_id>', methods=['PUT'])
def modificare_config_senzor(sensor_id):
    nume_fisier = f"config_{sensor_id}.txt"
    cale = os.path.join(director, nume_fisier)

    if not os.path.exists(cale):
        return jsonify({
            'error': 'Configurarea nu exista!',
            'details': 'Pentru a crea o configuratie noua se foloseste POST.'
        }), 409

    continut = request.json.get("continut", "")
    with open(cale, 'w', encoding='utf-8') as f:
        f.write(continut)

    return jsonify({'mesaj': 'Configurarea a fost modificata.', 'fisier': nume_fisier})


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('ca_cert.pem', 'ca_key.pem'), debug=True)