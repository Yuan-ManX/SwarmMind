from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from debate import Position, PositionSide


class ConsensusMethod(Enum):
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_AVERAGE = "weighted_average"
    HIERARCHICAL = "hierarchical"
    DELPHI = "delphi"


@dataclass
class ConsensusResult:
    consensus_reached: bool
    final_position: str
    confidence: float
    method: ConsensusMethod
    votes: Dict[str, int] = field(default_factory=dict)
    dissenting_opinions: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "consensus_reached": self.consensus_reached,
            "final_position": self.final_position,
            "confidence": self.confidence,
            "method": self.method.value,
            "votes": self.votes,
            "dissenting_opinions": self.dissenting_opinions,
            "reasoning": self.reasoning,
        }


class ConsensusEngine:
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self._votes: Dict[str, int] = {}
        self._weights: Dict[str, float] = {}

    def reset(self):
        self._votes.clear()
        self._weights.clear()

    def register_vote(self, agent_id: str, position: str, weight: float = 1.0):
        self._votes[position] = self._votes.get(position, 0) + 1
        self._weights[agent_id] = weight

    def calculate_majority_vote(self) -> ConsensusResult:
        if not self._votes:
            return ConsensusResult(
                consensus_reached=False,
                final_position="",
                confidence=0.0,
                method=ConsensusMethod.MAJORITY_VOTE,
                reasoning="No votes recorded",
            )

        total_votes = sum(self._votes.values())
        sorted_votes = sorted(self._votes.items(), key=lambda x: x[1], reverse=True)
        winner, winner_votes = sorted_votes[0]
        winner_ratio = winner_votes / total_votes

        consensus = winner_ratio >= self.threshold
        confidence = winner_ratio

        dissenting = []
        for pos, count in sorted_votes[1:]:
            dissenting.append({
                "position": pos,
                "votes": count,
                "percentage": count / total_votes,
            })

        return ConsensusResult(
            consensus_reached=consensus,
            final_position=winner,
            confidence=confidence,
            method=ConsensusMethod.MAJORITY_VOTE,
            votes=self._votes.copy(),
            dissenting_opinions=dissenting,
            reasoning=f"Winner '{winner}' achieved {winner_ratio:.2%} support" if consensus else f"No consensus - leading option '{winner}' has only {winner_ratio:.2%}",
        )

    def calculate_weighted_consensus(self, positions_with_weights: List[Dict[str, Any]]) -> ConsensusResult:
        if not positions_with_weights:
            return ConsensusResult(
                consensus_reached=False,
                final_position="",
                confidence=0.0,
                method=ConsensusMethod.WEIGHTED_AVERAGE,
                reasoning="No positions provided",
            )

        weighted_scores: Dict[str, float] = {}
        for item in positions_with_weights:
            pos = item["position"]
            weight = item.get("weight", 1.0)
            strength = item.get("strength", 0.5)
            score = weight * strength
            weighted_scores[pos] = weighted_scores.get(pos, 0) + score

        total_score = sum(weighted_scores.values())
        sorted_positions = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
        winner, winner_score = sorted_positions[0]
        winner_ratio = winner_score / total_score if total_score > 0 else 0

        return ConsensusResult(
            consensus_reached=winner_ratio >= self.threshold,
            final_position=winner,
            confidence=winner_ratio,
            method=ConsensusMethod.WEIGHTED_AVERAGE,
            votes=self._votes.copy(),
            dissenting_opinions=[
                {"position": pos, "weighted_score": score}
                for pos, score in sorted_positions[1:]
            ],
            reasoning=f"Weighted consensus for '{winner}' with score {winner_ratio:.2%}",
        )

    def calculate_delphi_consensus(self, rounds: int, positions_history: List[List[str]]) -> ConsensusResult:
        if not positions_history:
            return ConsensusResult(
                consensus_reached=False,
                final_position="",
                confidence=0.0,
                method=ConsensusMethod.DELPHI,
                reasoning="No Delphi rounds",
            )

        position_counts = {}
        for round_positions in positions_history:
            for pos in round_positions:
                position_counts[pos] = position_counts.get(pos, 0) + 1

        sorted_positions = sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
        final_position = sorted_positions[0][0]
        total = sum(position_counts.values())
        confidence = sorted_positions[0][1] / total if total > 0 else 0

        stability = 1.0
        if len(sorted_positions) > 1:
            first = sorted_positions[0][1]
            second = sorted_positions[1][1]
            stability = (first - second) / first if first > 0 else 0

        return ConsensusResult(
            consensus_reached=stability >= self.threshold,
            final_position=final_position,
            confidence=confidence * stability,
            method=ConsensusMethod.DELPHI,
            votes=position_counts,
            dissenting_opinions=[],
            reasoning=f"Delphi consensus reached after {rounds} rounds with {stability:.2%} stability",
        )
