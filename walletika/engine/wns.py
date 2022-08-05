from .provider import WNSProvider, Metadata
from ..abis import wnsABI
from ..tools import interface


class WNSEngine(object):
    def __init__(self, sender: interface.Address = None):
        self.sender = sender
        self.contract = WNSProvider.web3.eth.contract(
            address=WNSProvider.contract().value(), abi=wnsABI
        )
        self.latestTransactionDetails = {
            'abi': {},
            'args': {},
            'data': b''
        }

    def owner(self) -> interface.Address:
        return interface.Address(self.contract.functions.owner().call())

    def users_count(self) -> int:
        return self.contract.functions.usersCount().call()

    def is_reserved(self, name: str) -> bool:
        return self.contract.functions.isReserved(name).call()

    def is_recorded(self, name: str) -> bool:
        return self.contract.functions.isRecorded(name).call()

    def get_by_name(self, name: str) -> dict:
        result = self.contract.functions.getByName(name).call()
        return {
            'address': interface.Address(result[0]),
            'isVerified': result[1],
            'isScammer': result[2]
        }

    def get_by_address(self, address: interface.Address) -> dict:
        result = self.contract.functions.getByAddress(address.value()).call()
        return {
            'username': result[0],
            'isVerified': result[1],
            'isScammer': result[2]
        }

    def new_record(self, name: str) -> dict:
        return self._build_transaction(
            self.contract.functions.newRecord(name)
        )

    def transfer_name(self, new_owner: interface.Address) -> dict:
        return self._build_transaction(
            self.contract.functions.transferName(new_owner.value())
        )

    # Owner functions
    def set_verified(self, name: str, state: bool) -> dict:
        return self._build_transaction(
            self.contract.functions.setVerified(name, state)
        )

    def set_scammer(self, name: str, address: interface.Address, state: bool) -> dict:
        return self._build_transaction(
            self.contract.functions.setScammer(name, address.value(), state)
        )

    def reserve_users(self, users: list, statuses: list) -> dict:
        return self._build_transaction(
            self.contract.functions.reserveUsers(users, statuses)
        )

    def set_multi_verified(self, users: list, statuses: list) -> dict:
        return self._build_transaction(
            self.contract.functions.setMultiVerified(users, statuses)
        )

    def set_multi_scammers(self, users: list, addresses: list, statuses: list) -> dict:
        _addresses = [i.value() if isinstance(i, interface.Address) else i for i in addresses]

        return self._build_transaction(
            self.contract.functions.setMultiScammers(users, _addresses, statuses)
        )

    def renounce_ownership(self) -> dict:
        return self._build_transaction(
            self.contract.functions.renounceOwnership()
        )

    def transfer_ownership(self, new_owner: interface.Address) -> dict:
        return self._build_transaction(
            self.contract.functions.transferOwnership(new_owner.value())
        )

    def _build_transaction(self, method) -> dict:
        if not isinstance(self.sender, interface.Address):
            raise ValueError("The sender must not be a zero address")

        abi = method.abi
        args = {}

        # Get args
        for index, npt in enumerate(abi['inputs']):
            npt_name = npt['name']
            npt_type = npt['type']

            try:
                value = method.args[index]
            except IndexError:
                args[npt_name] = None
                continue

            if npt_type == 'address':
                args[npt_name] = interface.Address(value)
            elif npt_type == 'address[]':
                args[npt_name] = [interface.Address(address) for address in value]
            else:
                args[npt_name] = value

        tx = method.buildTransaction({
            Metadata.FROM: self.sender.value(),
            Metadata.GAS_PRICE: WNSProvider.web3.eth.gas_price
        })
        tx[Metadata.NONCE] = WNSProvider.web3.eth.get_transaction_count(self.sender.value())
        self.latestTransactionDetails.update({
            'abi': abi, 'args': args, 'data': tx[Metadata.DATA]
        })

        return tx


__all__ = ['WNSEngine']
