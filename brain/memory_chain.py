"""
⛓️ LUNA Memory Chain - Audit Trail System

Immutable audit trail using SHA-256 hash chain for LGPD compliance and dispute resolution.

Feature Flag: FEATURE_MEMORY_CHAIN

Usage:
    from brain.memory_chain import MemoryChain
    
    chain = MemoryChain()
    
    # Add interaction
    chain.add_interaction({
        "contact_id": "contact_123",
        "intent": "schedule_appointment",
        "outcome": "scheduled"
    })
    
    # Verify chain integrity
    is_valid = chain.verify_chain()
"""

import os
import json
import hashlib
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ChainEntry:
    """Single entry in the memory chain"""
    timestamp: float
    interaction_id: str
    contact_id: str
    data: Dict[str, Any]
    previous_hash: str
    current_hash: str = ""
    
    def __post_init__(self):
        """Calculate hash after initialization"""
        if not self.current_hash:
            self.current_hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of entry"""
        entry_data = {
            "timestamp": self.timestamp,
            "interaction_id": self.interaction_id,
            "contact_id": self.contact_id,
            "data": self.data,
            "previous_hash": self.previous_hash
        }
        
        entry_json = json.dumps(entry_data, sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary"""
        return {
            "timestamp": self.timestamp,
            "interaction_id": self.interaction_id,
            "contact_id": self.contact_id,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash
        }


class MemoryChain:
    """
    Immutable audit trail using SHA-256 hash chain.
    
    Features:
    - Tamper-proof audit trail
    - LGPD compliance
    - Dispute resolution
    - Training data integrity
    - Automatic chain verification
    
    Usage:
        chain = MemoryChain()
        chain.add_interaction(interaction_data)
        chain.save_to_file("memory_chain.jsonl")
        
        # Later verify integrity
        is_valid = chain.verify_chain()
    """
    
    def __init__(self, chain_file: Optional[Path] = None):
        """
        Initialize memory chain.
        
        Args:
            chain_file: Optional file to load/save chain
        """
        self.entries: List[ChainEntry] = []
        self.chain_file = chain_file
        self._genesis_hash = self._create_genesis_hash()
        
        # Load existing chain if file provided
        if chain_file and chain_file.exists():
            self.load_from_file(chain_file)
    
    def _create_genesis_hash(self) -> str:
        """Create genesis block hash"""
        genesis_data = {
            "type": "genesis",
            "timestamp": time.time(),
            "version": "1.0.0",
            "description": "LUNA Memory Chain Genesis Block"
        }
        genesis_json = json.dumps(genesis_data, sort_keys=True)
        return hashlib.sha256(genesis_json.encode()).hexdigest()
    
    def add_interaction(self, interaction: Dict[str, Any]) -> ChainEntry:
        """
        Add interaction to chain.
        
        Args:
            interaction: Interaction data with contact_id, intent, outcome, etc.
            
        Returns:
            ChainEntry created
        """
        # Get previous hash (genesis or last entry)
        previous_hash = self._genesis_hash if not self.entries else self.entries[-1].current_hash
        
        # Create entry
        entry = ChainEntry(
            timestamp=time.time(),
            interaction_id=interaction.get("id", f"int_{int(time.time() * 1000)}"),
            contact_id=interaction.get("contact_id", "unknown"),
            data=interaction,
            previous_hash=previous_hash
        )
        
        # Add to chain
        self.entries.append(entry)
        
        return entry
    
    def verify_chain(self) -> tuple[bool, Optional[int]]:
        """
        Verify chain integrity.
        
        Returns:
            Tuple of (is_valid, first_invalid_index)
        """
        if not self.entries:
            return True, None
        
        # Verify first entry
        if self.entries[0].previous_hash != self._genesis_hash:
            return False, 0
        
        # Verify each entry's hash and link
        for i in range(len(self.entries)):
            entry = self.entries[i]
            
            # Verify hash calculation
            calculated_hash = entry._calculate_hash()
            if calculated_hash != entry.current_hash:
                return False, i
            
            # Verify link to previous
            if i > 0:
                if entry.previous_hash != self.entries[i - 1].current_hash:
                    return False, i
        
        return True, None
    
    def get_entry(self, interaction_id: str) -> Optional[ChainEntry]:
        """Get entry by interaction ID"""
        for entry in self.entries:
            if entry.interaction_id == interaction_id:
                return entry
        return None
    
    def get_entries_by_contact(self, contact_id: str) -> List[ChainEntry]:
        """Get all entries for specific contact"""
        return [e for e in self.entries if e.contact_id == contact_id]
    
    def get_entries_in_range(self, start_time: float, end_time: float) -> List[ChainEntry]:
        """Get entries within time range"""
        return [
            e for e in self.entries
            if start_time <= e.timestamp <= end_time
        ]
    
    def save_to_file(self, file_path: Optional[Path] = None):
        """Save chain to JSONL file"""
        file_path = file_path or self.chain_file
        if not file_path:
            raise ValueError("No file path provided")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(json.dumps(entry.to_dict()) + '\n')
    
    def load_from_file(self, file_path: Optional[Path] = None):
        """Load chain from JSONL file"""
        file_path = file_path or self.chain_file
        if not file_path or not file_path.exists():
            return
        
        self.entries = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry_data = json.loads(line)
                    entry = ChainEntry(
                        timestamp=entry_data["timestamp"],
                        interaction_id=entry_data["interaction_id"],
                        contact_id=entry_data["contact_id"],
                        data=entry_data["data"],
                        previous_hash=entry_data["previous_hash"],
                        current_hash=entry_data["current_hash"]
                    )
                    self.entries.append(entry)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get chain statistics"""
        is_valid, invalid_idx = self.verify_chain()
        
        return {
            "total_entries": len(self.entries),
            "is_valid": is_valid,
            "first_invalid_index": invalid_idx,
            "genesis_hash": self._genesis_hash[:16] + "...",
            "last_hash": self.entries[-1].current_hash[:16] + "..." if self.entries else None,
            "file_path": str(self.chain_file) if self.chain_file else None
        }
    
    def export_for_audit(self, contact_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Export chain for audit purposes.
        
        Args:
            contact_id: Optional filter by contact
            
        Returns:
            Audit report with entries and verification
        """
        entries = (
            self.get_entries_by_contact(contact_id) if contact_id
            else self.entries
        )
        
        is_valid, _ = self.verify_chain()
        
        return {
            "export_timestamp": time.time(),
            "contact_id": contact_id,
            "total_entries": len(entries),
            "chain_valid": is_valid,
            "entries": [e.to_dict() for e in entries],
            "genesis_hash": self._genesis_hash,
            "last_hash": entries[-1].current_hash if entries else None
        }


# Global singleton
memory_chain = MemoryChain()


def get_memory_chain() -> MemoryChain:
    """Get global memory chain instance"""
    return memory_chain


# Feature flag check
def is_memory_chain_enabled() -> bool:
    """Check if memory chain feature is enabled"""
    return os.getenv("FEATURE_MEMORY_CHAIN", "false").lower() == "true"


# Convenience functions
def log_interaction(interaction: Dict[str, Any]) -> ChainEntry:
    """Log interaction to memory chain"""
    if not is_memory_chain_enabled():
        return None
    return memory_chain.add_interaction(interaction)


def verify_audit_trail() -> tuple[bool, Optional[int]]:
    """Verify audit trail integrity"""
    return memory_chain.verify_chain()
