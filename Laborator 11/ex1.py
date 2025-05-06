from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

director = "directory"

if not os.path.exists(director):
    os.makedirs(director)

@app.route("/")
def hello():
    return """
    <h1>Bine ai venit!</h1>
    <p>Foloseste rutele de mai jos pentru a accesa diferite functionalitati:</p>
    <ul>
        <li><a href="/files">http://localhost:5000/files</a> - listarea continutului directorului</li>
        <li>http://localhost:5000/files/&lt;nume&gt; - listarea continutului unui fisier (ex: /files/exemplu.txt)</li>
        <li>http://localhost:5000/files/&lt;nume&gt; - PUT- crearea unui fisier specificat prin nume si continut (se foloseste de ex Postman/curl)</li>
        <li>http://localhost:5000/files - POST- crearea unui fisier cu continut (numele este generat automat) (Postman/curl)</li>
        <li>http://localhost:5000/files/&lt;nume&gt; - stergerea unui fisier (Postman/curl)</li>
        <li>http://localhost:5000/files/&lt;nume&gt; - PUT- modificarea continutului unui fisier (Postman/curl)</li>
    </ul>
    """

@app.route('/files', methods=['GET'])
def afisare():
    fisiere = os.listdir(director)

    if not fisiere:
        return """
        <h2>Fisiere disponibile:</h2>
        <p>Momentan nu exista fisiere in director.</p>
        <p>Poti crea un fisier folosind metoda <strong>PUT</strong>de ex in Postman/curl, la adresa:<br>
        http://localhost:5000/files/&lt;nume&gt;</p>
        """
    
    html = "<h2>Fisiere disponibile:</h2><ul>"
    for fisier in fisiere:
        html += f'<li><a href="/files/{fisier}">{fisier}</a></li>'
    html += "</ul>"
    return html

@app.route('/files/<nume>', methods=['GET'])
def citire_fisier(nume):
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
