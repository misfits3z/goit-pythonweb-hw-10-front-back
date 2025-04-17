from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse
from src.services.contacts import ContactService
from src.services.auth import get_current_user
from src.database.models import User

from typing import List, Optional

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


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be >= 0)"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return (1-100)"
    ),
    first_name: Optional[str] = Query(
        None, description="Filter contacts by first name (case-insensitive)"
    ),
    last_name: Optional[str] = Query(
        None, description="Filter contacts by last name (case-insensitive)"
    ),
    email: Optional[str] = Query(
        None, description="Filter contacts by email address (case-insensitive)"
    ),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[ContactResponse]:
    """
    Search contacts by first name, last name, or email with pagination.

    Args:
        skip (int): Number of records to skip (default: 0, must be >= 0).
        limit (int): Maximum number of records to return (default: 10, range: 1-100).
        first_name (Optional[str]): Filter by first name (optional).
        last_name (Optional[str]): Filter by last name (optional).
        email (Optional[str]): Filter by email address (optional).
        db (AsyncSession): The database session.
        user (User): The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts matching the search criteria.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.search_contacts(
        skip, limit, first_name, last_name, email, user
    )
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    days: int = Query(
        7,
        ge=1,
        le=364,
        description="Number of days to look ahead for birthdays (default: 7, range: 1-364)",
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip (must be >= 0)"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return (1-100)"
    ),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[ContactResponse]:
    """
    Retrieve a list of contacts with upcoming birthdays within the next `days` days.

    Args:
        days (int): Number of days to look ahead for birthdays (default: 7, range: 1-364).
        skip (int): Number of records to skip (default: 0, must be >= 0).
        limit (int): Maximum number of records to return (default: 10, range: 1-100).
        db (AsyncSession): The database session.
        user (User): The currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts with upcoming birthdays.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays(days, skip, limit, user)
    return contacts
