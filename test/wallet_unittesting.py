from walletika import engine, tools, MainProvider
from web3 import Web3
import pyotp
import random
import string
import unittest


debugging = True


# Create a network interface
defaultNetwork = tools.interface.Network(
    rpc='https://data-seed-prebsc-1-s1.binance.org:8545',
    name='Binance Smart Chain (TestNet)',
    chain_id=97,
    symbol='BNB',
    explorer='https://testnet.bscscan.com'
)
MainProvider.connect(network_interface=defaultNetwork)


def random_wallet_details() -> tuple[str, str, str]:
    chars = string.ascii_letters + string.digits
    username = ''.join(random.choices(chars, k=15))
    password = ''.join(random.choices(chars, k=15))
    password_recovery = ''.join(random.choices(chars, k=15))

    return username, password, password_recovery


def specific_wallets_details() -> list:
    return [
        ['0xC94EA8D9694cfe25b94D977eEd4D60d7c0985BD3', 'username1', 'password1', '123456'],
        ['0xB41aD6b3EE5373dbAC2b471E4582A0b50f4bC9DE', 'username2', 'password2', '123457'],
        ['0xB72bEC2cB81F9B61321575D574BAC577BAb99141', 'username3', 'password3', '123458'],
        ['0x45EF6cc9f2aD7A85e282D14fc23C745727e547b6', 'username4', 'password4', '123459'],
        ['0x71471d05114c758eBfC3D3b952a722Ef2d53970b', 'username5', 'password5', '123460']
    ]


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


class WalletUnitTesting(unittest.TestCase):
    def test1_otp_hash(self):
        function_name('otp_hash')

        for i in range(5):
            # Task
            username, password, password_recovery = random_wallet_details()
            otp_hash = tools.walletcreator.otp_hash(username, password, password_recovery)
            otp_code = pyotp.TOTP(otp_hash).now()

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                username: {username}
                password: {password}
                password_recovery: {password_recovery}
                otp_hash: {otp_hash}
                otp_code: {otp_code}
                """)

            # Test
            self.assertIsInstance(otp_hash, str)
            self.assertIsInstance(otp_code, str)
            self.assertTrue(otp_code.isdigit())

    def test2_access(self):
        function_name('access')
        for i in range(5):
            # Task
            username, password, password_recovery = random_wallet_details()
            otp_hash = tools.walletcreator.otp_hash(username, password, password_recovery)
            otp_code = pyotp.TOTP(otp_hash).now()
            address, private_key, password_recovery_bytes = tools.walletcreator.access(
                username, password, password_recovery, otp_code
            )
            address = tools.interface.Address(address)

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                username: {username}
                password: {password}
                password_recovery: {password_recovery}
                password_recovery_bytes: {password_recovery_bytes}
                address: {address.value()}
                private_key: {private_key}
                otp_hash: {otp_hash}
                otp_code: {otp_code}
                """)

            # Test
            info = Web3(Web3.HTTPProvider).eth.account.from_key(private_key)
            self.assertIsInstance(address, tools.interface.Address, msg="it's not address interface")
            self.assertEqual(info.address, address.value())
            self.assertEqual(info.key.hex(), private_key)
            self.assertIsInstance(password_recovery_bytes, bytes)

    def test3_add_new(self):
        function_name('add_new')

        for i, (address, username, password, password_recovery) in enumerate(specific_wallets_details()):
            # Task
            otp_hash = tools.walletcreator.otp_hash(username, password, password_recovery)
            otp_code = pyotp.TOTP(otp_hash).now()
            result: bool = engine.wallet.add_new(
                username, password, password_recovery, otp_code
            )

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                username: {username}
                password: {password}
                password_recovery: {password_recovery}
                address: {address}
                otp_hash: {otp_hash}
                otp_code: {otp_code}
                result: {result}
                """)

            # Test
            self.assertTrue(result, msg="wallet failed to add to database")

    def test4_get_all(self):
        function_name('get_all')

        # Task
        result: [tools.interface.Wallet] = engine.wallet.get_all()

        for i, wallet in enumerate(result):
            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                address: {wallet.address.value()}
                username: {wallet.username}
                passwordRecovery: {wallet.passwordRecovery}
                dateCreated: {wallet.dateCreated}
                isFavorite: {wallet.isFavorite}
                """)

            # Test
            self.assertIsInstance(wallet, tools.interface.Wallet, msg="it's not wallet interface")
            self.assertIsInstance(wallet.address, tools.interface.Address, msg="it's not address interface")
            self.assertIsInstance(wallet.username, str)
            self.assertIsInstance(wallet.passwordRecovery, bytes)
            self.assertIsInstance(wallet.dateCreated, str)
            self.assertIsInstance(wallet.isFavorite, bool)

    def test5_wallet_engine(self):
        function_name('WalletEngine')

        # Task
        wallet: tools.interface.Wallet = engine.wallet.get_all()[0]
        wallet_engine = engine.wallet.WalletEngine(wallet_interface=wallet)
        address = wallet_engine.address()
        username = wallet_engine.username()
        password_recovery = wallet_engine.password_recovery()
        date_created = wallet_engine.date_created()
        is_favorite = wallet_engine.is_favorite()
        tokens = wallet_engine.tokens()
        transactions = wallet_engine.transactions()

        _, _, password, password_recovery_str = specific_wallets_details()[0]
        otp_hash = tools.walletcreator.otp_hash(username, password, password_recovery_str)
        otp_code = pyotp.TOTP(otp_hash).now()
        otp_code_failed = '123456'

        # Debugging
        if debugging:
            print(f"""
            address: {address.value()}
            username: {username}
            password: {password}
            password_recovery_str: {password_recovery_str}
            password_recovery: {password_recovery}
            dateCreated: {date_created}
            isFavorite: {is_favorite}
            tokens: {tokens}
            transactions: {transactions}
            otp_hash: {otp_hash}
            """)

        # Test
        self.assertIsInstance(wallet, tools.interface.Wallet, msg="it's not wallet interface")
        self.assertIsInstance(wallet_engine, engine.wallet.WalletEngine, msg="it's not wallet engine")
        self.assertIsInstance(address, tools.interface.Address, msg="it's not address interface")
        self.assertIsInstance(username, str)
        self.assertIsInstance(password_recovery, bytes)
        self.assertIsInstance(date_created, str)
        self.assertIsInstance(is_favorite, bool)
        self.assertIsInstance(tokens, list)
        self.assertIsInstance(transactions, list)
        self.assertEqual(address, wallet.address)
        self.assertEqual(username, wallet.username)
        self.assertEqual(password_recovery, wallet.passwordRecovery)
        self.assertEqual(date_created, wallet.dateCreated)
        self.assertEqual(is_favorite, wallet.isFavorite)
        self.assertEqual(tokens, [])
        self.assertEqual(transactions, [])
        self.assertFalse(wallet_engine.is_logged(), msg="must isLogged = False before login")
        self.assertEqual(wallet_engine.private_key(otp_code), '', msg="must privateKey = '' before login")
        self.assertFalse(wallet_engine.login(password, otp_code_failed), msg="login must fail")
        self.assertTrue(wallet_engine.login(password, otp_code), msg="login must be successful")
        self.assertTrue(wallet_engine.is_logged(), msg="must isLogged = True after login")
        self.assertAlmostEqual(
            len(wallet_engine.private_key(otp_code)), 66, msg="must privateKey == 66 char after login"
        )
        self.assertEqual(
            wallet_engine.private_key(otp_code_failed), '', msg="must privateKey = '' for wrong otp code"
        )
        self.assertIsNone(wallet_engine.logout())
        self.assertFalse(wallet_engine.is_logged(), msg="must isLogged = False after logout")

    def test6_remove(self):
        function_name('remove')

        for i, wallet in enumerate(engine.wallet.get_all()):
            # Task
            result: bool = engine.wallet.remove(wallet)

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                address: {wallet.address.value()}
                username: {wallet.username}
                passwordRecovery: {wallet.passwordRecovery}
                dateCreated: {wallet.dateCreated}
                isFavorite: {wallet.isFavorite}
                result: {result}
                """)

            # Test
            self.assertIsInstance(wallet, tools.interface.Wallet, msg="it's not wallet interface")
            self.assertTrue(result, msg="wallet failed to remove")

        self.assertAlmostEqual(len(engine.wallet.get_all()), 0, msg="wallets have not been removed")


if __name__ == '__main__':
    unittest.main()
