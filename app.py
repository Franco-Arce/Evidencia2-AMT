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
    if request.is_json:
        data = request.get_json()
        
        # Extraer directamente nivel_humedad y estado_sistema
        nivel_humedad = data.get("nivel_humedad")
        estado_sistema = data.get("estado_sistema")

        if nivel_humedad is None or estado_sistema is None:
            return jsonify({
                "status": "error", 
                "message": "nivel_humedad y estado_sistema son requeridos"
            }), 400

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Insertar en la tabla datos_humedad
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
            return jsonify({
                "status": "error", 
                "message": f"Error de base de datos: {str(err)}"
            }), 500
    else:
        return jsonify({
            "status": "error", 
            "message": "La solicitud debe ser JSON"
        }), 400

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT id, nivel_humedad, estado_sistema, fecha_registro 
            FROM datos_humedad 
            ORDER BY fecha_registro DESC 
            LIMIT 10
            """
        )
        
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "data": results
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({
            "status": "error", 
            "message": f"Error de base de datos: {str(err)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
