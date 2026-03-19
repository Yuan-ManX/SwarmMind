from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from agent import Agent, AgentRole, AgentMessage
from memory import SwarmMemory, MemoryType, MemoryEntry


class PositionSide(Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"


@dataclass
class Position:
    agent_id: str
    side: PositionSide
    argument: str
    evidence: List[str] = field(default_factory=list)
    strength: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "side": self.side.value,
            "argument": self.argument,
            "evidence": self.evidence,
            "strength": self.strength,
        }


@dataclass
class DebateRound:
    round_number: int
    topic: str
    positions: List[Position] = field(default_factory=list)
    cross_examinations: List[Dict[str, str]] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round_number": self.round_number,
            "topic": self.topic,
            "positions": [p.to_dict() for p in self.positions],
            "cross_examinations": self.cross_examinations,
            "summary": self.summary,
        }


class DebateEngine:
    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds
        self._rounds: List[DebateRound] = []
        self._current_round: int = 0

    def start_debate(self, topic: str) -> DebateRound:
        self._current_round = 0
        self._rounds.clear()
        return self._create_round(topic)

    def _create_round(self, topic: str) -> DebateRound:
        round_obj = DebateRound(round_number=self._current_round, topic=topic)
        self._rounds.append(round_obj)
        return round_obj

    def add_position(self, position: Position) -> None:
        if self._rounds:
            self._rounds[-1].positions.append(position)

    def add_cross_examination(self, question: str, answer: str) -> None:
        if self._rounds:
            self._rounds[-1].cross_examinations.append({
                "question": question,
                "answer": answer
            })

    def next_round(self, topic: Optional[str] = None) -> DebateRound:
        self._current_round += 1
        if self._current_round > self.max_rounds:
            raise ValueError(f"Maximum rounds ({self.max_rounds}) reached")
        topic = topic or (self._rounds[-1].topic if self._rounds else "")
        return self._create_round(topic)

    def set_round_summary(self, summary: str) -> None:
        if self._rounds:
            self._rounds[-1].summary = summary

    def get_rounds(self) -> List[DebateRound]:
        return self._rounds.copy()

    def get_current_round(self) -> Optional[DebateRound]:
        return self._rounds[-1] if self._rounds else None

    def get_all_positions(self) -> List[Position]:
        positions = []
        for round_obj in self._rounds:
            positions.extend(round_obj.positions)
        return positions

    def analyze_positions(self) -> Dict[str, Any]:
        positions = self.get_all_positions()
        support = [p for p in positions if p.side == PositionSide.SUPPORT]
        oppose = [p for p in positions if p.side == PositionSide.OPPOSE]
        neutral = [p for p in positions if p.side == PositionSide.NEUTRAL]

        avg_support_strength = sum(p.strength for p in support) / len(support) if support else 0
        avg_oppose_strength = sum(p.strength for p in oppose) / len(oppose) if oppose else 0

        return {
            "total_positions": len(positions),
            "support_count": len(support),
            "oppose_count": len(oppose),
            "neutral_count": len(neutral),
            "avg_support_strength": avg_support_strength,
            "avg_oppose_strength": avg_oppose_strength,
            "dominant_side": "support" if avg_support_strength > avg_oppose_strength else "oppose",
        }

    def extract_key_arguments(self) -> List[Dict[str, Any]]:
        positions = self.get_all_positions()
        sorted_positions = sorted(positions, key=lambda p: p.strength, reverse=True)
        return [
            {
                "agent_id": p.agent_id,
                "argument": p.argument,
                "strength": p.strength,
                "side": p.side.value,
            }
            for p in sorted_positions[:5]
        ]
