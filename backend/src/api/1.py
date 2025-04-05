# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy import text


# async def test():
#     engine = create_async_engine(
#         "postgresql+asyncpg://postgres:goit@localhost:5432/contacts", echo=True
#     )
#     async with engine.connect() as conn:
#         result = await conn.execute(text("SELECT 1"))
#         print(result.scalar())


# asyncio.run(test())
# import asyncio
# import os
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy import text
# from dotenv import load_dotenv

# load_dotenv()  # Підтягне змінні з .env


# async def test():
#     user = os.getenv("POSTGRES_USER")
#     password = os.getenv("POSTGRES_PASSWORD")
#     db_name = os.getenv("POSTGRES_DB")
#     db_url = f"postgresql+asyncpg://{user}:{password}@db:5432/{db_name}"

#     engine = create_async_engine(db_url, echo=True)

#     try:
#         async with engine.connect() as conn:
#             result = await conn.execute(text("SELECT 1"))
#             print("✅ Connected to database:", result.scalar())
#     except Exception as e:
#         print("❌ Failed to connect to database:", e)


# asyncio.run(test())
