# AgentMonitor/evaluation/mas_orchestrator.py
"""
MAS Orchestrator: Integrates AgentMonitor with MAS execution and evaluation.
"""

import asyncio
import os
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm

from ..core.agent_monitor import AgentMonitor
from ..features.feature_extractor import FeatureExtractor
from .benchmark_evaluator import BenchmarkEvaluator


class MASOrchestrator:
    """
    Orchestrates MAS execution, monitoring, and evaluation.
    Produces training data for XGBoost predictor.
    """
    
    def __init__(
        self,
        mas_factory,
        llm_judge: Optional[Any] = None,
        dataset_root: Optional[Path] = None
    ):
        """
        Args:
            mas_factory: Function that creates a MAS instance
            llm_judge: LLM for judging agent scores
            dataset_root: Path to benchmark datasets
        """
        self.mas_factory = mas_factory
        self.llm_judge = llm_judge
        self.feature_extractor = FeatureExtractor(llm_judge)
        self.benchmark_eval = BenchmarkEvaluator(dataset_root)
        
    async def evaluate_mas_variant(
        self,
        variant_config: Dict[str, Any],
        num_samples_per_benchmark: int = 10
    ) -> Dict[str, Any]:
        """
        Evaluate a single MAS variant on all three benchmarks.
        
        Args:
            variant_config: MAS configuration dict with keys:
                - name: variant name
                - threshold, max_retries, etc.
                - agent_capabilities: dict of {agent_name: capability_str}
            num_samples_per_benchmark: Samples per benchmark
            
        Returns:
            Dict with 20 columns (16 features + 3 scores + 1 label)
        """
        variant_name = variant_config.get("name", "MAS_Variant")
        print(f"\n{'='*60}")
        print(f"Evaluating MAS Variant: {variant_name}")
        print(f"Configuration: {variant_config}")
        print(f"{'='*60}\n")
        
        # Store all monitoring data across benchmarks
        all_monitor_data = []
        
        # Evaluate on each benchmark
        humaneval_score = await self._evaluate_on_humaneval(
            variant_config, num_samples_per_benchmark, all_monitor_data
        )
        
        gsm8k_score = await self._evaluate_on_gsm8k(
            variant_config, num_samples_per_benchmark, all_monitor_data
        )
        
        mmlu_score = await self._evaluate_on_mmlu(
            variant_config, num_samples_per_benchmark, all_monitor_data
        )
        
        # Aggregate features across all runs
        aggregated_features = self._aggregate_features(all_monitor_data, variant_config)
        
        # Compute label (weak supervision)
        label_mas_score = (
            0.5 * humaneval_score +
            0.3 * gsm8k_score +
            0.2 * mmlu_score
        )
        
        # Combine into final row
        row = {
            **aggregated_features,  # 16 features
            'humaneval_score': humaneval_score,
            'gsm8k_score': gsm8k_score,
            'mmlu_score': mmlu_score,
            'label_mas_score': label_mas_score
        }
        
        print(f"\n{'='*60}")
        print(f"Results for {variant_name}:")
        print(f"  HumanEval:   {humaneval_score:.4f}")
        print(f"  GSM8K:       {gsm8k_score:.4f}")
        print(f"  MMLU:        {mmlu_score:.4f}")
        print(f"  MAS Score:   {label_mas_score:.4f}")
        print(f"  Total Runs:  {len(all_monitor_data)}")
        print(f"{'='*60}\n")
        
        return row
    
    async def _evaluate_on_humaneval(
        self,
        variant_config: Dict[str, Any],
        num_samples: int,
        monitor_data_store: List[Dict[str, Any]]
    ) -> float:
        """Evaluate on HumanEval."""
        print(f"[HUMANEVAL] Evaluating...")
        
        # Load dataset
        dataset_path = Path(self.benchmark_eval.dataset_root) / "HumanEval" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        scores = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="HumanEval"):
            prompt = row['prompt']
            test_code = row.get('test', row.get('tests', ''))
            
            try:
                # Create MAS with monitor
                monitor = AgentMonitor(debug=False)
                mas = await self._create_monitored_mas(variant_config, monitor)
                
                # Run MAS on task
                result = await self._run_mas_task(mas, prompt, task_type='code')
                
                # Save monitor data
                monitor_data = self._export_monitor_data(monitor)
                monitor_data_store.append(monitor_data)
                
                # Test generated code
                generated_code = result.get('code', '')
                is_correct = self.benchmark_eval._test_code_execution(generated_code, test_code, timeout=5)
                scores.append(1.0 if is_correct else 0.0)
                
            except Exception as e:
                print(f"[WARNING] HumanEval task {idx} failed: {e}")
                scores.append(0.0)
        
        avg_score = np.mean(scores) if scores else 0.0
        print(f"[HUMANEVAL] Score: {avg_score:.4f}")
        return avg_score
    
    async def _evaluate_on_gsm8k(
        self,
        variant_config: Dict[str, Any],
        num_samples: int,
        monitor_data_store: List[Dict[str, Any]]
    ) -> float:
        """Evaluate on GSM8K."""
        print(f"[GSM8K] Evaluating...")
        
        # Load dataset
        dataset_path = Path(self.benchmark_eval.dataset_root) / "GSM8k" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        scores = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="GSM8K"):
            question = row['question']
            expected_answer = row['answer']
            
            try:
                # Create MAS with monitor
                monitor = AgentMonitor(debug=False)
                mas = await self._create_monitored_mas(variant_config, monitor)
                
                # Run MAS on task
                result = await self._run_mas_task(mas, question, task_type='qa')
                
                # Save monitor data
                monitor_data = self._export_monitor_data(monitor)
                monitor_data_store.append(monitor_data)
                
                # Check answer
                generated_answer = result.get('answer', '')
                is_correct = self.benchmark_eval._compare_numeric_answers(generated_answer, expected_answer)
                scores.append(1.0 if is_correct else 0.0)
                
            except Exception as e:
                print(f"[WARNING] GSM8K task {idx} failed: {e}")
                scores.append(0.0)
        
        avg_score = np.mean(scores) if scores else 0.0
        print(f"[GSM8K] Score: {avg_score:.4f}")
        return avg_score
    
    async def _evaluate_on_mmlu(
        self,
        variant_config: Dict[str, Any],
        num_samples: int,
        monitor_data_store: List[Dict[str, Any]]
    ) -> float:
        """Evaluate on MMLU."""
        print(f"[MMLU] Evaluating...")
        
        # Load dataset
        dataset_path = Path(self.benchmark_eval.dataset_root) / "MMLU" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        scores = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="MMLU"):
            question = row['question']
            correct_answer = row['answer']
            
            try:
                # Create MAS with monitor
                monitor = AgentMonitor(debug=False)
                mas = await self._create_monitored_mas(variant_config, monitor)
                
                # Run MAS on task
                result = await self._run_mas_task(mas, question, task_type='qa')
                
                # Save monitor data
                monitor_data = self._export_monitor_data(monitor)
                monitor_data_store.append(monitor_data)
                
                # Check answer
                generated_answer = result.get('answer', '')
                is_correct = self.benchmark_eval._compare_text_answers(generated_answer, correct_answer)
                scores.append(1.0 if is_correct else 0.0)
                
            except Exception as e:
                print(f"[WARNING] MMLU task {idx} failed: {e}")
                scores.append(0.0)
        
        avg_score = np.mean(scores) if scores else 0.0
        print(f"[MMLU] Score: {avg_score:.4f}")
        return avg_score
    
    async def _create_monitored_mas(
        self,
        variant_config: Dict[str, Any],
        monitor: AgentMonitor
    ) -> Any:
        """
        Create MAS instance and register all agents with monitor.
        Override this method for custom MAS implementations.
        """
        # Create MAS from factory
        mas = self.mas_factory(variant_config)
        
        # Register each agent
        agent_capabilities = variant_config.get('agent_capabilities', {})
        
        for agent_name, agent_obj in mas.get_agents().items():
            capability = agent_capabilities.get(agent_name, "unknown")
            
            # Assume agents have standard interface
            await monitor.register(
                agent_obj,
                agent_obj.receive_message,  # Input method
                agent_obj.generate_response,  # Output method
                name=agent_name,
                capability=capability
            )
        
        return mas
    
    async def _run_mas_task(
        self,
        mas: Any,
        task_prompt: str,
        task_type: str = 'code'
    ) -> Dict[str, Any]:
        """
        Run MAS on a single task.
        Override this method for custom MAS execution.
        """
        # Default implementation - override in subclass
        result = await mas.run(task_prompt, task_type=task_type)
        return result
    
    def _export_monitor_data(self, monitor: AgentMonitor) -> Dict[str, Any]:
        """Export monitor data as dictionary."""
        return {
            "agents": {
                name: {
                    "name": name,
                    "capability": agent["capability"],
                    "prompt_template": agent["prompt_template"],
                    "outputs": agent["outputs"],
                    "latencies": agent["latencies"],
                    "token_counts": agent["token_counts"],
                }
                for name, agent in monitor.agents.items()
            },
            "conversation_history": monitor.conversation_history,
            "graph_edges": monitor.graph_edges
        }
    
    def _aggregate_features(
        self,
        monitor_data_list: List[Dict[str, Any]],
        variant_config: Dict[str, Any]
    ) -> Dict[str, float]:
        """Aggregate features across all monitor runs."""
        if not monitor_data_list:
            return self._empty_features()
        
        # Extract features from each run
        all_features = []
        for monitor_data in monitor_data_list:
            features = self.feature_extractor.extract_all_features(monitor_data)
            all_features.append(features)
        
        # Aggregate (take mean across all runs)
        feature_keys = all_features[0].keys()
        aggregated = {}
        
        for key in feature_keys:
            values = [f[key] for f in all_features]
            aggregated[key] = np.mean(values) if values else 0.0
        
        return aggregated
    
    def _empty_features(self) -> Dict[str, float]:
        """Return empty feature dict."""
        return {
            "avg_personal_score": 0.0,
            "min_personal_score": 0.0,
            "max_loops": 0,
            "total_latency": 0.0,
            "total_token_usage": 0,
            "num_agents_triggered_enhancement": 0,
            "num_nodes": 0,
            "num_edges": 0,
            "clustering_coefficient": 0.0,
            "transitivity": 0.0,
            "avg_degree_centrality": 0.0,
            "avg_betweenness_centrality": 0.0,
            "avg_closeness_centrality": 0.0,
            "pagerank_entropy": 0.0,
            "heterogeneity_score": 0.0,
            "collective_score": 0.0
        }
