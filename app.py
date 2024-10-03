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
        value_data = data.get("value")

        if not value_data:
            return jsonify({"status": "error", "message": "value data is required"}), 400

        humidity = value_data.get("nivel_humedad")
        state = value_data.get("estado_sistema")

        if humidity is None or state is None:
            return jsonify({"status": "error", "message": "nivel_humedad and estado_sistema are required"}), 400

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Asumiendo que has actualizado la estructura de tu tabla para almacenar ambos valores
            cursor.execute(
                "INSERT INTO sensor_data (humidity_level, system_state) VALUES (%s, %s)",
                (humidity, state)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
