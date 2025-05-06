from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

director = "directory"

if not os.path.exists(director):
    os.makedirs(director)

@app.route("/")
def hello():
    fisiere = os.listdir(director)
    return fisiere

@app.route('/files', methods=['GET'])
def afisare():
    fisiere = os.listdir(director)
    return fisiere

@app.route('/files/<nume>', methods=['GET'])
def citire_nume(nume):
    cale = os.path.join(director, nume)

    if not os.path.isfile(cale):
        return jsonify({'error': 'Fisierul nu exista!!!!'}), 404
    
    with open(cale, 'r', encoding='utf-8') as f:
        continut = f.read()

    return jsonify({'nume': nume, 'continut': continut})


@app.route('/files/<nume>', methods=['PUT'])
def creare_fisier(nume):
    continut = request.json.get("continut", "")

    cale = os.path.join(director, nume)

    with open(cale, 'w', encoding='utf-8') as f:
        f.write(continut)
    return jsonify({'mesaj': 'Fisierul a fost creat cu succes!', 'nume': nume})

i = 0
@app.route('/files', methods=['POST'])
def creare_fisier_continut():
    global i
    continut = request.json.get("continut", "")
    nume = f"fisier{i}.txt"

    cale = os.path.join(director, nume)

    with open(cale, 'w', encoding='utf-8') as f:
        f.write(continut)
    
    i=i+1

    return jsonify({'mesaj': 'Fisierul a fost creat cu succes!', 'nume': nume})

@app.route('/files/<nume>', methods=['DELETE'])
def stergere_fisier(nume):
    cale = os.path.join(director, nume)

    if not os.path.isfile(cale):
        return jsonify({'error': 'Fisierul nu exista!!!!'}), 404
    
    os.remove(cale)

    return jsonify({'mesaj': 'Fisierul a fost sters cu succes!', 'nume': nume})

#update se poate face deja prin crearea cu PUT
# @app.route('/files/<nume>', methods=['PUT'])
# def modificare_fisier(nume):
#     cale = os.path.join(director, nume)

#     if not os.path.isfile(cale):
#         return jsonify({'error': 'Fisierul nu exista!!!!'}), 404
    
#     continut = request.json.get("continut", "")

#     with open(cale, 'w', encoding='utf-8') as f:
#         f.write(continut)
#     return jsonify({'mesaj': 'Fisierul a fost modificat cu succes!', 'nume': nume})

if __name__ == "__main__":
    app.run()