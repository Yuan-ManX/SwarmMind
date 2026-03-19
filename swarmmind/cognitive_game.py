from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from agent import Agent, AgentRole
from debate import Position, PositionSide


class CognitivePerspective(Enum):
    LOGICAL = "logical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    PRAGMATIC = "pragmatic"
    CRITICAL = "critical"
    EMPIRICAL = "empirical"


@dataclass
class CognitiveMove:
    agent_id: str
    perspective: CognitivePerspective
    content: str
    challenge_target: Optional[str] = None
    strength: float = 0.5
    round_number: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "perspective": self.perspective.value,
            "content": self.content,
            "challenge_target": self.challenge_target,
            "strength": self.strength,
            "round_number": self.round_number,
        }


@dataclass
class GameRound:
    round_number: int
    topic: str
    moves: List[CognitiveMove] = field(default_factory=list)
    votes: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round_number": self.round_number,
            "topic": self.topic,
            "moves": [m.to_dict() for m in self.moves],
            "votes": self.votes,
        }


class CognitiveGameEngine:
    def __init__(self, max_rounds: int = 5, voting_agents: int = 40):
        self.max_rounds = max_rounds
        self.voting_agents = voting_agents
        self._rounds: List[GameRound] = []
        self._current_round: int = 0
        self._topic: str = ""

    def start_game(self, topic: str) -> GameRound:
        self._topic = topic
        self._rounds.clear()
        self._current_round = 0
        return self._create_round()

    def _create_round(self) -> GameRound:
        round_obj = GameRound(round_number=self._current_round, topic=self._topic)
        self._rounds.append(round_obj)
        return round_obj

    def add_move(self, move: CognitiveMove) -> None:
        if self._rounds:
            self._rounds[-1].moves.append(move)

    def next_round(self) -> GameRound:
        self._current_round += 1
        if self._current_round > self.max_rounds:
            raise ValueError(f"Maximum rounds ({self.max_rounds}) reached")
        return self._create_round()

    def record_vote(self, agent_id: str, voted_for_agent_id: str) -> None:
        if self._rounds:
            if voted_for_agent_id not in self._rounds[-1].votes:
                self._rounds[-1].votes[voted_for_agent_id] = 0
            self._rounds[-1].votes[voted_for_agent_id] += 1

    def get_rounds(self) -> List[GameRound]:
        return self._rounds.copy()

    def get_current_round(self) -> Optional[GameRound]:
        return self._rounds[-1] if self._rounds else None

    def get_all_moves(self) -> List[CognitiveMove]:
        moves = []
        for round_obj in self._rounds:
            moves.extend(round_obj.moves)
        return moves

    def analyze_game(self) -> Dict[str, Any]:
        all_moves = self.get_all_moves()
        if not all_moves:
            return {"status": "no_moves"}

        perspective_counts = {}
        for move in all_moves:
            persp = move.perspective.value
            perspective_counts[persp] = perspective_counts.get(persp, 0) + 1

        challenges_made = len([m for m in all_moves if m.challenge_target])
        avg_strength = sum(m.strength for m in all_moves) / len(all_moves)

        final_round = self._rounds[-1] if self._rounds else None
        final_votes = final_round.votes if final_round else {}

        top_voted = None
        if final_votes:
            sorted_votes = sorted(final_votes.items(), key=lambda x: x[1], reverse=True)
            top_voted = sorted_votes[0][0] if sorted_votes else None

        return {
            "total_rounds": len(self._rounds),
            "total_moves": len(all_moves),
            "perspective_distribution": perspective_counts,
            "challenges_made": challenges_made,
            "average_strength": avg_strength,
            "final_votes": final_votes,
            "top_voted_agent": top_voted,
        }

    def select_experts_for_context(
        self,
        agents: List[Agent],
        context: str,
        num_experts: int = 3
    ) -> List[Agent]:
        role_scores = {}
        context_lower = context.lower()

        keyword_role_map = {
            "research": AgentRole.RESEARCHER,
            "code": AgentRole.CODER,
            "implement": AgentRole.CODER,
            "critic": AgentRole.CRITIC,
            "review": AgentRole.REVIEWER,
            "plan": AgentRole.PLANNER,
            "strategy": AgentRole.PLANNER,
            "creative": AgentRole.SYNTHESIZER,
            "combine": AgentRole.SYNTHESIZER,
        }

        for keyword, role in keyword_role_map.items():
            if keyword in context_lower:
                role_scores[role] = role_scores.get(role, 0) + 2

        scored_agents = []
        for agent in agents:
            score = role_scores.get(agent.role, 1)
            if agent.role == AgentRole.CRITIC:
                score += 1
            scored_agents.append((agent, score))

        scored_agents.sort(key=lambda x: x[1], reverse=True)
        return [a for a, _ in scored_agents[:num_experts]]

    def get_winning_position(self) -> Optional[str]:
        all_moves = self.get_all_moves()
        if not all_moves:
            return None

        agent_scores: Dict[str, float] = {}
        for move in all_moves:
            if move.agent_id not in agent_scores:
                agent_scores[move.agent_id] = 0
            agent_scores[move.agent_id] += move.strength

        if not agent_scores:
            return None

        sorted_scores = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[0][0]
