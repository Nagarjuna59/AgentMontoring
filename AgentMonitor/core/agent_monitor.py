# AgentMonitor/core/agent_monitor.py
"""
Core AgentMonitor class - Non-invasive monitoring wrapper for multi-agent systems.
Inspired by PEFT (Parameter-Efficient Fine-Tuning) design pattern.
"""

import asyncio
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
from functools import partial, wraps
import inspect


class AgentMonitor:
    """
    Non-invasive monitoring framework for multi-agent systems.
    
    Usage:
        monitor = AgentMonitor()
        await monitor.register(agent, agent.input_method, agent.output_method)
        # ... run your MAS ...
        monitor.save("output.json")
    """
    
    def __init__(self, name: str = "AgentMonitor", debug: bool = False):
        self.name = name
        self.debug = debug
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.graph_edges: List[Tuple[str, str]] = []
        self.start_time: Optional[float] = None
        self.metadata: Dict[str, Any] = {}
        
    async def register(
        self,
        agent_obj: Any,
        input_func: Callable,
        output_func: Callable,
        state_func: Optional[Callable] = None,
        context_in_str: Optional[str] = None,
        prompt: Optional[str] = None,
        name: Optional[str] = None,
        capability: Optional[str] = None,
        use_partial: bool = False,
        **kwargs
    ) -> None:
        """
        Register an agent for monitoring (non-invasive).
        
        Args:
            agent_obj: The agent instance
            input_func: Method that receives messages (e.g., put_message)
            output_func: Method that generates responses (e.g., act, _act)
            state_func: Optional method to check agent state
            context_in_str: Attribute path for agent context (e.g., "rc.memory")
            prompt: Agent's role prompt/template
            name: Agent name (auto-detected if None)
            capability: LLM capability (e.g., "gpt-4", "llama3-70b", "llama3-8b")
            use_partial: Use functools.partial for wrapping
            **kwargs: Additional metadata
        """
        agent_name = name or self._infer_agent_name(agent_obj)
        
        if agent_name in self.agents:
            print(f"[WARNING] Agent '{agent_name}' already registered. Skipping.")
            return
            
        # Store agent metadata
        self.agents[agent_name] = {
            "obj": agent_obj,
            "name": agent_name,
            "input_func_name": input_func.__name__,
            "output_func_name": output_func.__name__,
            "state_func": state_func,
            "context_path": context_in_str,
            "prompt_template": prompt,
            "capability": capability or "unknown",
            "inputs": [],
            "outputs": [],
            "timestamps": [],
            "token_counts": [],
            "latencies": [],
            "metadata": kwargs
        }
        
        # Wrap input function
        if asyncio.iscoroutinefunction(input_func):
            wrapped_input = self._wrap_async_input(agent_name, input_func)
        else:
            wrapped_input = self._wrap_sync_input(agent_name, input_func)
            
        # Wrap output function
        if asyncio.iscoroutinefunction(output_func):
            wrapped_output = self._wrap_async_output(agent_name, output_func)
        else:
            wrapped_output = self._wrap_sync_output(agent_name, output_func)
        
        # Replace methods on agent object (non-invasive monkey-patching)
        setattr(agent_obj, input_func.__name__, wrapped_input)
        setattr(agent_obj, output_func.__name__, wrapped_output)
        
        if self.debug:
            print(f"[Monitor] Registered agent: {agent_name}")
            print(f"  - Input: {input_func.__name__}")
            print(f"  - Output: {output_func.__name__}")
            print(f"  - Capability: {capability}")
    
    def _infer_agent_name(self, agent_obj: Any) -> str:
        """Infer agent name from object attributes."""
        if hasattr(agent_obj, 'name'):
            return agent_obj.name
        elif hasattr(agent_obj, 'profile'):
            return agent_obj.profile
        elif hasattr(agent_obj, '__class__'):
            return agent_obj.__class__.__name__
        else:
            return f"Agent_{id(agent_obj)}"
    
    def _wrap_sync_input(self, agent_name: str, original_func: Callable) -> Callable:
        """Wrap synchronous input function."""
        @wraps(original_func)
        def wrapped(*args, **kwargs):
            # Record input
            self._log_input(agent_name, args, kwargs)
            
            # Call original
            result = original_func(*args, **kwargs)
            
            return result
        return wrapped
    
    def _wrap_async_input(self, agent_name: str, original_func: Callable) -> Callable:
        """Wrap asynchronous input function."""
        @wraps(original_func)
        async def wrapped(*args, **kwargs):
            # Record input
            self._log_input(agent_name, args, kwargs)
            
            # Call original
            result = await original_func(*args, **kwargs)
            
            return result
        return wrapped
    
    def _wrap_sync_output(self, agent_name: str, original_func: Callable) -> Callable:
        """Wrap synchronous output function."""
        @wraps(original_func)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            
            # Call original
            result = original_func(*args, **kwargs)
            
            # Record output
            latency = time.time() - start_time
            self._log_output(agent_name, result, latency)
            
            return result
        return wrapped
    
    def _wrap_async_output(self, agent_name: str, original_func: Callable) -> Callable:
        """Wrap asynchronous output function."""
        @wraps(original_func)
        async def wrapped(*args, **kwargs):
            start_time = time.time()
            
            # Call original
            result = await original_func(*args, **kwargs)
            
            # Record output
            latency = time.time() - start_time
            self._log_output(agent_name, result, latency)
            
            return result
        return wrapped
    
    def _log_input(self, agent_name: str, args: tuple, kwargs: dict) -> None:
        """Log input to agent."""
        timestamp = time.time()
        
        # Extract message content
        message_content = self._extract_message_content(args, kwargs)
        
        self.agents[agent_name]["inputs"].append({
            "timestamp": timestamp,
            "content": message_content,
            "args": str(args)[:200],  # Truncate for storage
            "kwargs": {k: str(v)[:100] for k, v in kwargs.items()}
        })
        
        # Track conversation
        self.conversation_history.append({
            "timestamp": timestamp,
            "agent": agent_name,
            "type": "input",
            "content": message_content
        })
    
    def _log_output(self, agent_name: str, result: Any, latency: float) -> None:
        """Log output from agent."""
        timestamp = time.time()
        
        # Extract output content
        output_content = self._extract_output_content(result)
        
        # Estimate tokens (rough heuristic)
        token_count = len(str(output_content).split())
        
        self.agents[agent_name]["outputs"].append({
            "timestamp": timestamp,
            "content": output_content,
            "result": str(result)[:200]  # Truncate
        })
        self.agents[agent_name]["latencies"].append(latency)
        self.agents[agent_name]["timestamps"].append(timestamp)
        self.agents[agent_name]["token_counts"].append(token_count)
        
        # Track conversation
        self.conversation_history.append({
            "timestamp": timestamp,
            "agent": agent_name,
            "type": "output",
            "content": output_content,
            "latency": latency
        })
        
        # Track graph edge (agent communication)
        if len(self.conversation_history) >= 2:
            prev_agent = self.conversation_history[-2]["agent"]
            if prev_agent != agent_name:
                edge = (prev_agent, agent_name)
                if edge not in self.graph_edges:
                    self.graph_edges.append(edge)
    
    def _extract_message_content(self, args: tuple, kwargs: dict) -> str:
        """Extract message content from function arguments."""
        # Try common patterns
        if args and len(args) > 0:
            first_arg = args[0]
            if hasattr(first_arg, 'content'):
                return str(first_arg.content)
            elif isinstance(first_arg, str):
                return first_arg
            elif isinstance(first_arg, dict) and 'content' in first_arg:
                return first_arg['content']
        
        if 'message' in kwargs:
            msg = kwargs['message']
            if hasattr(msg, 'content'):
                return str(msg.content)
            return str(msg)
        
        if 'content' in kwargs:
            return str(kwargs['content'])
        
        return str(args)[:100] if args else ""
    
    def _extract_output_content(self, result: Any) -> str:
        """Extract output content from function result."""
        if hasattr(result, 'content'):
            return str(result.content)
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)[:200]
    
    def get_agent_names(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self.agents.keys())
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get full conversation history."""
        return self.conversation_history
    
    def get_graph_edges(self) -> List[Tuple[str, str]]:
        """Get communication graph edges."""
        return self.graph_edges
    
    def get_agent_stats(self, agent_name: str) -> Dict[str, Any]:
        """Get statistics for a specific agent."""
        if agent_name not in self.agents:
            return {}
        
        agent = self.agents[agent_name]
        return {
            "name": agent_name,
            "capability": agent["capability"],
            "num_inputs": len(agent["inputs"]),
            "num_outputs": len(agent["outputs"]),
            "avg_latency": sum(agent["latencies"]) / len(agent["latencies"]) if agent["latencies"] else 0,
            "total_tokens": sum(agent["token_counts"]),
            "avg_tokens": sum(agent["token_counts"]) / len(agent["token_counts"]) if agent["token_counts"] else 0
        }
    
    def save(self, filepath: str, task_instruction: Optional[str] = None) -> None:
        """Save monitoring data to JSON file."""
        output = {
            "monitor_name": self.name,
            "timestamp": datetime.now().isoformat(),
            "task_instruction": task_instruction,
            "agents": {
                name: {
                    "name": name,
                    "capability": agent["capability"],
                    "prompt_template": agent["prompt_template"],
                    "num_interactions": len(agent["outputs"]),
                    "inputs": agent["inputs"],
                    "outputs": agent["outputs"],
                    "latencies": agent["latencies"],
                    "token_counts": agent["token_counts"],
                    "metadata": agent["metadata"]
                }
                for name, agent in self.agents.items()
            },
            "conversation_history": self.conversation_history,
            "graph_edges": self.graph_edges,
            "metadata": self.metadata
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        if self.debug:
            print(f"[Monitor] Saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load monitoring data from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.name = data.get("monitor_name", "AgentMonitor")
        self.conversation_history = data.get("conversation_history", [])
        self.graph_edges = [tuple(e) for e in data.get("graph_edges", [])]
        self.metadata = data.get("metadata", {})
        
        if self.debug:
            print(f"[Monitor] Loaded from {filepath}")
    
    def reset(self) -> None:
        """Reset monitoring state (keep agent registrations)."""
        for agent_name in self.agents:
            self.agents[agent_name]["inputs"] = []
            self.agents[agent_name]["outputs"] = []
            self.agents[agent_name]["timestamps"] = []
            self.agents[agent_name]["token_counts"] = []
            self.agents[agent_name]["latencies"] = []
        
        self.conversation_history = []
        self.graph_edges = []
        self.metadata = {}
        
        if self.debug:
            print("[Monitor] Reset complete")
    
    def __repr__(self) -> str:
        return f"AgentMonitor(name='{self.name}', agents={len(self.agents)}, conversations={len(self.conversation_history)})"
