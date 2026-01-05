import json
from datetime import datetime
from typing import Dict, Any, Optional
from src.utils.crypto import CryptoUtils


class Transaction:
    """
    Emperor Token Transaction Class
    """

    def __init__(self, sender: str, recipient: str, amount: float,
                 transaction_type: str = "TRANSFER", data: Optional[Dict] = None):
        """
        Initialize a new transaction
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now()
        self.transaction_type = transaction_type
        self.data = data or {}
        self.transaction_id = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the transaction hash
        """
        transaction_data = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'type': self.transaction_type,
            'data': self.data
        }
        return CryptoUtils.hash_data(transaction_data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert transaction to dictionary
        """
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'type': self.transaction_type,
            'data': self.data
        }

    def is_valid(self) -> bool:
        """
        Validate transaction structure
        """
        if self.amount <= 0:
            return False

        if self.sender == self.recipient and self.transaction_type != "MINING_REWARD":
            return False

        if not isinstance(self.amount, (int, float)):
            return False

        # Verify hash integrity
        return self.transaction_id == self.calculate_hash()

    def __repr__(self) -> str:
        return f"Transaction({self.transaction_id[:8]}...: {self.sender} -> {self.recipient} {self.amount} EMPEROR)"