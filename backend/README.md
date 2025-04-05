🚀 Project Overview

goit-pythonweb-hw-10 is a FastAPI-based application featuring:

   * User authentication and authorization

   * JWT token handling

   * Email verification for account activation

   * Asynchronous PostgreSQL database integration via SQLAlchemy + Alembic

   * Redis support (optional for rate-limiting, caching, etc.)

🧪 Development Environment Setup
1. 🔧 Install Dependencies

Ensure you have Poetry and Docker installed. Then, install project dependencies:

        poetry install  


2. 🐳 Run with Docker

Start all required services (PostgreSQL, Redis, FastAPI app):

        docker-compose up --build

This will expose the API at:
👉 http://localhost:8000


3. 📦 Activate Virtual Environment

Activate the Poetry virtual environment manually if needed:

        source $(poetry env info --path)/bin/activate

🔐 Environment Variables

Create a .env file in the project root or inside the src/ directory.
You can also duplicate an existing .env.example

✅ Running the Seeder (Optional)

To populate the database with fake contacts:

        docker-compose exec app poetry run python -m src.database.seed_contacts