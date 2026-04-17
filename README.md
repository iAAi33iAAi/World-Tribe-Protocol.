# World Tribe Protocol

World Tribe Protocol is an early-stage on-chain prototype for a social provisioning system. The current repository focuses on one concrete slice of that idea: a Solidity contract that tracks membership, baseline credits, crisis signaling, and administrative updates, plus Python tooling to compile, test, and observe contract events.

This repo is not a full "civilization OS" yet. It is a working prototype of the contract layer and the developer workflow around it.

## What Exists Today

- A Solidity contract in `WorldTribe.sol`
- A compiler script in `scripts/compile_worldtribe.py`
- A test suite in `scripts/test_worldtribe.py`
- A sidecar listener prototype in `scripts/hardware_sidecar.py`
- A compiled artifact in `build/WorldTribe_compiled.json`

## Contract Scope

The current contract implements a small equilibrium model:

- `joinTribe()`: enroll a member and assign a starting balance
- `spendCredits(uint256)`: reduce a member's balance
- `maintainEquilibrium(address)`: restore a member to the baseline balance
- `triggerRedAlert()`: mark the caller as in crisis and emit an alert event
- `setBaseline(uint256)`: let the owner update the shared baseline
- `transferOwnership(address)`: transfer administrative control

Emitted events:

- `MemberJoined`
- `BaselineUpdated`
- `CrisisSignaled`
- `OwnershipTransferred`

## Why This Repo Matters

Most social or aid-oriented systems are implemented off-chain and managed by institutions. This project explores a different framing: can a small, inspectable contract express basic guarantees around membership, replenishment, and crisis signaling in a way that is transparent, testable, and easy to integrate with external systems?

That is the useful claim of this repository today. It is a prototype for programmable provision, not a finished governance platform.

## Current Status

Implemented now:

- Membership registration
- Credit accounting
- Baseline restoration logic
- Crisis event emission
- Owner-only baseline updates
- Local compilation and Python-based testing

Still conceptual or incomplete:

- Hardware integration
- Access control beyond owner/member checks
- Economic design and anti-abuse protections
- Production event processing and persistence

## Quick Start

Create a virtual environment and install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Compile the contract:

```bash
python scripts/compile_worldtribe.py
```

You can also compile a different source, output path, or Solidity version:

```bash
python scripts/compile_worldtribe.py --source WorldTribe.sol --output build/WorldTribe_compiled.json --solc-version 0.8.0
```

Run the tests:

```bash
pytest scripts/test_worldtribe.py
```

Create a deployment config:

```bash
python scripts/deploy_worldtribe.py
```

For a reusable local node, point the deploy script at JSON-RPC:

```bash
python scripts/deploy_worldtribe.py --provider-url http://localhost:8545
```

Serve the dashboard with live contract state:

```bash
python scripts/dashboard_server.py
```

The sidecar listener is a prototype for reacting to emitted contract events:

```bash
python scripts/hardware_sidecar.py
```

Note: `hardware_sidecar.py` and `dashboard_server.py` both read `config/deployment.json`. An ephemeral deploy created without `--provider-url` is useful for smoke testing the deploy step, but not for cross-process event listening or dashboard reads.

## Repository Structure

- `WorldTribe.sol`: contract source
- `requirements.txt`: Python dependencies for compile/test tooling
- `scripts/compile_worldtribe.py`: compiles the contract with `solcx` and supports CLI options
- `scripts/deploy_worldtribe.py`: deploys the contract and writes shared deployment metadata
- `scripts/dashboard_server.py`: serves the dashboard and exposes `/api/status` with live contract state
- `scripts/test_worldtribe.py`: deploys the contract in an in-memory test chain and verifies core behavior
- `scripts/hardware_sidecar.py`: listens for contract events using shared deployment config
- `config/deployment.example.json`: example shape for deployment metadata consumed by the dashboard and sidecar
- `build/WorldTribe_compiled.json`: generated ABI and bytecode output

## Design Notes

The contract intentionally stays small. That keeps the current prototype legible and makes it easier to inspect the rules being tested:

- a member can join once
- credits can be spent but not below zero
- any caller can restore a member to the baseline
- a member can signal crisis for off-chain responders
- only the owner can change the baseline

This simplicity is a strength for a prototype, but it also defines the next engineering challenge: turning a symbolic model into a system with tighter permissions, clearer incentives, and safer operational boundaries.

## Next Steps

- Expand tests for edge cases and failure modes
- Add write actions so admins and members can interact with the contract from the local app flow
- Add documentation for deployment, local development, and event consumption
- Specify the trust model and security assumptions

## License

Apache-2.0
