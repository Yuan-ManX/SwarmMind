"""
SwarmMind Quick Start Script
Run a simple swarm reasoning experiment
"""

from swarmmind import Swarm, SwarmConfig, AgentRole


def main():
    print("Initializing SwarmMind...")
    print("=" * 50)

    config = SwarmConfig(
        name="DemoSwarm",
        max_rounds=3,
        agents_per_role=1,
        roles=[
            AgentRole.RESEARCHER,
            AgentRole.CRITIC,
            AgentRole.PLANNER,
            AgentRole.REVIEWER,
        ],
    )

    swarm = Swarm(config=config)

    task = "Design an efficient training strategy for a language model"

    print(f"Task: {task}")
    print("=" * 50)
    print("Starting swarm reasoning...")
    print()

    result = swarm.solve(task)

    print("=" * 50)
    print("SWARM REASONING COMPLETE")
    print("=" * 50)
    print()
    print(result.solution)
    print()
    print("=" * 50)
    print("Execution Statistics:")
    print(f"  Rounds completed: {result.rounds_completed}")
    print(f"  Execution time: {result.execution_time:.2f}s")
    print(f"  Agents in swarm: {len(result.agents)}")
    print(f"  Memory entries: {result.memory_stats['total_entries']}")
    if result.consensus:
        print(f"  Consensus confidence: {result.consensus.confidence:.2%}")
    print("=" * 50)


if __name__ == "__main__":
    main()
