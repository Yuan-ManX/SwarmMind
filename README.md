<div align="center">

<img src="./assets/SwarmMind-logo.png" alt="SwarmMind Logo" width="75%"/>



# 🐝 SwarmMind  
### Many minds. One intelligence.
### Swarm Intelligence Engine for AI Agents.

### [English](./README.md) | [中文文档](./README_CN.md)

</div>


> Many AI minds. One collective intelligence.  
> Let AI agents think together, challenge each other, and converge to superior solutions.

SwarmMind is an open-source **Swarm Intelligence Engine** powered by multi-agent cognitive gaming with intelligent routing. Traditional AI systems rely on a **single model generating answers**. SwarmMind explores a different paradigm: **Intelligence emerging from many AI agents thinking together through cognitive confrontation and intelligent handoffs**.

Inspired by natural swarm systems such as **ant colonies, bee swarms, and distributed neural systems**, SwarmMind orchestrates multiple AI agents in **structured cognitive games** where they collaborate, debate, challenge, transfer control intelligently, and ultimately converge to optimal solutions through democratic voting.

Instead of a single AI responding once, SwarmMind creates **a cognitive swarm that thinks, games, routes, and decides together**.



## 📖 Table of Contents

- [Overview](#overview)
- [What is Swarm Intelligence](#what-is-swarm-intelligence)
- [Vision](#vision)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Innovation Points](#innovation-points)
- [Cognitive Gaming](#cognitive-gaming)
- [Handoff & Routing](#handoff--routing)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Example Usage](#example-usage)
- [API Reference](#api-reference)
- [Use Cases](#use-cases)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)



## Overview

SwarmMind is an open-source **Swarm Intelligence Engine** for multi-agent AI systems.

Most AI systems today rely on a **single model generating answers**.

SwarmMind explores a different paradigm:

> Intelligence emerging from many AI agents thinking together through cognitive confrontation and intelligent routing.

Inspired by natural swarm systems:

- ant colonies  
- bee swarms  
- bird flocks  
- human teams  

SwarmMind orchestrates AI agents to:

- collaborate on complex reasoning
- challenge each other's assumptions
- engage in cognitive games
- transfer control intelligently via handoffs
- route based on role and context
- reach consensus through democratic voting

The result is **a cognitive swarm that thinks together, games cognitively, routes intelligently, and converges**.



## What is Swarm Intelligence

Swarm Intelligence describes how **many simple agents interacting locally can produce powerful collective intelligence**.

Examples from nature:

| System | Behavior |
|------|---------|
| Ant colonies | discover shortest paths |
| Bee swarms | collective decision making |
| Bird flocks | coordinated movement |
| Human teams | collaborative problem solving |

SwarmMind brings this principle to **AI agent systems** with a unique focus on **cognitive confrontation, intelligent handoffs, and democratic convergence**.



## Vision

Modern AI models are powerful but **isolated**.

Each model works independently with no real intellectual confrontation or coordination.

SwarmMind is building the **Cognitive Swarm Intelligence Engine** that enables agents to:

- engage in multi-perspective reasoning
- challenge each other's cognitive blind spots
- transfer control intelligently through handoff mechanisms
- route tasks based on role specialization
- vote democratically on positions
- reach consensus that exceeds single-model capability

Our mission:

> The future of AI is not a single model — it's **many minds thinking together, gaming cognitively, routing intelligently, and converging to superior intelligence**.



## Key Features

### 🧠 Multi-Agent Cognitive Gaming

Unlike simple multi-agent collaboration, SwarmMind agents engage in **structured cognitive games**:

- Multiple perspectives analyzing the same problem
- Direct challenges between agents
- Strength scoring for arguments
- Democratic voting on positions

### 🔄 Seven-Phase Cognitive Pipeline

SwarmMind executes a **seven-phase cognitive pipeline**:

```
INITIALIZATION → RESEARCH → COGNITIVE_GAME → DEBATE → CRITIQUE → SYNTHESIS → CONSENSUS → COMPLETED
```

Each phase has specific agent roles active, ensuring comprehensive cognitive processing.

### 🧩 Modular Agent Roles

Agents can have specialized cognitive roles:

| Agent | Responsibility | Perspective |
|------|---------------|-------------|
| Research Agent | generate ideas | Empirical |
| Critic Agent | challenge assumptions | Critical |
| Planner Agent | organize reasoning | Logical |
| Coder Agent | implement solutions | Pragmatic |
| Reviewer Agent | evaluate results | Analytical |
| Synthesizer Agent | combine insights | Creative |
| Facilitator Agent | guide discussion | Balanced |

### 🔀 Intelligent Handoff & Routing

Inspired by multi-agent orchestration, SwarmMind features **intelligent handoff mechanisms**:

- **HandoffManager**: Tracks control transfers between agents
- **SwarmRouter**: Routes tasks based on role and context
- **ContextVariable**: Shared state across agent executions
- Role-based routing: Researcher → Planner → Critic → Reviewer → Synthesizer

### 🧠 Dual-Track Memory System

Agents share a collaborative memory system with dual tracks:

- **Proposal Track**: ideas and suggestions
- **Critique Track**: challenges and weaknesses
- **Reasoning Track**: cognitive moves and analysis
- **Consensus Track**: voting results and final positions

### ⚖️ Built-in Debate Engine

Structured debate capabilities:

- Position tracking (support/oppose/neutral)
- Cross-examination support
- Round-by-round argument management
- Strength scoring for positions

### 🎯 Multiple Consensus Methods

Flexible consensus mechanisms:

- Majority voting
- Weighted consensus
- Hierarchical voting
- Cognitive game voting (democratic confrontation)

### 🗳️ Cognitive Game Engine

Unique cognitive gaming features:

- 6 cognitive perspectives (Logical, Creative, Analytical, Pragmatic, Critical, Empirical)
- Multi-round cognitive confrontation
- Challenge targeting between agents
- 40-agent democratic voting simulation
- Perspective distribution analysis



## Architecture

SwarmMind follows a **distributed cognitive swarm architecture with intelligent routing**:

```
                User
                 │
                 ▼
           Swarm Engine
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 Agent A      Agent B      Agent C
 Researcher    Critic      Planner
     │           │           │
     └──── Cognitive Game ───┘
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
  Debate     Synthesis    Consensus
     │           │           │
     └─── Handoff Manager ───┘
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
  Router    Context Var   Network
```

Core components:

- **Swarm Engine** — orchestrates cognitive phases and execution flow
- **Agents** — autonomous reasoning units with specialized cognitive roles
- **Swarm Memory** — dual-track shared context and history
- **Cognitive Game Engine** — multi-agent cognitive confrontation engine
- **HandoffManager** — tracks and executes control transfers
- **SwarmRouter** — intelligent task routing based on roles
- **ContextVariable** — shared state management
- **Debate Engine** — structured argument exchange
- **Consensus Engine** — democratic aggregation and voting



## Innovation Points

SwarmMind introduces several original innovations:

### 1. Cognitive Gaming as Core Mechanism

Unlike systems that treat multi-agent as simple collaboration, SwarmMind makes **cognitive confrontation central**:

- Agents don't just collaborate — they **challenge** each other
- Every assumption can be challenged by a critic agent
- Arguments have **strength scores** that affect voting
- The cognitive game produces **winners** through democratic voting

### 2. Seven-Phase Cognitive Pipeline

The execution flow is structured as seven distinct phases:

```
INITIALIZATION → RESEARCH → COGNITIVE_GAME → DEBATE → CRITIQUE → SYNTHESIS → CONSENSUS → COMPLETED
```

This ensures **comprehensive cognitive processing** before reaching conclusions.

### 3. Intelligent Handoff & Role-Based Routing

Inspired by multi-agent orchestration, SwarmMind implements **intelligent handoff mechanisms**:

- **Handoff Reasons**: COMPLETE, ESCALATE, TRANSFER, COLLABORATE, CONSENSUS
- **Role Network**: Agents connected based on role relationships
- **SwarmRouter**: Automatic routing based on current role and context
- **ContextVariable**: Shared state passed during handoffs

### 4. Six Cognitive Perspectives

Agents operate from distinct cognitive perspectives:

| Perspective | Character | Best For |
|------------|----------|---------|
| Logical | Systematic reasoning | Architecture, planning |
| Creative | Novel combinations | Brainstorming, design |
| Analytical | Detail examination | Debugging, review |
| Pragmatic | Practical focus | Implementation |
| Critical | Challenge mindset | Risk identification |
| Empirical | Evidence-based | Research, validation |

### 5. Democratic Convergence

Final decisions emerge through **democratic convergence**:

- Multiple rounds of cognitive confrontation
- Agents vote on positions (simulating 40-agent voting)
- Strength scores affect final outcomes
- Consensus isn't compromise — it's **earned superiority**

### 6. Role-Based Cognitive Specialization

Each role has a **cognitive profile**:

- Researchers → Empirical perspective → Idea generation
- Critics → Critical perspective → Weakness identification
- Planners → Logical perspective → Structure creation
- Synthesizers → Creative perspective → Integration
- Reviewers → Analytical perspective → Evaluation



## Cognitive Gaming

SwarmMind's cognitive game engine enables **structured intellectual confrontation**:

### How It Works

1. **Perspective Assignment**: Each agent receives a cognitive perspective
2. **Initial Moves**: Agents make opening arguments from their perspective
3. **Challenge Phase**: Critics challenge other agents' assumptions
4. **Multi-Round Confrontation**: Multiple rounds of cognitive exchange
5. **Democratic Voting**: 40 simulated agents vote on positions
6. **Winner Declaration**: Strongest cognitive position wins

### Cognitive Perspectives

- **Logical**: Systematic, step-by-step reasoning
- **Creative**: Novel combinations and unexpected angles
- **Analytical**: Deep examination of details
- **Pragmatic**: Practical, implementable solutions
- **Critical**: Challenging assumptions and finding flaws
- **Empirical**: Evidence-based, data-driven approach



## Handoff & Routing

SwarmMind features **intelligent handoff and routing mechanisms**:

### Handoff Reasons

- **COMPLETE**: Task completed, return control
- **ESCALATE**: Issue requiring higher authority
- **TRANSFER**: Hand off to next agent in pipeline
- **COLLABORATE**: Request collaboration
- **CONSENSUS**: Reaching collective decision

### Role Network

Agents are connected in a role-based network:

```
Researcher → Planner, Critic
Critic → Reviewer, Researcher
Planner → Coder, Researcher
Coder → Reviewer, Planner
Reviewer → Synthesizer, Critic
Synthesizer → Facilitator, Reviewer
Facilitator → Researcher, Planner
```

### SwarmRouter

Intelligent routing based on:

- Current agent role
- Task context
- Handoff history
- Consensus state



## Installation

Clone the repository:

```bash
git clone https://github.com/Yuan-ManX/SwarmMind.git
cd SwarmMind
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install in development mode:

```bash
pip install -e .
```



## Quick Start

Run a simple swarm reasoning experiment:

```bash
python run_swarm.py
```



## Example Usage

Create a swarm of AI agents with cognitive gaming and handoffs:

```python
from swarmmind import Swarm

swarm = Swarm(
    agents=5,
    roles=["researcher", "critic", "planner", "coder", "reviewer"]
)

result = swarm.solve(
    task="Design an efficient training strategy for a language model"
)

print(result.solution)
```

Access handoff statistics:

```python
if result.handoff_stats:
    print(f"Total handoffs: {result.handoff_stats['total_handoffs']}")
    print(f"Unique agents: {result.handoff_stats['unique_agents']}")
```

Advanced configuration with handoff tuning:

```python
from swarmmind import SwarmConfig, AgentRole
from swarmmind.core import SwarmEngine
from swarmmind.handoff import HandoffManager, HandoffReason

config = SwarmConfig(
    name="ResearchSwarm",
    max_rounds=5,
    agents_per_role=2,
    roles=[
        AgentRole.RESEARCHER,
        AgentRole.CRITIC,
        AgentRole.PLANNER,
        AgentRole.REVIEWER,
    ],
    consensus_threshold=0.75,
    enable_debate=True,
)

engine = SwarmEngine(config)
result = engine.solve("Analyze the impact of quantum computing on cryptography")
```



## API Reference

### Swarm Class

```python
from swarmmind import Swarm

swarm = Swarm(
    agents=5,              # Total number of agents
    roles=["researcher", "critic", "planner"],
    model_name="gpt-4",   # Model to use
    max_rounds=5          # Maximum reasoning rounds
)

result = swarm.solve(task="Your task here")
```

### SwarmConfig

```python
from swarmmind import SwarmConfig, AgentRole

config = SwarmConfig(
    name="CustomSwarm",
    max_rounds=10,
    agents_per_role=2,
    roles=[AgentRole.RESEARCHER, AgentRole.CRITIC],
    model_name="gpt-4",
    temperature=0.7,
    consensus_threshold=0.7,
    enable_debate=True,
    enable_memory=True,
    memory_size=1000,
)
```

### Agent Roles

Available roles and their cognitive perspectives:

- `AgentRole.RESEARCHER` — generates ideas, empirical perspective
- `AgentRole.CRITIC` — challenges assumptions, critical perspective
- `AgentRole.PLANNER` — organizes reasoning, logical perspective
- `AgentRole.CODER` — implements solutions, pragmatic perspective
- `AgentRole.REVIEWER` — evaluates results, analytical perspective
- `AgentRole.SYNTHESIZER` — combines insights, creative perspective
- `AgentRole.FACILITATOR` — guides discussion, balanced perspective

### Handoff API

```python
from swarmmind.handoff import HandoffManager, HandoffReason, ContextVariable, SwarmRouter

# Handoff Manager
hm = HandoffManager()
hm.register_agent("agent_1")
hm.connect_agents("agent_1", "agent_2")
hm.execute_handoff("agent_1", "agent_2", HandoffReason.TRANSFER, message="Task transfer")
stats = hm.analyze_handoff_patterns()

# Context Variables
ctx = ContextVariable()
ctx.set("task", "analysis")
ctx.update({"key": "value"})

# Swarm Router
router = SwarmRouter(hm)
next_agent = router.auto_route_by_role("researcher", ctx)
```

### Cognitive Game Engine

```python
from swarmmind import CognitiveGameEngine, CognitivePerspective, CognitiveMove

game = CognitiveGameEngine(max_rounds=5, voting_agents=40)
game.start_game("Should we adopt transformer architecture?")

move = CognitiveMove(
    agent_id="agent_1",
    perspective=CognitivePerspective.CRITICAL,
    content="Transformer attention mechanisms may be overkill for simple tasks",
    strength=0.8,
    round_number=1
)
game.add_move(move)

analysis = game.analyze_game()
```

### Result Object

```python
result = swarm.solve(task="Your task")

# Basic results
print(result.task)
print(result.solution)
print(result.rounds_completed)
print(result.execution_time)

# Consensus
print(result.consensus.final_position)
print(result.consensus.confidence)

# Cognitive game results
if result.cognitive_game_result:
    print(result.cognitive_game_result['total_moves'])
    print(result.cognitive_game_result['perspective_distribution'])

# Handoff statistics
if result.handoff_stats:
    print(result.handoff_stats['total_handoffs'])
    print(result.handoff_stats['unique_agents'])

# Agent info
print(result.agents)
print(result.memory_stats)
```



## Use Cases

### Autonomous AI Research

- generate research ideas through cognitive confrontation
- design experiments with multiple perspectives
- analyze results with critics and synthesizers

### Collaborative Coding

- design architecture with logical planners
- write code with pragmatic coders
- review implementations with analytical reviewers
- detect bugs through critical challenges

### Complex Problem Solving

- planning with multi-perspective analysis
- strategy through cognitive gaming
- system design with creative synthesis

### Creative Collaboration

- storytelling with creative perspectives
- brainstorming through cognitive confrontation
- design concepts with multi-perspective voting



## Roadmap

Planned features:

- [ ] LLM integration layer (OpenAI, Anthropic, local models)
- [ ] Swarm visualization dashboard
- [ ] Distributed swarm execution
- [ ] Persistence and checkpointing
- [ ] WebSocket-based live progress
- [ ] Swarm knowledge graphs
- [ ] Autonomous research pipelines
- [ ] Multi-swarm coordination
- [ ] Cognitive perspective customization
- [ ] Interactive debate interface



## Contributing

SwarmMind welcomes contributions from:

- add new cognitive perspectives
- improve agent coordination algorithms
- build visualization tools
- optimize performance
- write tutorials

Feel free to open an **Issue** or submit a **Pull Request**.



## License

MIT License - see [LICENSE](LICENSE) for details.



## Star History

If you like this project, please ⭐ star the repo.

<p align="center">

<a href="https://star-history.com/#Yuan-ManX/SwarmMind&Date">
 <img src="https://api.star-history.com/svg?repos=Yuan-ManX/SwarmMind&type=Date" />
</a>

</p>
</div>
