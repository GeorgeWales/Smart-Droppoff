from flask import Flask, request, jsonify
import mysql.connector
from sshtunnel import SSHTunnelForwarder
import sensInf 

app = Flask(__name__)

# Function to establish SSH Tunnel & connect to MySQL
def get_db_connection():
    try:
        print("🔄 Establishing SSH Tunnel...")
        tunnel = SSHTunnelForwarder(
            (sensInf.SSH_HOST, 22),
            ssh_username=sensInf.SSH_USER,
            ssh_password=sensInf.SSH_PASSWORD,
            remote_bind_address=(sensInf.MYSQL_HOST, sensInf.MYSQL_PORT)
        )
        tunnel.start()
        print(f"✅ SSH Tunnel Established (Local Port: {tunnel.local_bind_port})")

        # Connect to MySQL through SSH tunnel
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            user=sensInf.MYSQL_USER,
            password=sensInf.MYSQL_PASSWORD,
            database=sensInf.MYSQL_DB,
            use_pure=True
        )

        return conn, tunnel
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None, None

# User registration API
@app.route("/users", methods=["GET"])
def get_users():
    conn, tunnel = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users;")  # Do not fetch passwords
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    tunnel.stop()

    return jsonify({"status": "success", "users": users})

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")  # No encryption

    conn, tunnel = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    tunnel.stop()

    if user:
        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    


#Start Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4001, debug=True)
