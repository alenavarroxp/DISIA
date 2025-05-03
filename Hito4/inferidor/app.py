import os
import glob
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Cargar modelo EfficientNetB0 más reciente
def cargar_modelo():
    modelos = glob.glob('/compartido/*.keras')
    if not modelos:
        raise FileNotFoundError("No se encontró ningún modelo .keras en /compartido")
    modelo_reciente = max(modelos, key=os.path.getctime)
    return load_model(modelo_reciente, compile=False)

try:
    modelo = cargar_modelo()
except FileNotFoundError as e:
    modelo = None
    print(e)

@app.route('/inferir', methods=['POST'])
def inferir():
    if modelo is None:
        return jsonify({"error": "Modelo no cargado correctamente, contacte al administrador."}), 500

    if 'imagen' not in request.files:
        return jsonify({"error": "No se encontró el archivo de imagen. Asegúrese de enviar un archivo con clave 'imagen'."}), 400

    file = request.files['imagen']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío. Por favor cargue una imagen válida."}), 400

    try:
        filepath = "/tmp/imagen.jpg"
        file.save(filepath)

        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predicciones = modelo.predict(img_array)

        transitado = 'si' if predicciones[0][0] > 0.5 else 'no'
        inundado = 'si' if predicciones[1][0] > 0.5 else 'no'

        resultado = {
            "imagen": file.filename,
            "inundado": inundado,
            "transitado": transitado
        }

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Error procesando la imagen: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
