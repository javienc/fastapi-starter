# FastAPI Demo Project

A demonstration project showcasing FastAPI features with authentication, CRUD operations, and interactive documentation.

## 🚀 Features

- RESTful API endpoints with FastAPI
- Token-based authentication
- Public and protected routes
- CRUD operations for items
- Interactive API documentation
- Mock database implementation
- Comprehensive tutorial page

## 📋 Requirements

- Python 3.9+2
- FastAPI
- Uvicorn
- Python-multipart (for form data processing)
- Jinja2 (for HTML templates)

## 🛠 Installation

1. Clone the repository:

```bash
bash
git clone https://github.com/yourusername/fastapi-demo.git
cd fastapi-demo
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install fastapi uvicorn python-multipart jinja2
```

## 🏃‍♂️ Running the Application

Start the server with:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## 📚 API Documentation

Visit these URLs after starting the application:

- Tutorial Page: [http://localhost:8000/](http://localhost:8000/)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- OpenAPI Schema: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## 🔑 Authentication

- Login endpoint: `/token`
- Tokens expire after 24 hours
- Token format: `user_username_timestamp`
- Manual token revocation available

### Test Credentials

```
Username: testuser
Password: testpass
```

## 🛣 Available Routes

### Public Endpoints (No Authentication Required)

- `GET /api` - API status check
- `GET /public/items` - List public items
- `GET /public/items/{item_id}` - Get specific public item

### Protected Endpoints (Authentication Required)

- `POST /token` - Get authentication token
- `POST /token/revoke` - Revoke current token
- `GET /items` - List all items
- `GET /items/{item_id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update entire item
- `PATCH /items/{item_id}` - Partially update item
- `DELETE /items/{item_id}` - Delete item

## 📝 Example Usage

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=testpass"
```

### Create New Item

```bash
curl -X POST http://localhost:8000/items \
    -H "Authorization: Bearer your_token_here" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "New Item",
        "description": "Description",
        "price": 29.99,
        "tags": ["new", "item"],
        "is_offer": false
    }'
```

## 🧪 Testing

The API includes mock databases for testing:

- `public_items_db`: Publicly accessible items
- `items_db`: Protected items requiring authentication
- `users_db`: User credentials for authentication

## 📦 Project Structure

```
fastapi-demo/
├── main.py              # Main application file
├── README.md            # Project documentation
└── templates/
    └── fastapi_tutorial.html  # Tutorial page template
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ✨ Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
