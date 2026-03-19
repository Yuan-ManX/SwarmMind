from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum


class HandoffReason(Enum):
    COMPLETE = "complete"
    ESCALATE = "escalate"
    TRANSFER = "transfer"
    COLLABORATE = "collaborate"
    CONSENSUS = "consensus"


@dataclass
class HandoffContext:
    source_agent_id: str
    target_agent_id: str
    reason: HandoffReason
    shared_state: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    timestamp: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_agent_id": self.source_agent_id,
            "target_agent_id": self.target_agent_id,
            "reason": self.reason.value,
            "shared_state": self.shared_state,
            "message": self.message,
            "timestamp": self.timestamp,
        }


class HandoffManager:
    def __init__(self):
        self._handoff_history: List[HandoffContext] = []
        self._agent_network: Dict[str, List[str]] = {}
        self._current_agent_id: Optional[str] = None

    def register_agent(self, agent_id: str, connected_agents: List[str] = None) -> None:
        self._agent_network[agent_id] = connected_agents or []

    def connect_agents(self, from_agent: str, to_agent: str) -> None:
        if from_agent not in self._agent_network:
            self._agent_network[from_agent] = []
        if to_agent not in self._agent_network[from_agent]:
            self._agent_network[from_agent].append(to_agent)

    def execute_handoff(
        self,
        source_id: str,
        target_id: str,
        reason: HandoffReason,
        shared_state: Optional[Dict[str, Any]] = None,
        message: str = ""
    ) -> HandoffContext:
        handoff = HandoffContext(
            source_agent_id=source_id,
            target_agent_id=target_id,
            reason=reason,
            shared_state=shared_state or {},
            message=message,
            timestamp=0.0,
        )
        self._handoff_history.append(handoff)
        self._current_agent_id = target_id
        return handoff

    def can_handoff(self, from_agent: str, to_agent: str) -> bool:
        if from_agent not in self._agent_network:
            return True
        return to_agent in self._agent_network[from_agent]

    def get_handoff_history(self) -> List[HandoffContext]:
        return self._handoff_history.copy()

    def get_current_agent(self) -> Optional[str]:
        return self._current_agent_id

    def get_connected_agents(self, agent_id: str) -> List[str]:
        return self._agent_network.get(agent_id, [])

    def analyze_handoff_patterns(self) -> Dict[str, Any]:
        if not self._handoff_history:
            return {"total_handoffs": 0}

        reason_counts = {}
        agent_handoff_counts = {}

        for handoff in self._handoff_history:
            reason = handoff.reason.value
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

            source = handoff.source_agent_id
            agent_handoff_counts[source] = agent_handoff_counts.get(source, 0) + 1

        return {
            "total_handoffs": len(self._handoff_history),
            "reason_distribution": reason_counts,
            "agent_activity": agent_handoff_counts,
            "unique_agents": len(set(list(agent_handoff_counts.keys()) + [h.target_agent_id for h in self._handoff_history])),
        }


class ContextVariable:
    def __init__(self):
        self._variables: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._variables.get(key, default)

    def update(self, updates: Dict[str, Any]) -> None:
        self._variables.update(updates)

    def get_all(self) -> Dict[str, Any]:
        return self._variables.copy()

    def clear(self) -> None:
        self._variables.clear()

    def has(self, key: str) -> bool:
        return key in self._variables


class SwarmRouter:
    def __init__(self, handoff_manager: HandoffManager):
        self._handoff_manager = handoff_manager
        self._routing_rules: Dict[str, Callable] = {}

    def add_rule(self, condition: str, handler: Callable) -> None:
        self._routing_rules[condition] = handler

    def route(self, agent_id: str, context: ContextVariable) -> Optional[str]:
        for condition, handler in self._routing_rules.items():
            result = handler(context.get_all())
            if result:
                return result
        return None

    def auto_route_by_role(self, current_role: str, context: ContextVariable) -> Optional[str]:
        role_routing = {
            "researcher": ["planner", "critic"],
            "critic": ["reviewer", "researcher"],
            "planner": ["coder", "researcher"],
            "reviewer": ["synthesizer", "critic"],
            "synthesizer": ["facilitator"],
        }
        target_roles = role_routing.get(current_role, [])
        if target_roles:
            return target_roles[0]
        return None

    def route_to_consensus(self, agents: List[str]) -> Optional[str]:
        if not agents:
            return None
        return agents[-1]

    def route_for_debate(self, debaters: List[str], current: str) -> Optional[str]:
        if current in debaters:
            idx = debaters.index(current)
            next_idx = (idx + 1) % len(debaters)
            return debaters[next_idx]
        return debaters[0] if debaters else None
