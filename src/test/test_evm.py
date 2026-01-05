import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from blockchain.blockchain import EmperorBlockchain
from blockchain.wallet import Wallet
from blockchain.evm.solidity_compiler import ContractTemplate


class TestEVMIntegration(unittest.TestCase):
    """Test cases for EVM and smart contract integration"""

    def setUp(self):
        self.blockchain = EmperorBlockchain(difficulty=2)
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

        # Fund wallet1
        fund_tx = self.blockchain.create_transaction(
            sender="0",
            recipient=self.wallet1.address,
            amount=1000.0,
            transaction_type="SYSTEM_ISSUANCE"
        )
        self.blockchain.add_transaction(fund_tx)
        self.blockchain.mine_pending_transactions(self.wallet2.address)

    def test_contract_deployment(self):
        """Test smart contract deployment"""
        source = ContractTemplate.get_simple_storage_template()
        contract = self.blockchain.deploy_contract(
            creator=self.wallet1.address,
            contract_source=source,
            contract_name="SimpleStorage"
        )

        self.assertIsNotNone(contract)
        self.assertTrue(contract.address.startswith("EMP"))

        # Mine deployment
        self.blockchain.mine_pending_transactions(self.wallet2.address)

        # Verify contract exists in registry
        contract_info = self.blockchain.get_contract_info(contract.address)
        self.assertIsNotNone(contract_info)

    def test_contract_interaction(self):
        """Test contract function calls"""
        # Deploy contract
        source = ContractTemplate.get_simple_storage_template()
        contract = self.blockchain.deploy_contract(
            creator=self.wallet1.address,
            contract_source=source,
            contract_name="SimpleStorage"
        )
        self.blockchain.mine_pending_transactions(self.wallet2.address)

        # Test set function
        result = self.blockchain.execute_contract_call(
            contract_address=contract.address,
            function_name="set",
            args=[123],
            caller=self.wallet1.address
        )

        self.blockchain.mine_pending_transactions(self.wallet2.address)

        # Test get function
        value = self.blockchain.execute_contract_call(
            contract_address=contract.address,
            function_name="get",
            args=[],
            caller=self.wallet1.address
        )

        self.assertEqual(value, 123)

    def test_token_contract(self):
        """Test ERC20 token contract functionality"""
        source = ContractTemplate.get_emperor_token_template()
        token_contract = self.blockchain.deploy_contract(
            creator=self.wallet1.address,
            contract_source=source,
            contract_name="EmperorToken",
            initial_supply=1000
        )
        self.blockchain.mine_pending_transactions(self.wallet2.address)

        # Check initial balance
        balance = self.blockchain.get_contract_balance(
            token_contract.address, self.wallet1.address
        )
        self.assertEqual(balance, 1000)

        # Test token transfer
        transfer_result = self.blockchain.execute_contract_call(
            contract_address=token_contract.address,
            function_name="transfer",
            args=[self.wallet2.address, 100],
            caller=self.wallet1.address
        )

        self.blockchain.mine_pending_transactions(self.wallet2.address)
        self.assertTrue(transfer_result)

        # Check updated balances
        balance1 = self.blockchain.get_contract_balance(
            token_contract.address, self.wallet1.address
        )
        balance2 = self.blockchain.get_contract_balance(
            token_contract.address, self.wallet2.address
        )

        self.assertEqual(balance1, 900)
        self.assertEqual(balance2, 100)


if __name__ == '__main__':
    unittest.main()