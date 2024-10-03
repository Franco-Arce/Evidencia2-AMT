from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={r"/data": {"origins": "*", "methods": ["POST", "GET", "OPTIONS"]}})

db_config = {
    "host": "b4fewpnrw63fxilykl7z-mysql.services.clever-cloud.com",
    "user": "uk0za9yhjsjmmpuy",
    "password": "eARyZjZuCQETChusm6wW",
    "database": "b4fewpnrw63fxilykl7z",
    "port": 3306
}

@app.route("/data", methods=["OPTIONS"])
def handle_options():
    response = app.make_default_options_response()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route("/data", methods=["POST"])
def insert_data():
    try:
        if not request.is_json:
            print("Request Content-Type:", request.headers.get('Content-Type'))
            print("Request body:", request.get_data(as_text=True))
            return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400

        data = request.get_json()
        
        nivel_humedad = data.get("nivel_humedad")
        estado_sistema = data.get("estado_sistema")

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
            
    except mysql.connector.Error as err:
        print("Error de MySQL:", str(err))
        return jsonify({
            "status": "error", 
            "message": f"Error de base de datos: {str(err)}"
        }), 500
    except Exception as e:
        print("Error general:", str(e))
        return jsonify({
            "status": "error", 
            "message": f"Error del servidor: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
