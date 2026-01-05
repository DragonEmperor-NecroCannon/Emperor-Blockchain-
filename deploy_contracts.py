#!/usr/bin/env python3
"""
Smart Contract Deployment Script for Emperor Blockchain
"""

import json
from src.blockchain.blockchain import EmperorBlockchain
from src.blockchain.wallet import Wallet
from src.blockchain.evm.solidity_compiler import ContractTemplate


def deploy_emperor_ecosystem():
    """Deploy the complete Emperor ecosystem with smart contracts"""

    print("🚀 Deploying Emperor Blockchain Ecosystem...\n")

    # Initialize blockchain
    blockchain = EmperorBlockchain(difficulty=3)

    # Create deployment wallet
    deployer = Wallet()
    print(f"📦 Deployment Wallet: {deployer.address}")

    # Fund deployer
    fund_tx = blockchain.create_transaction(
        sender="0",
        recipient=deployer.address,
        amount=10000.0,
        transaction_type="SYSTEM_ISSUANCE"
    )
    blockchain.add_transaction(fund_tx)
    blockchain.mine_pending_transactions(deployer.address)

    print("✓ Deployment wallet funded")

    # Deploy Emperor Token
    print("\n📄 Deploying Emperor Token Contract...")
    token_source = ContractTemplate.get_emperor_token_template()
    token_contract = blockchain.deploy_contract(
        creator=deployer.address,
        contract_source=token_source,
        contract_name="EmperorToken",
        initial_supply=1000000
    )

    if token_contract:
        blockchain.mine_pending_transactions(deployer.address)
        print(f"✅ Emperor Token deployed at: {token_contract.address}")

        # Verify deployment
        supply = blockchain.execute_contract_call(
            token_contract.address, "totalSupply", [], deployer.address
        )
        print(f"✓ Total Supply: {supply} EMPEROR tokens")

    # Deploy SimpleStorage
    print("\n📄 Deploying SimpleStorage Contract...")
    storage_source = ContractTemplate.get_simple_storage_template()
    storage_contract = blockchain.deploy_contract(
        creator=deployer.address,
        contract_source=storage_source,
        contract_name="SimpleStorage"
    )

    if storage_contract:
        blockchain.mine_pending_transactions(deployer.address)
        print(f"✅ SimpleStorage deployed at: {storage_contract.address}")

    # Display final state
    print(f"\n📊 Deployment Complete!")
    info = blockchain.get_blockchain_info()
    print(f"• Blocks: {info['length']}")
    print(f"• Transactions: {info['total_transactions']}")
    print(f"• Contracts: {info['contracts_deployed']}")
    print(f"• Chain Valid: {info['is_valid']}")

    return blockchain


if __name__ == "__main__":
    deploy_emperor_ecosystem()