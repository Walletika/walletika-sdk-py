from ..tools import interface
from ..data import addressesbook


def get_all() -> list:
    return [i['interface'] for _, i in addressesbook.db.select()]


def add_new(username: str, address: interface.Address) -> bool:
    """
    Add a new address book
    :exception aesdatabase.error.RowItemError
    """

    address_book_interface = interface.AddressBook(
        username=username, address=address
    )
    addressesbook.db.insert(
        row_index=addressesbook.db.count_row(), username=username, interface=address_book_interface
    )
    addressesbook.db.dump()

    return True


def remove(address_book_interface: interface.AddressBook) -> bool:
    """Remove specific address book interface"""

    valid = False

    for index, _ in addressesbook.db.select(
            username=address_book_interface.username, interface=address_book_interface
    ):
        addressesbook.db.remove_row(index)
        addressesbook.db.dump()
        valid = True
        break

    return valid


__all__ = ['get_all', 'add_new', 'remove']
