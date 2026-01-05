#!/usr/bin/env python3
"""
Emperor Blockchain - Main Application
A complete blockchain implementation with 1 billion EMPEROR tokens
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from blockchain.blockchain import EmperorBlockchain
    from blockchain.wallet import Wallet
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all files are in the correct location.")
    sys.exit(1)


def main():
    """
    Main function to demonstrate Emperor Blockchain functionality
    """
    print("=" * 70)
    print("🏛️  EMPEROR BLOCKCHAIN - 1 BILLION TOKEN ECOSYSTEM")
    print("=" * 70)

    try:
        # Initialize blockchain
        print("\n🚀 Initializing Emperor Blockchain...")
        blockchain = EmperorBlockchain(difficulty=3)  # Lower difficulty for faster testing
        print("✓ Blockchain initialized successfully")

        # Create wallets
        print("\n👛 Creating wallets...")
        wallet_miner = Wallet()
        wallet_foundation = Wallet()
        wallet_user1 = Wallet()
        wallet_user2 = Wallet()

        wallets = {
            "Miner": wallet_miner,
            "Foundation": wallet_foundation,
            "User 1": wallet_user1,
            "User 2": wallet_user2
        }

        for name, wallet in wallets.items():
            print(f"  {name}: {wallet.address}")

        # Display initial state
        print("\n📊 Initial Blockchain State:")
        info = blockchain.get_blockchain_info()
        for key, value in info.items():
            if key == 'is_valid':
                status = "✅ VALID" if value else "❌ INVALID"
                print(f"  {key.replace('_', ' ').title()}: {status}")
            elif isinstance(value, (int, float)) and value > 1000:
                print(f"  {key.replace('_', ' ').title()}: {value:,}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")

        # Phase 1: Initial Token Distribution
        print(f"\n{'=' * 50}")
        print("💰 PHASE 1: TOKEN DISTRIBUTION")
        print(f"{'=' * 50}")

        # Distribute tokens from genesis
        distribution_plan = [
            {"from": "genesis", "to": wallet_foundation.address, "amount": 200000000, "type": "FOUNDATION"},
            {"from": "genesis", "to": wallet_user1.address, "amount": 50000000, "type": "AIRDROP"},
            {"from": "genesis", "to": wallet_user2.address, "amount": 50000000, "type": "AIRDROP"},
        ]

        for dist in distribution_plan:
            tx = blockchain.create_transaction(
                sender=dist["from"],
                recipient=dist["to"],
                amount=dist["amount"],
                transaction_type=dist["type"]
            )
            if blockchain.add_transaction(tx):
                print(f"✓ Distributed {dist['amount']:,} EMPEROR to {dist['to'][:12]}... ({dist['type']})")

        # Mine the distribution block
        print(f"\n⛏️  Mining distribution transactions...")
        mined_block = blockchain.mine_pending_transactions(wallet_miner.address)
        print(f"✓ Block #{mined_block.index} mined with {len(mined_block.transactions)} transactions")
        print(f"✓ Miner received {blockchain.mining_reward} EMPEROR mining reward")

        # Phase 2: Peer-to-Peer Transactions
        print(f"\n{'=' * 50}")
        print("🔄 PHASE 2: PEER-TO-PEER TRANSACTIONS")
        print(f"{'=' * 50}")

        # Foundation sends tokens to users
        foundation_transfers = [
            {"to": wallet_user1.address, "amount": 1000000, "description": "Grant"},
            {"to": wallet_user2.address, "amount": 1000000, "description": "Grant"},
        ]

        for transfer in foundation_transfers:
            tx = blockchain.create_transaction(
                sender=wallet_foundation.address,
                recipient=transfer["to"],
                amount=transfer["amount"],
                transaction_type="TRANSFER"
            )
            if blockchain.add_transaction(tx):
                print(
                    f"✓ Foundation sent {transfer['amount']:,} EMPEROR to {transfer['to'][:12]}... ({transfer['description']})")

        # User1 sends tokens to User2
        user_tx = blockchain.create_transaction(
            sender=wallet_user1.address,
            recipient=wallet_user2.address,
            amount=500000,
            transaction_type="TRANSFER"
        )
        if blockchain.add_transaction(user_tx):
            print(f"✓ User 1 sent 500,000 EMPEROR to User 2")

        # Mine peer-to-peer transactions
        print(f"\n⛏️  Mining peer-to-peer transactions...")
        mined_block = blockchain.mine_pending_transactions(wallet_miner.address)
        print(f"✓ Block #{mined_block.index} mined with {len(mined_block.transactions)} transactions")

        # Final State and Validation
        print(f"\n{'=' * 50}")
        print("📈 FINAL BLOCKCHAIN STATE")
        print(f"{'=' * 50}")

        final_info = blockchain.get_blockchain_info()
        print("\n📊 Blockchain Statistics:")
        stats = [
            ("Total Blocks", f"{final_info['chain_length']}"),
            ("Total Transactions", f"{final_info['total_transactions']}"),
            ("Total Supply", f"{final_info['total_supply']:,} {final_info['token_symbol']}"),
            ("Circulating Supply", f"{final_info['circulating_supply']:,.0f} {final_info['token_symbol']}"),
            ("Mining Difficulty", f"{final_info['difficulty']}"),
            ("Mining Reward", f"{final_info['mining_reward']} {final_info['token_symbol']}"),
            ("Mining Rewards Distributed", f"{final_info['mining_rewards_distributed']} {final_info['token_symbol']}"),
            ("Pending Transactions", f"{final_info['pending_transactions']}"),
        ]

        for stat, value in stats:
            print(f"  {stat}: {value}")

        # Wallet Balances
        print(f"\n💰 Wallet Balances:")
        for name, wallet in wallets.items():
            balance = blockchain.get_balance(wallet.address)
            print(f"  {name:<12}: {balance:>15,.2f} {blockchain.token_symbol}")

        # Chain Validation
        print(f"\n{'=' * 50}")
        print("✅ VALIDATION SUMMARY")
        print(f"{'=' * 50}")

        validation_checks = [
            ("Blockchain Integrity", blockchain.is_chain_valid()),
            ("Genesis Block", len(blockchain.chain) > 0),
            ("Token Supply Conservation", final_info['circulating_supply'] <= final_info['total_supply']),
            ("Mining Rewards", final_info['mining_rewards_distributed'] > 0),
        ]

        all_valid = True
        for check, result in validation_checks:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {check}: {status}")
            if not result:
                all_valid = False

        # Final Success Message
        print(f"\n{'🎉' * 20}")
        if all_valid:
            print("EMPEROR BLOCKCHAIN DEPLOYED SUCCESSFULLY!")
            print(f"• 1,000,000,000 EMPEROR tokens initialized")
            print(f"• {final_info['chain_length']} blocks created")
            print(f"• {final_info['total_transactions']} transactions processed")
            print(f"• Proof-of-Work consensus active")
            print(f"• Ready for FinTech applications")
        else:
            print("DEPLOYMENT COMPLETED WITH WARNINGS")
        print(f"{'🎉' * 20}")

        # Optional: Print full chain
        show_chain = input("\nShow full blockchain? (y/n): ").lower()
        if show_chain == 'y':
            blockchain.print_chain()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("Please check your installation and try again.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())