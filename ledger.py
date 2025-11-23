# ledger.py
"""
SentinelSecure – Minimal In-Memory Threat Ledger

- Each security incident (intrusion + action) is turned into a log `entry` (dict)
- Each entry lives inside a "block"
- Each block is hashed with SHA-256 and linked to the previous block's hash
- This gives you an append-only, tamper-evident chain you can verify

This is purely in-memory (no real blockchain node) but perfect for a hackathon demo.
"""

import hashlib
import json
import time
from typing import Any, Dict, List

# Our in-memory chain
_chain: List[Dict[str, Any]] = []


# -------------------------------------------------------
# Internal helpers
# -------------------------------------------------------

def _hash_block_core(block_core: Dict[str, Any]) -> str:
    """
    Compute SHA-256 over the "core" fields of a block
    (everything except the final `hash` field).
    """
    encoded = json.dumps(block_core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _create_genesis_block() -> Dict[str, Any]:
    """
    First block in the chain, hard-coded "genesis" marker.
    """
    core = {
        "index": 0,
        "timestamp": time.time(),
        "event_type": "genesis",
        "data": {"info": "SentinelSecure threat ledger genesis block"},
        "prev_hash": "0",
    }
    block_hash = _hash_block_core(core)
    core["hash"] = block_hash
    return core


def _ensure_chain_initialized() -> None:
    """
    Lazily create the chain with a genesis block on first use.
    """
    global _chain
    if not _chain:
        _chain.append(_create_genesis_block())


# -------------------------------------------------------
# Public API
# -------------------------------------------------------

def add_log(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Append a new *threat log* entry as a block in the chain.

    `entry` is a dict describing the security incident, for example:
        {
          "flow_index": 42,
          "label": "Intrusion",
          "recommended_action": "BLOCK",
          "confidence": 0.97,
          "summary": "High-risk TCP SYN flood from 10.0.0.5"
        }

    Returns the full block (including index, hash, prev_hash, timestamp).
    """
    _ensure_chain_initialized()
    global _chain

    last_block = _chain[-1]

    core = {
        "index": last_block["index"] + 1,
        "timestamp": time.time(),
        "event_type": "intrusion_log",
        "data": entry,
        "prev_hash": last_block["hash"],
    }
    core["hash"] = _hash_block_core(core)

    _chain.append(core)
    return core


def verify_chain() -> bool:
    """
    Verify that:
    - each block's stored `hash` matches the recomputed hash of its core data
    - each block's `prev_hash` matches the previous block's `hash`

    Returns True if the chain is consistent; False if tampering is detected.
    """
    _ensure_chain_initialized()
    global _chain

    # Chain with only genesis is always valid
    if len(_chain) <= 1:
        return True

    for i in range(1, len(_chain)):
        current = _chain[i]
        prev = _chain[i - 1]

        # Recompute hash over core fields
        core = {
            "index": current["index"],
            "timestamp": current["timestamp"],
            "event_type": current["event_type"],
            "data": current["data"],
            "prev_hash": current["prev_hash"],
        }
        recalculated = _hash_block_core(core)

        if current["hash"] != recalculated:
            return False

        if current["prev_hash"] != prev["hash"]:
            return False

    return True


def get_chain_as_list() -> List[Dict[str, Any]]:
    """
    Return the whole chain as a list of blocks.
    Useful for displaying in Streamlit or exporting as JSON.
    """
    _ensure_chain_initialized()
    return list(_chain)  # return a shallow copy so callers don't modify in place
