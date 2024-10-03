from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "b4fewpnrw63fxilykl7z-mysql.services.clever-cloud.com",
    "user": "uk0za9yhjsjmmpuy",
    "password": "eARyZjZuCQETChusm6wW",
    "database": "b4fewpnrw63fxilykl7z",
    "port": 3306
}

@app.route("/data", methods=["POST"])
def insert_data():
    try:
        if not request.is_json:
            return jsonify({"status": "error", "message": "Request must be JSON"}), 400

        data = request.get_json()
        print("Datos recibidos:", data)  # Para depuración

        nivel_humedad = data.get('nivel_humedad')
        estado_sistema = data.get('estado_sistema')

        if nivel_humedad is None or estado_sistema is None:
            return jsonify({
                "status": "error",
                "message": "nivel_humedad y estado_sistema son requeridos"
            }), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO datos_humedad (nivel_humedad, estado_sistema) 
            VALUES (%s, %s)
            """,
            (nivel_humedad, estado_sistema)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Datos insertados correctamente"
        }), 201
            
    except Exception as e:
        print("Error en el servidor:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
