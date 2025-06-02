from sqlalchemy.orm import Session

from models.address_model import Address
from repositories import address_repo
from errors import AddressNotFoundError



def create_address(
    db: Session,
    city: str,
    zipcode: str,
    number: str,
    street: str,
    country: str
) -> Address:
    """
    Creates a new address entry in the database.

    Parameters:
    - db (Session): The database session used for queries.
    - city (str): The city of the address.
    - zipcode (str): The postal code of the address.
    - number (str): The building number of the address.
    - street (str): The street name of the address.
    - country (str): The country of the address.

    Returns:
    - Address: The newly created address object.

    Note:
    - This function adds the new address to the database, commits it, and refreshes the address object.
    """
    new_address = Address(
        city=city,
        zipcode=zipcode,
        number=number,
        street=street,
        country=country
    )
    address_repo.add_new_address(db, new_address)
    address_repo.commit_address(db)
    address_repo.refresh_address(db, new_address)
    return new_address


def get_address_by_id(db: Session, address_id: int) -> Address:
    """
    Retrieves an address by its ID from the database.

    Parameters:
    - db (Session): The database session used for queries.
    - address_id (int): The ID of the address to retrieve.

    Returns:
    - Address: The address object corresponding to the provided ID.

    Raises:
    - AddressNotFoundError: If no address is found with the given ID.

    Note:
    - If the address does not exist, an exception is raised with a 404 error.
    """
    address = address_repo.get_address_by_id(db, address_id)
    if not address:
        raise AddressNotFoundError(status_code=404, detail="Addresse introuvable")
    return address


def update_address(
    db: Session,
    address_id: int,
    city: str,
    zipcode: str,
    number: str,
    street: str,
    country: str
) -> Address:
    """
    Updates an existing address in the database.

    Parameters:
    - db (Session): The database session used for queries.
    - address_id (int): The ID of the address to update.
    - city (str): The new city for the address.
    - zipcode (str): The new postal code for the address.
    - number (str): The new building number for the address.
    - street (str): The new street name for the address.
    - country (str): The new country for the address.

    Returns:
    - Address: The updated address object.

    Raises:
    - AddressNotFoundError: If no address is found with the given ID.

    Note:
    - This function retrieves the address by its ID, updates its fields, commits the changes, and refreshes the address object.
    """
    address = address_repo.get_address_by_id(db, address_id)
    if not address:
        raise AddressNotFoundError(status_code=404, detail="Addresse introuvable")
    address.city = city
    address.zipcode = zipcode
    address.number = number
    address.street = street
    address.country = country
    address_repo.commit_address(db)
    address_repo.refresh_address(db, address)
    return address
