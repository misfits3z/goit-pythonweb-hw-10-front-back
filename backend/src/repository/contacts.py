from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactCreate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        """
        Initializes the ContactRepository with the provided database session.

        Args:
            session (AsyncSession): The asynchronous session for database operations.
        """
        self.db = session

    async def get_contacts(self, skip: int, limit: int, user: User) -> List[Contact]:
        """
        Retrieves a paginated list of contacts for the given user.

        Args:
            skip (int): Number of records to skip.
            limit (int): Maximum number of contacts to return.
            user (User): The user whose contacts are being queried.

        Returns:
            List[Contact]: A list of Contact objects.
        """
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """
        Retrieves a contact by its ID for the given user.

        Args:
            contact_id (int): ID of the contact.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: A Contact object if found, or None if not found.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactCreate, user: User) -> Contact:
        """
        Creates a new contact for the given user.

        Args:
            body (ContactCreate): Data for the new contact.
            user (User): The user who owns the new contact.

        Returns:
            Contact: The created Contact object.
        """
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id, user)

    async def update_contact(
        self, contact_id: int, body: ContactCreate, user: User
    ) -> Contact | None:
        """
        Updates an existing contact by ID for the given user.

        Args:
            contact_id (int): ID of the contact to update.
            body (ContactCreate): Updated contact data.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The updated Contact object if found, or None if not found.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            contact.first_name = body.first_name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone_number = body.phone_number
            contact.birth_date = body.birth_date
            contact.note = body.note
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """
        Deletes a contact by ID for the given user.

        Args:
            contact_id (int): ID of the contact to delete.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The deleted Contact object if found, or None if not found.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_contacts_by_ids(
        self, contact_ids: list[int], user: User
    ) -> list[Contact]:
        """
        Retrieves a list of contacts by their IDs for the given user.

        Args:
            contact_ids (list[int]): List of contact IDs.
            user (User): The user who owns the contacts.

        Returns:
            list[Contact]: A list of Contact objects.
        """
        stmt = select(Contact).where(Contact.id.in_(contact_ids), Contact.user == user)
        result = await self.db.execute(stmt)
        return result.scalars().all()


# class ContactRepository:
#     def __init__(self, session: AsyncSession):
#         self.db = session

#     async def get_contacts(self, skip: int, limit: int, user: User) -> List[Contact]:
#         """
#         Retrieves a paginated list of contacts for the given user.

#         :param skip: Number of records to skip.
#         :param limit: Maximum number of contacts to return.
#         :param user: The user whose contacts are being queried.
#         :return: List of Contact objects.
#         """
#         stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
#         contacts = await self.db.execute(stmt)
#         return contacts.scalars().all()

#     async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
#         """
#         Retrieves a contact by its ID for the given user.

#         :param contact_id: ID of the contact.
#         :param user: The user who owns the contact.
#         :return: A Contact object or None if not found.
#         """
#         stmt = select(Contact).filter_by(id=contact_id, user=user)
#         contact = await self.db.execute(stmt)
#         return contact.scalar_one_or_none()

#     async def create_contact(self, body: ContactCreate, user: User) -> Contact:
#         """
#         Creates a new contact for the given user.

#         :param body: Data for the new contact (ContactCreate).
#         :param user: The user who owns the new contact.
#         :return: The created Contact object.
#         """
#         contact = Contact(**body.model_dump(exclude_unset=True), user=user)
#         self.db.add(contact)
#         await self.db.commit()
#         await self.db.refresh(contact)
#         return await self.get_contact_by_id(contact.id, user)

#     async def update_contact(
#         self, contact_id: int, body: ContactCreate, user: User
#     ) -> Contact | None:
#         """
#         Updates an existing contact by ID for the given user.

#         :param contact_id: ID of the contact to update.
#         :param body: Updated contact data (ContactCreate).
#         :param user: The user who owns the contact.
#         :return: The updated Contact object or None if not found.
#         """
#         contact = await self.get_contact_by_id(contact_id, user)
#         if contact:
#             contact.first_name = body.first_name
#             contact.last_name = body.last_name
#             contact.email = body.email
#             contact.phone_number = body.phone_number
#             contact.birth_date = body.birth_date
#             contact.note = body.note
#             await self.db.commit()
#             await self.db.refresh(contact)
#         return contact

#     async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
#         """
#         Deletes a contact by ID for the given user.

#         :param contact_id: ID of the contact to delete.
#         :param user: The user who owns the contact.
#         :return: The deleted Contact object or None if not found.
#         """
#         contact = await self.get_contact_by_id(contact_id, user)
#         if contact:
#             await self.db.delete(contact)
#             await self.db.commit()
#         return contact

#     async def get_contacts_by_ids(self, contact_ids: list[int], user: User) -> list[Contact]:
#         """
#         Retrieves a list of contacts by their IDs for the given user.

#         :param contact_ids: List of contact IDs.
#         :param user: The user who owns the contacts.
#         :return: List of Contact objects.
#         """
#         stmt = select(Contact).where(Contact.id.in_(contact_ids), Contact.user == user)
#         result = await self.db.execute(stmt)
#         return result.scalars().all()
