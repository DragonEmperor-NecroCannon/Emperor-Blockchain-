import hashlib
import json
from datetime import datetime
from typing import Any, Dict


class CryptoUtils:
    """
    Cryptographic utilities for the Emperor blockchain
    """

    @staticmethod
    def hash_data(data: Any) -> str:
        """
        Create SHA-256 hash of any data
        """
        if isinstance(data, (dict, list)):
            data_string = json.dumps(data, sort_keys=True, default=str)
        else:
            data_string = str(data)

        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_block(block_data: Dict) -> str:
        """
        Create a hash for a block
        """
        block_string = json.dumps(block_data, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_hash(hash_value: str, difficulty: int) -> bool:
        """
        Validate if hash meets difficulty requirement
        """
        return hash_value.startswith('0' * difficulty)