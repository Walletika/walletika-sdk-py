from walletika import engine, tools
import unittest


debugging = True


def specific_networks_details() -> dict:
    return {
        "Ethereum": {
            "provider": "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            "explorer": "https://etherscan.io",
            "chainID": 1,
            "symbol": "ETH"
        },
        "Ethereum Ropsten (Testnet)": {
            "provider": "https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            "explorer": "https://ropsten.etherscan.io",
            "chainID": 3,
            "symbol": "ETH"
        },
        "Ethereum Goerli (Testnet)": {
            "provider": "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            "explorer": "https://goerli.etherscan.io",
            "chainID": 5,
            "symbol": "ETH",
        },
        "Binance Smart Chain": {
            "provider": "https://bsc-dataseed1.binance.org",
            "explorer": "https://bscscan.com",
            "chainID": 56,
            "symbol": "BNB",
        },
        "Binance Smart Chain (Testnet)": {
            "provider": "https://data-seed-prebsc-1-s1.binance.org:8545",
            "explorer": "https://testnet.bscscan.com",
            "chainID": 97,
            "symbol": "BNB",
        }
    }


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


class NetworkUnitTesting(unittest.TestCase):
    def test1_add_new(self):
        function_name('add_new')

        for i, (name, data) in enumerate(specific_networks_details().items()):
            # Task
            result: bool = engine.network.add_new(
                name=name,
                rpc=data['provider'],
                chain_id=data['chainID'],
                symbol=data['symbol'],
                explorer=data['explorer']
            )

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                name: {name}
                rpc: {data['provider']}
                chainID: {data['chainID']}
                symbol: {data['symbol']}
                explorer: {data['explorer']}
                result: {result}
                """)

            # Test
            self.assertTrue(result, msg="network failed to add to database")

    def test2_get_all(self):
        function_name('get_all')

        # Task
        result: [tools.interface.Network] = engine.network.get_all()

        for i, network in enumerate(result):
            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                name: {network.name}
                rpc: {network.rpc}
                chainID: {network.chainID}
                symbol: {network.symbol}
                explorer: {network.explorer}
                """)

            # Test
            self.assertIsInstance(network, tools.interface.Network, msg="it's not network interface")
            self.assertIsInstance(network.name, str)
            self.assertIsInstance(network.rpc, str)
            self.assertIsInstance(network.chainID, int)
            self.assertIsInstance(network.symbol, str)
            self.assertIsInstance(network.explorer, str)

    def test3_remove(self):
        function_name('remove')
        for i, network in enumerate(engine.network.get_all()):
            # Task
            result: bool = engine.network.remove(network)

            # Debugging
            if debugging:
                print(f"""
                attempt: {i}
                ------------
                name: {network.name}
                rpc: {network.rpc}
                chainID: {network.chainID}
                symbol: {network.symbol}
                explorer: {network.explorer}
                result: {result}
                """)

            # Test
            self.assertIsInstance(network, tools.interface.Network, msg="it's not network interface")
            self.assertTrue(result, msg="network failed to remove")

        self.assertAlmostEqual(len(engine.network.get_all()), 0, msg="networks have not been removed")


if __name__ == '__main__':
    unittest.main()
