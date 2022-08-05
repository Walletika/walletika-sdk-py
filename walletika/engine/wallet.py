from ..tools import interface, walletcreator
from ..data import wallets, tokens, transactions
from .provider import MainProvider
import time


recentWalletsEngine = {
    # id: walletEngine
}


def get_all() -> list:
    items = [i['interface'] for _, i in wallets.db.select()]
    favorites = [i for i in items if i.isFavorite]
    for i in favorites:
        items.remove(i)

    return favorites + items


def add_new(username: str, password: str, password_recovery: str, otp_code: str) -> bool:
    """
    Add a new wallet
    :exception aesdatabase.error.RowItemError
    """

    valid = False

    address, _, password_recovery_bytes = walletcreator.access(
        username, password, password_recovery, otp_code
    )

    if address:
        wallet_interface = interface.Wallet(
            username=username,
            address=interface.Address(address),
            password_recovery=password_recovery_bytes,
            date_created=time.ctime(),
            is_favorite=False
        )
        wallets.db.insert(
            row_index=wallets.db.count_row(), username=username, interface=wallet_interface
        )
        wallets.db.dump()
        valid = True

    return valid


def remove(wallet_interface: interface.Wallet) -> bool:
    """Remove specific wallet interface"""

    valid = False

    for index, _ in wallets.db.select(username=wallet_interface.username, interface=wallet_interface):
        wallets.db.remove_row(index)
        wallets.db.dump()
        valid = True
        break

    return valid


def backup_wallets(output_dir: str, wallet_indexes: list = None, password: str = None) -> str:
    """Backup all wallets are selected"""

    return wallets.db.dump_backup(
        row_indexes=wallet_indexes, output_dir=output_dir, password=password
    )


def import_wallets(path: str, wallet_indexes: list = None, password: str = None) -> bool:
    """
    Import all wallets are selected
    :exception aesdatabase.error.SignatureNotFoundError
    :exception aescrypto.error.SignatureNotFoundError
    :exception aescrypto.error.WrongKeyError
    :exception FileNotFoundError
    """

    wallets.db.load_backup(path=path, row_indexes=wallet_indexes, password=password)

    return True


class WalletEngine(object):
    def __init__(self, wallet_interface: interface.Wallet):
        recentWalletsEngine[wallet_interface.address] = self
        self.interface = wallet_interface

        self.__password = None
        self.__isLogged = False

    def username(self) -> str:
        return self.interface.username

    def address(self) -> interface.Address:
        return self.interface.address

    def password_recovery(self) -> bytes:
        return self.interface.passwordRecovery

    def private_key(self, otp_code: str) -> str:
        value = ''

        if self.__isLogged:
            _, value, _ = walletcreator.access(
                self.interface.username, self.__password, self.interface.passwordRecovery, otp_code
            )

        return value

    def date_created(self) -> str:
        return self.interface.dateCreated

    def is_favorite(self) -> bool:
        return self.interface.isFavorite

    def is_logged(self) -> bool:
        return self.__isLogged

    def set_favorite(self, status: bool):
        self.interface.isFavorite = status
        wallets.db.dump()

    def login(self, password: str, otp_code: str) -> bool:
        address, _, _ = walletcreator.access(
            self.interface.username, password, self.interface.passwordRecovery, otp_code
        )

        if address:
            self.__password = password
            self.__isLogged = True

        return self.__isLogged

    def logout(self):
        self.__password = None
        self.__isLogged = False

    def tokens(self) -> list:
        result = []

        for _, i in tokens.db.select(
                rpc=MainProvider.interface.rpc, address=self.interface.address.value()
        ):
            result.append(i['interface'])

        return result

    def add_token(self, token_interface: interface.Token) -> bool:
        valid = False

        if isinstance(token_interface, interface.Token):
            tokens.db.insert(
                row_index=tokens.db.count_row(),
                rpc=MainProvider.interface.rpc,
                address=self.interface.address.value(),
                interface=token_interface
            )
            tokens.db.dump()
            valid = True

        return valid

    def remove_token(self, token_interface: interface.Token) -> bool:
        valid = False

        if isinstance(token_interface, interface.Token):
            for index, _ in tokens.db.select(
                    rpc=MainProvider.interface.rpc,
                    address=self.interface.address.value(),
                    interface=token_interface
            ):
                tokens.db.remove_row(index)
                tokens.db.dump()
                valid = True
                break

        return valid

    def transactions(self, latest: int = None) -> list:
        result = []

        for _, i in transactions.db.select(
                rpc=MainProvider.interface.rpc, address=self.interface.address.value()
        ):
            result.append(i['interface'])

            if latest and len(result) >= latest:
                break

        return result

    def add_transaction(self, transaction_interface: interface.Transaction) -> bool:
        valid = False

        if isinstance(transaction_interface, interface.Transaction):
            transactions.db.insert(
                rpc=MainProvider.interface.rpc,
                address=self.interface.address.value(),
                interface=transaction_interface
            )
            transactions.db.dump()
            valid = True

        return valid

    def remove_transaction(self, transaction_interface: interface.Transaction) -> bool:
        valid = False

        if isinstance(transaction_interface, interface.Transaction):
            for index, _ in transactions.db.select(
                    rpc=MainProvider.interface.rpc,
                    address=self.interface.address.value(),
                    interface=transaction_interface
            ):
                transactions.db.remove_row(index)
                transactions.db.dump()
                valid = True
                break

        return valid


__all__ = ['get_all', 'add_new', 'remove', 'backup_wallets', 'import_wallets', 'WalletEngine']
