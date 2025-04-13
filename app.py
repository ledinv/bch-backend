from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Lee la clave desde las variables de entorno; asegúrate de que en Render o tu entorno la variable se llame BCH_API_KEY.
API_KEY = os.environ.get("BCH_API_KEY")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    # Endpoint según la documentación del producto bchapi-fnc
    url = "https://bchapi-am.developer.azure-api.net/bchapi-fnc/api/v1/indicadores/cifras/620?formato=json"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 200 OK.
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
    # Usa el puerto asignado por Render (o 10000 si no está definido)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
