# AgentMonitor/mas/mas_factory.py
"""
MAS Factory: Creates multiple MAS architecture variants

This generates 30-50 different MAS configurations by varying:
- Number of agents (2, 3, 4, 5)
- Agent roles
- Topology (sequential, parallel, hierarchical)
- Max enhancement loops
"""

from typing import List, Dict, Any
from .code_generation_mas import CodeGenerationMAS, Agent


class MASFactory:
    """Creates different MAS architecture variants"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def create_variants(self, count: int = 30) -> List[Dict[str, Any]]:
        """
        Create multiple MAS variants with different architectures
        
        Returns:
            List of MAS variant configs
        """
        variants = []
        
        # 2-agent variants
        variants.extend(self._create_2agent_variants())
        
        # 3-agent variants
        variants.extend(self._create_3agent_variants())
        
        # 4-agent variants
        variants.extend(self._create_4agent_variants())
        
        # 5-agent variants
        variants.extend(self._create_5agent_variants())
        
        # Return requested count
        return variants[:count]
    
    def _create_2agent_variants(self) -> List[Dict]:
        """2-agent MAS variants"""
        variants = []
        
        # Variant 1: Coder + Reviewer
        variants.append({
            "id": "2agent_coder_reviewer",
            "num_agents": 2,
            "agents": [
                {"name": "Coder", "role": "Python programmer"},
                {"name": "Reviewer", "role": "code reviewer"}
            ],
            "topology": "sequential",
            "max_loops": 1
        })
        
        # Variant 2: Planner + Executor
        variants.append({
            "id": "2agent_planner_executor",
            "num_agents": 2,
            "agents": [
                {"name": "Planner", "role": "requirement planner"},
                {"name": "Executor", "role": "code executor"}
            ],
            "topology": "sequential",
            "max_loops": 2
        })
        
        # Variant 3: Designer + Builder
        variants.append({
            "id": "2agent_designer_builder",
            "num_agents": 2,
            "agents": [
                {"name": "Designer", "role": "algorithm designer"},
                {"name": "Builder", "role": "code builder"}
            ],
            "topology": "sequential",
            "max_loops": 1
        })
        
        return variants
    
    def _create_3agent_variants(self) -> List[Dict]:
        """3-agent MAS variants"""
        variants = []
        
        # Variant 1: Analyzer + Coder + Tester
        variants.append({
            "id": "3agent_analyze_code_test",
            "num_agents": 3,
            "agents": [
                {"name": "Analyzer", "role": "requirement analyzer"},
                {"name": "Coder", "role": "Python developer"},
                {"name": "Tester", "role": "test writer"}
            ],
            "topology": "sequential",
            "max_loops": 1
        })
        
        # Variant 2: Planner + Developer + Reviewer
        variants.append({
            "id": "3agent_plan_dev_review",
            "num_agents": 3,
            "agents": [
                {"name": "Planner", "role": "solution planner"},
                {"name": "Developer", "role": "code developer"},
                {"name": "Reviewer", "role": "quality reviewer"}
            ],
            "topology": "sequential",
            "max_loops": 2
        })
        
        # Variant 3: Parallel coders
        variants.append({
            "id": "3agent_parallel_coders",
            "num_agents": 3,
            "agents": [
                {"name": "Coder1", "role": "approach 1 coder"},
                {"name": "Coder2", "role": "approach 2 coder"},
                {"name": "Coder3", "role": "approach 3 coder"}
            ],
            "topology": "parallel",
            "max_loops": 1
        })
        
        return variants
    
    def _create_4agent_variants(self) -> List[Dict]:
        """4-agent MAS variants"""
        variants = []
        
        # Variant 1: Full pipeline
        variants.append({
            "id": "4agent_full_pipeline",
            "num_agents": 4,
            "agents": [
                {"name": "Analyzer", "role": "requirement analyzer"},
                {"name": "Coder", "role": "expert Python programmer"},
                {"name": "Tester", "role": "unit test writer"},
                {"name": "Reviewer", "role": "code reviewer"}
            ],
            "topology": "sequential",
            "max_loops": 1
        })
        
        # Variant 2: With optimizer
        variants.append({
            "id": "4agent_with_optimizer",
            "num_agents": 4,
            "agents": [
                {"name": "Planner", "role": "solution planner"},
                {"name": "Coder", "role": "code writer"},
                {"name": "Optimizer", "role": "code optimizer"},
                {"name": "Validator", "role": "solution validator"}
            ],
            "topology": "sequential",
            "max_loops": 2
        })
        
        # Variant 3: Hierarchical
        variants.append({
            "id": "4agent_hierarchical",
            "num_agents": 4,
            "agents": [
                {"name": "Architect", "role": "system architect"},
                {"name": "Developer", "role": "developer"},
                {"name": "Tester", "role": "tester"},
                {"name": "Manager", "role": "project manager"}
            ],
            "topology": "hierarchical",
            "max_loops": 1
        })
        
        return variants
    
    def _create_5agent_variants(self) -> List[Dict]:
        """5-agent MAS variants"""
        variants = []
        
        # Variant 1: Extended pipeline
        variants.append({
            "id": "5agent_extended",
            "num_agents": 5,
            "agents": [
                {"name": "Analyzer", "role": "requirement analyzer"},
                {"name": "Designer", "role": "algorithm designer"},
                {"name": "Coder", "role": "code implementer"},
                {"name": "Tester", "role": "test creator"},
                {"name": "Reviewer", "role": "final reviewer"}
            ],
            "topology": "sequential",
            "max_loops": 1
        })
        
        # Variant 2: With debugger
        variants.append({
            "id": "5agent_with_debugger",
            "num_agents": 5,
            "agents": [
                {"name": "Planner", "role": "planner"},
                {"name": "Coder", "role": "coder"},
                {"name": "Tester", "role": "tester"},
                {"name": "Debugger", "role": "debugger"},
                {"name": "Optimizer", "role": "optimizer"}
            ],
            "topology": "sequential",
            "max_loops": 3
        })
        
        return variants
    
    def instantiate_mas(self, variant_config: Dict) -> 'SimpleMAS':
        """Create actual MAS instance from config"""
        
        # Create agent instances
        agents = []
        for agent_config in variant_config["agents"]:
            agent = Agent(
                name=agent_config["name"],
                role=agent_config["role"],
                llm=self.llm
            )
            agents.append(agent)
        
        # Create MAS
        mas = SimpleMAS(
            variant_id=variant_config["id"],
            agents=agents,
            topology=variant_config["topology"],
            max_loops=variant_config["max_loops"]
        )
        
        return mas


class SimpleMAS:
    """Simple MAS implementation that can have different architectures"""
    
    def __init__(self, variant_id: str, agents: List, topology: str, max_loops: int):
        self.variant_id = variant_id
        self.agents = agents
        self.topology = topology
        self.max_loops = max_loops
    
    async def run(self, task: str, monitor=None):
        """Run MAS with given topology"""
        
        if self.topology == "sequential":
            return await self._run_sequential(task, monitor)
        elif self.topology == "parallel":
            return await self._run_parallel(task, monitor)
        elif self.topology == "hierarchical":
            return await self._run_hierarchical(task, monitor)
        else:
            return await self._run_sequential(task, monitor)
    
    async def _run_sequential(self, task: str, monitor):
        """Sequential: A → B → C → D"""
        result = task
        
        for agent in self.agents:
            if monitor:
                output = await monitor.run_agent_with_enhancement(
                    agent=agent,
                    task=f"Previous: {result}\n\nYour task: {task}",
                    agent_name=agent.name,
                    capability="llama"
                )
                result = output.get("output", "") if isinstance(output, dict) else str(output)
            else:
                result = agent.generate_response(f"Task: {task}\nPrevious: {result}")
        
        return result
    
    async def _run_parallel(self, task: str, monitor):
        """Parallel: All agents run simultaneously"""
        import asyncio
        
        tasks = []
        for agent in self.agents:
            if monitor:
                tasks.append(monitor.run_agent_with_enhancement(
                    agent=agent,
                    task=task,
                    agent_name=agent.name,
                    capability="llama"
                ))
            else:
                tasks.append(asyncio.create_task(
                    asyncio.coroutine(lambda: agent.generate_response(task))()
                ))
        
        results = await asyncio.gather(*tasks)
        return "\n\n".join([str(r.get("output", r) if isinstance(r, dict) else r) for r in results])
    
    async def _run_hierarchical(self, task: str, monitor):
        """Hierarchical: Manager coordinates workers"""
        # First agent is manager
        manager = self.agents[0]
        workers = self.agents[1:]
        
        # Manager plans
        if monitor:
            plan = await monitor.run_agent_with_enhancement(
                agent=manager,
                task=f"Plan how to solve: {task}",
                agent_name=manager.name,
                capability="llama"
            )
            plan_text = plan.get("output", "") if isinstance(plan, dict) else str(plan)
        else:
            plan_text = manager.generate_response(f"Plan: {task}")
        
        # Workers execute
        results = []
        for worker in workers:
            if monitor:
                output = await monitor.run_agent_with_enhancement(
                    agent=worker,
                    task=f"Plan: {plan_text}\n\nExecute: {task}",
                    agent_name=worker.name,
                    capability="llama"
                )
                results.append(output.get("output", "") if isinstance(output, dict) else str(output))
            else:
                results.append(worker.generate_response(f"Plan: {plan_text}\nTask: {task}"))
        
        return "\n\n".join(results)
