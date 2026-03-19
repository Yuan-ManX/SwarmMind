from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class MemoryType(Enum):
    PROPOSAL = "proposal"
    CRITIQUE = "critique"
    REASONING = "reasoning"
    CONSENSUS = "consensus"
    CONTEXT = "context"


@dataclass
class MemoryEntry:
    id: str
    content: str
    memory_type: MemoryType
    agent_id: Optional[str] = None
    round_number: int = 0
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    relevance_score: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "agent_id": self.agent_id,
            "round_number": self.round_number,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "relevance_score": self.relevance_score,
        }


class SwarmMemory:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._entries: List[MemoryEntry] = []
        self._agent_memories: Dict[str, List[str]] = {}

    def add(self, entry: MemoryEntry) -> None:
        self._entries.append(entry)
        if entry.agent_id:
            if entry.agent_id not in self._agent_memories:
                self._agent_memories[entry.agent_id] = []
            self._agent_memories[entry.agent_id].append(entry.id)
        if len(self._entries) > self.max_size:
            self._evict_oldest()

    def _evict_oldest(self) -> None:
        if self._entries:
            oldest = self._entries.pop(0)
            if oldest.agent_id and oldest.id in self._agent_memories.get(oldest.agent_id, []):
                self._agent_memories[oldest.agent_id].remove(oldest.id)

    def get_all(self) -> List[MemoryEntry]:
        return self._entries.copy()

    def get_by_type(self, memory_type: MemoryType) -> List[MemoryEntry]:
        return [e for e in self._entries if e.memory_type == memory_type]

    def get_by_agent(self, agent_id: str) -> List[MemoryEntry]:
        return [e for e in self._entries if e.agent_id == agent_id]

    def get_recent(self, n: int = 10) -> List[MemoryEntry]:
        return self._entries[-n:] if self._entries else []

    def get_by_round(self, round_number: int) -> List[MemoryEntry]:
        return [e for e in self._entries if e.round_number == round_number]

    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        query_lower = query.lower()
        scored = []
        for entry in self._entries:
            if query_lower in entry.content.lower():
                scored.append((entry, entry.relevance_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [e for e, _ in scored[:limit]]

    def clear(self) -> None:
        self._entries.clear()
        self._agent_memories.clear()

    def get_statistics(self) -> Dict[str, Any]:
        type_counts = {}
        for entry in self._entries:
            type_key = entry.memory_type.value
            type_counts[type_key] = type_counts.get(type_key, 0) + 1
        return {
            "total_entries": len(self._entries),
            "type_distribution": type_counts,
            "agent_count": len(self._agent_memories),
        }

    def get_context_for_agent(self, agent_id: str, round_num: int) -> str:
        agent_entries = self.get_by_agent(agent_id)
        round_entries = self.get_by_round(round_num)
        recent_entries = self.get_recent(20)
        all_relevant = list({e.id: e for e in agent_entries + round_entries + recent_entries}.values())
        context_lines = []
        for entry in sorted(all_relevant, key=lambda x: x.timestamp):
            type_tag = entry.memory_type.value.upper()
            context_lines.append(f"[{type_tag}] {entry.content}")
        return "\n".join(context_lines) if context_lines else "No relevant context."
