from flask import Flask, request, jsonify
import mysql.connector
import xmltodict
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = '1234'
jwt = JWTManager(app)

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

##################################################################################

# Protected route example using JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# JWT Authentication route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check username and password against your database
    # For simplicity, let's assume a static username and password for demonstration purposes
    if data['username'] == 'username' and data['password'] == 'password':
        # Create a JWT token
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

#################################################################################

# CRUD operations

@app.route('/users', methods=['GET'])
def get_all_users():
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if format_type.lower() == 'xml':
        # Code to convert users to XML format using xmltodict
        xml_data = xmltodict.unparse({'users': {'user': users}}, full_document=False)
        return xml_data, 200, {'Content-Type': 'application/xml'}
    else:
        return jsonify({'users': users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        if format_type.lower() == 'xml':
            # Code to convert user to XML format using xmltodict
            xml_data = xmltodict.unparse({'user': user}, full_document=False)
            return xml_data, 200, {'Content-Type': 'application/xml'}
        else:
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
