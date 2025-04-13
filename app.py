from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Lee la clave desde las variables de entorno.
API_KEY = os.environ.get("BCH_API_KEY", "72f7ce1eed9746b3af662b7104fc0432")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    # Usamos la URL que probaste
    url = "https://bchapi-am.azure-api.net/api/v1/indicadores/620/cifras?formato=json"
    headers = {
        "Cache-Control": "no-cache",
        "clave": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si no es 200
        data = response.json()
        # DEBUG: Imprimir datos recibidos (solo si es posible ver logs)
        print("DEBUG - Data recibida:", data)
        
        if isinstance(data, list) and len(data) > 0:
            valor = data[0].get("valor")
            # Si no existe, intenta con mayúscula
            if valor is None:
                valor = data[0].get("Valor")
            if valor is None:
                return jsonify({"error": "La propiedad 'valor' no se encontró en la respuesta."}), 404
            return jsonify({"valor": round(float(valor), 2)})
        return jsonify({"error": "No se encontró el valor"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
