# 🏋️ Fitness Studio Booking API

A complete REST API for fitness class bookings with JWT authentication, built with FastAPI, SQLAlchemy, and SQLite.

## ✨ Features

- 🔐 **JWT Authentication** (signup/login)
- 🧘 **Class Management** (create/view fitness classes)
- 📅 **Smart Booking** (prevents overbooking, timezone-aware)
- 👤 **User Management** (view personal bookings)
- 🌍 **Timezone Support** (IST default)
- 📚 **Auto-generated API docs** (Swagger/ReDoc)
- 🧪 **Testing suite** included

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/sathishrouthu1909/fitness-booking-api
cd Fitness-Booking-API
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./fitness_studio.db
```

### 3. Run Server
```bash
uvicorn app.main:app --reload
```

API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### Classes
- `GET /classes/` - View all upcoming classes
- `POST /classes/` - Create new class (auth required)
- `GET /classes/{id}` - Get specific class details

### Bookings
- `POST /bookings/` - Book a class (auth required)
- `GET /bookings/` - View your bookings (auth required)
- `DELETE /bookings/{id}` - Cancel booking (auth required)

## 🧪 Testing

```bash
pytest
```

## 📝 Usage Examples

### 1. Register User
```bash
curl -X POST "http://localhost:8000/auth/signup" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123"
}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john@example.com",
  "password": "securepass123"
}'
```

### 3. Create Class (with auth token)
```bash
curl -X POST "http://localhost:8000/classes/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{
  "name": "Yoga Flow",
  "dateTime": "2025-12-15T10:00:00",
  "instructor": "Jane Smith",
  "availableSlots": 20
}'
```

### 4. Book Class
```bash
curl -X POST "http://localhost:8000/bookings/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}'
```

## 🏗️ Project Structure
```
fitness-booking-api/
├── app/
│   ├── main.py          # FastAPI app and routes
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT utilities
│   ├── dependencies.py  # FastAPI dependencies
│   └── routers/         # Route handlers
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── .env                # Environment variables
└── README.md           # This file
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected endpoints with dependency injection
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM

## 🌍 Timezone Support

All class times are stored and handled in IST (Asia/Kolkata) timezone by default. The API automatically converts and validates datetime inputs.

## 🚀 Deployment

The API is production-ready and can be deployed to:
- Render (included Dockerfile)
- Heroku
- AWS/GCP/Azure
- Any platform supporting Python/FastAPI

## 👨‍💻 Developer

**Abhishek Vats**  
Python Developer | Full Stack API Development  
📧 Contact: [your-email@example.com]  
🔗 GitHub: [@sathishrouthu1909]https://github.com/sathishrouthu1909/fitness-booking-api

---

Built with ❤️ using FastAPI, SQLAlchemy, and JWT
```

## Installation Instructions for Your PC:

1. **Clone your repository:**
```bash

cd Fitness-Booking-API
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file** with the environment variables shown above

5. **Run the application:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with automatic documentation at `/docs`.