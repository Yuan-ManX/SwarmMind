from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class AgentRole(Enum):
    RESEARCHER = "researcher"
    CRITIC = "critic"
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    SYNTHESIZER = "synthesizer"
    FACILITATOR = "facilitator"


@dataclass
class AgentMessage:
    sender_id: str
    content: str
    message_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0
    round_number: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender_id": self.sender_id,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "round_number": self.round_number,
        }


@dataclass
class Agent:
    id: str
    name: str
    role: AgentRole
    model_name: str = "gpt-4"
    system_prompt: str = ""
    max_tokens: int = 2048
    temperature: float = 0.7

    def __post_init__(self):
        self._messages: List[AgentMessage] = []
        self._context: Dict[str, Any] = {}

    def add_message(self, message: AgentMessage):
        self._messages.append(message)

    def get_messages(self) -> List[AgentMessage]:
        return self._messages.copy()

    def clear_messages(self):
        self._messages.clear()

    def set_context(self, key: str, value: Any):
        self._context[key] = value

    def get_context(self, key: str) -> Optional[Any]:
        return self._context.get(key)

    def get_role_description(self) -> str:
        role_descriptions = {
            AgentRole.RESEARCHER: "You are a researcher who generates ideas and explores possibilities.",
            AgentRole.CRITIC: "You are a critic who identifies weaknesses and challenges assumptions.",
            AgentRole.PLANNER: "You are a planner who organizes reasoning and creates structure.",
            AgentRole.CODER: "You are a coder who implements solutions and writes code.",
            AgentRole.REVIEWER: "You are a reviewer who evaluates results and provides feedback.",
            AgentRole.SYNTHESIZER: "You are a synthesizer who combines ideas into coherent wholes.",
            AgentRole.FACILITATOR: "You are a facilitator who guides discussion and ensures progress.",
        }
        return role_descriptions.get(self.role, "")

    def build_system_prompt(self, task: str, swarm_context: Dict[str, Any]) -> str:
        base_prompt = self.get_role_description()
        context_str = "\n".join([f"{k}: {v}" for k, v in swarm_context.items()])
        return f"{base_prompt}\n\nCurrent Task: {task}\n\nSwarm Context:\n{context_str}\n\nYour name: {self.name}\nYour ID: {self.id}"


@dataclass
class SwarmConfig:
    name: str = "SwarmMind"
    max_rounds: int = 5
    agents_per_role: int = 1
    roles: List[AgentRole] = field(default_factory=list)
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2048
    consensus_threshold: float = 0.7
    enable_debate: bool = True
    enable_memory: bool = True
    memory_size: int = 1000

    def __post_init__(self):
        if not self.roles:
            self.roles = [
                AgentRole.RESEARCHER,
                AgentRole.CRITIC,
                AgentRole.PLANNER,
                AgentRole.REVIEWER,
            ]
