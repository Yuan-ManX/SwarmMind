from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import time
import uuid

from agent import Agent, AgentRole, AgentMessage, SwarmConfig
from memory import SwarmMemory, MemoryType, MemoryEntry
from debate import DebateEngine, Position, PositionSide
from consensus import ConsensusEngine, ConsensusMethod, ConsensusResult
from cognitive_game import CognitiveGameEngine, CognitiveMove, CognitivePerspective
from handoff import HandoffManager, HandoffReason, HandoffContext, ContextVariable, SwarmRouter


class SwarmPhase(Enum):
    IDLE = "idle"
    INITIALIZATION = "initialization"
    RESEARCH = "research"
    COGNITIVE_GAME = "cognitive_game"
    DEBATE = "debate"
    CRITIQUE = "critique"
    SYNTHESIS = "synthesis"
    CONSENSUS = "consensus"
    COMPLETED = "completed"


@dataclass
class SwarmResult:
    task: str
    solution: str
    consensus: Optional[ConsensusResult]
    rounds_completed: int
    agents: List[Dict[str, Any]]
    memory_stats: Dict[str, Any]
    execution_time: float
    cognitive_game_result: Optional[Dict[str, Any]] = None
    handoff_stats: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "solution": self.solution,
            "consensus": self.consensus.to_dict() if self.consensus else None,
            "rounds_completed": self.rounds_completed,
            "agents": self.agents,
            "memory_stats": self.memory_stats,
            "execution_time": self.execution_time,
            "cognitive_game_result": self.cognitive_game_result,
            "handoff_stats": self.handoff_stats,
            "metadata": self.metadata,
        }


class SwarmEngine:
    def __init__(self, config: Optional[SwarmConfig] = None):
        self.config = config or SwarmConfig()
        self._agents: List[Agent] = []
        self._memory: SwarmMemory = SwarmMemory(max_size=self.config.memory_size)
        self._debate_engine: DebateEngine = DebateEngine(max_rounds=self.config.max_rounds)
        self._consensus_engine: ConsensusEngine = ConsensusEngine(threshold=self.config.consensus_threshold)
        self._cognitive_engine: CognitiveGameEngine = CognitiveGameEngine(
            max_rounds=self.config.max_rounds,
            voting_agents=40
        )
        self._handoff_manager: HandoffManager = HandoffManager()
        self._context_variables: ContextVariable = ContextVariable()
        self._swarm_router: SwarmRouter = SwarmRouter(self._handoff_manager)
        self._phase: SwarmPhase = SwarmPhase.IDLE
        self._current_round: int = 0
        self._task: str = ""
        self._start_time: float = 0.0

    def initialize(self) -> None:
        self._phase = SwarmPhase.INITIALIZATION
        self._agents.clear()
        self._memory.clear()
        self._current_round = 0
        self._handoff_manager = HandoffManager()
        self._context_variables = ContextVariable()
        self._swarm_router = SwarmRouter(self._handoff_manager)

        agent_id = 0
        for role in self.config.roles:
            for _ in range(self.config.agents_per_role):
                agent = Agent(
                    id=f"agent_{agent_id}",
                    name=f"{role.value}_{agent_id}",
                    role=role,
                    model_name=self.config.model_name,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
                self._agents.append(agent)
                self._handoff_manager.register_agent(agent.id)
                agent_id += 1

        self._setup_agent_network()
        self._context_variables.set("task", self._task)

        self._add_memory_entry(
            content=f"Swarm initialized with {len(self._agents)} agents",
            memory_type=MemoryType.CONTEXT,
        )

    def _setup_agent_network(self) -> None:
        role_connections = {
            AgentRole.RESEARCHER: [AgentRole.PLANNER, AgentRole.CRITIC],
            AgentRole.CRITIC: [AgentRole.REVIEWER, AgentRole.RESEARCHER],
            AgentRole.PLANNER: [AgentRole.CODER, AgentRole.RESEARCHER],
            AgentRole.CODER: [AgentRole.REVIEWER, AgentRole.PLANNER],
            AgentRole.REVIEWER: [AgentRole.SYNTHESIZER, AgentRole.CRITIC],
            AgentRole.SYNTHESIZER: [AgentRole.FACILITATOR, AgentRole.REVIEWER],
            AgentRole.FACILITATOR: [AgentRole.RESEARCHER, AgentRole.PLANNER],
        }

        for agent in self._agents:
            connected_roles = role_connections.get(agent.role, [])
            for target_role in connected_roles:
                targets = [a.id for a in self._agents if a.role == target_role]
                for target_id in targets:
                    self._handoff_manager.connect_agents(agent.id, target_id)

    def solve(self, task: str, progress_callback: Optional[Callable] = None) -> SwarmResult:
        self._task = task
        self._start_time = time.time()
        self._current_round = 0
        self._context_variables.set("task", task)

        self.initialize()
        self._add_memory_entry(content=f"Task received: {task}", memory_type=MemoryType.CONTEXT)

        if progress_callback:
            progress_callback(self._phase, 0, self.config.max_rounds)

        self._run_research_phase()
        if progress_callback:
            progress_callback(SwarmPhase.COGNITIVE_GAME, 1, self.config.max_rounds)

        cognitive_result = self._run_cognitive_game_phase()
        if progress_callback:
            progress_callback(SwarmPhase.DEBATE, 2, self.config.max_rounds)

        self._run_debate_phase()
        if progress_callback:
            progress_callback(SwarmPhase.SYNTHESIS, 3, self.config.max_rounds)

        self._run_synthesis_phase()
        if progress_callback:
            progress_callback(SwarmPhase.CONSENSUS, 4, self.config.max_rounds)

        consensus = self._run_consensus_phase()

        self._phase = SwarmPhase.COMPLETED
        execution_time = time.time() - self._start_time

        if progress_callback:
            progress_callback(SwarmPhase.COMPLETED, self.config.max_rounds, self.config.max_rounds)

        solution = self._generate_solution(cognitive_result)
        handoff_stats = self._handoff_manager.analyze_handoff_patterns()

        return SwarmResult(
            task=self._task,
            solution=solution,
            consensus=consensus,
            rounds_completed=self._current_round,
            agents=[{"id": a.id, "name": a.name, "role": a.role.value} for a in self._agents],
            memory_stats=self._memory.get_statistics(),
            execution_time=execution_time,
            cognitive_game_result=cognitive_result,
            handoff_stats=handoff_stats,
        )

    def _run_research_phase(self) -> None:
        self._phase = SwarmPhase.RESEARCH
        researchers = [a for a in self._agents if a.role == AgentRole.RESEARCHER]

        for researcher in researchers:
            self._execute_agent_with_handoff(researcher, "research")

        self._add_memory_entry(
            content=f"Research phase completed with {len(researchers)} researchers",
            memory_type=MemoryType.CONTEXT,
        )

    def _execute_agent_with_handoff(self, agent: Agent, action: str) -> None:
        if action == "research":
            proposal = f"Research proposal from {agent.name} regarding: {self._task}"
            self._add_memory_entry(
                content=proposal,
                memory_type=MemoryType.PROPOSAL,
                agent_id=agent.id,
            )

            msg = AgentMessage(
                sender_id="system",
                content=f"Generate research ideas for: {self._task}",
                message_type="research_request",
                round_number=self._current_round,
            )
            agent.add_message(msg)

            self._handoff_manager.execute_handoff(
                source_id="system",
                target_id=agent.id,
                reason=HandoffReason.TRANSFER,
                shared_state=self._context_variables.get_all(),
                message=f"Assigned research task"
            )

    def _run_cognitive_game_phase(self) -> Optional[Dict[str, Any]]:
        self._phase = SwarmPhase.COGNITIVE_GAME
        self._current_round += 1

        self._cognitive_engine.start_game(self._task)

        critics = [a for a in self._agents if a.role == AgentRole.CRITIC]
        synthesizers = [a for a in self._agents if a.role == AgentRole.SYNTHESIZER]
        planners = [a for a in self._agents if a.role == AgentRole.PLANNER]

        perspective_mapping = {
            AgentRole.CRITIC: CognitivePerspective.CRITICAL,
            AgentRole.SYNTHESIZER: CognitivePerspective.CREATIVE,
            AgentRole.PLANNER: CognitivePerspective.LOGICAL,
            AgentRole.RESEARCHER: CognitivePerspective.EMPIRICAL,
        }

        all_cognitive_agents = critics + synthesizers + planners
        for i, agent in enumerate(all_cognitive_agents):
            perspective = perspective_mapping.get(agent.role, CognitivePerspective.LOGICAL)
            move = CognitiveMove(
                agent_id=agent.id,
                perspective=perspective,
                content=f"Cognitive perspective from {agent.name} ({perspective.value}): analyzing {self._task}",
                strength=0.6 + (i % 3) * 0.1,
                round_number=self._current_round,
            )
            self._cognitive_engine.add_move(move)

            self._add_memory_entry(
                content=f"Cognitive move [{perspective.value}] from {agent.name}: {move.content}",
                memory_type=MemoryType.REASONING,
                agent_id=agent.id,
                round_number=self._current_round,
            )

            self._handoff_manager.execute_handoff(
                source_id="system",
                target_id=agent.id,
                reason=HandoffReason.COLLABORATE,
                message=f"Cognitive game: {perspective.value} perspective"
            )

        for _ in range(3):
            for agent in all_cognitive_agents[:2]:
                perspective = perspective_mapping.get(agent.role, CognitivePerspective.LOGICAL)
                challenge_target = None
                if agent.role == AgentRole.CRITIC and all_cognitive_agents:
                    target = all_cognitive_agents[0]
                    challenge_target = target.id

                move = CognitiveMove(
                    agent_id=agent.id,
                    perspective=perspective,
                    content=f"Deep analysis from {agent.name}: challenging assumptions in {self._task}",
                    challenge_target=challenge_target,
                    strength=0.7,
                    round_number=self._current_round,
                )
                self._cognitive_engine.add_move(move)

                if challenge_target:
                    self._handoff_manager.execute_handoff(
                        source_id=agent.id,
                        target_id=challenge_target,
                        reason=HandoffReason.ESCALATE,
                        message=f"Challenge from {agent.name}"
                    )

        game_analysis = self._cognitive_engine.analyze_game()

        self._add_memory_entry(
            content=f"Cognitive game completed: {game_analysis.get('total_moves', 0)} moves, top voted: {game_analysis.get('top_voted_agent', 'N/A')}",
            memory_type=MemoryType.REASONING,
            round_number=self._current_round,
        )

        return game_analysis

    def _run_debate_phase(self) -> None:
        if not self.config.enable_debate:
            return

        self._phase = SwarmPhase.DEBATE
        self._current_round += 1

        critics = [a for a in self._agents if a.role == AgentRole.CRITIC]
        self._debate_engine.start_debate(self._task)

        for critic in critics:
            position = Position(
                agent_id=critic.id,
                side=PositionSide.SUPPORT,
                argument=f"Critique and analysis from {critic.name}",
                strength=0.7,
            )
            self._debate_engine.add_position(position)

            self._add_memory_entry(
                content=f"Debate contribution from {critic.name}: {position.argument}",
                memory_type=MemoryType.CRITIQUE,
                agent_id=critic.id,
                round_number=self._current_round,
            )

            self._handoff_manager.execute_handoff(
                source_id="system",
                target_id=critic.id,
                reason=HandoffReason.TRANSFER,
                message=f"Debate round {self._current_round}"
            )

    def _run_synthesis_phase(self) -> None:
        self._phase = SwarmPhase.SYNTHESIS
        synthesizers = [a for a in self._agents if a.role == AgentRole.SYNTHESIZER]

        if not synthesizers:
            synthesizers = [a for a in self._agents if a.role == AgentRole.PLANNER]

        synthesis_content = []
        for syn in synthesizers:
            synthesis_content.append(f"Synthesis from {syn.name}")
            self._handoff_manager.execute_handoff(
                source_id="system",
                target_id=syn.id,
                reason=HandoffReason.TRANSFER,
                message="Synthesis phase"
            )

        recent_memories = self._memory.get_recent(50)
        context_parts = [f"[{m.memory_type.value}] {m.content}" for m in recent_memories]

        synthesis = " | ".join(synthesis_content) + f"\n\nIntegrated insights:\n" + "\n".join(context_parts[:10])

        self._add_memory_entry(
            content=synthesis,
            memory_type=MemoryType.REASONING,
            round_number=self._current_round,
        )

    def _run_consensus_phase(self) -> Optional[ConsensusResult]:
        self._phase = SwarmPhase.CONSENSUS

        proposals = self._memory.get_by_type(MemoryType.PROPOSAL)
        positions_for_vote = [
            {"position": p.content[:100], "weight": 1.0, "strength": 0.5 + (hash(p.id) % 50) / 100}
            for p in proposals
        ]

        if not positions_for_vote:
            recent = self._memory.get_recent(10)
            positions_for_vote = [
                {"position": m.content[:100], "weight": 1.0, "strength": 0.5}
                for m in recent
            ]

        self._consensus_engine.reset()
        for item in positions_for_vote:
            self._consensus_engine.register_vote(
                agent_id=str(uuid.uuid4())[:8],
                position=item["position"],
                weight=item["weight"],
            )

        consensus = self._consensus_engine.calculate_weighted_consensus(positions_for_vote)

        self._add_memory_entry(
            content=f"Consensus reached: {consensus.final_position} (confidence: {consensus.confidence:.2%})",
            memory_type=MemoryType.CONSENSUS,
        )

        synthesizers = [a for a in self._agents if a.role == AgentRole.SYNTHESIZER]
        if synthesizers:
            self._handoff_manager.execute_handoff(
                source_id="system",
                target_id=synthesizers[0].id,
                reason=HandoffReason.CONSENSUS,
                message=f"Consensus reached with {consensus.confidence:.2%} confidence"
            )

        return consensus

    def _generate_solution(self, cognitive_result: Optional[Dict[str, Any]] = None) -> str:
        consensus = self._consensus_engine.calculate_majority_vote()
        recent = self._memory.get_recent(20)

        solution_parts = [
            f"## SwarmMind Solution",
            f"",
            f"**Task**: {self._task}",
            f"",
            f"**Consensus**: {consensus.final_position or 'No consensus reached'}",
            f"**Confidence**: {consensus.confidence:.2%}",
            f"",
        ]

        if cognitive_result:
            solution_parts.append("## Cognitive Game Analysis")
            solution_parts.append(f"- Total moves: {cognitive_result.get('total_moves', 0)}")
            solution_parts.append(f"- Perspectives: {cognitive_result.get('perspective_distribution', {})}")
            solution_parts.append(f"- Top voted agent: {cognitive_result.get('top_voted_agent', 'N/A')}")
            solution_parts.append("")

        handoff_stats = self._handoff_manager.analyze_handoff_patterns()
        if handoff_stats.get("total_handoffs", 0) > 0:
            solution_parts.append("## Handoff Analysis")
            solution_parts.append(f"- Total handoffs: {handoff_stats.get('total_handoffs', 0)}")
            solution_parts.append(f"- Unique agents involved: {handoff_stats.get('unique_agents', 0)}")
            solution_parts.append("")

        solution_parts.append("## Key Insights from Swarm")

        proposals = self._memory.get_by_type(MemoryType.PROPOSAL)
        for i, p in enumerate(proposals[:5], 1):
            solution_parts.append(f"{i}. {p.content}")

        solution_parts.append("")
        solution_parts.append("## Reasoning Trace")

        reasoning = self._memory.get_by_type(MemoryType.REASONING)
        for r in reasoning[-5:]:
            solution_parts.append(f"- {r.content}")

        return "\n".join(solution_parts)

    def _add_memory_entry(
        self,
        content: str,
        memory_type: MemoryType,
        agent_id: Optional[str] = None,
        round_number: Optional[int] = None,
    ) -> None:
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            content=content,
            memory_type=memory_type,
            agent_id=agent_id,
            round_number=round_number or self._current_round,
            timestamp=time.time(),
        )
        self._memory.add(entry)

    def get_agents(self) -> List[Agent]:
        return self._agents.copy()

    def get_memory(self) -> SwarmMemory:
        return self._memory

    def get_current_phase(self) -> SwarmPhase:
        return self._phase

    def get_debate_engine(self) -> DebateEngine:
        return self._debate_engine

    def get_consensus_engine(self) -> ConsensusEngine:
        return self._consensus_engine

    def get_cognitive_engine(self) -> CognitiveGameEngine:
        return self._cognitive_engine

    def get_handoff_manager(self) -> HandoffManager:
        return self._handoff_manager

    def get_context_variables(self) -> ContextVariable:
        return self._context_variables

    def execute_handoff(self, source_id: str, target_id: str, reason: HandoffReason, message: str = "") -> HandoffContext:
        return self._handoff_manager.execute_handoff(
            source_id=source_id,
            target_id=target_id,
            reason=reason,
            shared_state=self._context_variables.get_all(),
            message=message,
        )
