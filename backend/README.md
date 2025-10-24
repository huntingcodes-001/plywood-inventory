# Inventory Management Backend API

A FastAPI-based REST API for inventory management with role-based access control and Supabase integration.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Supabase account and project

### Installation

1. **Clone and navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your Supabase credentials:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_KEY`: Your Supabase service role key
   - `JWT_SECRET_KEY`: A secure secret key (minimum 32 characters)

### Supabase Setup

1. Create a new Supabase project at https://supabase.com
2. Go to Settings > API to find your project URL and service role key
3. Copy these values to your `.env` file

### Running the Application

1. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Supabase connection utilities
│   ├── auth/                # Authentication modules
│   ├── models/              # Pydantic data models
│   ├── routers/             # API route handlers
│   └── utils/               # Utility functions
├── migrations/              # Database migration scripts
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens (min 32 chars) | Yes |
| `JWT_ALGORITHM` | JWT algorithm (default: HS256) | No |
| `JWT_EXPIRATION_HOURS` | JWT token expiration (default: 24) | No |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | No |
| `DEBUG` | Enable debug mode (default: false) | No |

## Next Steps

After completing the setup:

1. Run database migrations to create the required tables
2. Seed the database with the default admin user
3. Implement the remaining API endpoints according to the task list

## API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation.