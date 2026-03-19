from swarmmind.core import SwarmEngine, SwarmConfig, SwarmPhase, SwarmResult
from swarmmind.agent import Agent, AgentRole, AgentMessage
from swarmmind.memory import SwarmMemory, MemoryEntry, MemoryType
from swarmmind.debate import DebateEngine, DebateRound, Position, PositionSide
from swarmmind.consensus import ConsensusEngine, ConsensusResult, ConsensusMethod


class Swarm:
    def __init__(
        self,
        agents: int = 5,
        roles: list = None,
        model_name: str = "gpt-4",
        max_rounds: int = 5,
        **kwargs
    ):
        if roles is None:
            roles = ["researcher", "critic", "planner", "reviewer"]

        role_mapping = {
            "researcher": AgentRole.RESEARCHER,
            "critic": AgentRole.CRITIC,
            "planner": AgentRole.PLANNER,
            "coder": AgentRole.CODER,
            "reviewer": AgentRole.REVIEWER,
            "synthesizer": AgentRole.SYNTHESIZER,
            "facilitator": AgentRole.FACILITATOR,
        }

        agent_roles = [role_mapping.get(r, AgentRole.RESEARCHER) for r in roles]
        agents_per_role = max(1, agents // len(roles))

        self.config = SwarmConfig(
            name="Swarm",
            max_rounds=max_rounds,
            agents_per_role=agents_per_role,
            roles=agent_roles,
            model_name=model_name,
            **kwargs
        )
        self._engine = SwarmEngine(self.config)

    def solve(self, task: str, progress_callback=None) -> SwarmResult:
        return self._engine.solve(task, progress_callback)

    def get_agents(self):
        return self._engine.get_agents()

    def get_memory(self):
        return self._engine.get_memory()


__all__ = [
    "Swarm",
    "SwarmEngine",
    "SwarmConfig",
    "SwarmPhase",
    "SwarmResult",
    "Agent",
    "AgentRole",
    "AgentMessage",
    "SwarmMemory",
    "MemoryEntry",
    "MemoryType",
    "DebateEngine",
    "DebateRound",
    "Position",
    "PositionSide",
    "ConsensusEngine",
    "ConsensusResult",
    "ConsensusMethod",
]
