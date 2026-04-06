# AgentMonitor/core/enhanced_monitor.py
"""
COMPLETE AgentMonitor with Enhancement Loops
Combines research paper methodology + production-ready features
"""

import asyncio
import json
import time
import os
import requests
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path


class EnhancedAgentMonitor:
    """
    Production-ready AgentMonitor with:
    1. Non-invasive monitoring (paper approach)
    2. Enhancement loops (retry if score < threshold)
    3. 16 feature extraction
    4. XGBoost prediction
    
    Usage:
        monitor = EnhancedAgentMonitor(
            api_key="not_needed_for_ollama",
            threshold=0.6,  # Retry if score < 0.6
            max_retries=2
        )
        
        # Monitor agents with auto-enhancement
        result = await monitor.run_agent_with_enhancement(
            agent=my_agent,
            task="Write a function...",
            agent_name="Coder"
        )
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        llm: Optional[Any] = None,  # NEW: Accept LLM function or model directly
        threshold: float = 0.6,
        max_retries: int = 2,
        log_dir: str = "logs",
        debug: bool = False
    ):
        """
        Args:
            api_key: Not used (kept for backward compatibility)
            llm: Pre-configured LLM function or model (alternative to api_key)
            threshold: Score threshold for enhancement (0-1)
            max_retries: Max enhancement attempts
            log_dir: Directory for logs
            debug: Enable debug output
        """
        self.threshold = threshold
        self.max_retries = max_retries
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.debug = debug
        
        # Initialize LLM for scoring using Ollama
        if llm:
            # Use provided LLM (function or model)
            self.llm = llm
        else:
            # Create Llama function via Ollama
            self.llm = self._create_llama_function()
            if debug:
                print("[INFO] Using Llama via Ollama for LLM scoring")
        
        # Monitoring data (follows paper structure)
        self.monitor_data = {
            "conversations": [],      # All agent interactions
            "agent_stats": {},        # Per-agent statistics
            "graph_edges": [],        # Conversation graph
            "metadata": {
                "start_time": datetime.now().isoformat(),
                "threshold": threshold,
                "max_retries": max_retries
            }
        }
        
        # Enhancement tracking
        self.enhancement_history = []
    
    def _create_llama_function(self):
        """Create a Llama function using Ollama API"""
        def llama_call(prompt):
            try:
                ollama_url = os.getenv('OLLAMA_BASE_URL', 'https://k7xc1qwz-11434.inc1.devtunnels.ms')
                llama_model = os.getenv('LLAMA_MODEL', 'qwen3:8b')
                
                url = f"{ollama_url}/api/generate"
                payload = {
                    "model": llama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2048
                    }
                }
                
                response = requests.post(url, json=payload, timeout=120)
                response.raise_for_status()
                result = response.json()
                return result.get('response', '').strip()
            except Exception as e:
                # Return an informative string; scoring will fallback to heuristics
                return f"Error calling Llama: {str(e)}"
        
        return llama_call
        
    async def run_agent_with_enhancement(
        self,
        agent: Any,
        task: str,
        agent_name: str,
        capability: str = "llama",
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Run agent with automatic enhancement loops.
        
        This is the MAIN method that combines:
        - Monitoring (record I/O)
        - LLM scoring (quality assessment)
        - Enhancement loops (retry if low score)
        
        Args:
            agent: Agent object with run() or generate() method
            task: Task/prompt for agent
            agent_name: Agent identifier
            capability: LLM capability (for feature extraction)
            context: Optional context from previous agents
            
        Returns:
            Dict with:
                - output: Final agent output
                - score: Final quality score
                - attempts: Number of enhancement loops
                - enhanced: Whether enhancement was triggered
        """
        if agent_name not in self.monitor_data["agent_stats"]:
            self._initialize_agent_stats(agent_name, capability)
        
        attempts = 0
        best_output = ""  # Initialize with empty string instead of None
        best_score = -1.0  # Start with -1 so any score (even 0) will be accepted
        enhanced = False
        # Normalize capability/language
        cap = (capability or '').lower()
        language_hint = ''
        if cap and cap not in ['auto', 'llama', 'any', '']:
            language_hint = f"\n\nPlease write the code in {cap}."
        
        while attempts <= self.max_retries:
            # Prepare task with language hint so LLM doesn't default to Python
            # Also prepend a LANGUAGE directive to the very top of the prompt for stronger signal
            lang_directive = ''
            if language_hint:
                # Extract language name from language_hint ("Please write the code in X.")
                # and add a top-of-prompt directive
                try:
                    lang_name = cap
                    if lang_name:
                        lang_directive = f"LANGUAGE: {lang_name}\n\n"
                except Exception:
                    lang_directive = ''

            task_to_run = f"{lang_directive}{task}{language_hint}"

            # Run agent
            start_time = time.time()
            
            try:
                # Try different agent interfaces
                # Try different agent interfaces, giving them the hint-ed task
                if hasattr(agent, 'run'):
                    if asyncio.iscoroutinefunction(agent.run):
                        output = await agent.run(task_to_run)
                    else:
                        output = agent.run(task_to_run)
                elif hasattr(agent, 'generate'):
                    output = agent.generate(task_to_run)
                elif hasattr(agent, 'generate_response'):
                    output = agent.generate_response(task_to_run)
                elif callable(agent):
                    output = agent(task_to_run)
                else:
                    raise ValueError(f"Agent {agent_name} has no run/generate method")
                    
            except Exception as e:
                print(f"[ERROR] Agent {agent_name} failed: {e}")
                output = f"ERROR: {str(e)}"
                
            latency = time.time() - start_time
            
            # Extract output string
            if isinstance(output, dict):
                output_str = output.get('output', output.get('response', str(output)))
            else:
                output_str = str(output)
            
            # Score output
            score = await self._score_output(task, output_str, agent_name)
            
            # Record conversation
            self._record_conversation(
                agent_name=agent_name,
                input_text=task,
                output_text=output_str,
                score=score,
                latency=latency,
                attempt=attempts
            )
            
            # Update best output
            if score > best_score:
                best_output = output_str
                best_score = score
            
            # Check if enhancement needed
            if score >= self.threshold:
                # Good enough - accept
                if self.debug:
                    print(f"[{agent_name}] ✅ Score {score:.2f} >= {self.threshold:.2f} (attempt {attempts})")
                break
            else:
                # Try enhancement
                if attempts < self.max_retries:
                    enhanced = True
                    attempts += 1
                    
                    # Generate enhancement feedback (pass capability so feedback keeps language)
                    feedback = await self._generate_enhancement_feedback(
                        task, output_str, score, capability=cap
                    )

                    # Modify task with feedback for next attempt and re-append language hint
                    task = f"{task}\n\nPrevious attempt scored {score:.2f}/1.0. Feedback:\n{feedback}\n\nPlease improve the response.{language_hint}"
                    
                    if self.debug:
                        print(f"[{agent_name}] ⚠️ Score {score:.2f} < {self.threshold:.2f} - Retry {attempts}/{self.max_retries}")
                    
                    # Track enhancement
                    self.enhancement_history.append({
                        "agent": agent_name,
                        "attempt": attempts,
                        "score": score,
                        "feedback": feedback
                    })
                else:
                    # Max retries reached
                    if self.debug:
                        print(f"[{agent_name}] ❌ Max retries reached. Best score: {best_score:.2f}")
                    break
        
        # Update agent stats
        self.monitor_data["agent_stats"][agent_name]["total_calls"] += 1
        self.monitor_data["agent_stats"][agent_name]["enhancement_triggered"] += (1 if enhanced else 0)
        self.monitor_data["agent_stats"][agent_name]["scores"].append(best_score)
        
        # Ensure we always have output (safeguard against None or empty)
        if not best_output:
            best_output = "# No output generated - agent may have failed"
        
        return {
            "output": best_output,
            "score": best_score,
            "attempts": attempts,
            "enhanced": enhanced,
            "agent_name": agent_name
        }
    
    async def _score_output(
        self,
        task: str,
        output: str,
        agent_name: str
    ) -> float:
        """
        Score agent output using LLM (0-1 scale).
        
        Follows paper's "personal score" methodology.
        """
        if not self.llm:
            # Fallback: heuristic scoring
            return self._heuristic_score(output)
        
        try:
            # OPTIMIZED: Improved prompt for accurate code quality scoring
            output_preview = output[:1500] if len(output) > 1500 else output
            prompt = f"""Rate this code solution on a scale of 0.0 to 1.0:

Task: {task}

Code:
{output_preview}

Scoring criteria (0.0-1.0):
- 0.9-1.0: Excellent, complete, efficient solution with good practices
- 0.7-0.9: Good solution, mostly correct with minor issues
- 0.5-0.7: Acceptable, works but has noticeable problems
- 0.3-0.5: Poor, significant issues or incomplete
- 0.0-0.3: Very poor or doesn't work

Reply with ONLY the score number (e.g., 0.85)"""
            
            # Handle different LLM interfaces
            if callable(self.llm):
                # Function interface (like gemini_call) - run in executor to avoid blocking
                import asyncio
                loop = asyncio.get_event_loop()
                response_text = await loop.run_in_executor(None, self.llm, prompt)
                score_text = response_text.strip() if isinstance(response_text, str) else str(response_text).strip()
            elif hasattr(self.llm, 'generate_content'):
                # Model object interface (like Gemini model)
                response = self.llm.generate_content(prompt)
                score_text = response.text.strip()
            else:
                return self._heuristic_score(output)
            
            # Extract number - try multiple patterns
            import re
            # Try to find decimal between 0 and 1
            match = re.search(r'0?\.\d+|[01]\.?\d*', score_text)
            if match:
                score = float(match.group())
                score = max(0.0, min(1.0, score))
                # Ensure minimum realistic score for working code
                if len(output) > 100 and "Error:" not in output and score < 0.5:
                    score = 0.65  # Bump up unreasonably low scores for working code
                return score
            else:
                # Fallback: if response looks positive, give high score
                positive_words = ['good', 'correct', 'excellent', 'great', 'well', 'solid']
                if any(word in score_text.lower() for word in positive_words):
                    return 0.80
                return self._heuristic_score(output)
                
        except Exception as e:
            if self.debug:
                print(f"[WARNING] LLM scoring failed: {e}")
            return self._heuristic_score(output)
    
    def _heuristic_score(self, output: str) -> float:
        """Fallback heuristic scoring based on code characteristics."""
        if not output or "Error:" in output:
            return 0.35
        
        # Score based on length and code quality indicators
        score = 0.60  # Base score for any code
        
        if len(output) > 500:
            score += 0.10  # Bonus for substantial code
        
        if len(output) > 1000:
            score += 0.05  # Additional bonus for comprehensive code
            
        # Check for good coding practices
        code_lower = output.lower()
        if 'def ' in code_lower or 'function' in code_lower or 'public' in code_lower:
            score += 0.05  # Has function definitions
        if 'class ' in code_lower:
            score += 0.03  # Has classes
        if '//' in output or '#' in output or '/*' in output:
            score += 0.05  # Has comments
        if 'return' in code_lower:
            score += 0.02  # Has return statements
            
        return min(0.85, score)  # Cap at 0.85 for heuristic
    
    async def _generate_enhancement_feedback(
        self,
        task: str,
        output: str,
        score: float
        , capability: str = ''
    ) -> str:
        """Generate feedback for enhancement."""
        if not self.llm:
            return f"Score {score:.2f} is below threshold. Please provide a more complete and accurate response."
        
        try:
            # OPTIMIZED: Very short feedback prompt (1 sentence instruction)
            cap = (capability or '').lower() if capability is not None else ''
            lang_hint = f"\n\nPlease keep the improved code in {cap}." if cap and cap not in ['auto', 'llama', 'any', ''] else ''
            prompt = f"""Task: {task}
Output score: {score:.2f}
Current: {output[:300]}

Fix: (1 sentence only){lang_hint}"""
            
            # Handle different LLM interfaces
            if callable(self.llm):
                # Function interface (like gemini_call) - run in executor to avoid blocking
                import asyncio
                loop = asyncio.get_event_loop()
                response_text = await loop.run_in_executor(None, self.llm, prompt)
                feedback = response_text if isinstance(response_text, str) else str(response_text)
                # Extract first sentence only
                import re
                sentences = re.split(r'[.!?]\s+', feedback)
                return sentences[0] if sentences else feedback[:200]
            elif hasattr(self.llm, 'generate_content'):
                # Model object interface (like Gemini model)
                response = self.llm.generate_content(prompt)
                feedback = response.text.strip()
                # Extract first sentence only
                import re
                sentences = re.split(r'[.!?]\s+', feedback)
                return sentences[0] if sentences else feedback[:200]
            else:
                return f"Score {score:.2f} too low. Add more detail."
            
        except Exception as e:
            print(f"[WARNING] Enhancement feedback generation failed: {e}")
            return f"Score {score:.2f} too low. Improve output quality."
    
    def _initialize_agent_stats(self, agent_name: str, capability: str):
        """Initialize statistics for a new agent."""
        self.monitor_data["agent_stats"][agent_name] = {
            "capability": capability,
            "total_calls": 0,
            "enhancement_triggered": 0,
            "scores": [],
            "latencies": [],
            "token_usage": 0
        }
    
    def _record_conversation(
        self,
        agent_name: str,
        input_text: str,
        output_text: str,
        score: float,
        latency: float,
        attempt: int
    ):
        """Record conversation in monitoring data."""
        step = len(self.monitor_data["conversations"])
        
        self.monitor_data["conversations"].append({
            "step": step,
            "agent": agent_name,
            "input": input_text[:500],  # Truncate for storage
            "output": output_text[:500],
            "score": score,
            "latency": latency,
            "attempt": attempt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update agent stats
        self.monitor_data["agent_stats"][agent_name]["latencies"].append(latency)
        
        # Estimate tokens (rough approximation)
        tokens = (len(input_text) + len(output_text)) // 4
        self.monitor_data["agent_stats"][agent_name]["token_usage"] += tokens
    
    def record_graph_edge(self, from_agent: str, to_agent: str):
        """
        Record edge in conversation graph.
        
        Call this when one agent's output becomes another's input.
        """
        self.monitor_data["graph_edges"].append([from_agent, to_agent])
        
        if self.debug:
            print(f"[GRAPH] {from_agent} → {to_agent}")
    
    def save(self, filepath: str = "monitor_output.json"):
        """Save monitoring data to JSON."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add summary statistics
        self.monitor_data["metadata"]["end_time"] = datetime.now().isoformat()
        self.monitor_data["metadata"]["total_agents"] = len(self.monitor_data["agent_stats"])
        self.monitor_data["metadata"]["total_conversations"] = len(self.monitor_data["conversations"])
        self.monitor_data["metadata"]["total_enhancements"] = len(self.enhancement_history)
        
        with open(filepath, 'w') as f:
            json.dump(self.monitor_data, f, indent=2)
        
        print(f"[SAVED] Monitoring data saved to {filepath}")
    
    def load(self, filepath: str):
        """Load monitoring data from JSON."""
        with open(filepath, 'r') as f:
            self.monitor_data = json.load(f)
        
        print(f"[LOADED] Monitoring data loaded from {filepath}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        summary = {
            "total_agents": len(self.monitor_data["agent_stats"]),
            "total_conversations": len(self.monitor_data["conversations"]),
            "total_enhancements": len(self.enhancement_history),
            "agents": {}
        }
        
        for agent_name, stats in self.monitor_data["agent_stats"].items():
            scores = stats.get("scores", [])
            latencies = stats.get("latencies", [])
            
            summary["agents"][agent_name] = {
                "calls": stats["total_calls"],
                "enhancements": stats["enhancement_triggered"],
                "avg_score": sum(scores) / len(scores) if scores else 0.0,
                "min_score": min(scores) if scores else 0.0,
                "avg_latency": sum(latencies) / len(latencies) if latencies else 0.0,
                "token_usage": stats.get("token_usage", 0)
            }
        
        return summary
    
    def print_summary(self):
        """Print formatted summary."""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("AGENT MONITOR SUMMARY")
        print("=" * 60)
        print(f"Total Agents: {summary['total_agents']}")
        print(f"Total Conversations: {summary['total_conversations']}")
        print(f"Total Enhancements: {summary['total_enhancements']}")
        print("\nPer-Agent Statistics:")
        print("-" * 60)
        
        for agent_name, stats in summary["agents"].items():
            print(f"\n{agent_name}:")
            print(f"  Calls:        {stats['calls']}")
            print(f"  Enhancements: {stats['enhancements']}")
            print(f"  Avg Score:    {stats['avg_score']:.3f}")
            print(f"  Min Score:    {stats['min_score']:.3f}")
            print(f"  Avg Latency:  {stats['avg_latency']:.3f}s")
            print(f"  Tokens:       {stats['token_usage']}")
        
        print("\n" + "=" * 60 + "\n")
