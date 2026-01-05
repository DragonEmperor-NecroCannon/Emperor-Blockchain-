import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from src.utils.crypto import CryptoUtils
from src.blockchain.block import Block
from src.blockchain.transaction import Transaction
from src.blockchain.wallet import Wallet


class EmperorBlockchain:
    """
    Main Emperor Blockchain Class
    """

    def __init__(self, difficulty: int = 4):
        """
        Initialize the blockchain
        """
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = 50  # Emperor tokens
        self.token_symbol = "EMPEROR"
        self.total_supply = 1000000000  # 1 billion tokens

        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Create the genesis block (first block)
        """
        print("Creating genesis block with 1 billion EMPEROR tokens...")

        genesis_transaction = Transaction(
            sender="0",  # System address
            recipient="genesis",  # Genesis address
            amount=self.total_supply,
            transaction_type="GENESIS"
        )

        genesis_block = Block(
            index=0,
            transactions=[genesis_transaction],
            timestamp=datetime.now(),
            previous_hash="0" * 64  # 64 zeros for genesis
        )

        # Genesis block doesn't need mining
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        print("✓ Genesis block created successfully")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the chain
        """
        return self.chain[-1]

    def create_transaction(self, sender: str, recipient: str, amount: float,
                           transaction_type: str = "TRANSFER",
                           data: Optional[Dict] = None) -> Transaction:
        """
        Create a new transaction
        """
        return Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            transaction_type=transaction_type,
            data=data
        )

    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a transaction to pending transactions
        """
        if not transaction.is_valid():
            print("❌ Invalid transaction")
            return False

        # System transactions (mining rewards, genesis) are always valid
        if transaction.sender == "0":
            self.pending_transactions.append(transaction)
            return True

        # Check sender balance for regular transactions
        sender_balance = self.get_balance(transaction.sender)
        if sender_balance < transaction.amount:
            print(f"❌ Insufficient balance: {sender_balance} {self.token_symbol}")
            return False

        self.pending_transactions.append(transaction)
        print(f"✓ Transaction added to pending pool: {transaction.amount} {self.token_symbol}")
        return True

    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """
        Mine pending transactions and create new block
        """
        if not self.pending_transactions:
            print("No pending transactions to mine")
            return self.get_latest_block()

        print(f"Mining block with {len(self.pending_transactions)} transactions...")

        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="0",  # System
            recipient=mining_reward_address,
            amount=self.mining_reward,
            transaction_type="MINING_REWARD"
        )
        self.pending_transactions.append(reward_transaction)

        # Create new block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),  # Copy to avoid reference issues
            timestamp=datetime.now(),
            previous_hash=self.get_latest_block().hash
        )

        # Mine the block
        new_block.mine_block(self.difficulty)

        # Add to chain
        self.chain.append(new_block)

        # Reset pending transactions
        self.pending_transactions = []

        print(f"✓ Block #{new_block.index} mined successfully!")
        return new_block

    def get_balance(self, address: str) -> float:
        """
        Get balance for an address
        """
        balance = 0.0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount

        return balance

    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        """
        # Check genesis block
        genesis_block = self.chain[0]
        if (genesis_block.hash != genesis_block.calculate_hash() or
                genesis_block.previous_hash != "0" * 64):
            print("❌ Genesis block is invalid")
            return False

        # Check subsequent blocks
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not current_block.is_valid(previous_block):
                print(f"❌ Block {current_block.index} is invalid")
                return False

            if not CryptoUtils.validate_hash(current_block.hash, self.difficulty):
                print(f"❌ Block {current_block.index} has invalid proof of work")
                return False

        print("✓ Blockchain validation passed")
        return True

    def get_blockchain_info(self) -> Dict[str, Any]:
        """
        Get blockchain information
        """
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_mined = sum(
            1 for block in self.chain for tx in block.transactions if tx.transaction_type == "MINING_REWARD")

        # Calculate circulating supply (all tokens not held by system)
        circulating_supply = 0
        addresses = set()

        for block in self.chain:
            for tx in block.transactions:
                if tx.sender != "0":
                    addresses.add(tx.sender)
                if tx.recipient != "0":
                    addresses.add(tx.recipient)

        for address in addresses:
            circulating_supply += self.get_balance(address)

        return {
            'chain_length': len(self.chain),
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward,
            'token_symbol': self.token_symbol,
            'total_supply': self.total_supply,
            'circulating_supply': circulating_supply,
            'total_transactions': total_transactions,
            'pending_transactions': len(self.pending_transactions),
            'blocks_mined': len(self.chain) - 1,  # Exclude genesis
            'mining_rewards_distributed': total_mined * self.mining_reward,
            'is_valid': self.is_chain_valid()
        }

    def print_chain(self) -> None:
        """
        Print the entire blockchain
        """
        print("\n" + "=" * 80)
        print("EMPEROR BLOCKCHAIN - FULL CHAIN")
        print("=" * 80)

        for block in self.chain:
            print(f"\nBlock #{block.index}:")
            print(f"  Hash: {block.hash}")
            print(f"  Previous: {block.previous_hash}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Transactions: {len(block.transactions)}")

            for tx in block.transactions:
                print(f"    - {tx.transaction_type}: {tx.sender} -> {tx.recipient} {tx.amount} {self.token_symbol}")

    def __repr__(self) -> str:
        return f"EmperorBlockchain(Blocks: {len(self.chain)}, Pending TXs: {len(self.pending_transactions)})"