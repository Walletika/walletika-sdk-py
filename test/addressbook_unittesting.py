from walletika import engine, tools
import unittest


debugging = True


def specific_addresses_details() -> list:
    return [
        ['0xC94EA8D9694cfe25b94D977eEd4D60d7c0985BD3', 'username1'],
        ['0xB41aD6b3EE5373dbAC2b471E4582A0b50f4bC9DE', 'username2'],
        ['0xB72bEC2cB81F9B61321575D574BAC577BAb99141', 'username3'],
        ['0x45EF6cc9f2aD7A85e282D14fc23C745727e547b6', 'username4'],
        ['0x71471d05114c758eBfC3D3b952a722Ef2d53970b', 'username5']
    ]


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


class AddressBookUnitTesting(unittest.TestCase):
    def test1_add_new(self):
        function_name('add_new')

        for i, (address, username) in enumerate(specific_addresses_details()):
            # Task
            address = tools.interface.Address(address)
            result: bool = engine.addressbook.add_new(
                username=username,
                address=address
            )

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                address: {address.value()}
                username: {username}
                result: {result}
                """)

            # Test
            self.assertTrue(result, msg="address book failed to add to database")

    def test2_get_all(self):
        function_name('get_all')

        # Task
        result: [tools.interface.AddressBook] = engine.addressbook.get_all()

        for i, address_book in enumerate(result):
            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                address: {address_book.address.value()}
                username: {address_book.username}
                """)

            # Test
            self.assertIsInstance(address_book, tools.interface.AddressBook, msg="it's not address book interface")
            self.assertIsInstance(address_book.address, tools.interface.Address, msg="it's not address interface")
            self.assertIsInstance(address_book.username, str)

    def test3_remove(self):
        function_name('remove')

        for i, address_book in enumerate(engine.addressbook.get_all()):
            # Task
            result: bool = engine.addressbook.remove(address_book)

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                address: {address_book.address.value()}
                username: {address_book.username}
                result: {result}
                """)

            # Test
            self.assertIsInstance(address_book, tools.interface.AddressBook, msg="it's not address book interface")
            self.assertTrue(result, msg="address book failed to remove")

        self.assertAlmostEqual(len(engine.addressbook.get_all()), 0, msg="addresses book have not been removed")


if __name__ == '__main__':
    unittest.main()
