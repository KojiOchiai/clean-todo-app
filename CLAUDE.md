# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a clean architecture implementation of a todo application demonstrating separation of concerns with pluggable storage backends, multiple UI implementations, and comprehensive user management.

## Architecture

### Clean Architecture Layers
- **Domain Models** (`app/models.py`): Core business entities (Todo, User)
- **Storage Layer** (`app/storages/`): Repository pattern with multiple backends (file, SQLite, in-memory)
- **Business Logic** (`app/manager.py`): UserManager and TaskManager classes
- **UI Layer** (`app/ui/`): CLI and Web implementations

### Key Components
- **UserManager**: JWT authentication, password hashing, user CRUD
- **TaskManager**: Todo operations with user-based isolation
- **Storage Abstraction**: `UserStorage` and `TodoStorage` base classes with pluggable implementations
- **Frontend**: Next.js app with TypeScript, Tailwind CSS, and Radix UI components

## Development Commands

### Backend Development
```bash
# Run with different storage backends
uv run python main.py --storage file --ui web      # Default file storage + web UI
uv run python main.py --storage sqlite --ui cli    # SQLite + CLI
uv run python main.py --storage memory --ui web    # In-memory + web UI

# Development tools
uv run ruff check                                   # Lint code
uv run ruff format                                  # Format code
uv run pytest                                       # Run tests
```

### Frontend Development
```bash
cd app/frontend
npm install    # Install dependencies first
npm run dev    # Development server
npm run build  # Static export build
npm run start  # Production server
npm run lint   # ESLint
```

## Storage Configuration

The application supports three storage backends selected at runtime:
- **file**: JSON files in `data/` directory (default)
- **sqlite**: SQLAlchemy ORM with `todos.db`
- **memory**: Runtime-only storage for testing

## Authentication Flow

1. Users register/login through CLI or web interface
2. JWT tokens issued with 15-minute expiration
3. All todo operations require valid authentication
4. User isolation enforced at the storage layer

## Environment Variables

- `SECRET_KEY`: JWT signing key (required for production)
- `IS_DEV_ENV=True`: Enables CORS for frontend development

## Frontend Integration

The Next.js frontend (`app/frontend/`) communicates with the FastAPI backend via REST API. Key features:
- JWT token storage in localStorage
- Real-time todo operations with optimistic updates
- Inline editing with blur-to-save functionality
- Static export configuration with `/static` base path

## Key Files to Understand

- `main.py`: Application entry point with dependency injection
- `app/manager.py`: Core business logic managers
- `app/storages/base.py`: Storage abstraction interfaces
- `app/ui/web_ui.py`: FastAPI web server and API endpoints
- `app/frontend/app/page.tsx`: Main frontend application logic

## Development Notes

- All storage operations are user-scoped for security
- Password hashing uses bcrypt with salt
- Frontend uses TypeScript with strict type checking
- Ruff configured for Python linting (E, F, I, W rules)
- Architecture supports easy extension of storage backends and UI implementations
- Frontend requires `lib/utils.ts` for Tailwind class merging utilities