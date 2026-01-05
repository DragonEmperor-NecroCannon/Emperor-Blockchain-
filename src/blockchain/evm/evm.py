"""
Ethereum Virtual Machine (EVM) Implementation for Emperor Blockchain
"""

from typing import List, Dict, Any, Optional, Tuple
from src.blockchain.evm.opcodes import Opcodes, GAS_COSTS
from src.blockchain.evm.bytecode import Bytecode, ABIEncoder, ABIDecoder


class EVM:
    """
    Simplified Ethereum Virtual Machine implementation
    """

    def __init__(self):
        self.memory = bytearray()
        self.stack = []
        self.storage: Dict[str, Any] = {}
        self.pc = 0  # Program counter
        self.gas_remaining = 0
        self.return_data = b''

    def execute(self, code: bytes, gas_limit: int = 1000000,
                call_data: bytes = b'', sender: str = "", value: int = 0) -> Tuple[bool, bytes, int]:
        """
        Execute EVM bytecode

        Args:
            code: EVM bytecode to execute
            gas_limit: Maximum gas allowed
            call_data: Call data for transaction
            sender: Sender address
            value: Value sent with call

        Returns:
            Tuple: (success, return_data, gas_used)
        """
        self.memory = bytearray()
        self.stack = []
        self.storage = {}
        self.pc = 0
        self.gas_remaining = gas_limit
        self.return_data = b''

        try:
            while self.pc < len(code) and self.gas_remaining > 0:
                opcode = code[self.pc]
                self.pc += 1

                # Execute opcode
                success = self.execute_opcode(opcode, code)
                if not success:
                    return False, b'', gas_limit - self.gas_remaining

                # Check for STOP, RETURN, or REVERT
                if opcode in [Opcodes.STOP, Opcodes.RETURN, Opcodes.REVERT]:
                    break

            return True, self.return_data, gas_limit - self.gas_remaining

        except Exception as e:
            print(f"EVM execution error: {e}")
            return False, b'', gas_limit - self.gas_remaining

    def execute_opcode(self, opcode: int, code: bytes) -> bool:
        """
        Execute a single opcode

        Args:
            opcode: Opcode to execute
            code: Full bytecode

        Returns:
            bool: True if execution should continue
        """
        # Check gas
        gas_cost = GAS_COSTS.get(opcode, 0)
        if self.gas_remaining < gas_cost:
            return False

        self.gas_remaining -= gas_cost

        # Execute based on opcode
        if opcode == Opcodes.STOP:
            return False

        elif opcode == Opcodes.ADD:
            if len(self.stack) < 2:
                return False
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((a + b) & ((1 << 256) - 1))

        elif opcode == Opcodes.MUL:
            if len(self.stack) < 2:
                return False
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((a * b) & ((1 << 256) - 1))

        elif opcode == Opcodes.SUB:
            if len(self.stack) < 2:
                return False
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((a - b) & ((1 << 256) - 1))

        elif Opcodes.PUSH1 <= opcode <= Opcodes.PUSH32:
            n = opcode - Opcodes.PUSH1 + 1
            if self.pc + n > len(code):
                return False
            value = int.from_bytes(code[self.pc:self.pc + n], 'big')
            self.stack.append(value)
            self.pc += n

        elif opcode == Opcodes.POP:
            if not self.stack:
                return False
            self.stack.pop()

        elif opcode == Opcodes.MSTORE:
            if len(self.stack) < 2:
                return False
            offset = self.stack.pop()
            value = self.stack.pop()
            # Expand memory if needed
            if offset + 32 > len(self.memory):
                self.memory.extend(b'\x00' * (offset + 32 - len(self.memory)))
            self.memory[offset:offset + 32] = value.to_bytes(32, 'big')

        elif opcode == Opcodes.MLOAD:
            if len(self.stack) < 1:
                return False
            offset = self.stack.pop()
            if offset + 32 > len(self.memory):
                # Expand memory and read zeros
                value = 0
            else:
                value = int.from_bytes(self.memory[offset:offset + 32], 'big')
            self.stack.append(value)

        elif opcode == Opcodes.SSTORE:
            if len(self.stack) < 2:
                return False
            key = hex(self.stack.pop())
            value = self.stack.pop()
            self.storage[key] = value

        elif opcode == Opcodes.SLOAD:
            if len(self.stack) < 1:
                return False
            key = hex(self.stack.pop())
            value = self.storage.get(key, 0)
            self.stack.append(value)

        elif opcode == Opcodes.JUMP:
            if len(self.stack) < 1:
                return False
            jump_dest = self.stack.pop()
            if jump_dest >= len(code) or code[jump_dest] != Opcodes.JUMPDEST:
                return False
            self.pc = jump_dest

        elif opcode == Opcodes.JUMPI:
            if len(self.stack) < 2:
                return False
            jump_dest = self.stack.pop()
            condition = self.stack.pop()
            if condition != 0:
                if jump_dest >= len(code) or code[jump_dest] != Opcodes.JUMPDEST:
                    return False
                self.pc = jump_dest

        elif opcode == Opcodes.JUMPDEST:
            pass  # No operation

        elif opcode == Opcodes.RETURN:
            if len(self.stack) < 2:
                return False
            offset = self.stack.pop()
            size = self.stack.pop()
            if offset + size > len(self.memory):
                self.return_data = b''
            else:
                self.return_data = bytes(self.memory[offset:offset + size])
            return False

        elif opcode == Opcodes.REVERT:
            if len(self.stack) < 2:
                return False
            offset = self.stack.pop()
            size = self.stack.pop()
            if offset + size > len(self.memory):
                self.return_data = b''
            else:
                self.return_data = bytes(self.memory[offset:offset + size])
            return False

        else:
            # Unimplemented opcode - treat as INVALID
            return False

        return True

    def get_memory_hex(self) -> str:
        """Get memory as hex string"""
        return self.memory.hex()

    def get_stack_hex(self) -> List[str]:
        """Get stack as hex strings"""
        return [hex(item) for item in self.stack]