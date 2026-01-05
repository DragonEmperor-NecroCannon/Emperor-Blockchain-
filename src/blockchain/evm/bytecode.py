"""
EVM Bytecode Utilities and ABI Encoding
"""

import struct
from typing import List, Any, Dict


class Bytecode:
    """EVM Bytecode manipulation utilities"""

    @staticmethod
    def encode_int(value: int, size: int = 32) -> bytes:
        """Encode integer to bytes"""
        return value.to_bytes(size, byteorder='big', signed=False)

    @staticmethod
    def decode_int(data: bytes) -> int:
        """Decode bytes to integer"""
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def encode_string(value: str) -> bytes:
        """Encode string to bytes"""
        return value.encode('utf-8')

    @staticmethod
    def decode_string(data: bytes) -> str:
        """Decode bytes to string"""
        return data.decode('utf-8').rstrip('\x00')

    @staticmethod
    def encode_address(address: str) -> bytes:
        """Encode Ethereum-style address to bytes"""
        # Remove 'EMP' prefix if present and convert to bytes
        clean_addr = address[3:] if address.startswith('EMP') else address
        return bytes.fromhex(clean_addr)

    @staticmethod
    def decode_address(data: bytes) -> str:
        """Decode bytes to Emperor address format"""
        hex_addr = data.hex()
        return f"EMP{hex_addr}"


class ABIEncoder:
    """ABI Encoding for smart contract calls"""

    @staticmethod
    def encode_function_signature(signature: str) -> bytes:
        """Encode function signature (first 4 bytes of keccak hash)"""
        from src.utils.crypto import CryptoUtils
        hash_hex = CryptoUtils.hash_data(signature)
        return bytes.fromhex(hash_hex[:8])

    @staticmethod
    def encode_parameters(types: List[str], values: List[Any]) -> bytes:
        """Encode parameters according to ABI specification"""
        result = b''

        for t, v in zip(types, values):
            if t == 'uint256':
                result += ABIEncoder.encode_uint256(v)
            elif t == 'address':
                result += ABIEncoder.encode_address(v)
            elif t == 'string':
                result += ABIEncoder.encode_string(v)
            elif t == 'bool':
                result += ABIEncoder.encode_bool(v)
            else:
                raise ValueError(f"Unsupported type: {t}")

        return result

    @staticmethod
    def encode_uint256(value: int) -> bytes:
        """Encode uint256"""
        return value.to_bytes(32, byteorder='big')

    @staticmethod
    def encode_address(address: str) -> bytes:
        """Encode address (20 bytes)"""
        clean_addr = address[3:] if address.startswith('EMP') else address
        addr_bytes = bytes.fromhex(clean_addr.zfill(40))
        return addr_bytes.rjust(32, b'\x00')

    @staticmethod
    def encode_string(value: str) -> bytes:
        """Encode string with length prefix"""
        encoded = value.encode('utf-8')
        length = len(encoded)
        # Encode offset to string data
        offset = 32  # After the first 32 bytes for offset
        result = offset.to_bytes(32, byteorder='big')
        # Enstring length
        result += length.to_bytes(32, byteorder='big')
        # Encode string data (padded to 32 bytes)
        result += encoded.ljust((length + 31) // 32 * 32, b'\x00')
        return result

    @staticmethod
    def encode_bool(value: bool) -> bytes:
        """Encode boolean"""
        return b'\x01' if value else b'\x00'


class ABIDecoder:
    """ABI Decoding for smart contract responses"""

    @staticmethod
    def decode_parameters(types: List[str], data: bytes) -> List[Any]:
        """Decode parameters from ABI-encoded data"""
        results = []
        offset = 0

        for t in types:
            if t == 'uint256':
                value = ABIDecoder.decode_uint256(data[offset:offset + 32])
                offset += 32
            elif t == 'address':
                value = ABIDecoder.decode_address(data[offset:offset + 32])
                offset += 32
            elif t == 'string':
                # For dynamic types, we need to handle offsets
                value, new_offset = ABIDecoder.decode_string(data, offset)
                offset = new_offset
            elif t == 'bool':
                value = ABIDecoder.decode_bool(data[offset:offset + 32])
                offset += 32
            else:
                raise ValueError(f"Unsupported type: {t}")

            results.append(value)

        return results

    @staticmethod
    def decode_uint256(data: bytes) -> int:
        """Decode uint256 from bytes"""
        return int.from_bytes(data[:32], byteorder='big')

    @staticmethod
    def decode_address(data: bytes) -> str:
        """Decode address from bytes"""
        # Address is in last 20 bytes of 32-byte slot
        addr_bytes = data[12:32] if len(data) >= 32 else data
        hex_addr = addr_bytes.hex()
        return f"EMP{hex_addr}"

    @staticmethod
    def decode_string(data: bytes, offset: int) -> tuple:
        """Decode string from ABI-encoded data"""
        # Read offset to string data
        data_offset = ABIDecoder.decode_uint256(data[offset:offset + 32])
        # Read string length
        length = ABIDecoder.decode_uint256(data[data_offset:data_offset + 32])
        # Read string data
        string_data = data[data_offset + 32:data_offset + 32 + length]
        string_value = string_data.decode('utf-8').rstrip('\x00')
        return string_value, offset + 32

    @staticmethod
    def decode_bool(data: bytes) -> bool:
        """Decode boolean from bytes"""
        return bool(int.from_bytes(data[:32], byteorder='big'))