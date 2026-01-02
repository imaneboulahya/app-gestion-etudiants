from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Create a new database connection for each request"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lpan3677_2006",
            database="student_db",
            autocommit=True
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route("/students", methods=["GET"])
def get_students():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        students = cursor.fetchall()
        return jsonify(students)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()
        if student:
            return jsonify(student)
        return jsonify({"error": "Student not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/students", methods=["POST"])
def add_student():
    try:
        data = request.json
        
        required_fields = ["nom", "prenom", "email", "age", "filiere"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM students WHERE email = %s", (data["email"],))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400
        
        sql = """INSERT INTO students (nom, prenom, email, age, filiere)
                 VALUES (%s, %s, %s, %s, %s)"""
        values = (
            data["nom"],
            data["prenom"],
            data["email"],
            int(data["age"]),
            data["filiere"]
        )
        
        cursor.execute(sql, values)
        connection.commit()
        
        student_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        new_student = cursor.fetchone()
        
        return jsonify({
            "message": "Student added successfully",
            "student": new_student
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    try:
        data = request.json
        
        required_fields = ["nom", "prenom", "email", "age", "filiere"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM students WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404
        
        cursor.execute("SELECT id FROM students WHERE email = %s AND id != %s", 
                      (data["email"], id))
        if cursor.fetchone():
            return jsonify({"error": "Email already used by another student"}), 400
        
        sql = """UPDATE students
                 SET nom=%s, prenom=%s, email=%s, age=%s, filiere=%s
                 WHERE id=%s"""
        values = (
            data["nom"],
            data["prenom"],
            data["email"],
            int(data["age"]),
            data["filiere"],
            id
        )
        
        cursor.execute(sql, values)
        connection.commit()
        
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        updated_student = cursor.fetchone()
        
        return jsonify({
            "message": "Student updated successfully",
            "student": updated_student
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM students WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404
        
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        connection.commit()
        
        return jsonify({"message": "Student deleted successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/health", methods=["GET"])
def health_check():
    connection = get_db_connection()
    if connection:
        connection.close()
        return jsonify({"status": "healthy", "database": "connected"})
    return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)