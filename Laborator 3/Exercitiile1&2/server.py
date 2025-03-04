import io
from flask import Flask, send_file, jsonify
import os.path

app = Flask(__name__)

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

@app.route('/versionNumber')
def versionNumber():
    try:
        with open('versioning') as f:
            version = f.readline().strip()
        return jsonify({"version": version})
    except FileNotFoundError:
        return jsonify({"error": "version.h not found"}), 404
    
@app.route('/version')
def version():
    try:
        with open('include/version.h', 'r') as version_file:
            version = version_file.read().strip()
        return jsonify({"version": version})
    except FileNotFoundError:
        return jsonify({"error": "version.h not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('ca_cert.pem', 'ca_key.pem'), debug=True)