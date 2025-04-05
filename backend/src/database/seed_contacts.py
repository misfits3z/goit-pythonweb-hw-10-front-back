from src.database.db import sessionmanager
import asyncio
from datetime import date

from src.database.models import Contact


async def seed_contacts():
    # Створення кількох фіктивних контактів
    contacts = [
        Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            birth_date=date(1990, 5, 15),
        ),
        Contact(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone_number="0987654321",
            birth_date=date(1992, 7, 20),
        ),
        Contact(
            first_name="Mark",
            last_name="Johnson",
            email="mark.johnson@example.com",
            phone_number="1122334455",
            birth_date=date(1988, 3, 10),
        ),
        Contact(
            first_name="Emily",
            last_name="Davis",
            email="emily.davis@example.com",
            phone_number="6677889900",
            birth_date=date(1995, 11, 2),
        ),
        Contact(
            first_name="Michael",
            last_name="Brown",
            email="michael.brown@example.com",
            phone_number="2233445566",
            birth_date=date(1987, 1, 25),
        ),
        Contact(
            first_name="Sarah",
            last_name="Wilson",
            email="sarah.wilson@example.com",
            phone_number="4455667788",
            birth_date=date(1993, 9, 30),
        ),
        Contact(
            first_name="David",
            last_name="Miller",
            email="david.miller@example.com",
            phone_number="5566778899",
            birth_date=date(1991, 6, 12),
        ),
        Contact(
            first_name="Olivia",
            last_name="Taylor",
            email="olivia.taylor@example.com",
            phone_number="9988776655",
            birth_date=date(1994, 12, 5),
        ),
    ]

    # Додавання контактів у базу даних
    async with sessionmanager.session() as session:
        session.add_all(contacts)
        await session.commit()

    print("Contacts have been seeded successfully!")


# Запуск асинхронної функції
async def main():
    await seed_contacts()


if __name__ == "__main__":
    asyncio.run(main())
