# CS ELECTIVES Final Hands On Drill

This project aims to show our skills by building a CRUD (Create, Read, Update, Delete) REST API using Flask and MySQL, and perform several tasks related to testing, formatting options, security, and documentation. 

## Table of Contents

- [Installation](#installion)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Additional Information](#additional-information)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/allen-ix/electives-finaldrill
    cd your-repository
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    - Ensure MySQL server is installed and running.
    - Create a database and import the SQL dump provided in the `db_dump` directory.

5. Configure environment variables:

    Create a `.env` file in the project root and set the following variables:

    ```env
    FLASK_APP=your_flask_app.py
    FLASK_ENV=development
    JWT_SECRET_KEY=your_jwt_secret_key
    DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/database_name
    ```

    Replace `your_jwt_secret_key`, `username`, `password`, and `database_name` with your actual values.

6. Run the application:

    ```bash
    flask run
    ```

## Usage
## API Endpoints

After python app.py in console... 
add 'users' at the end of http://127.0.0.1:5000/
...to see the security mechanims applied to the program go to this... http://127.0.0.1:5000/users?format=xml
...to get/update... /users/{user_id} ...to search... /users/search

### GET /users

- Description: Get a list of all users.
- Parameters: None.
- Response:
  - JSON format: `{ "users": [...] }`
  - XML format: `<users><user>...</user></users>`

### GET /users/<user_id>

- Description: Get details of a specific user.
- Parameters: `format` (optional, default is JSON).
- Response:
  - JSON format: `{ "user": {...} }`
  - XML format: `<user>...</user>`

### POST /users

- Description: Create a new user.
- Parameters: User data in the request body.
- Response: `{ "message": "User created successfully" }`

### PUT /users/<user_id>

- Description: Update details of a specific user.
- Parameters: User data in the request body.
- Response: `{ "message": "User updated successfully" }`

### DELETE /users/<user_id>

- Description: Delete a specific user.
- Parameters: None.
- Response: `{ "message": "User deleted successfully" }`

## Authentication

- To access protected routes, obtain a JWT token by making a POST request to `/login`.
- Use the obtained token in the `Authorization` header for requests to protected routes.

Example:
   ```http
   POST /login
   Content-Type: application/json

   {
     "username": "your_username",
     "password": "your_password"
   }
