import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from src.utils.crypto import CryptoUtils
from src.blockchain.transaction import Transaction


class Block:
    """
    Emperor Blockchain Block Class
    """

    def __init__(self, index: int, transactions: List[Transaction],
                 timestamp: datetime, previous_hash: str, nonce: int = 0):
        """
        Initialize a new block
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the block hash
        """
        block_data = {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp.isoformat(),
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        return CryptoUtils.hash_block(block_data)

    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block (Proof of Work)
        """
        print(f"Mining block {self.index}...")
        start_time = datetime.now()

        while not CryptoUtils.validate_hash(self.hash, difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()

        mining_time = (datetime.now() - start_time).total_seconds()
        print(f"Block mined: {self.hash} (Time: {mining_time:.2f}s, Nonce: {self.nonce})")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary
        """
        return {
            'index': self.index,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp.isoformat(),
            'nonce': self.nonce,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'transaction_count': len(self.transactions)
        }

    def is_valid(self, previous_block: Optional['Block'] = None) -> bool:
        """
        Validate block integrity
        """
        # Verify hash integrity
        if self.hash != self.calculate_hash():
            return False

        # Verify transactions are valid
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False

        # Verify chain linkage (skip for genesis block)
        if previous_block and self.previous_hash != previous_block.hash:
            return False

        return True

    def __repr__(self) -> str:
        return f"Block({self.index}: {self.hash[:8]}..., TXs: {len(self.transactions)})"