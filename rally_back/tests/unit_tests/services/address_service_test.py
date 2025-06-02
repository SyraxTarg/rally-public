from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session

from models.address_model import Address
from services import address_service
from errors import AddressNotFoundError

 

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_add_new_address(mocker):
    return mocker.patch("repositories.address_repo.add_new_address")

@pytest.fixture
def mock_commit_address(mocker):
    return mocker.patch("repositories.address_repo.commit_address")

@pytest.fixture
def mock_refresh_address(mocker):
    return mocker.patch("repositories.address_repo.refresh_address")

@pytest.fixture
def mock_get_address_by_id(mocker):
    return mocker.patch("repositories.address_repo.get_address_by_id")




@pytest.fixture
def mock_address():
    fake_address = MagicMock(spec=Address)
    fake_address.city = "Bordeaux"
    fake_address.id = 1
    fake_address.zipcode = "33300"
    fake_address.number = "15"
    fake_address.street = "Cours Louis Fargue"
    fake_address.country = "France"
    return fake_address


@patch("services.address_service.Address")
def test_create_address(
    mock_address_class,
    mock_address,
    mock_db_session,
    mock_add_new_address,
    mock_commit_address,
    mock_refresh_address
):
    # Arrange
    mock_address_class.return_value = mock_address
    mock_add_new_address.return_value = None
    mock_commit_address.return_value = None
    mock_refresh_address.return_value = None

    # Act
    result = address_service.create_address(
        db=mock_db_session,
        city="Bordeaux",
        zipcode="33300",
        number="15",
        street="Cours Louis Fargue",
        country="France"
    )

    # Assert
    assert result.city == "Bordeaux"
    assert result.zipcode == "33300"
    assert result.number == "15"
    assert result.street == "Cours Louis Fargue"
    assert result.country == "France"
    mock_add_new_address.assert_called_once()
    mock_commit_address.assert_called_once()
    mock_refresh_address.assert_called_once()


def test_get_address_by_id(mock_address, mock_db_session, mock_get_address_by_id):
    # Arrange
    mock_get_address_by_id.return_value = mock_address

    # Act
    result = address_service.get_address_by_id(db=mock_db_session, address_id=1)

    # Assert
    assert result.id == 1
    mock_get_address_by_id.assert_called_once()


def test_get_address_by_id_not_found(mock_db_session, mock_get_address_by_id):
    # Arrange
    mock_get_address_by_id.return_value = None

    # Act
    with pytest.raises(AddressNotFoundError) as result:
        address_service.get_address_by_id(db=mock_db_session, address_id=1)

    # Assert
    assert str(result.value) == "404: Addresse introuvable"
    mock_get_address_by_id.assert_called_once()


def test_update_address(
    mock_address,
    mock_db_session,
    mock_commit_address,
    mock_refresh_address,
    mock_get_address_by_id
):
    # Arrange
    mock_get_address_by_id.return_value = mock_address
    mock_commit_address.return_value = None
    mock_refresh_address.return_value = None

    # Act
    result = address_service.update_address(
        db=mock_db_session,
        address_id=1,
        city="Paris",
        zipcode="75000",
        number="8",
        street="Rue de la paix",
        country="France"
    )

    # Assert
    assert result.city == "Paris"
    assert result.zipcode == "75000"
    assert result.number == "8"
    assert result.street == "Rue de la paix"
    assert result.country == "France"
    mock_commit_address.assert_called_once()
    mock_refresh_address.assert_called_once()

def test_update_address_not_found(
    mock_db_session,
    mock_get_address_by_id
):
    # Arrange
    mock_get_address_by_id.return_value = None

    # Act
    with pytest.raises(AddressNotFoundError) as result:
        address_service.update_address(
            db=mock_db_session,
            address_id=1,
            city="Paris",
            zipcode="75000",
            number="8",
            street="Rue de la paix",
            country="France"
        )

    # Assert
    assert str(result.value) == "404: Addresse introuvable"
