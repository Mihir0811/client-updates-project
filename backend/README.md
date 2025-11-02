# Client Updates Backend

A FastAPI backend for automating client update generation and management.

## Features

- **User Authentication**: JWT-based authentication system
- **Task Management**: Add, view, and manage daily tasks
- **Custom Formats**: Create and manage client update formats
- **Auto-generation**: Generate client update summaries from tasks
- **Export Options**: Copy or download generated updates

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (local) → Supabase (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Validation**: Pydantic

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Update database credentials and secret key

3. **Database Setup**
   ```bash
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

4. **Run Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Tasks
- `GET /tasks/` - Get user tasks
- `POST /tasks/` - Create new task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

### Formats
- `GET /formats/` - Get user formats
- `POST /formats/` - Create new format
- `PUT /formats/{format_id}` - Update format
- `DELETE /formats/{format_id}` - Delete format

## Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Railway)
1. Connect your backend branch to Railway
2. Update `.env` with Supabase database URL
3. Deploy automatically via git push

## Project Structure

```
backend/
├── app/
│   ├── core/          # Configuration and database setup
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   ├── utils/         # Utility functions
│   └── main.py        # FastAPI application
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md         # This file
```
