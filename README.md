# F1 Pulse API 🏎️

A production-grade REST API for Formula 1 data built with FastAPI, SQLAlchemy, and JWT authentication.

## What it does

- Live F1 driver data and championship standings from the 2025 season
- User authentication with JWT tokens and refresh token flow
- Follow/unfollow your favourite drivers
- Clean architecture — repositories, services, routers
- Rate limiting, CORS, structured error handling

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database (dev)
- **Pydantic** — data validation
- **python-jose** — JWT tokens
- **bcrypt** — password hashing
- **httpx** — async HTTP client
- **slowapi** — rate limiting
- **Jolpica F1 API** — live F1 data source
- **uv** — package management

## Project Structure
f1-pulse/
├── app/
│   ├── models/          # database tables
│   ├── schemas/         # Pydantic validation
│   ├── repositories/    # database operations
│   ├── services/        # business logic
│   ├── routers/         # HTTP endpoints
│   ├── config.py        # environment config
│   ├── database.py      # SQLAlchemy setup
│   ├── exceptions.py    # custom exceptions
│   └── main.py          # app entry point
└── tests/

## API Endpoints

### Auth
POST /auth/register    — create account
POST /auth/login       — get JWT tokens
POST /auth/refresh     — refresh access token
GET  /auth/me          — get current user

### Drivers
GET  /drivers/                    — all current F1 drivers
GET  /drivers/standings           — championship standings
GET  /drivers/{driver_id}         — single driver profile
POST /drivers/{driver_id}/follow  — follow a driver
DEL  /drivers/{driver_id}/unfollow — unfollow a driver
GET  /drivers/me/following        — your followed drivers
