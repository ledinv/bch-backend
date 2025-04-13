from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("BCH_API_KEY", "72f7ce1eed9746b3af662b7104fc0432")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    url = "https://bchapi-am.azure-api.net/api/v1/indicadores/620/cifras"
    headers = {
        "Cache-Control": "no-cache",
        "clave": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            # Supongamos que la clave es "valor" en minúsculas
            valor = data[0].get("valor")
            # Si no existe, prueba con "Valor"
            if valor is None:
                valor = data[0].get("Valor")
            if valor is None:
                return jsonify({"error": "No se encontró la clave 'valor'"}), 404

            # 1) Convertir a float
            valor_float = float(valor)
            # 2) Formatear a 4 decimales y devolver como string
            valor_str = f"{valor_float:.4f}"

            return jsonify({"valor": valor_str})
        return jsonify({"error": "No se encontró el valor"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
