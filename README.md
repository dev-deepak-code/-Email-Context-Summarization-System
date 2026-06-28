# Email Context & Summarization System

A production-ready, asynchronous API built with **FastAPI** that acts as an intelligence layer for CPA firms. This system aggregates client email threads, processes them using LLMs to extract actionable insights, and provides role-based reporting—all while ensuring strict data security through at-rest encryption and robust caching.

---

## 🚀 Key Features

- **Automated Summarization:** Extracts *Actors*, *Concluded Discussions*, and *Open Action Items* using OpenRouter API (GPT-4o-mini).
- **Security First:** 
  - JWT Authentication with strict Role-Based Access Control (Accountant, Firm Admin, Superuser).
  - All LLM-generated summaries are encrypted at rest using AES-GCM (`cryptography.fernet`) before hitting the PostgreSQL database.
- **High Performance:** 
  - Fully asynchronous architecture using `asyncpg` and `SQLAlchemy 2.0`.
  - Redis caching layer to ensure lightning-fast repeated queries while providing a forced `/refresh` mechanism.
- **Advanced Reporting:** Role-restricted analytic endpoints using optimized SQL joins.

---

## 🛠️ Technology Stack

- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async)
- **Caching:** Redis
- **Authentication:** JWT (JSON Web Tokens)
- **AI Integration:** OpenRouter API 
- **Infrastructure:** Docker & Docker Compose

---

## 📦 Local Setup & Installation

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Docker and Docker Compose (for Postgres and Redis)

### 2. Environment Variables
Copy the example environment file and update it with your OpenRouter API Key.
```bash
cp .env.example .env
```
Ensure your `.env` has a valid `OPENROUTER_API_KEY` and a generated `SECRET_KEY`.

### 3. Start Infrastructure (Database & Cache)
Use Docker Compose to spin up PostgreSQL and Redis:
```bash
docker-compose up -d
```

### 4. Install Dependencies
Create a virtual environment and install the required Python packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Initialize & Seed Database
The project includes a seeding script that wipes the database clean and injects mock data (A Firm, a Client, Mock Emails, and 3 distinct Users) to test with.
```bash
python init_db.py
python -m app.db.seed
```
*(A deterministic Client UUID is seeded so you can easily test the summarization endpoints. Use this Client ID for testing: `12345678-1234-5678-1234-567812345678`)*

### 6. Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Testing the API

The API documentation is interactive and available at: **http://127.0.0.1:8000/docs**

### Authentication & Roles
The database seed script provides three default users for testing different authorization levels:

| Role | Email | Password | Allowed Access |
|---|---|---|---|
| **Accountant** | `jane.doe@smithcpa.com` | `securepassword123` | Summaries only |
| **Firm Admin** | `admin@smithcpa.com` | `securepassword123` | Summaries + Firm Reports |
| **Superuser** | `superuser@ascend.com` | `securepassword123` | Summaries + Global Reports |

### Testing Workflow
1. Go to `POST /auth/login` to obtain an access token.
2. Click the **Authorize** button at the top of the Swagger UI and paste your token.
3. Test `GET /summaries/{client_id}` using the seeded Client ID: `12345678-1234-5678-1234-567812345678`.
4. Try out the `/reports` endpoints with the different user roles to verify RBAC enforcement!

---

## 🏗️ Architecture & Project Structure

```text
├── app/
│   ├── api/          # API Routers (auth, summaries, reports)
│   ├── core/         # Core config, JWT auth, and Exception handlers
│   ├── db/           # Database setup, sessions, and seeders
│   ├── models/       # SQLAlchemy ORM schemas
│   ├── repositories/ # Database query abstraction layer
│   ├── schemas/      # Pydantic validation schemas
│   └── services/     # Business logic (Encryption, Cache, AI, Email)
├── alembic/          # Database migrations
├── .env              # Environment configurations
├── docker-compose.yml # Container definitions
├── init_db.py        # Database creation script
└── requirements.txt  # Python dependencies
```

## 🔐 Design Decisions & Trade-offs

1. **Repository Pattern:** Implemented to strictly separate business logic (Services) from database querying (Repositories), making the system highly testable and modular.
2. **At-Rest Encryption:** The `EncryptionService` acts as a middleman between the business logic and the database, ensuring that sensitive LLM summaries are heavily encrypted before persistence.
3. **OpenRouter vs Gemini:** OpenRouter was chosen for its flexibility, allowing the system to easily swap models (e.g., GPT-4o-mini) without changing the underlying integration code, while still strictly enforcing the required JSON output format.
