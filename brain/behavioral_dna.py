"""
🧬 LUNA Behavioral DNA - Customer Personalization

Unique behavioral fingerprint for each customer. Adapts tone, vocabulary, and response style.

Feature Flag: FEATURE_BEHAVIORAL_DNA

Usage:
    from brain.behavioral_dna import BehavioralDNA
    
    dna = BehavioralDNA()
    
    # Get or create DNA for customer
    customer_dna = dna.get_dna("contact_123")
    
    # Adapt response using DNA
    response = dna.adapt_response(
        base_response="Obrigado pelo contato",
        dna=customer_dna
    )
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ToneType(Enum):
    """Communication tone types"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    EMPATHETIC = "empathetic"
    DIRECT = "direct"
    ENTHUSIASTIC = "enthusiastic"
    FORMAL = "formal"
    WARM = "warm"


class VocabularyType(Enum):
    """Vocabulary complexity types"""
    SIMPLE = "simple"           # Basic words, short sentences
    STANDARD = "standard"       # Normal business language
    TECHNICAL = "technical"     # Industry terminology
    EXECUTIVE = "executive"     # High-level, concise


@dataclass
class BehavioralDNA:
    """
    Behavioral DNA profile for a customer.
    
    Attributes:
        contact_id: Customer identifier
        tone: Preferred communication tone
        vocabulary: Vocabulary complexity level
        emoji_usage: Emoji usage policy
        response_length: Preferred response length
        formality_level: Formality level (1-10)
        common_phrases: Frequently used phrases
        topics_of_interest: Topics customer engages with
        communication_style: Direct vs indirect
        decision_speed: Fast vs slow decision maker
    """
    contact_id: str
    tone: ToneType = ToneType.PROFESSIONAL
    vocabulary: VocabularyType = VocabularyType.STANDARD
    emoji_usage: str = "moderate"  # none, minimal, moderate, liberal
    response_length: str = "medium"  # short, medium, long
    formality_level: int = 6  # 1-10
    common_phrases: List[str] = field(default_factory=list)
    topics_of_interest: List[str] = field(default_factory=list)
    communication_style: str = "balanced"  # direct, indirect, balanced
    decision_speed: str = "medium"  # fast, medium, slow
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    interaction_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DNA to dictionary"""
        return {
            "contact_id": self.contact_id,
            "tone": self.tone.value,
            "vocabulary": self.vocabulary.value,
            "emoji_usage": self.emoji_usage,
            "response_length": self.response_length,
            "formality_level": self.formality_level,
            "common_phrases": self.common_phrases,
            "topics_of_interest": self.topics_of_interest,
            "communication_style": self.communication_style,
            "decision_speed": self.decision_speed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "interaction_count": self.interaction_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BehavioralDNA":
        """Create DNA from dictionary"""
        return cls(
            contact_id=data["contact_id"],
            tone=ToneType(data.get("tone", "professional")),
            vocabulary=VocabularyType(data.get("vocabulary", "standard")),
            emoji_usage=data.get("emoji_usage", "moderate"),
            response_length=data.get("response_length", "medium"),
            formality_level=data.get("formality_level", 6),
            common_phrases=data.get("common_phrases", []),
            topics_of_interest=data.get("topics_of_interest", []),
            communication_style=data.get("communication_style", "balanced"),
            decision_speed=data.get("decision_speed", "medium"),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            interaction_count=data.get("interaction_count", 0)
        )


class DNAManager:
    """
    Manager for Behavioral DNA profiles.
    
    Features:
    - Create and store DNA profiles
    - Analyze interactions to infer DNA
    - Adapt responses using DNA
    - Evolve DNA over time
    
    Usage:
        manager = DNAManager()
        dna = manager.get_or_create_dna("contact_123")
        adapted = manager.adapt_response("Hello!", dna)
    """
    
    def __init__(self, storage_file: Optional[Path] = None):
        """
        Initialize DNA Manager.
        
        Args:
            storage_file: Optional file to store DNA profiles
        """
        self.storage_file = storage_file
        self._profiles: Dict[str, BehavioralDNA] = {}
        
        # Load existing profiles
        if storage_file and storage_file.exists():
            self._load_profiles(storage_file)
        
        # Default DNA templates by industry
        self._default_templates = {
            "healthcare": {
                "tone": ToneType.EMPATHETIC,
                "vocabulary": VocabularyType.STANDARD,
                "formality_level": 7,
                "emoji_usage": "minimal"
            },
            "retail": {
                "tone": ToneType.FRIENDLY,
                "vocabulary": VocabularyType.SIMPLE,
                "formality_level": 4,
                "emoji_usage": "moderate"
            },
            "finance": {
                "tone": ToneType.PROFESSIONAL,
                "vocabulary": VocabularyType.TECHNICAL,
                "formality_level": 8,
                "emoji_usage": "none"
            },
            "tech": {
                "tone": ToneType.CASUAL,
                "vocabulary": VocabularyType.TECHNICAL,
                "formality_level": 3,
                "emoji_usage": "liberal"
            }
        }
    
    def get_dna(self, contact_id: str) -> Optional[BehavioralDNA]:
        """Get DNA profile for contact"""
        return self._profiles.get(contact_id)
    
    def create_dna(
        self,
        contact_id: str,
        industry: Optional[str] = None,
        **kwargs
    ) -> BehavioralDNA:
        """
        Create new DNA profile.
        
        Args:
            contact_id: Customer identifier
            industry: Industry template to use
            **kwargs: Override default values
            
        Returns:
            Created BehavioralDNA profile
        """
        # Start with defaults
        dna_kwargs = {"contact_id": contact_id}
        
        # Apply industry template if provided
        if industry and industry in self._default_templates:
            dna_kwargs.update(self._default_templates[industry])
        
        # Apply custom overrides
        dna_kwargs.update(kwargs)
        
        # Create profile
        dna = BehavioralDNA(**dna_kwargs)
        
        # Store
        self._profiles[contact_id] = dna
        
        return dna
    
    def get_or_create_dna(
        self,
        contact_id: str,
        industry: Optional[str] = None,
        **kwargs
    ) -> BehavioralDNA:
        """Get existing DNA or create new one"""
        dna = self.get_dna(contact_id)
        if dna:
            return dna
        return self.create_dna(contact_id, industry, **kwargs)
    
    def update_dna(self, contact_id: str, **updates) -> bool:
        """
        Update DNA profile.
        
        Args:
            contact_id: Customer identifier
            **updates: Fields to update
            
        Returns:
            True if updated successfully
        """
        dna = self.get_dna(contact_id)
        if not dna:
            return False
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(dna, key):
                setattr(dna, key, value)
        
        dna.updated_at = time.time()
        dna.interaction_count += 1
        
        return True
    
    def analyze_interaction(
        self,
        contact_id: str,
        customer_message: str,
        infer_dna: bool = True
    ) -> Optional[BehavioralDNA]:
        """
        Analyze customer interaction to infer DNA.
        
        Args:
            contact_id: Customer identifier
            customer_message: Customer's message
            infer_dna: Whether to update DNA based on analysis
            
        Returns:
            Updated DNA profile
        """
        dna = self.get_or_create_dna(contact_id)
        
        if not infer_dna:
            return dna
        
        # Analyze message for tone indicators
        updates = {}
        
        # Detect formality from word choice
        formal_words = ["gostaria", "por favor", "agradeço", "senhor", "senhora"]
        informal_words = ["oi", "tudo bem", "valeu", "obrigado", "blz"]
        
        message_lower = customer_message.lower()
        formal_count = sum(1 for word in formal_words if word in message_lower)
        informal_count = sum(1 for word in informal_words if word in message_lower)
        
        # Adjust formality level
        if formal_count > informal_count:
            updates["formality_level"] = min(10, dna.formality_level + 1)
        elif informal_count > formal_count:
            updates["formality_level"] = max(1, dna.formality_level - 1)
        
        # Detect emoji usage preference
        emoji_count = sum(1 for char in customer_message if char in '😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖')
        if emoji_count > 2:
            updates["emoji_usage"] = "liberal"
        elif emoji_count > 0:
            updates["emoji_usage"] = "moderate"
        else:
            updates["emoji_usage"] = "minimal"
        
        # Detect response length preference
        word_count = len(customer_message.split())
        if word_count > 50:
            updates["response_length"] = "long"
        elif word_count < 10:
            updates["response_length"] = "short"
        
        # Apply updates
        if updates:
            self.update_dna(contact_id, **updates)
        
        return self.get_dna(contact_id)
    
    def adapt_response(
        self,
        base_response: str,
        dna: BehavioralDNA,
        context: Optional[Dict] = None
    ) -> str:
        """
        Adapt response using customer's DNA.
        
        Args:
            base_response: Standard AI response
            dna: Customer's behavioral DNA
            context: Additional context
            
        Returns:
            Adapted response
        """
        adapted = base_response
        
        # Adjust emoji based on DNA
        if dna.emoji_usage == "none":
            # Remove all emoji
            adapted = self._remove_emoji(adapted)
        elif dna.emoji_usage == "minimal":
            # Keep only 1 emoji max
            adapted = self._limit_emoji(adapted, 1)
        elif dna.emoji_usage == "liberal":
            # Add friendly emoji
            if "Obrigado" in adapted:
                adapted = adapted.replace("Obrigado", "Obrigado 😊")
            elif "Olá" in adapted:
                adapted = adapted.replace("Olá", "Olá 👋")
        
        # Adjust formality
        if dna.formality_level >= 8:
            # More formal
            adapted = adapted.replace("Oi", "Olá")
            adapted = adapted.replace("tudo bem?", "como está?")
            adapted = adapted.replace("valeu", "agradeço")
        elif dna.formality_level <= 3:
            # More casual
            adapted = adapted.replace("Olá", "Oi")
            adapted = adapted.replace("como está?", "tudo bem?")
        
        # Adjust length
        if dna.response_length == "short":
            # Truncate to essential
            adapted = adapted.split(".")[0]
            if len(adapted) > 100:
                adapted = adapted[:100] + "..."
        elif dna.response_length == "long":
            # Add more detail
            if not adapted.endswith("."):
                adapted += "."
            adapted += " Se tiver mais alguma dúvida, estou à disposição!"
        
        return adapted
    
    def _remove_emoji(self, text: str) -> str:
        """Remove all emoji from text"""
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0001F900-\U0001F9FF]'
        import re
        return re.sub(emoji_pattern, '', text)
    
    def _limit_emoji(self, text: str, limit: int) -> str:
        """Limit emoji count in text"""
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0001F900-\U0001F9FF]'
        import re
        emojis = re.findall(emoji_pattern, text)
        if len(emojis) > limit:
            # Remove excess emoji
            for i, emoji in enumerate(emojis):
                if i >= limit:
                    text = text.replace(emoji, '', 1)
        return text
    
    def _load_profiles(self, file_path: Path):
        """Load profiles from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for profile_data in data:
                    dna = BehavioralDNA.from_dict(profile_data)
                    self._profiles[dna.contact_id] = dna
        except Exception as e:
            print(f"Warning: Could not load profiles: {e}")
    
    def save_profiles(self, file_path: Optional[Path] = None):
        """Save profiles to file"""
        file_path = file_path or self.storage_file
        if not file_path:
            raise ValueError("No storage file provided")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        profiles_data = [dna.to_dict() for dna in self._profiles.values()]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profiles_data, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get DNA manager statistics"""
        tone_counts = {}
        for dna in self._profiles.values():
            tone = dna.tone.value
            tone_counts[tone] = tone_counts.get(tone, 0) + 1
        
        return {
            "total_profiles": len(self._profiles),
            "by_tone": tone_counts,
            "avg_interactions": sum(d.interaction_count for d in self._profiles.values()) / max(1, len(self._profiles)),
            "storage_file": str(self.storage_file) if self.storage_file else None
        }


# Global singleton
dna_manager = DNAManager()


def get_dna_manager() -> DNAManager:
    """Get global DNA manager instance"""
    return dna_manager


# Feature flag check
def is_behavioral_dna_enabled() -> bool:
    """Check if behavioral DNA feature is enabled"""
    return os.getenv("FEATURE_BEHAVIORAL_DNA", "false").lower() == "true"


# Convenience functions
def get_customer_dna(contact_id: str, industry: Optional[str] = None) -> Optional[BehavioralDNA]:
    """Get or create customer DNA"""
    return dna_manager.get_or_create_dna(contact_id, industry)


def adapt_response_to_customer(
    base_response: str,
    contact_id: str,
    industry: Optional[str] = None
) -> str:
    """Adapt response to customer's DNA"""
    dna = get_customer_dna(contact_id, industry)
    if not dna:
        return base_response
    return dna_manager.adapt_response(base_response, dna)
