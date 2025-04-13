from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("BCH_API_KEY")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    url = "https://bchapi-am.developer.azure-api.net/api/v1/indicadores/620/cifras?formato=json"
    headers = {
        "clave": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            valor = data[0].get("valor")
            return jsonify({"valor": round(float(valor), 2)})
        return jsonify({"error": "No se encontró el valor"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
