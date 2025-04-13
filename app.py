from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Lee la clave desde la variable de entorno.
# Si deseas testear directamente, puedes usar el valor por defecto (¡pero recuerda quitarlo después!)
API_KEY = os.environ.get("BCH_API_KEY", "72f7ce1eed9746b3af662b7104fc0432")

@app.route('/api/tipo-cambio-bch')
def tipo_cambio_bch():
    # Usamos la URL tal cual como la mostró el request.
    url = "https://bchapi-am.azure-api.net/api/v1/indicadores/620/cifras"
    # Configuramos los headers exactamente como en la petición:
    headers = {
        "Cache-Control": "no-cache",
        "clave": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto arrojará un error si la respuesta no es 200 OK.
        data = response.json()

        # Se espera recibir un array con al menos un objeto "Cifra"
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
    # Render asigna el puerto en la variable PORT, usamos 10000 como fallback.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
