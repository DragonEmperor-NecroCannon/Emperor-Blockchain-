"""
Smart Contract Implementation for Emperor Blockchain
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.utils.crypto import CryptoUtils


class SmartContract:
    """
    Smart Contract class for Emperor Blockchain
    """

    def __init__(self, address: str, bytecode: bytes, abi: List[Dict] = None):
        """
        Initialize a smart contract

        Args:
            address: Contract address
            bytecode: Contract bytecode
            abi: Contract ABI
        """
        self.address = address
        self.bytecode = bytecode
        self.abi = abi or []
        self.storage: Dict[str, Any] = {}
        self.creation_timestamp = datetime.now()

    @classmethod
    def create_contract(cls, creator: str, bytecode: bytes, abi: List[Dict] = None) -> 'SmartContract':
        """
        Create a new smart contract

        Args:
            creator: Creator's address
            bytecode: Contract bytecode
            abi: Contract ABI

        Returns:
            SmartContract: New contract instance
        """
        # Generate contract address from creator and nonce
        contract_data = f"{creator}{datetime.now().isoformat()}{bytecode.hex()}"
        contract_hash = CryptoUtils.hash_data(contract_data)
        contract_address = f"EMP{contract_hash[:37]}"  # EMP + 37 chars

        return cls(contract_address, bytecode, abi)

    def get_function_abi(self, function_name: str) -> Optional[Dict]:
        """Get ABI for a specific function"""
        for item in self.abi:
            if item.get('name') == function_name and item.get('type') == 'function':
                return item
        return None

    def execute_function(self, function_name: str, args: List[Any], caller: str, value: int = 0) -> Any:
        """
        Execute a contract function (simplified simulation)

        Args:
            function_name: Function to execute
            args: Function arguments
            caller: Caller address
            value: Value sent with call

        Returns:
            Any: Function result
        """
        function_abi = self.get_function_abi(function_name)
        if not function_abi:
            raise ValueError(f"Function {function_name} not found in ABI")

        # Simulate function execution based on ABI
        if function_name == "balanceOf":
            return self._execute_balance_of(args[0])
        elif function_name == "transfer":
            return self._execute_transfer(caller, args[0], args[1])
        elif function_name == "get":
            return self._execute_get()
        elif function_name == "set":
            return self._execute_set(args[0])
        else:
            raise ValueError(f"Function {function_name} not implemented in simulator")

    def _execute_balance_of(self, address: str) -> int:
        """Execute balanceOf function"""
        return self.storage.get(f"balance_{address}", 0)

    def _execute_transfer(self, sender: str, recipient: str, amount: int) -> bool:
        """Execute transfer function"""
        sender_balance = self.storage.get(f"balance_{sender}", 0)

        if sender_balance >= amount:
            self.storage[f"balance_{sender}"] = sender_balance - amount
            recipient_balance = self.storage.get(f"balance_{recipient}", 0)
            self.storage[f"balance_{recipient}"] = recipient_balance + amount
            return True
        return False

    def _execute_get(self) -> Any:
        """Execute get function for simple storage"""
        return self.storage.get("value", 0)

    def _execute_set(self, value: Any) -> bool:
        """Execute set function for simple storage"""
        self.storage["value"] = value
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary"""
        return {
            'address': self.address,
            'bytecode_length': len(self.bytecode),
            'abi_functions': len([item for item in self.abi if item.get('type') == 'function']),
            'storage_entries': len(self.storage),
            'created_at': self.creation_timestamp.isoformat()
        }


class ContractRegistry:
    """
    Registry for managing smart contracts
    """

    def __init__(self):
        self.contracts: Dict[str, SmartContract] = {}

    def deploy_contract(self, creator: str, bytecode: bytes, abi: List[Dict] = None) -> SmartContract:
        """
        Deploy a new contract

        Args:
            creator: Creator address
            bytecode: Contract bytecode
            abi: Contract ABI

        Returns:
            SmartContract: Deployed contract
        """
        contract = SmartContract.create_contract(creator, bytecode, abi)
        self.contracts[contract.address] = contract
        return contract

    def get_contract(self, address: str) -> Optional[SmartContract]:
        """Get contract by address"""
        return self.contracts.get(address)

    def execute_contract_call(self, contract_address: str, function_name: str,
                              args: List[Any], caller: str, value: int = 0) -> Any:
        """
        Execute a contract function call

        Args:
            contract_address: Contract address
            function_name: Function to call
            args: Function arguments
            caller: Caller address
            value: Value to send

        Returns:
            Any: Function result
        """
        contract = self.get_contract(contract_address)
        if not contract:
            raise ValueError(f"Contract not found: {contract_address}")

        return contract.execute_function(function_name, args, caller, value)

    def get_contract_count(self) -> int:
        """Get total number of deployed contracts"""
        return len(self.contracts)