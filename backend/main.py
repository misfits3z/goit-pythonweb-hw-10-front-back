from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from src.api import utils, contacts, auth_router, users, create_admin
import os

# source $(poetry env info --path)/bin/activate

app = FastAPI(debug=True)

# 👇 Дозволяємо CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Додати тут деплой, наприклад:
    # "https://your-frontend.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


# 👇 Роутери
app.include_router(auth_router.router, prefix="/auth")
app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(create_admin.router, prefix="/api")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
