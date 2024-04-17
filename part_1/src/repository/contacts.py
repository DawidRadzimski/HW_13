from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_
from part_1.src.database.models import Contact
from part_1.src.schemas import ContactIn, ContactUpdate
from datetime import date, datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def find_contact(keyword: str, skip: int, limit: int, db: Session) -> List[Contact]:
    word = f"%{keyword}%"
    query = db.query(Contact).filter(or_(Contact.first_name.ilike(word), Contact.last_name.ilike(
        word), Contact.email.ilike(word))).offset(skip).limit(limit).all()
    return query


async def create_contact(body: ContactIn, db: Session) -> Contact:
    contact = Contact(name=body.first_name, lastname=body.last_name, email=body.email,
                      phone=body.phone_number, birthday=body.date_of_birth, notes=body.additional_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        if body.name:
            contact.first_name = body.first_name
        if body.lastname:
            contact.last_name = body.last_name
        if body.email:
            contact.email = body.email
        if body.phone:
            contact.phone_number = body.phone_number
        if body.birthday:
            contact.date_of_birth = body.date_of_birth
        if body.notes:
            contact.additional_data = body.additional_data
        db.commit()
        db.refresh(contact)
    return contact


async def get_contacts_birthday_for_next_week(skip: int, limit: int, db: Session) -> List[Contact]:
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    query = db.query(Contact).filter(
        or_(
            and_(
                extract("month", today) == extract("month", next_week),
                extract("month", Contact.date_of_birth) == extract("month", today),
                extract("day", Contact.date_of_birth) >= extract("day", today),
                extract("day", Contact.date_of_birth) <= extract("day", next_week)
            ),
            and_(
                extract("month", today) != extract("month", next_week),
                extract("month", Contact.date_of_birth) == extract("month", today),
                extract("day", Contact.date_of_birth) >= extract("day", today)
            ),
            and_(
                extract("month", today) != extract("month", next_week),
                extract("month", Contact.date_of_birth) == extract(
                    "month", next_week),
                extract("day", Contact.date_of_birth) <= extract("day", next_week)
            )
        )).order_by("date_of_birth").offset(skip).limit(limit).all()
    return query