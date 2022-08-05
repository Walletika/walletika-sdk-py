from ..tools import interface
from ..data import networks


def get_all() -> list:
    return [i['interface'] for _, i in networks.db.select()]


def add_new(rpc: str, name: str, chain_id: int, symbol: str, explorer: str) -> bool:
    """
    Add a new network
    :exception aesdatabase.error.RowItemError
    """

    network_interface = interface.Network(
        rpc=rpc, name=name, chain_id=chain_id, symbol=symbol, explorer=explorer
    )
    networks.db.insert(row_index=networks.db.count_row(), rpc=rpc, interface=network_interface)
    networks.db.dump()

    return True


def remove(network_interface: interface.Network) -> bool:
    """Remove specific network interface"""

    valid = False

    for index, _ in networks.db.select(
            rpc=network_interface.rpc, interface=network_interface
    ):
        networks.db.remove_row(index)
        networks.db.dump()
        valid = True
        break

    return valid


__all__ = ['get_all', 'add_new', 'remove']
