# AgentMonitor/evaluation/benchmark_evaluator.py
"""
Benchmark evaluation for Multi-Agent Systems.
Implements robust evaluation for HumanEval, GSM8K, and MMLU benchmarks.
"""

import os
import re
import io
import sys
import ast
import traceback
import multiprocessing
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm


class BenchmarkEvaluator:
    """
    Evaluate MAS on standard benchmarks with robust scoring.
    """
    
    def __init__(self, dataset_root: Optional[Path] = None):
        """
        Args:
            dataset_root: Path to BenchmarkDatasetFolder
        """
        self.dataset_root = dataset_root or Path(__file__).parent.parent.parent / "BenchmarkDatasetFolder"
        
    def evaluate_humaneval(
        self,
        code_generator_func,
        num_samples: int = 20,
        timeout: int = 5
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Evaluate on HumanEval coding tasks.
        
        Args:
            code_generator_func: Function that takes prompt and returns code
            num_samples: Number of samples to evaluate
            timeout: Execution timeout in seconds
            
        Returns:
            (average_score, results_list)
        """
        dataset_path = self.dataset_root / "HumanEval" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        results = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="HumanEval"):
            prompt = row['prompt']
            test_code = row.get('test', row.get('tests', ''))
            
            try:
                # Generate code
                generated_code = code_generator_func(prompt)
                
                # Test code execution
                is_correct = self._test_code_execution(generated_code, test_code, timeout)
                score = 1.0 if is_correct else 0.0
                
                results.append({
                    "task_id": idx,
                    "prompt": prompt,
                    "generated_code": generated_code,
                    "score": score,
                    "is_correct": is_correct
                })
                
            except Exception as e:
                print(f"[WARNING] HumanEval task {idx} failed: {e}")
                results.append({
                    "task_id": idx,
                    "prompt": prompt,
                    "generated_code": "",
                    "score": 0.0,
                    "is_correct": False,
                    "error": str(e)
                })
        
        avg_score = np.mean([r["score"] for r in results])
        return avg_score, results
    
    def evaluate_gsm8k(
        self,
        answer_generator_func,
        num_samples: int = 20
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Evaluate on GSM8K math reasoning tasks.
        
        Args:
            answer_generator_func: Function that takes question and returns answer
            num_samples: Number of samples to evaluate
            
        Returns:
            (average_score, results_list)
        """
        dataset_path = self.dataset_root / "GSM8k" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        results = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="GSM8K"):
            question = row['question']
            expected_answer = row['answer']
            
            try:
                # Generate answer
                generated_answer = answer_generator_func(question)
                
                # Extract and compare numeric answers
                is_correct = self._compare_numeric_answers(generated_answer, expected_answer)
                score = 1.0 if is_correct else 0.0
                
                results.append({
                    "task_id": idx,
                    "question": question,
                    "expected": expected_answer,
                    "generated": generated_answer,
                    "score": score,
                    "is_correct": is_correct
                })
                
            except Exception as e:
                print(f"[WARNING] GSM8K task {idx} failed: {e}")
                results.append({
                    "task_id": idx,
                    "question": question,
                    "expected": expected_answer,
                    "generated": "",
                    "score": 0.0,
                    "is_correct": False,
                    "error": str(e)
                })
        
        avg_score = np.mean([r["score"] for r in results])
        return avg_score, results
    
    def evaluate_mmlu(
        self,
        answer_generator_func,
        num_samples: int = 20
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Evaluate on MMLU knowledge/reasoning tasks.
        
        Args:
            answer_generator_func: Function that takes question and returns answer
            num_samples: Number of samples to evaluate
            
        Returns:
            (average_score, results_list)
        """
        dataset_path = self.dataset_root / "MMLU" / "data.csv"
        df = pd.read_csv(dataset_path)
        sampled = df.sample(n=min(num_samples, len(df)), random_state=42)
        
        results = []
        for idx, row in tqdm(sampled.iterrows(), total=len(sampled), desc="MMLU"):
            question = row['question']
            correct_answer = row['answer']
            
            try:
                # Generate answer
                generated_answer = answer_generator_func(question)
                
                # Compare answers (flexible matching)
                is_correct = self._compare_text_answers(generated_answer, correct_answer)
                score = 1.0 if is_correct else 0.0
                
                results.append({
                    "task_id": idx,
                    "question": question,
                    "expected": correct_answer,
                    "generated": generated_answer,
                    "score": score,
                    "is_correct": is_correct
                })
                
            except Exception as e:
                print(f"[WARNING] MMLU task {idx} failed: {e}")
                results.append({
                    "task_id": idx,
                    "question": question,
                    "expected": correct_answer,
                    "generated": "",
                    "score": 0.0,
                    "is_correct": False,
                    "error": str(e)
                })
        
        avg_score = np.mean([r["score"] for r in results])
        return avg_score, results
    
    def _test_code_execution(
        self,
        code: str,
        test_code: str,
        timeout: int = 5
    ) -> bool:
        """
        Test code execution (with timeout and safety).
        
        Returns True if code runs without errors, False otherwise.
        """
        # Basic syntax check first
        try:
            ast.parse(code)
        except SyntaxError:
            return False
        
        # Combine code and test
        full_code = code + "\n" + test_code
        
        # Execute with timeout
        try:
            result = self._execute_code_with_timeout(full_code, timeout)
            # If no error message, consider it successful
            return "error" not in result.lower() and "traceback" not in result.lower()
        except Exception:
            return False
    
    def _execute_code_with_timeout(self, code: str, timeout: int) -> str:
        """Execute code with multiprocessing timeout."""
        def target(queue):
            try:
                local_vars = {}
                captured_output = io.StringIO()
                with redirect_stdout(captured_output), redirect_stderr(captured_output):
                    exec(code, {}, local_vars)
                output = captured_output.getvalue()
                queue.put({"output": output, "error": ""})
            except Exception as e:
                error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
                queue.put({"output": "", "error": error_msg})
        
        output_queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=target, args=(output_queue,))
        process.start()
        process.join(timeout)
        
        if process.is_alive():
            process.terminate()
            process.join()
            return "Execution timed out"
        
        if not output_queue.empty():
            result = output_queue.get()
            return result.get("error", result.get("output", ""))
        
        return ""
    
    def _compare_numeric_answers(self, generated: str, expected: str) -> bool:
        """
        Compare numeric answers with robust extraction.
        Handles formats like: "42", "The answer is 42", "#### 42", "$42.50"
        """
        # Extract numbers from both strings
        gen_nums = self._extract_numbers(str(generated))
        exp_nums = self._extract_numbers(str(expected))
        
        if not gen_nums or not exp_nums:
            # Fallback to string matching
            return str(expected).strip().lower() in str(generated).strip().lower()
        
        # Compare the last/largest number (common in GSM8K)
        gen_answer = gen_nums[-1]
        exp_answer = exp_nums[-1]
        
        # Fuzzy numeric comparison (allow small floating point differences)
        return abs(gen_answer - exp_answer) < 0.01
    
    def _extract_numbers(self, text: str) -> list:
        """Extract all numbers from text."""
        # Remove commas from numbers
        text = text.replace(',', '')
        
        # Find all numeric patterns (including decimals, negatives, percentages)
        patterns = [
            r'-?\d+\.\d+',  # Decimals: -3.14, 42.5
            r'-?\d+',        # Integers: -42, 123
        ]
        
        numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            numbers.extend([float(m) for m in matches])
        
        return numbers
    
    def _compare_text_answers(self, generated: str, expected: str) -> bool:
        """
        Compare text answers with flexible matching.
        """
        gen_clean = self._normalize_answer(str(generated))
        exp_clean = self._normalize_answer(str(expected))
        
        # Exact match
        if gen_clean == exp_clean:
            return True
        
        # Substring match (expected in generated)
        if exp_clean in gen_clean:
            return True
        
        # Multiple choice: check if single letter matches
        if len(exp_clean) == 1 and exp_clean.isalpha():
            # Extract first letter from generated
            letters = re.findall(r'\b([A-Da-d])\b', generated)
            if letters and letters[0].upper() == exp_clean.upper():
                return True
        
        return False
    
    def _normalize_answer(self, text: str) -> str:
        """Normalize answer text for comparison."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Lowercase
        text = text.lower()
        # Remove punctuation (except periods in numbers)
        text = re.sub(r'[^\w\s\.]', '', text)
        # Strip
        return text.strip()
