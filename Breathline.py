"""
breath_line_model.py
====================

This module implements a simple "breath line" loop inspired by the
Persistent Memory Logic Loop (PMLL) concept.  The model repeatedly
senses its environment, thinks about the observations, acts upon
the results, and finally emits a heartbeat (the breath).  To
illustrate how cross‑checking Non‑Fungible Tokens (NFTs) can be
incorporated into such a loop, a verification step is included
before each cycle.  Verifying NFT metadata ensures that token
ownership records remain authentic and tamper‑proof, leveraging
blockchain properties for added security【481861696090440†L40-L46】【481861696090440†L79-L83】.

The example below is deliberately simple: it defines stubbed
functions for each stage of the loop and a rudimentary NFT
verification routine.  In a real system you would replace these
stubs with actual sensor reads, reasoning logic, robotic actions
and calls to a blockchain API.  This scaffold demonstrates how
the different concerns can be composed together in a cohesive
control flow.

Usage:

    python breath_line_model.py

The script will run a finite number of iterations for demonstration
purposes; adjust MAX_CYCLES in `main()` to control how long it runs.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class NFT:
    """Simple representation of a Non‑Fungible Token for verification.

    Attributes:
        token_id: A unique identifier for the NFT.
        metadata: Arbitrary metadata associated with the NFT.  In a real
            application this might include serial numbers, QR codes,
            descriptions or links to physical assets【481861696090440†L118-L125】.
        signature: A simulated cryptographic digest of the metadata.
    """

    token_id: str
    metadata: Dict[str, str]
    signature: str = field(init=False)

    def __post_init__(self) -> None:
        # Generate a simple SHA‑256 signature over the JSON serialised metadata.
        # This emulates how an NFT might embed a tamper‑proof hash of its
        # associated data on a blockchain【481861696090440†L79-L83】.
        self.signature = hashlib.sha256(json.dumps(self.metadata, sort_keys=True).encode()).hexdigest()


def cross_verify_nfts(nfts: List[NFT]) -> bool:
    """Cross‑verify a collection of NFTs.

    The function checks that every NFT in the list has a unique
    signature and that the signature matches the hash of its
    metadata.  If any duplicate signatures or mismatches are found
    the function returns False to signal an integrity failure.

    Args:
        nfts: A list of NFTs to verify.

    Returns:
        True if all NFTs pass verification, otherwise False.
    """
    seen_signatures: set[str] = set()
    for nft in nfts:
        # recompute the signature from the metadata
        expected_sig = hashlib.sha256(json.dumps(nft.metadata, sort_keys=True).encode()).hexdigest()
        if expected_sig != nft.signature:
            print(f"[ERROR] NFT {nft.token_id} has mismatched signature.")
            return False
        if expected_sig in seen_signatures:
            print(f"[ERROR] Duplicate signature detected for NFT {nft.token_id}.")
            return False
        seen_signatures.add(expected_sig)
    return True


def update() -> Dict[str, float]:
    """Stub for the sense/update phase.

    Simulates reading from a set of sensors by returning random
    floating‑point values.  In a real system this might read from
    hardware sensors or external APIs.

    Returns:
        A dictionary of sensor readings.
    """
    readings = {
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "pressure": round(random.uniform(990.0, 1020.0), 2),
    }
    print(f"[update] Sensor readings: {readings}")
    return readings


def think(readings: Dict[str, float]) -> Tuple[str, float]:
    """Stub for the logic/thinking phase.

    Performs a simple evaluation on the sensor data and returns a
    descriptive state plus a numeric score.  Replace this with your
    own inference or control logic.

    Args:
        readings: A dictionary of sensor readings from `update()`.

    Returns:
        A tuple of a status label and a computed value.
    """
    # For demonstration, compute an average and categorise
    avg = sum(readings.values()) / len(readings)
    status = "normal" if 24.0 <= avg <= 26.0 else "anomaly"
    print(f"[think] Average reading: {avg:.2f}, status: {status}")
    return status, avg


def act(status: str, value: float) -> None:
    """Stub for the action phase.

    Takes a decision based on the status and value computed in
    `think()`.  In this example it simply prints messages; in a real
    system this might actuate hardware, send alerts, or store data.

    Args:
        status: The status label from the logic phase.
        value: The numeric value computed from sensor data.
    """
    if status == "normal":
        print(f"[act] All systems nominal. Avg value {value:.2f} within expected range.")
    else:
        print(f"[act] Warning! Sensor average {value:.2f} is outside the normal range.")


def breath(cycle: int) -> None:
    """Stub for the breath/heartbeat/logging phase.

    Emits a heartbeat message to indicate the system is alive and
    reports the current cycle number.  In practice this might log
    to a file, send telemetry, or synchronise with a distributed
    ledger【481861696090440†L79-L83】.

    Args:
        cycle: The current iteration count.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[breath] Heartbeat at {timestamp}, cycle {cycle}")


def main() -> None:
    """Entry point for the breath line model demo.

    The function creates a small set of simulated NFTs, verifies them
    before each cycle, and then executes the update → think → act →
    breath loop.  If NFT verification fails the loop exits early,
    signalling a security breach.
    """
    # Prepare a list of mock NFTs
    nfts = [
        NFT(token_id="nft1", metadata={"owner": "alice", "asset": "artwork", "serial": "A123"}),
        NFT(token_id="nft2", metadata={"owner": "bob",   "asset": "watch",   "serial": "W456"}),
        NFT(token_id="nft3", metadata={"owner": "carol", "asset": "car",     "serial": "C789"}),
    ]

    MAX_CYCLES = 5  # Run a finite number of cycles for demonstration
    for cycle in range(1, MAX_CYCLES + 1):
        print(f"\n=== Cycle {cycle} ===")
        # Cross‑verify NFTs before proceeding
        if not cross_verify_nfts(nfts):
            print("[fatal] NFT verification failed. Aborting loop to maintain integrity.")
            break
        # Sense
        readings = update()
        # Think
        status, value = think(readings)
        # Act
        act(status, value)
        # Breath / heartbeat
        breath(cycle)
        # Sleep briefly to simulate real time passing
        time.sleep(0.5)


if __name__ == "__main__":
    main()
