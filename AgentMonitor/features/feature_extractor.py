# AgentMonitor/features/feature_extractor.py
"""
Feature Extraction for Multi-Agent Systems.
Implements indicators from the AgentMonitor paper:
1. LLM-judged scores (personal, collective)
2. Graph-based indicators (topology metrics)
3. Agent capability encoding
"""

import networkx as nx
import math
import json
from typing import Dict, List, Tuple, Any, Optional


class FeatureExtractor:
    """
    Extract features from monitored MAS data for prediction.
    """
    
    def __init__(self, llm_judge: Optional[Any] = None):
        """
        Args:
            llm_judge: LLM instance for judging agent scores (optional)
        """
        self.llm_judge = llm_judge
    
    def extract_all_features(
        self,
        monitor_data: Dict[str, Any],
        agent_prompts: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        """
        Extract all features from monitor data.
        
        Returns dict with keys:
            - System metrics (6): avg_personal_score, min_personal_score, max_loops,
              total_latency, total_token_usage, num_agents_triggered
            - Graph metrics (9): num_nodes, num_edges, clustering, transitivity,
              avg_degree/betweenness/closeness, pagerank_entropy, heterogeneity
            - Collective score (1): collective_score
        Total: 16 features
        """
        features = {}
        
        # Extract agents and edges
        agents_data = monitor_data.get("agents", {})
        edges = monitor_data.get("graph_edges", [])
        conversation = monitor_data.get("conversation_history", [])
        
        # 1. LLM-judged scores (personal and collective)
        personal_scores = self._compute_personal_scores(agents_data, agent_prompts)
        collective_score = self._compute_collective_score(agents_data, conversation)
        
        # 2. System-level features
        system_features = self._extract_system_features(agents_data, personal_scores)
        
        # 3. Graph-based features
        graph_features = self._extract_graph_features(edges, list(agents_data.keys()))
        
        # Combine all
        features.update(system_features)
        features.update(graph_features)
        features["collective_score"] = collective_score
        
        return features
    
    def _compute_personal_scores(
        self,
        agents_data: Dict[str, Any],
        agent_prompts: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        """
        Compute personal score for each agent using LLM judge.
        Personal score: How well the agent completes its assigned task.
        """
        scores = {}
        
        if not self.llm_judge:
            # Fallback: heuristic scoring
            for agent_name, agent in agents_data.items():
                # Simple heuristic: based on number of interactions and avg latency
                num_outputs = len(agent.get("outputs", []))
                avg_latency = sum(agent.get("latencies", [0])) / max(len(agent.get("latencies", [1])), 1)
                
                # Normalize (higher outputs = better, lower latency = better)
                score = min(1.0, num_outputs / 10.0) * (1.0 / (1.0 + avg_latency / 10.0))
                scores[agent_name] = max(0.0, min(1.0, score))
            return scores
        
        # LLM-based scoring
        for agent_name, agent in agents_data.items():
            prompt_template = agent.get("prompt_template", "")
            outputs = agent.get("outputs", [])
            
            if not outputs:
                scores[agent_name] = 0.5  # Neutral if no activity
                continue
            
            # Sample recent outputs
            recent_outputs = outputs[-3:] if len(outputs) > 3 else outputs
            output_text = "\n".join([str(o.get("content", "")) for o in recent_outputs])
            
            judge_prompt = f"""
You are evaluating an agent's performance on its assigned task.

Agent Role: {agent_name}
Task Description: {prompt_template}

Agent's Recent Outputs:
{output_text}

Rate how well this agent completed its specific task on a scale of 0.0 to 1.0.
Consider:
- Task completion
- Output quality
- Relevance to role

Return ONLY a JSON object: {{"personal_score": <float>}}
"""
            
            try:
                # Use provided llm_judge if available; accept callable or model-like
                if self.llm_judge and callable(self.llm_judge):
                    response = self.llm_judge(judge_prompt).strip()
                elif self.llm_judge and hasattr(self.llm_judge, 'generate_content'):
                    response = self.llm_judge.generate_content(judge_prompt).strip()
                else:
                    raise RuntimeError("No llm_judge available")

                response = self._extract_json(response)
                parsed = json.loads(response)
                score = float(parsed.get("personal_score", 0.5))
                scores[agent_name] = max(0.0, min(1.0, score))
            except Exception as e:
                print(f"[WARNING] Personal score for {agent_name} failed: {e}")
                scores[agent_name] = 0.5
        
        return scores
    
    def _compute_collective_score(
        self,
        agents_data: Dict[str, Any],
        conversation: List[Dict[str, Any]]
    ) -> float:
        """
        Compute collective score: How well agents contribute to overall system goal.
        """
        if not self.llm_judge:
            # Fallback: heuristic based on interaction diversity
            unique_agents = set(c.get("agent", "") for c in conversation)
            interaction_count = len(conversation)
            
            # More diverse interactions = better
            score = len(unique_agents) / max(len(agents_data), 1) * min(1.0, interaction_count / 20.0)
            return max(0.0, min(1.0, score))
        
        # LLM-based collective scoring
        # Summarize conversation
        conversation_summary = []
        for entry in conversation[-10:]:  # Last 10 interactions
            agent = entry.get("agent", "Unknown")
            content = str(entry.get("content", ""))[:100]
            conversation_summary.append(f"{agent}: {content}")
        
        summary_text = "\n".join(conversation_summary)
        
        judge_prompt = f"""
You are evaluating how well agents in a multi-agent system collaborate toward a common goal.

Recent Conversation:
{summary_text}

Rate the collective collaboration quality on a scale of 0.0 to 1.0.
Consider:
- Information flow between agents
- Contribution to final goal
- Coordination effectiveness

Return ONLY a JSON object: {{"collective_score": <float>}}
"""
        
        try:
            if self.llm_judge and callable(self.llm_judge):
                response = self.llm_judge(judge_prompt).strip()
            elif self.llm_judge and hasattr(self.llm_judge, 'generate_content'):
                response = self.llm_judge.generate_content(judge_prompt).strip()
            else:
                raise RuntimeError("No llm_judge available")

            response = self._extract_json(response)
            parsed = json.loads(response)
            score = float(parsed.get("collective_score", 0.5))
            return max(0.0, min(1.0, score))
        except Exception as e:
            print(f"[WARNING] Collective score failed: {e}")
            return 0.5
    
    def _extract_system_features(
        self,
        agents_data: Dict[str, Any],
        personal_scores: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Extract system-level features (6 metrics).
        """
        all_latencies = []
        all_tokens = []
        all_loops = []  # Approximation: num of outputs per agent
        
        for agent in agents_data.values():
            all_latencies.extend(agent.get("latencies", []))
            all_tokens.extend(agent.get("token_counts", []))
            all_loops.append(len(agent.get("outputs", [])))
        
        scores_list = list(personal_scores.values())
        
        return {
            "avg_personal_score": sum(scores_list) / len(scores_list) if scores_list else 0.0,
            "min_personal_score": min(scores_list) if scores_list else 0.0,
            "max_loops": max(all_loops) if all_loops else 0,
            "total_latency": sum(all_latencies),
            "total_token_usage": sum(all_tokens),
            "num_agents_triggered_enhancement": sum(1 for loops in all_loops if loops > 1)
        }
    
    def _extract_graph_features(
        self,
        edges: List[Tuple[str, str]],
        agent_names: List[str]
    ) -> Dict[str, float]:
        """
        Extract graph-based features (9 metrics).
        """
        if not agent_names:
            return self._empty_graph_features()
        
        # Build directed graph
        G = nx.DiGraph()
        G.add_nodes_from(agent_names)
        G.add_edges_from(edges)
        
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        
        # Convert to undirected for some metrics
        G_undirected = G.to_undirected()
        
        # Clustering and transitivity
        clustering = nx.average_clustering(G_undirected) if num_nodes > 1 else 0.0
        transitivity = nx.transitivity(G_undirected) if num_nodes > 2 else 0.0
        
        # Centrality metrics
        degree_centrality = nx.degree_centrality(G) if num_nodes > 0 else {}
        betweenness = nx.betweenness_centrality(G) if num_nodes > 0 else {}
        closeness = nx.closeness_centrality(G) if num_nodes > 1 else {}
        
        avg_degree = sum(degree_centrality.values()) / num_nodes if num_nodes > 0 else 0.0
        avg_betweenness = sum(betweenness.values()) / num_nodes if num_nodes > 0 else 0.0
        avg_closeness = sum(closeness.values()) / num_nodes if num_nodes > 0 else 0.0
        
        # PageRank
        pagerank = nx.pagerank(G) if num_nodes > 0 and num_edges > 0 else {n: 1/num_nodes for n in agent_names}
        
        # PageRank entropy (information diversity)
        pr_values = list(pagerank.values())
        pagerank_entropy = -sum(p * math.log(p, 2) for p in pr_values if p > 0) if pr_values else 0.0
        
        # Heterogeneity score (variance in PageRank)
        mean_pr = sum(pr_values) / len(pr_values) if pr_values else 0.0
        heterogeneity = sum((p - mean_pr) ** 2 for p in pr_values) / len(pr_values) if pr_values else 0.0
        
        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "clustering_coefficient": clustering,
            "transitivity": transitivity,
            "avg_degree_centrality": avg_degree,
            "avg_betweenness_centrality": avg_betweenness,
            "avg_closeness_centrality": avg_closeness,
            "pagerank_entropy": pagerank_entropy,
            "heterogeneity_score": heterogeneity
        }
    
    def _empty_graph_features(self) -> Dict[str, float]:
        """Return zero graph features when no agents."""
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "clustering_coefficient": 0.0,
            "transitivity": 0.0,
            "avg_degree_centrality": 0.0,
            "avg_betweenness_centrality": 0.0,
            "avg_closeness_centrality": 0.0,
            "pagerank_entropy": 0.0,
            "heterogeneity_score": 0.0
        }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown code blocks."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    
    def encode_agent_capability(self, capability: str) -> float:
        """
        Encode agent capability as a numeric feature.
        Based on known LLM model strengths.
        """
        capability_lower = capability.lower()
        
        # Capability mapping (higher = more capable)
        if "gpt-4" in capability_lower or "claude-3" in capability_lower:
            return 3.0
        elif "gpt-3.5" in capability_lower or "gemini" in capability_lower or "llama" in capability_lower:
            return 2.0
        elif "70b" in capability_lower or "65b" in capability_lower:
            return 2.5
        elif "13b" in capability_lower or "8b" in capability_lower:
            return 1.5
        elif "7b" in capability_lower or "3b" in capability_lower:
            return 1.0
        else:
            return 1.0  # Default/unknown
