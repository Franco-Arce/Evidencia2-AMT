from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

# Configura tu conexión a la base de datos
db_config = {
    "host": "bfmflcykgagrhfka6afi-mysql.services.clever-cloud.com",
    "user": "ux84ttbmxq3e0gfs",
    "password": "pdLPgMM64VWz57nsQCvQ",
    "database": "bfmflcykgagrhfka6afi",
    "port": 3306
}

@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()
        nivel_humedad = data.get("nivel_humedad")  # Recibir el valor de humedad
        estado_sistema = data.get("estado_sistema")  # Recibir el estado del sistema

        if nivel_humedad is None or estado_sistema is None:
            return jsonify({"status": "error", "message": "Faltan datos en la solicitud"}), 400

        # Lógica para insertar los datos en la base de datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO datos_humedad (nivel_humedad, estado_sistema) VALUES (%s, %s)", 
                (nivel_humedad, estado_sistema)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "La solicitud debe ser JSON"}), 400


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
