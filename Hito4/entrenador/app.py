from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/train', methods=['GET'])
def train():
    return jsonify({"mensaje": "Llamada al entrenador recibida, entrenamiento iniciado."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)