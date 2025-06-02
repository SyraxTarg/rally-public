"""This file contains the address repository"""
from sqlalchemy.orm import Session
from models.address_model import Address

def add_new_address(db: Session, address: Address)->None:
    """
    Adding a new address object in database

    Args:
        db (Session): The database session used to interact with the database.
        address (Address): the address object to add in database.
    """
    db.add(address)

def commit_address(db: Session)->None:
    """
    Commiting the changes in the database

    Args:
        db (Session): The database session used to interact with the database.
    """
    db.commit()

def refresh_address(db: Session, address: Address)->None:
    """
    Refreshing the changes from the database

    Args:
        db (Session): The database session used to interact with the database.
        address (Address): The address object to refresh
    """
    db.refresh(address)

def delete_address(db: Session, address: Address)->None:
    """
    Deleting an address object from the database.

    Args:
        db (Session): _description_
        address (Address): _description_
    """
    db.delete(address)

def get_address_by_id(db: Session, address_id: int)->Address:
    """
    Fetching an address by its id from the database

    Args:
        db (Session): The database session used to interact with the database.
        id (int): address id

    Returns:
        Address
    """
    return db.query(Address).filter(Address.id == address_id).first()
