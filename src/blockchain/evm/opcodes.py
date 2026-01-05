"""
EVM Opcodes Implementation
Based on Ethereum Yellow Paper
"""


# EVM Opcodes
class Opcodes:
    STOP = 0x00
    ADD = 0x01
    MUL = 0x02
    SUB = 0x03
    DIV = 0x04
    SDIV = 0x05
    MOD = 0x06
    SMOD = 0x07
    ADDMOD = 0x08
    MULMOD = 0x09
    EXP = 0x0A
    SIGNEXTEND = 0x0B

    LT = 0x10
    GT = 0x11
    SLT = 0x12
    SGT = 0x13
    EQ = 0x14
    ISZERO = 0x15
    AND = 0x16
    OR = 0x17
    XOR = 0x18
    NOT = 0x19
    BYTE = 0x1A

    SHA3 = 0x20

    ADDRESS = 0x30
    BALANCE = 0x31
    ORIGIN = 0x32
    CALLER = 0x33
    CALLVALUE = 0x34
    CALLDATALOAD = 0x35
    CALLDATASIZE = 0x36
    CALLDATACOPY = 0x37
    CODESIZE = 0x38
    CODECOPY = 0x39
    GASPRICE = 0x3A
    EXTCODESIZE = 0x3B
    EXTCODECOPY = 0x3C
    RETURNDATASIZE = 0x3D
    RETURNDATACOPY = 0x3E

    BLOCKHASH = 0x40
    COINBASE = 0x41
    TIMESTAMP = 0x42
    NUMBER = 0x43
    DIFFICULTY = 0x44
    GASLIMIT = 0x45

    POP = 0x50
    MLOAD = 0x51
    MSTORE = 0x52
    MSTORE8 = 0x53
    SLOAD = 0x54
    SSTORE = 0x55
    JUMP = 0x56
    JUMPI = 0x57
    PC = 0x58
    MSIZE = 0x59
    GAS = 0x5A
    JUMPDEST = 0x5B

    PUSH1 = 0x60
    PUSH32 = 0x7F
    DUP1 = 0x80
    DUP16 = 0x8F
    SWAP1 = 0x90
    SWAP16 = 0x9F

    LOG0 = 0xA0
    LOG4 = 0xA4

    CREATE = 0xF0
    CALL = 0xF1
    CALLCODE = 0xF2
    RETURN = 0xF3
    DELEGATECALL = 0xF4
    CREATE2 = 0xF5
    STATICCALL = 0xFA
    REVERT = 0xFD
    INVALID = 0xFE
    SELFDESTRUCT = 0xFF


# Gas costs for opcodes
GAS_COSTS = {
    Opcodes.STOP: 0,
    Opcodes.ADD: 3,
    Opcodes.MUL: 5,
    Opcodes.SUB: 3,
    Opcodes.DIV: 5,
    Opcodes.SDIV: 5,
    Opcodes.MOD: 5,
    Opcodes.SMOD: 5,
    Opcodes.ADDMOD: 8,
    Opcodes.MULMOD: 8,
    Opcodes.EXP: 10,
    Opcodes.SIGNEXTEND: 5,
    Opcodes.LT: 3,
    Opcodes.GT: 3,
    Opcodes.SLT: 3,
    Opcodes.SGT: 3,
    Opcodes.EQ: 3,
    Opcodes.ISZERO: 3,
    Opcodes.AND: 3,
    Opcodes.OR: 3,
    Opcodes.XOR: 3,
    Opcodes.NOT: 3,
    Opcodes.BYTE: 3,
    Opcodes.SHA3: 30,
    Opcodes.ADDRESS: 2,
    Opcodes.BALANCE: 400,
    Opcodes.ORIGIN: 2,
    Opcodes.CALLER: 2,
    Opcodes.CALLVALUE: 2,
    Opcodes.CALLDATALOAD: 3,
    Opcodes.CALLDATASIZE: 2,
    Opcodes.CALLDATACOPY: 3,
    Opcodes.CODESIZE: 2,
    Opcodes.CODECOPY: 3,
    Opcodes.GASPRICE: 2,
    Opcodes.EXTCODESIZE: 700,
    Opcodes.EXTCODECOPY: 700,
    Opcodes.RETURNDATASIZE: 2,
    Opcodes.RETURNDATACOPY: 3,
    Opcodes.BLOCKHASH: 20,
    Opcodes.COINBASE: 2,
    Opcodes.TIMESTAMP: 2,
    Opcodes.NUMBER: 2,
    Opcodes.DIFFICULTY: 2,
    Opcodes.GASLIMIT: 2,
    Opcodes.POP: 2,
    Opcodes.MLOAD: 3,
    Opcodes.MSTORE: 3,
    Opcodes.MSTORE8: 3,
    Opcodes.SLOAD: 200,
    Opcodes.SSTORE: 5000,
    Opcodes.JUMP: 8,
    Opcodes.JUMPI: 10,
    Opcodes.PC: 2,
    Opcodes.MSIZE: 2,
    Opcodes.GAS: 2,
    Opcodes.JUMPDEST: 1,
    Opcodes.PUSH1: 3,
    Opcodes.PUSH32: 3,
    Opcodes.DUP1: 3,
    Opcodes.DUP16: 3,
    Opcodes.SWAP1: 3,
    Opcodes.SWAP16: 3,
    Opcodes.LOG0: 375,
    Opcodes.LOG4: 375,
    Opcodes.CREATE: 32000,
    Opcodes.CALL: 700,
    Opcodes.CALLCODE: 700,
    Opcodes.RETURN: 0,
    Opcodes.DELEGATECALL: 700,
    Opcodes.CREATE2: 32000,
    Opcodes.STATICCALL: 700,
    Opcodes.REVERT: 0,
    Opcodes.INVALID: 0,
    Opcodes.SELFDESTRUCT: 5000,
}