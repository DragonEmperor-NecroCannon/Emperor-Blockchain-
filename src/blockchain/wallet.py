import hashlib
import secrets
from typing import Dict, Any, Optional
from src.blockchain.transaction import Transaction


class Wallet:
    """
    Emperor Blockchain Wallet Class
    """

    def __init__(self, address: Optional[str] = None):
        """
        Initialize a wallet
        """
        if address:
            self.address = address
        else:
            self.address = self.generate_address()

    @staticmethod
    def generate_address() -> str:
        """
        Generate a new wallet address
        """
        random_data = secrets.token_bytes(32)
        address_hash = hashlib.sha256(random_data).hexdigest()[:40]
        return f"EMP{address_hash}"

    def create_transaction(self, recipient: str, amount: float,
                           transaction_type: str = "TRANSFER",
                           data: Optional[Dict] = None) -> Transaction:
        """
        Create a new transaction
        """
        return Transaction(
            sender=self.address,
            recipient=recipient,
            amount=amount,
            transaction_type=transaction_type,
            data=data
        )

    def get_balance(self, blockchain) -> float:
        """
        Get wallet balance from blockchain
        """
        return blockchain.get_balance(self.address)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert wallet to dictionary
        """
        return {
            'address': self.address
        }

    def __repr__(self) -> str:
        return f"Wallet({self.address})"