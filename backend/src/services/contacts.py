from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, timedelta

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate 
from src.database.models import User


class ContactService:
    """
    Service layer for managing contacts. Provides methods for creating, retrieving,
    updating, and deleting contacts.
    """

    def __init__(self, db: AsyncSession):
        """
        Initializes the ContactService with a database session.

        Args:
            db (AsyncSession): The database session used to interact with the repository.
        """
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactCreate, user: User):
        """
        Creates a new contact for a given user.

        Args:
            body (ContactCreate): The data to create a new contact.
            user (User): The user who owns the contact.

        Returns:
            Contact: The newly created contact.
        """
        return await self.repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, user: User):
        """
        Retrieves a paginated list of contacts for a specific user.

        Args:
            skip (int): The number of records to skip for pagination.
            limit (int): The maximum number of contacts to return.
            user (User): The user whose contacts are being queried.

        Returns:
            list[Contact]: A list of Contact objects.
        """
        return await self.repository.get_contacts(skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        """
        Retrieves a single contact by its ID for a given user.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The requested contact or None if not found.
        """
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(
        self, contact_id: int, body: ContactCreate, user: User
    ) :
        """
        Updates an existing contact by its ID for a given user.

        Args:
            contact_id (int): The ID of the contact to update.
            body (ContactCreate): The updated contact data.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The updated contact or None if not found.
        """
        return await self.repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Deletes a contact by its ID for a given user.

        Args:
            contact_id (int): The ID of the contact to delete.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The deleted contact or None if not found.
        """
        return await self.repository.remove_contact(contact_id, user)

    async def search_contacts(
        self,
        skip: int,
        limit: int,
        first_name: Optional[str],
        last_name: Optional[str],
        email: Optional[str],
        user: User,
    ) -> List[ContactCreate]:
        """
        Search for contacts by first name, last name, or email for a specific user.

        Args:
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to retrieve.
            first_name (Optional[str]): The first name to search for.
            last_name (Optional[str]): The last name to search for.
            email (Optional[str]): The email to search for.
            user (User): The user whose contacts are being searched.

        Returns:
            List[ContactModel]: A list of contacts matching the search criteria.
        """
        return await self.repository.search_contacts(
            skip, limit, first_name, last_name, email, user
        )

    async def get_upcoming_birthdays(
        self, days: int, skip: int, limit: int, user: User
    ) -> List[ContactCreate]:
        """
        Retrieve contacts with upcoming birthdays within a specified date range.

        Args:
            days (int): The number of days ahead to search for birthdays.
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to retrieve.
            user (User): The user whose contacts are being retrieved.

        Returns:
            List[ContactModel]: A list of contacts with upcoming birthdays.
        """
        today = date.today()
        next_date = today + timedelta(days=days)
        return await self.repository.get_upcoming_birthdays(
            today, next_date, skip, limit, user
        )


