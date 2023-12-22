from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'allen',
    'database': 'elective',
}

# Create MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# CRUD operations

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    if 'username' not in data or 'email' not in data or 'age' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    query = "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)"
    values = (data['username'], data['email'], data['age'])
    
    cursor.execute(query, values)
    conn.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    
    if 'username' not in data or 'email' not in data or 'age' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    query = "UPDATE users SET username = %s, email = %s, age = %s WHERE id = %s"
    values = (data['username'], data['email'], data['age'], user_id)
    
    cursor.execute(query, values)
    conn.commit()
    
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    
    cursor.execute(query, values)
    conn.commit()
    
    return jsonify({'message': 'User deleted successfully'})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
