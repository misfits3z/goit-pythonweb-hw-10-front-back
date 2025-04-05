from fastapi import FastAPI
from fastapi.responses import Response
from src.api import utils, contacts, auth_router, users
import os


app = FastAPI(debug=True)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

app.include_router(auth_router.router, prefix="/auth")
app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
