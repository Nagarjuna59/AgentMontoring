# AgentMonitor/core/agent_wrapper.py
"""
Agent Wrapper for simplified agent creation and registration.
"""

from typing import Any, Callable, Dict, Optional


class AgentWrapper:
    """
    Wrapper class for agents to simplify monitoring integration.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        llm: Optional[Any] = None,
        capability: str = "unknown"
    ):
        """
        Args:
            name: Agent name
            role: Agent role/profile
            llm: LLM instance
            capability: LLM capability descriptor
        """
        self.name = name
        self.role = role
        self.llm = llm
        self.capability = capability
        self.message_history: list = []
        
    def receive_message(self, message: Any) -> None:
        """
        Receive and store a message.
        """
        self.message_history.append({
            'type': 'input',
            'content': str(message)
        })
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate response using LLM.
        """
        if self.llm is None:
            response = f"[{self.name}] Placeholder response for: {prompt[:50]}..."
        else:
            try:
                response = self.llm.generate_content(prompt).strip()
            except Exception as e:
                response = f"[{self.name}] Error: {e}"
        
        self.message_history.append({
            'type': 'output',
            'content': response
        })
        
        return response
    
    def get_context(self) -> str:
        """Get conversation context."""
        return "\n".join([f"{m['type']}: {m['content']}" for m in self.message_history])
    
    def reset(self) -> None:
        """Reset agent state."""
        self.message_history = []
    
    def __repr__(self) -> str:
        return f"AgentWrapper(name='{self.name}', role='{self.role}', capability='{self.capability}')"
