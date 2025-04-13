from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Lee la clave desde las variables de entorno en Render
API_KEY = os.environ.get("BCH_API_KEY")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    # URL CORREGIDA
    url = "https://bchapi-am.developer.azure-api.net/api/v1/indicadores/cifras/620?formato=json"
    headers = {
        "clave": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # data suele ser una lista con al menos un objeto
        if isinstance(data, list) and len(data) > 0:
            valor = data[0].get("valor")
            return jsonify({"valor": round(float(valor), 2)})
        return jsonify({"error": "No se encontró el valor"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint de ping para mantener despierto
@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # El puerto 10000 es opcional; depende de la config de Render
    app.run(host="0.0.0.0", port=10000)
