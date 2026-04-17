import asyncio
import json
import time
from pathlib import Path
from web3 import Web3

# Path to your compiled contract metadata
ROOT = Path(__file__).resolve().parent.parent
BUILD_PATH = ROOT / 'build' / 'WorldTribe_compiled.json'

def handle_crisis(event):
    """Trigger hardware response for CrisisSignaled event."""
    member = event['args']['member']
    print(f"🚨 [HARDWARE ALERT] Crisis detected for member: {member}")
    print(">>> Activating emergency mentorship protocols and hardware indicators...")
    # Example: GPIO.output(RED_LED_PIN, GPIO.HIGH)

def handle_new_member(event):
    """Trigger hardware response for MemberJoined event."""
    member = event['args']['member']
    balance = event['args']['initialBalance']
    print(f"🌍 [COMMUNITY] New member joined: {member} with {balance} credits.")
    # Example: play_welcome_sound()

async def log_loop(event_filter, poll_interval, callback):
    """Asynchronous loop to check for new entries in the event filter."""
    while True:
        for event in event_filter.get_new_entries():
            callback(event)
        await asyncio.sleep(poll_interval)

def main():
    # 1. Initialization
    if not BUILD_PATH.exists():
        print("Error: Contract metadata not found. Run compile_worldtribe.py first.")
        return

    with open(BUILD_PATH) as f:
        compiled = json.load(f)

    # In production, use your node provider URL (Infura, Alchemy, or Local Node)
    # w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    # For this example, we assume you are running against a local dev environment
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

    if not w3.is_connected():
        print("Failed to connect to Ethereum node.")
        return

    # 2. Setup Contract (Replace with your deployed address)
    # Note: In a real side-car, the address would be loaded from an environment variable
    contract_address = "0x..." 
    contract_meta = compiled['contracts']['WorldTribe.sol']['WorldTribe']
    contract = w3.eth.contract(address=contract_address, abi=contract_meta['abi'])

    print(f"Listening for Tribe events on {contract_address}...")

    # 3. Create Event Filters
    # Using 'latest' ensures we only catch new events from this point forward
    crisis_filter = contract.events.CrisisSignaled.create_filter(fromBlock='latest')
    join_filter = contract.events.MemberJoined.create_filter(fromBlock='latest')

    try:
        print("System active. Press Ctrl+C to exit.")
        asyncio.run(asyncio.gather(
            log_loop(crisis_filter, 2, handle_crisis),
            log_loop(join_filter, 2, handle_new_member)
        ))
    except KeyboardInterrupt:
        print("Hardware side-car shutting down.")

if __name__ == "__main__":
    main()
