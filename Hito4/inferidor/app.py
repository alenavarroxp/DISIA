from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/inferir', methods=['POST'])
def inferir():
    return jsonify({"mensaje": "Llamada al inferidor recibida."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)