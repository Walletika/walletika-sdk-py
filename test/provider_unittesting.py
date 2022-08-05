from walletika import engine, tools
from web3 import datastructures
import time
import pyotp
import unittest


debugging = True
sendTransactionEnabled = True


def specific_wallets_details() -> list:
    return [
        ['0xC94EA8D9694cfe25b94D977eEd4D60d7c0985BD3', 'username1', 'password1', '123456'],
        ['0xB41aD6b3EE5373dbAC2b471E4582A0b50f4bC9DE', 'username2', 'password2', '123457'],
        ['0xB72bEC2cB81F9B61321575D574BAC577BAb99141', 'username3', 'password3', '123458'],
        ['0x45EF6cc9f2aD7A85e282D14fc23C745727e547b6', 'username4', 'password4', '123459'],
        ['0x71471d05114c758eBfC3D3b952a722Ef2d53970b', 'username5', 'password5', '123460']
    ]


def specific_networks_details() -> dict:
    return {
        "Ethereum": tools.interface.Network(
            name="Ethereum",
            rpc="https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=1,
            symbol="ETH",
            explorer="https://etherscan.io"
        ),
        "Ethereum Ropsten (Testnet)": tools.interface.Network(
            name="Ethereum Ropsten (Testnet)",
            rpc="https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=3,
            symbol="ETH",
            explorer="https://ropsten.etherscan.io"
        ),
        "Ethereum Goerli (Testnet)": tools.interface.Network(
            name="Ethereum Goerli (Testnet)",
            rpc="https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            chain_id=5,
            symbol="ETH",
            explorer="https://goerli.etherscan.io"
        ),
        "Binance Smart Chain": tools.interface.Network(
            name="Binance Smart Chain",
            rpc="https://bsc-dataseed1.binance.org",
            chain_id=56,
            symbol="BNB",
            explorer="https://bscscan.com"
        ),
        "Binance Smart Chain (Testnet)": tools.interface.Network(
            name="Binance Smart Chain (Testnet)",
            rpc="https://data-seed-prebsc-1-s1.binance.org:8545",
            chain_id=97,
            symbol="BNB",
            explorer="https://testnet.bscscan.com"
        ),
        "Matic Mumbai (Testnet)": tools.interface.Network(
            name="Binance Smart Chain (Testnet)",
            rpc="https://rpc-mumbai.maticvigil.com",
            chain_id=80001,
            symbol="MATIC",
            explorer="https://mumbai.polygonscan.com"
        )
    }


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


class NetworkUnitTesting(unittest.TestCase):
    def test_main_provider_ethereum(self):
        network_name = "Ethereum Ropsten (Testnet)"
        function_name('MainProvider > %s' % network_name)

        self.__run(network_name)

    def test_main_provider_binance(self):
        network_name = "Binance Smart Chain (Testnet)"
        function_name('MainProvider > %s' % network_name)

        self.__run(network_name)

    def test_main_provider_polygon(self):
        network_name = "Matic Mumbai (Testnet)"
        function_name('MainProvider > %s' % network_name)

        self.__run(network_name)

    def __run(self, network_name: str):
        # Task
        network = specific_networks_details()[network_name]
        engine.provider.MainProvider.connect(network)

        # Network test
        self.assertIsInstance(
            engine.provider.MainProvider.interface,
            tools.interface.Network, msg="it's not network interface"
        )
        self.assertTrue(engine.provider.MainProvider.is_connected())
        self.assertIsInstance(engine.provider.MainProvider.block_number(), int)

        # Wallet interaction test
        receipt = tools.interface.Address('0x71471d05114c758eBfC3D3b952a722Ef2d53970b')
        amount = tools.interface.EtherAmount(0.01, decimals=18)

        for address, username, password, recoveryPassword in specific_wallets_details():
            # Task
            otp_hash = tools.walletcreator.otp_hash(username, password, recoveryPassword)
            otp_code = pyotp.TOTP(otp_hash).now()
            address, private_key, _ = tools.walletcreator.access(
                username, password, recoveryPassword, otp_code
            )
            address = tools.interface.Address(address)
            balance = engine.provider.MainProvider.balance_of(address)

            # Debugging
            if debugging:
                print(f"""
                address: {address.value()}
                username: {username}
                otp_code: {otp_code}
                balance: {balance.to_ether_string()}
                """)

            # Test
            self.assertIsInstance(balance.value(), int)

            if sendTransactionEnabled and balance.to_ether() > 0.1:
                tx = engine.provider.MainProvider.build_transaction(address, receipt, amount)

                eip1559_status = False
                if address.value() == receipt.value() and network.symbol == 'ETH':
                    eip1559_status = True

                engine.provider.MainProvider.add_gas(tx, eip1559_enabled=eip1559_status)
                tx_hash = engine.provider.MainProvider.send_transaction(tx, private_key)
                time.sleep(5)
                tx_hash.explorer_view()
                transaction = engine.provider.MainProvider.get_transaction(tx_hash)
                transaction_receipt = engine.provider.MainProvider.get_transaction_receipt(tx_hash)

                self.assertIsInstance(tx_hash, tools.interface.TXHash)
                self.assertIsInstance(transaction, datastructures.AttributeDict)
                self.assertIsInstance(transaction_receipt, datastructures.AttributeDict)

                if debugging:
                    print(f"""
                    tx_hash: {tx_hash.value()}
                    receipt: {receipt.value()}
                    amount: {amount.value()}
                    transaction: {transaction}
                    transaction_receipt: {transaction_receipt}
                    """)


if __name__ == '__main__':
    unittest.main()
