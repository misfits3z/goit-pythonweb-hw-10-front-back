from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse
from src.services.contacts import ContactService
from src.services.auth import get_current_user
from src.database.models import User


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get a list of user's contacts.

    Args:
        skip (int): Number of records to skip. Defaults to 0.
        limit (int): Maximum number of contacts to return. Defaults to 100.
        db (AsyncSession): Database session.
        user (User): Authenticated user.

    Returns:
        List[ContactResponse]: List of contacts belonging to the user.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Retrieve a specific contact by ID.

    Args:
        contact_id (int): ID of the contact to retrieve.
        db (AsyncSession): Database session.
        user (User): Authenticated user.

    Returns:
        ContactResponse: Contact details.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    print(contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new contact for the authenticated user.

    Args:
        body (ContactCreate): Contact data to create.
        db (AsyncSession): Database session.
        user (User): Authenticated user.

    Returns:
        ContactResponse: The created contact.
    """
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactCreate,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update an existing contact.

    Args:
        body (ContactCreate): Updated contact data.
        contact_id (int): ID of the contact to update.
        db (AsyncSession): Database session.
        user (User): Authenticated user.

    Returns:
        ContactResponse: The updated contact.

    Raises:
        HTTPException: If the contact is not found.
    """

    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Delete a contact by ID.

    Args:
        contact_id (int): ID of the contact to delete.
        db (AsyncSession): Database session.
        user (User): Authenticated user.

    Returns:
        ContactResponse: The deleted contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
