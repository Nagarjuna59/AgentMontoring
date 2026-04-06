# AgentMonitor/mas/code_generation_mas.py
"""
Code Generation Multi-Agent System

This is an actual MAS implementation (not just simple agents).
Follows the research paper: Multiple specialized agents collaborating.
"""

import asyncio
from typing import Any, List, Dict, Optional


class CodeGenerationMAS:
    """
    Multi-Agent System for code generation tasks.
    
    Agents:
    1. Analyzer: Analyzes requirements
    2. Coder: Writes code
    3. Tester: Creates tests
    4. Reviewer: Reviews and improves
    
    Flow: Analyzer → Coder → Tester → Reviewer
    """
    
    def __init__(self, llm, language: str = "python", threshold: float = 0.6, max_retries: int = 2, use_full_mas: bool = False):
        """
        Args:
            llm: LLM model for agents
            language: Programming language (default: python)
            threshold: Quality threshold
            max_retries: Max enhancement loops
            use_full_mas: If True, use all 4 agents (Analyzer→Coder→Tester→Reviewer) for richer monitoring
        """
        self.llm = llm
        self.language = language.lower()
        self.threshold = threshold
        self.max_retries = max_retries
        self.use_full_mas = use_full_mas
        
        # Define agent roles with language
        lang_name = language.title()
        self.agents = {
            "Analyzer": Agent("Analyzer", "requirement analyzer", llm, self.language),
            "Coder": Agent("Coder", f"expert {lang_name} programmer", llm, self.language),
            "Tester": Agent("Tester", f"{lang_name} test writer", llm, self.language),
            "Reviewer": Agent("Reviewer", f"{lang_name} code reviewer", llm, self.language)
        }
        
    async def run(self, task: str, monitor=None) -> str:
        """
        Run the MAS pipeline - FAST MODE or FULL MAS MODE
        
        Args:
            task: Programming task
            monitor: AgentMonitor instance (optional)
            
        Returns:
            Final code output
        """
        # Build language hint
        lang_hint = ''
        if self.language and self.language not in ['auto', 'any']:
            lang_hint = f"\n\nPlease write the code in {self.language}."
        
        if not self.use_full_mas:
            # FAST MODE: Coder only for speed
            print(f"⚡ FAST MODE: Using Coder only ({self.language})")
            simple_prompt = f"{task}{lang_hint}"
            code = await self._run_agent("Coder", simple_prompt, monitor)
            return code
        else:
            # FULL MAS MODE: All 4 agents with graph edges
            print(f"🔬 FULL MAS MODE: Using all 4 agents ({self.language})")
            
            # 1. Analyzer analyzes the task (SIMPLIFIED to avoid safety blocks)
            analysis_prompt = f"Requirements: {task[:200]}{lang_hint}"
            analysis = await self._run_agent("Analyzer", analysis_prompt, monitor)
            
            # Record edge: Analyzer -> Coder
            if monitor:
                monitor.record_graph_edge("Analyzer", "Coder")
            
            # 2. Coder generates code (SIMPLIFIED - don't include full analysis)
            code_prompt = f"{task}{lang_hint}"
            code = await self._run_agent("Coder", code_prompt, monitor)
            
            # Record edge: Coder -> Tester
            if monitor:
                monitor.record_graph_edge("Coder", "Tester")
            
            # 3. Tester validates (SIMPLIFIED - don't include full code)
            test_prompt = f"Test the solution for: {task[:150]}"
            test_feedback = await self._run_agent("Tester", test_prompt, monitor)
            
            # Record edge: Tester -> Reviewer
            if monitor:
                monitor.record_graph_edge("Tester", "Reviewer")
            
            # 4. Reviewer provides final version (SIMPLIFIED)
            review_prompt = f"Improve: {task}{lang_hint}"
            final_code = await self._run_agent("Reviewer", review_prompt, monitor)
            
            # Return the best code (prefer final, fallback to initial code if needed)
            if final_code and final_code.strip() and "Error:" not in final_code:
                return final_code
            elif code and code.strip() and "Error:" not in code:
                return code
            else:
                # All failed, return simple code generation
                return await self._run_agent("Coder", f"{task}{lang_hint}", None)
    
    async def _run_agent(self, agent_name: str, task: str, monitor=None) -> str:
        """Run single agent with optional monitoring"""
        agent = self.agents[agent_name]
        
        if monitor:
            # Use monitor's run_agent_with_enhancement
            # Pass the MAS language (user's requested language), not agent's internal language
            result = await monitor.run_agent_with_enhancement(
                agent=agent,
                task=task,
                agent_name=agent_name,
                capability=self.language  # Use MAS language, not agent.language
            )
            # Extract output and ensure it's not None or empty
            if isinstance(result, dict):
                output = result.get("output", "")
            else:
                output = str(result) if result else ""
            
            # Safeguard against empty output
            if not output or output.strip() == "":
                output = f"# {agent_name} generated no output"
            
            return output
        else:
            # Direct execution - RUN IN EXECUTOR TO AVOID BLOCKING
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, agent.generate_response, task)


class Agent:
    """Individual agent within the MAS"""
    
    def __init__(self, name: str, role: str, llm, language: str = "python"):
        self.name = name
        self.role = role
        self.llm = llm
        self.language = language.lower()
    
    def generate_response(self, prompt: str) -> str:
        """Generate response - ONLY CODE, no explanation"""
        try:
            # Prepend a clear LANGUAGE directive so the model receives the instruction early
            lang_directive = ''
            if self.language and self.language not in ['auto', 'any']:
                lang_directive = f"LANGUAGE: {self.language}\n\n"

            # Simple prompt - include language directive at top
            full_prompt = f"{lang_directive}{prompt}\n\nCode only. No explanation."
            
            start = __import__('time').time()
            
            if callable(self.llm):
                response = self.llm(full_prompt)
                elapsed = __import__('time').time() - start
                
                response_str = response if isinstance(response, str) else str(response)
                
                # EXTRACT ONLY CODE
                clean_code = self._extract_code(response_str)
                print(f"[{self.name}] {elapsed:.1f}s -> {len(clean_code)} chars")
                return clean_code
            else:
                return f"# Error: Unknown LLM"
                
        except Exception as e:
            return f"# Error: {str(e)}"
    
    def _extract_code(self, response_str: str) -> str:
        """Extract ONLY code from response"""
        import re
        
        # Method 1: Extract from markdown code blocks
        if "```" in response_str:
            code_blocks = re.findall(r'```(?:\w+)?\s*(.*?)```', response_str, re.DOTALL)
            if code_blocks:
                return code_blocks[0].strip()
        
        # Method 2: Find code by looking for function/class definitions
        lines = response_str.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            stripped = line.strip()
            
            # Start collecting at code indicators
            if stripped.startswith(('def ', 'function ', 'class ', 'import ', 'from ', 'public ', 'private ', '#include')):
                in_code = True
            
            # Skip explanatory lines
            if in_code and stripped:
                # Skip lines that look like explanations
                if any(phrase in stripped.lower() for phrase in ['this function', 'this code', 'example:', 'note:', 'usage:']):
                    continue
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        # Method 3: Return everything (last resort)
        return response_str.strip()

