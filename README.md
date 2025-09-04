# Ticket System API

A FastAPI-based ticket management system with best practices for structure, security, and development convenience.

## Project Structure

```
├── app/                    # Application package
│   ├── api/                # API endpoints
│   │   ├── api_v1/         # API version 1
│   │   │   ├── endpoints/  # API endpoint modules
│   │   │   └── api.py      # API router
│   ├── core/               # Core modules
│   │   ├── config.py       # Configuration settings
│   │   ├── security.py     # Security utilities
│   │   └── errors.py       # Error handling
│   ├── crud/               # CRUD operations
│   ├── db/                 # Database setup
│   │   ├── base.py         # Base class for models
│   │   ├── session.py      # Database session
│   │   └── init_db.py      # Database initialization
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   └── main.py             # FastAPI application
├── alembic/                # Database migrations
├── tests/                  # Test modules
├── .env                    # Environment variables
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Features

- **Modern FastAPI Framework**: Utilizing FastAPI's high performance and automatic OpenAPI documentation
- **Secure Authentication**: JWT token-based authentication with password hashing
- **SQLAlchemy ORM**: Database integration with SQLAlchemy ORM
- **Alembic Migrations**: Database schema migrations with Alembic
- **Pydantic Models**: Request and response validation with Pydantic
- **Dependency Injection**: Clean dependency injection system
- **CORS Middleware**: Cross-Origin Resource Sharing support
- **Error Handling**: Comprehensive error handling
- **Logging**: Structured logging with Loguru
- **Testing**: Pytest-based testing framework

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example`

6. Initialize the database:
   ```bash
   python -m app.db.init_db
   ```

7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

8. Access the API documentation at http://localhost:8000/docs

## API Documentation

The API documentation is automatically generated and available at `/docs` endpoint when the application is running.

## Authentication

The API uses JWT token-based authentication. To authenticate:

1. Register a new user at `/api/v1/auth/register`
2. Login with the user credentials at `/api/v1/auth/login`
3. Use the returned access token in the Authorization header for protected endpoints

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Security Best Practices

- Environment variables for sensitive information
- Password hashing with bcrypt
- JWT token with expiration
- HTTPS recommended for production
- Input validation with Pydantic
- Role-based access control
- Rate limiting for API endpoints

## License

MIT