#!/usr/bin/env python3
"""
Basic tests for Emperor Blockchain
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from blockchain.blockchain import EmperorBlockchain
from blockchain.wallet import Wallet


def test_basic_functionality():
    """Test basic blockchain functionality"""
    print("🧪 Testing Emperor Blockchain...")

    try:
        # Initialize blockchain
        blockchain = EmperorBlockchain(difficulty=2)

        # Create wallets
        wallet1 = Wallet()
        wallet2 = Wallet()

        # Test initial state
        info = blockchain.get_blockchain_info()
        assert info['chain_length'] == 1, "Genesis block should be created"
        assert info['total_supply'] == 1000000000, "Total supply should be 1 billion"

        # Test transaction
        tx = blockchain.create_transaction(
            sender="genesis",
            recipient=wallet1.address,
            amount=1000,
            transaction_type="TEST"
        )
        assert blockchain.add_transaction(tx), "Transaction should be added"

        # Test mining
        block = blockchain.mine_pending_transactions(wallet2.address)
        assert block.index == 1, "New block should be mined"

        # Test balance
        balance = blockchain.get_balance(wallet1.address)
        assert balance == 1000, "Balance should be correct"

        # Test chain validation
        assert blockchain.is_chain_valid(), "Blockchain should be valid"

        print("✅ All tests passed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_basic_functionality()