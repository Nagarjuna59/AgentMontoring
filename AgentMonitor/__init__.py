# AgentMonitor/__init__.py
"""
AgentMonitor: A Plug-and-Play Framework for Predictive and Secure Multi-Agent Systems
"""

from .core.agent_monitor import AgentMonitor
from .core.enhanced_monitor import EnhancedAgentMonitor
from .core.agent_wrapper import AgentWrapper
from .features.feature_extractor import FeatureExtractor
from .evaluation.benchmark_evaluator import BenchmarkEvaluator
from .models.predictor import MASPredictor
from .mas.code_generation_mas import CodeGenerationMAS
from .mas.mas_factory import MASFactory, SimpleMAS

__version__ = "1.0.0"
__all__ = [
    "AgentMonitor",
    "EnhancedAgentMonitor",  # NEW: With enhancement loops!
    "AgentWrapper",
    "FeatureExtractor",
    "BenchmarkEvaluator",
    "MASPredictor",
    "CodeGenerationMAS",  # NEW: Actual MAS implementation!
    "MASFactory",  # NEW: Creates MAS variants!
    "SimpleMAS",  # NEW: Simple MAS with different topologies!
]

