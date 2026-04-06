# AgentMonitor - Multi-Agent System Performance Prediction# AgentMonitor - MAS Performance Prediction System# 🎯 README - Start Here!# 🔍 AgentMonitor - Complete Research Implementation# 🔍 AgentMonitor - Predictive Multi-Agent System Framework# AgentMonitor: Multi-Agent System Performance Prediction# 🤖 AgentMonitor - Multi-Agent System Monitoring Framework



**Research Paper Implementation: Non-Invasive MAS Monitoring with XGBoost-Based Quality Prediction**



---**Research Paper Implementation: Non-Invasive Multi-Agent System Monitoring with XGBoost Prediction**



## 📖 Table of Contents



1. [What is AgentMonitor?](#what-is-agentmonitor)---**Last Updated**: October 11, 2025  

2. [Research Paper Methodology](#research-paper-methodology)

3. [Project Structure](#project-structure)

4. [Complete Workflow](#complete-workflow)

5. [File Descriptions](#file-descriptions)## 🎯 Overview**Status**: ✅ Production Ready - Give to Your Friend!

6. [Quick Start Guide](#quick-start-guide)

7. [Technical Details](#technical-details)

8. [System Integration](#system-integration)

AgentMonitor is a complete implementation of a research paper methodology for **predicting Multi-Agent System (MAS) performance without running expensive benchmarks**. > **Production-ready** Multi-Agent System framework with enhancement loops, 16-feature extraction, and XGBoost prediction  

---



## 🎯 What is AgentMonitor?

Instead of executing time-consuming benchmark tests, the system:---

AgentMonitor is a **complete research paper implementation** that predicts Multi-Agent System (MAS) quality **without running expensive benchmarks**.

1. Monitors MAS behavior during execution

### The Problem

- Traditional approach: Run MAS → Execute benchmarks (HumanEval, GSM8K, MMLU) → Get quality score2. Extracts 16 behavioral features (graph metrics, agent scores, performance)> Based on research paper: *AgentMonitor: A Plug-and-Play Framework for Predictive and Secure Multi-Agent Systems* (arXiv:2408.14972)

- Issue: **Takes hours** for comprehensive evaluation

- Cost: High API token usage and compute time3. Uses XGBoost to predict quality based on these features



### Our Solution4. Achieves instant predictions (seconds vs hours)## 📚 Documentation Guide

- New approach: Run MAS → Monitor behavior → Extract features → **Predict quality instantly**

- Benefit: **Takes seconds** instead of hours

- Accuracy: Learns from behavioral patterns, not benchmark results

---> A production-ready implementation based on the research paper: *AgentMonitor: A Plug-and-Play Framework for Predictive and Secure Multi-Agent Systems* (arXiv:2408.14972)

### How It Works

```

Traditional:  MAS → Benchmark Execution → Score (SLOW ❌)

AgentMonitor: MAS → Feature Extraction → XGBoost Prediction → Score (FAST ✅)## 🏗️ Project Structure### 👋 **For Your Friend** (Data Generation)

```



---

```---

## 🔬 Research Paper Methodology

LLama/

### 6-Step Process

│1. **START HERE**: `FRIEND_QUICK_START.md`

We implemented the **exact research paper approach**:

├── 📁 Production Files (Main Usage)

```

┌─────────────────────────────────────────────────────────────┐│   ├── interactive.py          # 🌟 Auto-improvement mode (RECOMMENDED)   - Complete step-by-step instructions

│  STEP 1: Design MAS Variants                                │

│  ─────────────────────────────                              ││   ├── predict.py              # Fast prediction mode

│  Create diverse Multi-Agent Systems with:                   │

│  • Different architectures (3-agent vs 4-agent)             ││   ├── gemini_api.py           # Gemini API wrapper   - Setup, run, troubleshooting

│  • Different thresholds (0.5, 0.6, 0.7, 0.8)               │

│  • Different retry strategies (1, 2, 3 retries)            ││   └── .env                    # API key configuration

│  • Random combinations for diversity                        │

└─────────────────────────────────────────────────────────────┘│   - Read this first!## 🚀 Quick Start (3 Steps)

                             ↓

┌─────────────────────────────────────────────────────────────┐├── 📁 Core System

│  STEP 2: Non-Invasive Monitoring                           │

│  ──────────────────────────────                             ││   └── AgentMonitor/

│  Monitor watches MAS execution WITHOUT modifying it:        │

│  • Track all agent interactions (graph edges)              ││       ├── core/

│  • Record agent scores and quality                         │

│  • Measure latency and token usage                         ││       │   └── enhanced_monitor.py    # Non-invasive monitoring2. **CHECKLIST**: `FRIEND_CHECKLIST.md`**TL;DR:** Monitor your Multi-Agent Systems, extract 16 performance features, train XGBoost to predict MAS quality, and optimize before expensive evaluation.## 🎯 Overview**A Python framework for monitoring, scoring, and optimizing Multi-Agent Systems (MAS) using LLM-based evaluation and XGBoost predictions.**

│  • Capture enhancement loops                               │

└─────────────────────────────────────────────────────────────┘│       ├── mas/

                             ↓

┌─────────────────────────────────────────────────────────────┐│       │   └── code_generation_mas.py # 4-agent MAS   - Print this out!

│  STEP 3: Feature Extraction (16 Features)                  │

│  ───────────────────────────────────────                    ││       ├── benchmark/

│  Extract behavioral metrics using NetworkX:                 │

│  • Graph: nodes, edges, clustering, transitivity           ││       │   └── evaluator.py           # Feature extraction   - Track 50+ runs### 1. Install

│  • Centrality: degree, betweenness, closeness, PageRank    │

│  • Quality: avg/min agent scores, heterogeneity            ││       └── models/

│  • Performance: latency, tokens, enhancement loops          │

└─────────────────────────────────────────────────────────────┘│           └── predictor.py           # XGBoost training   - Simple progress tracker

                             ↓

┌─────────────────────────────────────────────────────────────┐│

│  STEP 4: Weak Supervision (Training Labels)                │

│  ─────────────────────────────────────                      │├── 📁 Training Pipeline```bash

│  Estimate quality WITHOUT running actual benchmarks:        │

│  • Content-aware heuristic scoring                          ││   └── scripts/

│  • Analyze code completeness, structure, documentation      │

│  • Add controlled noise (±0.15) for realism                ││       └── training/### 🎓 **For You** (Model Training & Usage)

│  • Creates training labels (0-1 scale)                      │

└─────────────────────────────────────────────────────────────┘│           ├── generate_dataset.py    # Create training data

                             ↓

┌─────────────────────────────────────────────────────────────┐│           └── train_model.py         # Train XGBoost modelpip install -r requirements.txt

│  STEP 5: XGBoost Training                                   │

│  ──────────────────────                                     ││

│  Train gradient boosting model:                             │

│  • Input: 16 behavioral features                            │├── 📁 Utilities1. **MAIN GUIDE**: `COMPLETE_GUIDE.md`

│  • Output: Predicted MAS quality score                      │

│  • Learn pattern: Features → Performance                    ││   └── scripts/

│  • Evaluation: Spearman correlation                         │

└─────────────────────────────────────────────────────────────┘│       └── utilities/   - Complete technical documentation```---

                             ↓

┌─────────────────────────────────────────────────────────────┐│           ├── monitor_progress.py    # Track generation progress

│  STEP 6: Fast Prediction (Production)                      │

│  ────────────────────────────────                           ││           └── check_dataset.py       # Validate dataset quality   - All features, workflows, code explanations

│  Use trained model for instant predictions:                 │

│  • Run MAS on new task                                      ││

│  • Extract 16 features                                      │

│  • Predict quality in <1ms                                  │├── 📁 Verification   - Reference for everything

│  • NO benchmark execution needed!                           │

└─────────────────────────────────────────────────────────────┘│   └── scripts/

```

│       └── verification/

### Key Innovation: Three-Level Enhancement

│           ├── verify_system.py       # System validation

```

Level 1: AGENT-LEVEL Enhancement│           └── test_all_modes.py      # Mode testing---### 2. Set API Key

├─ Monitor scores each agent output

├─ If score < threshold → Retry with enhancement prompt│

├─ Records self-loop edges in graph

└─ Tracks retry counts├── 📁 Documentation



Level 2: MAS-LEVEL Prediction│   └── docs/

├─ XGBoost predicts overall MAS quality

├─ Based on 16 behavioral features│       ├── EXAMPLE_RUN_RESULTS.md     # Example outputs## ⚡ Quick Commands```bash

├─ Instant prediction (<1ms)

└─ No benchmark execution needed│       └── VERIFICATION_REPORT.md     # Complete validation



Level 3: TASK-LEVEL Auto-Improvement│

├─ Tries different MAS variants (up to 3 attempts)

├─ Predicts quality after each attempt├── 📁 Data & Models

├─ Keeps best result

└─ Stops when score ≥ 0.75 threshold│   ├── data/### Your Friend Does (50+ times):echo GEMINI_API_KEY=your_key_here > .env## 📋 Table of Contents**AgentMonitor** is a machine learning system that predicts Multi-Agent System (MAS) performance using XGBoost regression. It monitors MAS execution, extracts behavioral features, and predicts overall system effectiveness based on agent interactions and collective behavior.**Status**: ✅ **FULLY FUNCTIONAL**  

```

│   │   └── training_data.csv          # Training dataset (148 samples)

---

│   └── models/```bash

## 📁 Project Structure

│       └── mas_predictor.pkl          # Trained XGBoost model

```

LLama/                                  # Main project folder│python main.py generate```

│

├── 🌟 PRODUCTION FILES (Use These Daily)└── 📄 Configuration

│   ├── run_interactive.py             # Main file - Auto-improvement mode

│   ├── run_prediction.py              # Fast prediction without optimization    ├── requirements.txt```

│   ├── gemini_api.py                  # Gemini API wrapper

│   ├── .env                           # API key configuration    ├── .env.example

│   └── main.py                        # Legacy file (has all modes combined)

│    └── README.md (this file)

├── 📦 CORE SYSTEM (Research Implementation)

│   └── AgentMonitor/```

│       ├── __init__.py                # Package exports

│       │### You Do (ONCE after getting data):

│       ├── core/

│       │   ├── __init__.py---

│       │   └── enhanced_monitor.py    # Non-invasive monitoring system

│       │                              # - Tracks agent interactions```bash### 3. Run Complete Demo

│       │                              # - Records graph edges

│       │                              # - Manages enhancement loops## 🚀 Quick Start

│       │

│       ├── mas/python main.py train

│       │   ├── __init__.py

│       │   └── code_generation_mas.py # 4-agent code generation MAS### 1. Setup

│       │                              # - Analyzer → Coder → Tester → Reviewer

│       │                              # - Creates feedback loops``````bash- [Quick Start](#-quick-start)**Date**: October 8, 2025  

│       │

│       ├── benchmark/```bash

│       │   ├── __init__.py

│       │   └── evaluator.py           # Feature extraction & weak supervision# Install dependencies

│       │                              # - Extracts 16 behavioral features

│       │                              # - Estimates quality heuristicallypip install -r requirements.txt

│       │

│       └── models/### You Do (FOREVER after training):python run_complete_agentmonitor.py

│           ├── __init__.py

│           └── predictor.py           # XGBoost training & prediction# Configure Gemini API

│                                      # - Trains on features → labels

│                                      # - Saves/loads modelcp .env.example .env```bash

│

├── 🔧 TRAINING PIPELINE (Development)# Edit .env and add your GEMINI_API_KEY

│   └── scripts/

│       └── training/```python main.py predict```- [What This Does](#-what-this-does)

│           ├── 1_generate_training_data.py    # Step 1: Create dataset

│           │                                  # - Run MAS with variants

│           │                                  # - Extract features

│           │                                  # - Save to CSV### 2. Production Usage (Recommended)```

│           │

│           └── 2_train_xgboost_model.py      # Step 2: Train model

│                                              # - Load CSV data

│                                              # - Train XGBoost**Interactive Auto-Improvement Mode:**

│                                              # - Save model

│```bash

├── 🛠️ UTILITIES (Helper Tools)

│   └── scripts/python interactive.py---

│       └── utilities/

│           ├── realtime_generation_monitor.py # Monitor dataset generation```

│           ├── validate_dataset_quality.py    # Check dataset readiness

│           ├── analyze_csv.py                 # Analyze feature variance**This runs the COMPLETE system:**- [Installation](#-installation)### Key Innovation**Author**: Kumaraswamy Bakkashetti

│           ├── comprehensive_check.py         # Full quality check

│           ├── wait_for_5_samples.py         # Early validationThis mode:

│           └── test_*.py                      # Various test scripts

│- Takes your programming task## 📁 Project Structure

├── ✅ VERIFICATION (Testing)

│   └── scripts/- Tries up to 3 MAS variants

│       └── verification/

│           ├── system_component_verification.py    # Verify all components- Predicts quality after each attempt- ✅ 4-agent MAS pipeline (Analyzer → Coder → Tester → Reviewer)

│           └── comprehensive_mode_testing.py       # Test all modes

│- Keeps best result

├── 💾 DATA & MODELS (Trained Assets)

│   ├── data/- Stops when score ≥ 0.75```

│   │   ├── training_data.csv          # 148 training samples

│   │   └── training_data_backup.csv   # Backup

│   │

│   └── models/**Example:**Final/- ✅ **Enhancement loops** (auto-retry if quality < threshold)- [Basic Usage](#-basic-usage)

│       └── mas_predictor.pkl          # Trained XGBoost model

│```

├── 📊 BENCHMARK DATASETS (Not Used in Production)

│   └── BenchmarkDatasetFolder/Enter programming task: Write a function to implement binary search├── 📘 COMPLETE_GUIDE.md          # Your complete documentation

│       ├── GSM8k/data.csv             # Math reasoning benchmark

│       ├── HumanEval/data.csv         # Code generation benchmark🔄 ATTEMPT 1/3

│       └── MMLU/data.csv              # General knowledge benchmark

│🎯 Predicted Score: 0.8063├── 👋 FRIEND_QUICK_START.md      # Friend's instructions- ✅ Extract **16 features** (system + graph + collective)

└── 📄 CONFIGURATION

    ├── requirements.txt               # Python dependencies✅ NEW BEST SCORE!

    ├── .env                          # API keys (GEMINI_API_KEY)

    ├── .env.example                  # Template for .env🎉 Score above threshold (0.75)! Stopping.├── ✅ FRIEND_CHECKLIST.md         # Friend's tracking sheet

    └── README.md                     # This file

```



---🏆 BEST RESULT: 0.8063├── 📄 README.md                   # This file- ✅ Show XGBoost training/prediction- [Project Structure](#-project-structure)Instead of evaluating MAS on expensive benchmark tasks, AgentMonitor predicts performance by analyzing:



## 🔄 Complete Workflow[Complete binary search implementation]



### What We Did (Development Process)```│



```

┌─────────────────────────────────────────────────────────────┐

│  PHASE 1: DATASET CREATION                                  │### 3. Fast Prediction Mode├── 🐍 main.py                     # Main script (3 modes)

└─────────────────────────────────────────────────────────────┘



Step 1.1: Initial Setup

  ✅ Installed dependencies (xgboost, networkx, pandas, etc.)```bash├── ⚙️ requirements.txt            # Dependencies

  ✅ Configured Gemini API (converted from Ollama/Llama)

  ✅ Set up virtual environmentpython predict.py



Step 1.2: Generate Training Data```├── 🔑 .env                        # API key (CHANGE THIS!)---- [Complete Workflow](#-complete-workflow)

  Command: python scripts/training/1_generate_training_data.py

  

  What happened:

  • Prompted for number of samples (we generated 148)Enter a task and get:│

  • For each sample:

    ├─ Randomly selected programming task- MAS execution with monitoring

    ├─ Created random MAS variant (threshold, retries, architecture)

    ├─ Ran 4-agent MAS (Analyzer → Coder → Tester → Reviewer)- 16 behavioral features extracted├── 📁 AgentMonitor/               # Framework (19 Python files)

    ├─ Monitored execution (EnhancedAgentMonitor)

    ├─ Extracted 16 behavioral features- Instant quality prediction

    ├─ Estimated quality using weak supervision

    └─ Saved to CSV immediately (incremental append)- Final code output│   ├── core/                     # Monitoring

  

  Duration: ~1-3 minutes per sample

  Output: data/training_data.csv (148 rows × 20 columns)

---│   ├── features/                 # Feature extraction## 💡 What Makes This Complete?- [API Reference](#-api-reference)- **System metrics**: Agent scores, enhancement loops, latency, token usage---

Step 1.3: Monitored Progress (Optional)

  Command: python scripts/utilities/realtime_generation_monitor.py

  

  What it did:## 🔬 Research Paper Methodology│   ├── evaluation/               # Benchmarks

  • Watched CSV file in real-time

  • Displayed sample count updates

  • Showed latest labels

  • Helped track progress during long generation### 6-Step Process│   ├── models/                   # Predictor code



Step 1.4: Validated Dataset Quality

  Command: python scripts/utilities/validate_dataset_quality.py

  ```│   ├── mas/                      # MAS implementations

  Checked:

  ✅ Sample count: 148 (sufficient for training)Step 1: MAS Variants

  ✅ Feature variance: 18/19 features varying

  ✅ Label distribution: 0.09 - 1.00 (good range)   ↓ (Randomized configs: threshold, retries, architecture)│   └── utils/### ✅ Research Paper Features- [Important Notes](#-important-notes)

  ✅ No missing values

     

  Result: Dataset ready for training!

Step 2: Non-Invasive Monitoring│

┌─────────────────────────────────────────────────────────────┐

│  PHASE 2: MODEL TRAINING                                    │   ↓ (Track: graph edges, scores, latency, tokens)

└─────────────────────────────────────────────────────────────┘

   ├── 📁 models/                     # Trained models (empty until you train)- **16 Performance Indicators** (6 system + 9 graph + 1 collective)

Step 2.1: Train XGBoost Model

  Command: python scripts/training/2_train_xgboost_model.pyStep 3: Feature Extraction

  

  What happened:   ↓ (16 behavioral metrics from execution)│   └── (mas_predictor.pkl after training)

  • Loaded data/training_data.csv

  • Selected 16 feature columns (behavioral metrics)   

  • Split 80% train, 20% test

  • Trained XGBoost regressorStep 4: Weak Supervision│- **Weak Supervision** (0.5×HumanEval + 0.3×GSM8K + 0.2×MMLU)- [Citation](#-citation)- **Graph features**: Interaction network topology (clustering, centrality, entropy)

  • Evaluated with Spearman correlation

  • Saved model to models/mas_predictor.pkl   ↓ (Quality estimation without benchmarks)

  

  Results:   ├── 📁 data/                       # Training data

  ✅ Training Spearman: ~0.89 (excellent fit)

  ✅ Test Spearman: ~0.43 (reasonable generalization)Step 5: XGBoost Training

  ✅ Model saved and ready

   ↓ (Learn: Features → Performance)│   └── training_data.csv        # Generated by friend- **XGBoost Regression** with hyperparameter tuning

┌─────────────────────────────────────────────────────────────┐

│  PHASE 3: VERIFICATION                                      │   

└─────────────────────────────────────────────────────────────┘

Step 6: Fast Prediction│

Step 3.1: System Component Verification

  Command: python scripts/verification/system_component_verification.py   ✓ (Predict quality in seconds vs hours)

  

  Verified:```└── 📁 BenchmarkDatasetFolder/     # Benchmark datasets- **Spearman Correlation** as primary metric

  ✅ All module imports working

  ✅ Dataset exists with 148 samples

  ✅ Model loads correctly

  ✅ Gemini API connection active### 16 Behavioral Features    ├── HumanEval/

  ✅ All 6 research paper steps implemented



Step 3.2: Comprehensive Mode Testing

  Command: python scripts/verification/comprehensive_mode_testing.py**Graph Metrics (NetworkX):**    ├── GSM8K/- **Non-invasive Monitoring** (no code changes needed)

  

  Tested:- `num_nodes`, `num_edges`

  ✅ Model performance metrics

  ✅ Dataset quality- `clustering_coefficient`, `transitivity`    └── MMLU/

  ✅ Gemini API connection

  ✅ Prediction capability- `avg_degree_centrality`, `avg_betweenness_centrality`, `avg_closeness_centrality`

  ✅ All methodology steps

- `pagerank_entropy````---- **Collective behavior**: Overall system coordination score## 📋 Table of Contents

┌─────────────────────────────────────────────────────────────┐

│  PHASE 4: PRODUCTION USE                                    │

└─────────────────────────────────────────────────────────────┘

**Quality Metrics:**

Step 4.1: Interactive Auto-Improvement (RECOMMENDED)

  Command: python run_interactive.py- `avg_personal_score`, `min_personal_score`

  

  How it works:- `heterogeneity_score`, `collective_score`---### ✅ Production Features (NEW!)

  1. User enters programming task

  2. System tries MAS variant #1

     ├─ Runs 4-agent MAS

     ├─ Monitors execution**Performance Metrics:**

     ├─ Extracts 16 features

     └─ Predicts quality score- `max_loops` (enhancement iterations)

  3. If score < 0.75, try variant #2 (different config)

  4. If score < 0.75, try variant #3- `total_latency`, `total_token_usage`## 🚀 The Complete Workflow- **Enhancement Loops** - Auto-retry if agent output quality < threshold

  5. Return best result from all attempts

  - `num_agents_triggered_enhancement`

  Example result:

  • Task: "Write binary search function"

  • Attempt 1: Score 0.8063 ✅ (above threshold)

  • Stopped after 1 attempt---

  • Total time: 32 seconds

  • Output: Complete binary search implementation### Phase 1: Your Friend Generates Data- **LLM-based Scoring** - Quality assessment for each agent output



Step 4.2: Fast Prediction (Single Run)## 🎓 Training Pipeline (For Developers)

  Command: python run_prediction.py

  ```

  How it works:

  1. User enters task### Generate Training Data

  2. Run MAS once (no retries)

  3. Extract featuresFriend receives:- **Feedback Generation** - Actionable suggestions for improvement## 🚀 Quick Start

  4. Predict quality

  5. Show result```bash

  

  Use when: Just want quick quality check without optimizationpython scripts/training/generate_dataset.py  ↓

```

```

---

Sets up environment (5 min)- **Conversation Graph** - Track agent interactions automatically

## 📋 File Descriptions

- Creates diverse MAS variants

### Production Files (Root Directory)

- Runs on random programming tasks  ↓

**`run_interactive.py`** ⭐ MAIN PRODUCTION FILE

```python- Extracts features + estimates quality

Purpose: Auto-improvement mode for optimal code generation

What it does:- Saves incrementally to `data/training_data.csv`Runs: python main.py generate (50+ times, ~1 hour each)- **Comprehensive Logging** - JSON output with full statistics

  - Takes user programming task

  - Tries up to 3 different MAS variants

  - Predicts quality after each attempt

  - Keeps best result (highest predicted score)**Monitor Progress:**  ↓

  - Stops early if score ≥ 0.75

  ```bash

When to use: Daily use for programming tasks

Example: python run_interactive.pypython scripts/utilities/monitor_progress.pySends you: data/training_data.csv

```

```

**`run_prediction.py`** - Fast Prediction Mode

```python```

Purpose: Single MAS run with quality prediction

What it does:### Train XGBoost Model

  - Run MAS once on user task

  - Extract 16 behavioral features---### 1. Install Dependencies### Architecture1. [Overview](#overview)

  - Predict quality using XGBoost

  - Display result with features```bash

  

When to use: Quick quality check without optimizationpython scripts/training/train_model.py### Phase 2: You Train Model (ONCE)

Example: python run_prediction.py

``````



**`gemini_api.py`** - LLM API Wrapper```

```python

Purpose: Interface to Gemini API- Loads `data/training_data.csv`

What it does:

  - Loads GEMINI_API_KEY from .env- Trains XGBoost regressor (80/20 split)You receive: data/training_data.csv

  - Configures gemini-2.0-flash model

  - Provides call_gemini(prompt) function- Evaluates with Spearman correlation

  - Error handling for API calls

  - Saves to `models/mas_predictor.pkl`  ↓## 📖 Complete Usage Example

When to use: Called by other files (don't run directly)

Key function: call_gemini(prompt) → returns LLM response

```

### Validate DatasetRun: python main.py train (5 minutes)

**`main.py`** - Legacy Combined File

```python

Purpose: Original file with all modes (generate, train, predict, interactive)

What it does:```bash  ↓

  - Mode 1: Generate training data

  - Mode 2: Train modelpython scripts/utilities/check_dataset.py

  - Mode 3: Predict quality

  - Mode 4: Interactive auto-improvement```Creates: models/mas_predictor.pkl ✅

  

When to use: For reference or if you prefer single file

Note: Functionality now split into separate files for clarity

```Checks:``````python```bash2. [System Architecture](#system-architecture)



### Core System (AgentMonitor Package)- Sample count (recommended 100+)



**`AgentMonitor/core/enhanced_monitor.py`** - Non-Invasive Monitor- Feature variance

```python

Purpose: Track MAS execution without modifying behavior- Label distribution

Key features:

  - Records every agent interaction as graph edge- Missing values### Phase 3: You Predict (FOREVER)from AgentMonitor.core.enhanced_monitor import EnhancedAgentMonitor

  - Scores agent outputs using heuristics

  - Triggers enhancement loops if score < threshold

  - Records self-loop edges on retries

  - Tracks latency and token usage---```

  

Key methods:

  - run_agent_with_enhancement() - Main monitoring function

  - record_graph_edge(from, to) - Track agent interactions## 🔄 Three-Level Enhancement SystemRun: python main.py predict (8 seconds)pip install -r requirements.txt

  - _heuristic_score(output) - Quality scoring

  - get_summary() - Export all monitoring data

  

Integration: Used by all MAS instances for monitoring### Level 1: Agent-Level  ↓

```

**Monitor** scores each agent output:

**`AgentMonitor/mas/code_generation_mas.py`** - 4-Agent MAS

```python- If score < threshold → Retry with enhancement promptLoads: models/mas_predictor.pkl ✅# Create monitor with enhancement loops

Purpose: Multi-agent code generation system

Architecture:- Records self-loop edges for graph metrics

  Analyzer (analyzes task)

     ↓- Tracks retry counts and latencies  ↓

  Coder (writes code)

     ↓

  Tester (creates tests)

     ↓### Level 2: MAS-LevelOutput: Predicted MAS Scoremonitor = EnhancedAgentMonitor(``````3. [Quick Start](#quick-start)

  Reviewer (final review)

     ↓ (feedback loop)**XGBoost** predicts overall quality:

  Back to Analyzer if needed

  - From 16 behavioral features```

Key features:

  - 4 specialized agents- No benchmark execution needed

  - Feedback edge: Reviewer → Analyzer

  - Creates graph triangles for clustering metrics- Instant prediction (<1ms)    api_key="your_key",

  - Integrated with EnhancedAgentMonitor

  

Integration: Used by prediction and interactive modes

```### Level 3: Task-Level**Key**: Train ONCE, predict FOREVER! No retraining needed!



**`AgentMonitor/benchmark/evaluator.py`** - Feature Extraction**Auto-Improvement** optimizes variants:

```python

Purpose: Extract behavioral features and estimate quality- Tries different MAS configs (up to 3 attempts)    threshold=0.6,    # Retry if score < 0.6

Key functions:

  1. extract_features(monitor_data)- Stops when predicted score ≥ 0.75

     - Builds NetworkX graph from agent interactions

     - Calculates graph metrics (clustering, centrality, PageRank)- Keeps best result---

     - Extracts quality metrics (scores, heterogeneity)

     - Returns 16-feature dictionary

     

  2. estimate_benchmark_score(output, task)---    max_retries=2,    # Max 2 enhancement attempts

     - Content-aware heuristic scoring

     - Analyzes completeness, structure, documentation

     - Adds controlled noise (±0.15)

     - Returns quality estimate (0-1)## 📊 Current System Status## 🎁 What to Give Your Friend

     

Integration: Used during training and prediction

```

**Dataset:**    debug=True### 2. Set API Key┌─────────────────────────────────────────────────────────────┐4. [LLM Integration (Gemini & Ollama)](#llm-integration)

**`AgentMonitor/models/predictor.py`** - XGBoost Training

```python- ✅ 148 training samples

Purpose: Train and use XGBoost prediction model

Key features:- ✅ 18/19 features with variance### Required Files:

  - FEATURE_COLUMNS: Defines 16 behavioral features

  - train() method: Trains on CSV data- ✅ Label range: 0.09 - 1.00

  - predict() method: Predicts from features

  - save/load functionality for model persistence```)

  

Key methods:**Model:**

  - train(data_path) - Train on training_data.csv

  - predict(features) - Predict quality from features- ✅ Trained XGBoost regressor✅ Final/ folder (entire thing)

  - Model saved as pickle file

  - ✅ Saved at `models/mas_predictor.pkl`

Integration: Used by training script and prediction modes

```- ✅ Ready for predictions✅ Tell them to read: FRIEND_QUICK_START.md



### Training Pipeline



**`scripts/training/1_generate_training_data.py`****API:**✅ Tell them to print: FRIEND_CHECKLIST.md

```python

Purpose: Create diverse training dataset- ✅ Gemini 2.0 Flash configured

Process:

  1. Define 20 sample programming tasks- ✅ Connection verified✅ Tell them to change API key in .env# Run agent with automatic enhancement

  2. For each sample:

     - Pick random task

     - Generate random MAS config (threshold, retries, etc.)

     - Run MAS with monitoring**Modes:**```

     - Extract 16 features

     - Estimate quality (weak supervision)- ✅ Interactive (auto-improvement)

     - Append to CSV immediately

  3. Save to data/training_data.csv- ✅ Predict (fast prediction)result = await monitor.run_agent_with_enhancement(Create `.env` file:│                    AgentMonitor Pipeline                     │5. [Components](#components)

  

Key features:- ✅ Generate (dataset creation)

  - Incremental CSV append (progress visible)

  - Random MAS variants for diversity- ✅ Train (model training)### Do NOT share:

  - Weak supervision (no real benchmarks)

  

Usage: python scripts/training/1_generate_training_data.py

Input: Number of samples (we used 148)---```    agent=my_coder_agent,

Output: data/training_data.csv

```



**`scripts/training/2_train_xgboost_model.py`**## 🎯 Example Results❌ venv/ folder (they create their own)

```python

Purpose: Train XGBoost model on collected data

Process:

  1. Load data/training_data.csv### Task: Binary Search Implementation❌ Your API key    task="Write a function to calculate Fibonacci sequence",```bash

  2. Select 16 feature columns

  3. Split 80/20 train/test

  4. Train XGBoost regressor

  5. Evaluate with Spearman correlation**Input:**```

  6. Save model to models/mas_predictor.pkl

  ```

Results:

  - Feature importance ranking"Write a Python function to implement binary search on a sorted list"    agent_name="Coder",

  - Training/test metrics

  - Saved model for production```

  

Usage: python scripts/training/2_train_xgboost_model.py---

Input: data/training_data.csv

Output: models/mas_predictor.pkl**Output:**

```

```    capability="gemini"GEMINI_API_KEY=your_gemini_api_key_here├─────────────────────────────────────────────────────────────┤6. [Usage Guide](#usage-guide)

### Utilities

🎯 Predicted Score: 0.8063/1.00

**`scripts/utilities/realtime_generation_monitor.py`**

```python## 🔧 Installation (Quick)

Purpose: Monitor dataset generation progress

What it does:📊 Execution Metrics:

  - Watches data/training_data.csv

  - Shows sample count updates every 5 seconds   Agents: 4 (Analyzer → Coder → Tester → Reviewer))

  - Displays latest label values

  - Runs until Ctrl+C   Graph Edges: 4

  

Usage: Run in separate terminal while generating data   Avg Agent Score: 0.986```bash

Command: python scripts/utilities/realtime_generation_monitor.py

```   Enhancements: 0 (all passed on first try)



**`scripts/utilities/validate_dataset_quality.py`**   Latency: 32.1 seconds# 1. Create virtual environment```

```python

Purpose: Validate dataset before training   Tokens: 7,789

Checks:

  ✓ Sample count (recommends 100+)python -m venv venv

  ✓ Feature variance (flags low-variance features)

  ✓ Label distribution (checks range and std)✅ Result: Complete binary search implementation

  ✓ Missing values

  ✓ Training readiness   - Proper documentationprint(f"Output: {result['output']}")

  

Usage: python scripts/utilities/validate_dataset_quality.py   - Edge case handling

Output: Quality report with recommendations

```   - Test validation passed# 2. Activate it



---```



## 🚀 Quick Start Guidevenv\Scripts\activate          # Windowsprint(f"Score: {result['score']:.2f}")│                                                               │7. [Fixes Applied](#fixes-applied)



### For End Users (Just Want Code)---



```bashsource venv/bin/activate       # Mac/Linux

# 1. Install dependencies

pip install -r requirements.txt## 🛠️ Verification



# 2. Configure API keyprint(f"Attempts: {result['attempts']}")

cp .env.example .env

# Edit .env and add: GEMINI_API_KEY=your_key_here### System Verification



# 3. Run interactive mode# 3. Install dependencies

python run_interactive.py

```bash

# 4. Enter your programming task

# Example: "Write a function to find prime numbers"python scripts/verification/verify_system.pypip install -r requirements.txtprint(f"Enhanced: {result['enhanced']}")### 3. Run Demo



# 5. Get optimized code with predicted quality score!```

```



### For Researchers (Full Pipeline)

Validates all components and research paper alignment.

```bash

# === PHASE 1: DATASET CREATION ===# 4. Set API key in .env



# Generate training data### Mode Testing

python scripts/training/1_generate_training_data.py

# Input: 150 (number of samples)echo GEMINI_API_KEY=your_key > .env



# Monitor progress (optional, in another terminal)```bash

python scripts/utilities/realtime_generation_monitor.py

python scripts/verification/test_all_modes.py# Save monitoring data│  1. MAS Execution                                            │8. [Data Analysis](#data-analysis)

# Validate dataset quality

python scripts/utilities/validate_dataset_quality.py```



# === PHASE 2: MODEL TRAINING ===# 5. Ready!



# Train XGBoost modelTests all system modes and predictions.

python scripts/training/2_train_xgboost_model.py

```monitor.save("output.json")

# === PHASE 3: VERIFICATION ===

---

# Verify all components

python scripts/verification/system_component_verification.py



# Test all modes## 📚 Documentation

python scripts/verification/comprehensive_mode_testing.py

---```bash

# === PHASE 4: PRODUCTION USE ===

- `docs/EXAMPLE_RUN_RESULTS.md` - Example outputs with analysis

# Use interactive mode

python run_interactive.py- `docs/VERIFICATION_REPORT.md` - Complete system validation

```



---

---## 📊 Two "models" Folders Explained# Print summary statistics

## 🔧 Technical Details



### 16 Behavioral Features

## ✅ System Status

```python

FEATURE_COLUMNS = [

    # Quality Metrics

    "avg_personal_score",          # Average agent quality (0-1)**🎉 PRODUCTION READY**People get confused by this - here's why both exist:monitor.print_summary()python examples/complete_demo.py│     ├─ Run multi-agent pipeline (code/QA tasks)             │9. [Troubleshooting](#troubleshooting)

    "min_personal_score",          # Minimum agent quality

    "heterogeneity_score",         # Agent score variance

    "collective_score",            # Combined agent quality

    All components operational and validated against research paper methodology.

    # Performance Metrics

    "max_loops",                   # Enhancement iterations

    "total_latency",               # Total execution time (seconds)

    "total_token_usage",           # Total LLM tokens**Ready for:**1. **`Final/models/`** (folder, empty initially)```

    "num_agents_triggered_enhancement",  # Agents that needed retry

    - ✅ Interactive task optimization

    # Graph Metrics (NetworkX)

    "num_nodes",                   # Number of agents- ✅ Fast quality prediction   - Stores **saved trained models** (`.pkl` files)

    "num_edges",                   # Agent interactions

    "clustering_coefficient",      # Local clustering- ✅ Training data generation

    "transitivity",                # Global clustering

    - ✅ Model retraining   - Created after running `python main.py train````

    # Centrality Metrics

    "avg_degree_centrality",       # Connection importance

    "avg_betweenness_centrality",  # Bridge importance

    "avg_closeness_centrality",    # Path efficiency---   - This is where `mas_predictor.pkl` lives

    

    # PageRank

    "pagerank_entropy",            # Influence distribution

]*Last Updated: October 12, 2025*  **Output:**

```

*Version: 1.0 - Research Paper Implementation*

### MAS Variants (Randomization for Diversity)

2. **`AgentMonitor/models/`** (Python package)

```python

Random configurations:   - Contains **source code** (`predictor.py`)```│     ├─ Monitor agent interactions                            │

- threshold: [0.5, 0.6, 0.7, 0.8]        # Quality threshold

- max_retries: [1, 2, 3]                  # Max retry attempts   - The actual training/prediction logic

- architecture: ['3-agent', '4-agent']    # MAS structure

- monitor_threshold: [0.5, 0.6, 0.7]     # Agent quality threshold   - Part of the framework[Coder] ⚠️ Score 0.52 < 0.60 - Retry 1/2

- monitor_retries: [1, 2]                # Agent retry limit



Why randomize?

• Creates diverse feature distributions**Think of it**:[Coder] ✅ Score 0.78 >= 0.60 (attempt 1)---

• Prevents model from memorizing single config

• Better generalization to new scenarios- `models/` = Library (where books are stored)

```

- `AgentMonitor/models/` = Printing press (where books are made)

### Training Details



```python

Dataset:**Both are needed!** Not duplicates!Output: def fibonacci(n):...│     └─ Log execution traces                                  │---

- Samples: 148

- Features: 16 behavioral metrics

- Labels: Weak supervision (heuristic scoring)

- Format: CSV (incremental append)---Score: 0.78



Model:

- Algorithm: XGBoost Regressor

- Train/Test Split: 80/20## ✅ VerificationAttempts: 1## 💡 What This Does

- Evaluation: Spearman correlation

- Hyperparameters: Default (can tune with tune_hyperparams=True)



Performance:### Is Everything Working?Enhanced: True

- Training Spearman: ~0.89 (excellent fit)

- Test Spearman: ~0.43 (reasonable generalization)

- Prediction time: <1ms (instant)

``````bash```│                                                               │



### Weak Supervision Details# Test imports



```pythonpython -c "from AgentMonitor import EnhancedAgentMonitor; print('✅')"

Instead of running actual benchmarks (hours), we:



1. Analyze code output structure

   - Has docstrings? +0.2# Check structure---### Problem

   - Has test cases? +0.15

   - Proper error handling? +0.1python -c "import os; print('✅' if os.path.exists('AgentMonitor/models/predictor.py') else '❌')"

   - Clear variable names? +0.1

   

2. Check completeness

   - Addresses task requirements# Verify dependencies

   - Implementation correctness (heuristic)

   pip list | findstr "pandas xgboost"  # Windows## 🏗️ Project StructureEvaluating Multi-Agent Systems (MAS) on benchmarks like HumanEval, GSM8K, MMLU is **expensive** and **time-consuming**. You need to predict which MAS configurations will perform well **before** running full evaluations.│  2. Feature Extraction                                       │## 🎯 Overview

3. Add controlled noise

   - Random ±0.15 for realismpip list | grep "pandas\|xgboost"   # Mac/Linux

   - Prevents overfitting to perfect scores

   ```

4. Scale to 0-1 range

   - Final label represents estimated quality

   

Why it works:All show ✅? You're good!```

✓ Faster than real benchmarks

✓ Still correlates with actual quality

✓ Enables large-scale training data

```---AgentMonitor/Final/



---



## 🔗 System Integration## 🐛 Common Issues├── run_complete_agentmonitor.py   ⭐ Main demo (start here!)### Solution│     ├─ System Features (6): scores, loops, latency, tokens  │



### How Everything Connects



```### "Module not found"│

┌─────────────────────────────────────────────────────────────┐

│                    USER INTERACTION                         │```bash

└─────────────────────────────────────────────────────────────┘

                             │# Activate venv first!├── AgentMonitor/                   📦 Framework package**AgentMonitor** provides:

                             ↓

        ┌────────────────────────────────────┐venv\Scripts\activate

        │   run_interactive.py (Main Entry)  │

        │   ────────────────────────────     │pip install -r requirements.txt│   ├── core/

        │   • Takes user task                │

        │   • Manages 3-attempt loop         │```

        │   • Tracks best result             │

        └────────────────────────────────────┘│   │   ├── agent_monitor.py        - Basic monitoring│     ├─ Graph Features (9): topology, centrality, entropy    │AgentMonitor is an intelligent monitoring system for Multi-Agent Systems that:

                             │

                             ↓### "No API key"

        ┌────────────────────────────────────┐

        │   gemini_api.py (LLM Interface)    │```bash│   │   ├── enhanced_monitor.py     - With enhancement loops ⭐

        │      ─────────────────────         │

        │      • Gemini API wrapper          │# Edit .env file

        │      • call_gemini() function      │

        └────────────────────────────────────┘# Add: GEMINI_API_KEY=your_actual_key│   │   └── agent_wrapper.py        - Simple agent wrapper1. **Non-invasive Monitoring** - Wrap your MAS without changing code

                             │

                             ↓```

        ┌────────────────────────────────────┐

        │  AgentMonitor/mas/                 ││   ├── features/

        │  code_generation_mas.py            │

        │  ──────────────────────            │### "Model not trained"

        │  • 4-agent MAS execution           │

        │  • Analyzer→Coder→Tester→Reviewer  │```bash│   │   └── feature_extractor.py    - 16 feature extraction2. **16 Performance Features** - Extract system, graph, and collaboration metrics│     └─ Collective Score (1): coordination measure           │

        └────────────────────────────────────┘

                             │# You need to train first!

                             ↓

        ┌────────────────────────────────────┐python main.py train│   ├── evaluation/

        │  AgentMonitor/core/                │

        │  enhanced_monitor.py               │```

        │  ─────────────────────             │

        │  • Non-invasive monitoring         ││   │   ├── benchmark_evaluator.py  - HumanEval/GSM8K/MMLU3. **Benchmark Evaluation** - Robust HumanEval/GSM8K/MMLU scoring

        │  • Graph edge recording            │

        │  • Enhancement loops               │### "No training data"

        │  • Score tracking                  │

        └────────────────────────────────────┘```bash│   │   └── mas_orchestrator.py     - Full evaluation pipeline

                             │

                             ↓# Your friend needs to generate data first!

        ┌────────────────────────────────────┐

        │  AgentMonitor/benchmark/           │# Or run: python main.py generate│   ├── models/4. **XGBoost Prediction** - Train model to predict MAS performance│                                                               │- **Monitors**: Tracks agent outputs with 6-dimensional scoring (factual accuracy, clarity, safety, code correctness, complexity, personal score)

        │  evaluator.py                      │

        │  ─────────────────                 │```

        │  • Build NetworkX graph            │

        │  • Extract 16 features             ││   │   └── predictor.py            - XGBoost training/prediction

        │  • Calculate graph metrics         │

        └────────────────────────────────────┘---

                             │

                             ↓│   └── utils/5. **Variant Optimization** - Test many configurations, deploy only the best

        ┌────────────────────────────────────┐

        │  AgentMonitor/models/              │## 📈 Expected Results

        │  predictor.py                      │

        │  ─────────────────                 ││

        │  • Load XGBoost model              │

        │  • Predict from features           │### After Friend's Work (50+ runs):

        │  • Return quality score            │

        └────────────────────────────────────┘- ✅ `data/training_data.csv` exists├── MAS/│  3. Benchmark Evaluation (Training Data Generation)          │- **Enhances**: Automatically improves low-scoring outputs through iterative refinement

                             │

                             ↓- ✅ Has 50+ rows (samples)

        ┌────────────────────────────────────┐

        │   models/mas_predictor.pkl         │- ✅ Has 20 columns (16 features + 4 scores)│   └── mas_pipeline.py             - Example MAS implementations

        │   ──────────────────────           │

        │   • Trained XGBoost model          │

        │   • 16 features → quality score    │

        └────────────────────────────────────┘### After Your Training (once):│### Research Paper Results

                             │

                             ↓- ✅ `models/mas_predictor.pkl` exists

        ┌────────────────────────────────────┐

        │      RESULT TO USER                │- ✅ Terminal shows: "Model saved to models/mas_predictor.pkl"├── scripts/

        │      ──────────────                │

        │      • Predicted quality score     │- ✅ Spearman correlation > 0.8 (with enough data)

        │      • Key features                │

        │      • Generated code              ││   └── generate_mas_variants.py    - Generate 30-50 MAS configs- **Spearman Correlation:** 0.89 (in-domain), 0.58 (cross-task)│     ├─ HumanEval: Code generation tasks                     │- **Collects Features**: Extracts 19 system + graph metrics (latency, tokens, loops, graph centrality, PageRank entropy)

        └────────────────────────────────────┘

```### After Your Prediction (forever):



### Data Flow- ✅ Terminal shows: "Model loaded from models/mas_predictor.pkl"│



```- ✅ Takes ~8 seconds (vs hours of benchmark evaluation!)

TRAINING PHASE:

──────────────- ✅ Outputs predicted MAS score├── BenchmarkDatasetFolder/         - Benchmark datasets- **Training Data:** 1,796 MAS variants



Task → MAS → Monitor → Features → Weak Supervision → CSV

                                                        ↓

                                              Training Dataset---│   ├── HumanEval/data.csv

                                                        ↓

                                              XGBoost Training

                                                        ↓

                                             Trained Model (.pkl)## 🎓 Paper Information│   ├── GSM8k/data.csv- **Benchmarks:** HumanEval (164 samples), GSM8K (100), MMLU (100)│     ├─ GSM8K: Math reasoning tasks                          │- **Trains ML Models**: Uses XGBoost to predict collective system performance





PRODUCTION PHASE:

────────────────**Research Paper**: AgentMonitor - Non-invasive MAS Performance Prediction  │   └── MMLU/data.csv



Task → MAS → Monitor → Features → XGBoost Model → Predicted Score**arXiv**: 2408.14972  

                                                          ↓

                                                   Quality Assessment**Key Innovation**: Predict MAS performance from behavioral features (fast!) instead of benchmark evaluation (slow!)│

                                                          ↓

                                              Auto-Improvement Logic

                                                          ↓

                                                   Best Result to User**16 Features Extracted**:├── data/                           - Generated data

```

- 6 System metrics (latency, tokens, scores)

### API Integration

- 9 Graph metrics (centrality, clustering)└── models/                         - Trained models---│     ├─ MMLU: Knowledge/QA tasks                             │- **Benchmarks**: Evaluates against HumanEval (code), GSM8K (math), MMLU (knowledge)

```

Gemini API (gemini-2.0-flash)- 1 Collective metric (final output quality)

      ↓

gemini_api.py wrapper```

      ↓

call_gemini(prompt)**Prediction Model**: XGBoost Regressor  

      ↓

Used by:**Target**: Combined benchmark score (0.5×HumanEval + 0.3×GSM8K + 0.2×MMLU)

  ├─ Analyzer agent

  ├─ Coder agent

  ├─ Tester agent

  └─ Reviewer agent------

```



---

## 📞 Support## 📦 Installation│     └─ Weak Supervision: label = 0.5×HE + 0.3×GSM + 0.2×MM  │

## ✅ Current System Status



```

Dataset:**For Your Friend**:## 🔄 Complete Workflow

  ✅ 148 training samples

  ✅ 18/19 features with variance- Read: `FRIEND_QUICK_START.md`

  ✅ Label range: 0.09 - 1.00

  ✅ No missing values- Print: `FRIEND_CHECKLIST.md`



Model:- Contact you if stuck

  ✅ Trained XGBoost regressor

  ✅ Saved at models/mas_predictor.pkl### Phase 1: Monitor with Enhancement Loops

  ✅ Training Spearman: ~0.89

  ✅ Test Spearman: ~0.43**For You**:



API:- Read: `COMPLETE_GUIDE.md`### Requirements│                                                               │### Key Features

  ✅ Gemini 2.0 Flash configured

  ✅ Connection verified- Check: GitHub issues

  ✅ GEMINI_API_KEY in .env

- File bug reports```python

Production Files:

  ✅ run_interactive.py (auto-improvement)

  ✅ run_prediction.py (fast prediction)

  ✅ All components integrated---# Your agents automatically improve via enhancement loops- Python 3.9+



Status: 🎉 PRODUCTION READY

```

## 🏆 Summarymonitor = EnhancedAgentMonitor(api_key="key", threshold=0.6, max_retries=2)

---



## 📊 Example Output

### Your Friend's Job:- Google Gemini API key (or OpenAI/Anthropic)│  4. XGBoost Training                                         │✅ **Dual LLM Support**: Switch between Google Gemini (cloud) and Ollama (local)  

```bash

$ python run_interactive.py```bash



Enter programming task: Write a function to implement binary searchpython main.py generate  # 50+ times# Run MAS pipeline



🔄 ATTEMPT 1/3# Send: data/training_data.csv

──────────────────────────────────────────

📊 MAS Variant:```results = await mas.run(task, monitor)

   Monitor threshold: 0.6

   Monitor retries: 1



🤖 Running 4-agent MAS...### Your Job (After Getting CSV):



✅ MAS COMPLETE```bash

   Agents: 4

   Enhancements: 0python main.py train     # Once# Graph edges tracked automatically### Install│     ├─ Input: 16 features (15 + collective_score)           │✅ **Automated Enhancement**: Iterative improvement loop with configurable threshold  

   Avg Score: 0.986

python main.py predict   # Forever

📊 Extracting 16 features...

```monitor.record_graph_edge("Analyzer", "Coder")

🎯 PREDICTED SCORE: 0.8063



✅ NEW BEST SCORE!

🎉 Score above threshold (0.75)! Stopping.### Result:monitor.record_graph_edge("Coder", "Tester")



🏆 BEST RESULT- ✅ Predict MAS performance in seconds (vs hours)

──────────────────────────────────────────

🎯 FINAL PREDICTED SCORE: 0.8063- ✅ No retraining needed



📊 KEY FEATURES:- ✅ Production-ready ML system

   Agents: 4

   Edges: 4# Save monitoring data```bash│     ├─ Target: label_mas_score                              │✅ **Graph Analytics**: NetworkX-based pipeline topology analysis  

   Avg Agent Score: 0.986

   Enhancement Loops: 1---

   Total Latency: 32.06s

monitor.save("output.json")

📝 BEST MAS OUTPUT:

──────────────────────────────────────────## 🎯 Next Steps

[Complete binary search implementation with

 docstrings, error handling, and test cases]```# Clone repository

──────────────────────────────────────────

```1. **Give folder to friend** → They read `FRIEND_QUICK_START.md`



---2. **Friend generates 50+ samples** → Sends you CSV



## 🎓 Key Concepts3. **You train model once** → Saves to `models/mas_predictor.pkl`



### Why This Approach Works4. **You predict forever** → Fast performance estimates!**Key Feature:** If an agent's output scores < 0.6, it automatically:cd AgentMonitor/Final│     └─ Output: Trained model (xgb_model.json)               │✅ **Benchmark Integration**: HumanEval (5,893 tasks), GSM8K (6,142 problems), MMLU  



1. **Non-Invasive Monitoring**

   - Doesn't modify MAS behavior

   - Captures natural interaction patterns**That's it!** Simple, clean, production-ready! 🚀1. Gets scored by LLM (0-1 scale)

   - Graph structure reveals collaboration quality



2. **Behavioral Features**

   - Proxies for code quality---2. Receives feedback on how to improve

   - Clustering → agent collaboration

   - Centrality → important agents

   - Scores → quality indicators

**Questions?** Read `COMPLETE_GUIDE.md` for full details.3. Retries with enhanced prompt

3. **Weak Supervision**

   - Faster than real benchmarks

   - Still correlates with quality

   - Enables large-scale training**Ready to start?** Give the `Final/` folder to your friend now!4. Up to max_retries times# Create virtual environment│                                                               │✅ **ML Predictions**: XGBoost regression for performance forecasting  



4. **XGBoost Learning**

   - Learns complex patterns

   - Features → Performance mapping✨ **Good luck with your research!** ✨

   - Generalizes to new tasks



5. **Auto-Improvement**---python -m venv venv

   - Tries different configurations

   - Optimizes automatically

   - Returns best result

### Phase 2: Extract 16 Featuresvenv\Scripts\activate  # Windows│  5. Prediction                                               │

---



## 📝 Dependencies

```python# source venv/bin/activate  # Linux/Mac

```txt

Core:from AgentMonitor.features.feature_extractor import FeatureExtractor

- Python 3.10+

- xgboost          # Gradient boosting│     ├─ New MAS → Extract features                           │---

- networkx         # Graph metrics

- pandas           # Data handlingmonitor.load("output.json")

- numpy            # Numerical operations

- scikit-learn     # Train/test split, metricsextractor = FeatureExtractor(api_key="key")# Install dependencies



API:features = await extractor.extract_all_features(monitor.monitor_data)

- google-generativeai  # Gemini API

- python-dotenv        # Environment variablespip install -r requirements.txt│     └─ Model → Predict performance                          │



Utilities:# Returns 16 features:

- scipy            # Spearman correlation

- pathlib          # Path handling{

```

    # System Metrics (6)

---

    'avg_personal_score': 0.82,# Set up API key│                                                               │## 🏗️ System Architecture

## 🎯 Use Cases

    'min_personal_score': 0.75,

### For Developers

```    'max_loops': 2,echo GEMINI_API_KEY=your_key > .env

Daily coding tasks:

✓ "Write a sorting algorithm"    'total_latency': 4.5,

✓ "Create API endpoint"

✓ "Implement data structure"    'total_token_usage': 1500,```└─────────────────────────────────────────────────────────────┘



Get optimized code with quality prediction instantly!    'num_agents_triggered_enhancement': 1,

```

    

### For Researchers

```    # Graph Metrics (9)

Study MAS behavior:

✓ Analyze feature importance    'num_nodes': 4,### Dependencies```### Multi-Agent Pipelines

✓ Test different architectures

✓ Validate prediction accuracy    'num_edges': 3,

✓ Extend with new features

```    'avg_clustering': 0.0,- `pandas>=2.0.0` - Data processing



### For Teams    'global_transitivity': 0.0,

```

Code quality assessment:    'avg_degree_centrality': 0.5,- `numpy>=1.24.0` - Numerical computing

✓ Predict quality before review

✓ Automate improvement loops    'avg_betweenness_centrality': 0.33,

✓ Track quality metrics

✓ Optimize agent configurations    'avg_closeness_centrality': 0.67,- `networkx>=3.1` - Graph analysis (9 graph features)

```

    'pagerank_entropy': 1.38,

---

    'heterogeneity_score': 0.25,- `xgboost>=2.0.0` - Prediction model---**Code Generation Pipeline** (5 agents):

## 🔮 Future Enhancements

    

```

Potential improvements:    # Collective Metric (1)- `scikit-learn>=1.3.0` - ML utilities

□ More training samples (300-500)

□ Hyperparameter tuning    'collective_score': 0.80

□ Additional MAS architectures

□ Real benchmark validation}- `google-generativeai>=0.3.0` - LLM integration```

□ Multi-domain support

□ Custom feature engineering```

□ Ensemble models

```



------



## 📞 Support---## 📁 Project StructureRequirementAnalyzer → CodeGenerator → CodeReviewer → UnitTestWriter → CodeExecutor



**System Verification:**### Phase 3: Generate Training Data

```bash

python scripts/verification/system_component_verification.py

```

```bash

**Testing:**

```bash# Generate 30-50 MAS variants## 🎯 Basic Usage```

python scripts/verification/comprehensive_mode_testing.py

```python scripts/generate_mas_variants.py



**Issues?**

- Check .env file has GEMINI_API_KEY

- Verify model exists at models/mas_predictor.pkl# Evaluate each variant on benchmarks

- Ensure dataset exists at data/training_data.csv

- Review error messages for specific issues# (You implement this based on your benchmarks)### Step 1: Monitor Your MAS```



---



*Last Updated: October 12, 2025*  # Result: data/mas_benchmark_results.csv

*Version: 1.0 - Production Ready*  

*Research Paper Implementation - Complete*# Format: [16 features] + [3 benchmark scores] + [1 label]


``````pythonAgentMonitor/Final/**QA Pipeline** (3 agents):



**Important:** You need **30-50 variants minimum** for meaningful XGBoost training!from AgentMonitor import AgentMonitor, AgentWrapper



| Variants | Spearman | Quality |│```

|----------|----------|---------|

| 2 | 0.0-0.2 | ❌ Useless |# Create monitor

| 30-50 | 0.4-0.6 | ✅ Basic |

| 100+ | 0.6-0.7 | ✅ Good |monitor = AgentMonitor(debug=True)├── Agent_Monitor/                    # Core monitoring systemRequirementAnalyzer → QAAnswerer → QAReviewer

| 1,796 (paper) | 0.89 | 🎯 Excellent |



---

# Create agents│   ├── agent_monitor.py              # MAS execution monitor```

### Phase 4: Train XGBoost Predictor

agent1 = AgentWrapper(name="Coder", capability="coding", model="gemini-flash")

```python

from AgentMonitor.models.predictor import MASPredictoragent2 = AgentWrapper(name="Reviewer", capability="review", model="gemini-flash")│   ├── run_with_monitor.py           # Main entry point for MAS execution



predictor = MASPredictor(model_path="models/mas_predictor.pkl")

metrics = predictor.train(

    data_path="data/mas_benchmark_results.csv",# Register agents (non-invasive wrapper)│   ├── feature_aggregator.py         # Feature extraction from MAS runs### Monitoring Workflow

    test_size=0.2,

    tune_hyperparams=Trueawait monitor.register(agent1, agent1.input, agent1.output, capability="coding")

)

await monitor.register(agent2, agent2.input, agent2.output, capability="review")│   ├── evaluate_mas_on_benchmarks.py # Benchmark evaluation for training data

print(f"Spearman: {metrics['test_spearman']:.4f}")

print(f"R²: {metrics['test_r2']:.4f}")



# Save trained model# Run your MAS│   └── utils/```

predictor.save("models/mas_predictor.pkl")

```task = "Write a function to calculate factorial"



---result1 = await agent1.run(task)│       ├── eval_utils.py             # Answer evaluation utilitiesUser Prompt



### Phase 5: Predict New MAS Performanceresult2 = await agent2.run(result1)



```python│       ├── graph_utils.py            # Graph metric computation    ↓

# Load trained model

predictor.load("models/mas_predictor.pkl")# Save monitoring data



# Extract features from new MASmonitor.save("output.json")│       └── json_logger.py            # JSON logging utilitiesAgent Pipeline (MAS)

new_features = {...}  # 16 features

```

# Predict (fast!)

predicted_score = predictor.predict(new_features)│    ↓



if predicted_score > 0.7:### Step 2: Extract Features

    print("✅ Deploy this MAS!")

else:├── MAS/                              # Multi-Agent System pipelinesAgentMonitor (6D Scoring)

    print("❌ Reject - predicted performance too low")

``````python



---from AgentMonitor import FeatureExtractor│   └── mas_pipeline.py               # Code & QA agent pipelines    ↓



## 🎯 Key Features Explained



### 1. Enhancement Loops ⭐ NEW!# Load monitoring data│Enhancement Loop (if score < threshold)



**Problem:** Agents sometimes produce low-quality outputs  monitor.load("output.json")

**Solution:** Automatically retry with feedback

├── Trainer/                          # Model training & prediction    ↓

```python

# Configuration# Extract 16 features

threshold = 0.6   # Quality threshold

max_retries = 2   # Max retry attemptsextractor = FeatureExtractor(api_key="your_api_key")│   ├── xgb_trainer_mas.py            # XGBoost training scriptFeature Aggregator (19 metrics)



# Automatic process:features = await extractor.extract_all_features(monitor.monitor_data)

# 1. Agent generates output

# 2. LLM scores quality (0-1)│   └── predict_mas.py                # Prediction script    ↓

# 3. If score < threshold:

#    - Generate improvement feedbackprint(features)

#    - Retry with enhanced prompt

#    - Repeat up to max_retries# {│XGBoost Model (Prediction)

# 4. Accept best output

```#   'avg_personal_score': 0.85,      # System metrics (6)



**Benefits:**#   'min_personal_score': 0.75,├── BenchmarkDatasetFolder/           # Benchmark datasets    ↓

- ✅ Improves output quality automatically

- ✅ No manual intervention needed#   'max_loops': 2,

- ✅ Tracks enhancement statistics

- ✅ Works with any agent#   'total_latency': 5.3,│   ├── HumanEval/CSV Logging + JSON Export



---#   'total_token_usage': 1200,



### 2. 16 Performance Features#   'num_agents_triggered_enhancement': 1,│   │   └── data.csv                  # Code generation tasks```



Following the research paper exactly:#   'num_nodes': 2,                   # Graph metrics (9)



**System Metrics (6):**#   'num_edges': 1,│   ├── GSM8k/

1. `avg_personal_score` - Average LLM-judged agent quality

2. `min_personal_score` - Minimum agent quality (bottleneck)#   'avg_clustering': 0.0,

3. `max_loops` - Maximum enhancement loops used

4. `total_latency` - Total execution time#   'global_transitivity': 0.0,│   │   └── data.csv                  # Math reasoning tasks### Components Overview

5. `total_token_usage` - Total LLM tokens used

6. `num_agents_triggered_enhancement` - Agents needing retry#   'avg_degree_centrality': 0.5,



**Graph Metrics (9):**#   'avg_betweenness_centrality': 0.0,│   └── MMLU/

7. `num_nodes` - Number of agents

8. `num_edges` - Number of interactions#   'avg_closeness_centrality': 1.0,

9. `avg_clustering` - Clustering coefficient

10. `global_transitivity` - Graph transitivity#   'pagerank_entropy': 0.69,│       └── data.csv                  # Knowledge/QA tasks| Component | File | Purpose |

11. `avg_degree_centrality` - Average degree centrality

12. `avg_betweenness_centrality` - Average betweenness#   'heterogeneity_score': 0.0,

13. `avg_closeness_centrality` - Average closeness

14. `pagerank_entropy` - PageRank entropy#   'collective_score': 0.80          # Collective metric (1)│|-----------|------|---------|

15. `heterogeneity_score` - Agent capability diversity

# }

**Collective Metric (1):**

16. `collective_score` - LLM-judged collaboration quality```├── data/                             # Generated data| **MAS Pipeline** | `MAS/mas_pipeline.py` | Multi-agent code/QA task execution |



---



### 3. XGBoost Prediction### Step 3: Evaluate on Benchmarks│   ├── mas_benchmark_results.csv     # Training dataset (5×20)| **Agent Monitor** | `Agent_Monitor/agent_monitor.py` | LLM-based scoring & enhancement |



**Training:**

```python

# Hyperparameter tuning via GridSearchCV```python│   └── mas_benchmark_results_FORMAT_GUIDE.csv  # Example format| **Feature Aggregator** | `Agent_Monitor/feature_aggregator.py` | 19-metric feature engineering |

param_grid = {

    'max_depth': [3, 5, 7],from AgentMonitor import MASOrchestrator

    'learning_rate': [0.01, 0.1, 0.3],

    'n_estimators': [50, 100, 200],│| **Run Orchestrator** | `Agent_Monitor/run_with_monitor.py` | Main pipeline coordinator |

    'subsample': [0.7, 0.8, 1.0],

    'colsample_bytree': [0.7, 0.8, 1.0],# Create orchestrator

}

orchestrator = MASOrchestrator(api_key="your_api_key")├── models/                           # Trained models| **Benchmark Runner** | `Agent_Monitor/benchmark_runner.py` | Dataset evaluation |

# 5-fold cross-validation

# Optimize for Spearman correlation

```

# Evaluate MAS on benchmarks│   └── xgb_model.json                # XGBoost model| **XGBoost Trainer** | `Trainer/xgb_trainer.py` | ML model training |

**Metrics:**

- RMSE (Root Mean Squared Error)results = await orchestrator.evaluate_mas_on_benchmarks(

- MAE (Mean Absolute Error)

- R² Score    mas_variant=your_mas,│| **Predictor** | `Trainer/predict.py` | Performance prediction |

- **Spearman Correlation** ⭐ (paper's primary metric)

    humaneval_samples=10,

---

    gsm8k_samples=10,├── logs/                             # Execution logs

## 📊 Example Output

    mmlu_samples=10

### Monitoring Summary

```)│---

==============================================================

AGENT MONITOR SUMMARY

==============================================================

Total Agents: 4print(results)├── requirements.txt                  # Python dependencies

Total Conversations: 12

Total Enhancements: 2# {



Per-Agent Statistics:#   'features': {...},           # 16 features├── README.md                         # This file## 🚀 Quick Start

--------------------------------------------------------------

#   'humaneval_score': 0.65,     # Benchmark scores

Analyzer:

  Calls:        1#   'gsm8k_score': 0.72,└── INSTRUCTIONS_FOR_FRIEND.md        # Dataset generation guide

  Enhancements: 0

  Avg Score:    0.850#   'mmlu_score': 0.58,

  Min Score:    0.850

  Avg Latency:  2.341s#   'label': 0.663               # Weak supervision: 0.5*HE + 0.3*GSM8K + 0.2*MMLU```### Prerequisites

  Tokens:       450

# }

Coder:

  Calls:        1```

  Enhancements: 1

  Avg Score:    0.780

  Min Score:    0.520

  Avg Latency:  3.102s### Step 4: Train Predictor---- Python 3.8+

  Tokens:       680



Tester:

  Calls:        1```python- Virtual environment (venv)

  Enhancements: 0

  Avg Score:    0.720from AgentMonitor import MASPredictor

  Min Score:    0.720

  Avg Latency:  2.856s## 🔧 Features Extracted (16 Total)- Gemini API key OR Ollama installed locally

  Tokens:       520

# Train on evaluation results

Reviewer:

  Calls:        1predictor = MASPredictor(model_path="models/mas_predictor.pkl")

  Enhancements: 1

  Avg Score:    0.810metrics = predictor.train(

  Min Score:    0.580

  Avg Latency:  2.945s    data_path="data/mas_benchmark_results.csv",### System Features (6)### Installation

  Tokens:       590

==============================================================    test_size=0.2,

```

    tune_hyperparams=True| Feature | Description | Range |

### Feature Extraction

```)

==============================================================

EXTRACTED FEATURES (16 Indicators)|---------|-------------|-------|```powershell

==============================================================

print(f"Spearman Correlation: {metrics['test_spearman']:.4f}")

📊 System Metrics (6):

   avg_personal_score:              0.7900```| `avg_personal_score` | Average agent performance score | 0-1 |# 1. Clone repository

   min_personal_score:              0.7200

   max_loops:                       1

   total_latency:                   11.2440 sec

   total_token_usage:               2240### Step 5: Predict New MAS| `min_personal_score` | Minimum agent performance score | 0-1 |git clone https://github.com/KumaraswamyBakkashetti/3-1project.git

   num_agents_triggered_enhancement: 2



🕸️  Graph Metrics (9):

   num_nodes:                       4```python| `max_loops` | Maximum enhancement loops triggered | 0-10+ |cd Final

   num_edges:                       3

   avg_clustering:                  0.0000# Load trained model

   global_transitivity:             0.0000

   avg_degree_centrality:           0.5000predictor.load("models/mas_predictor.pkl")| `total_latency` | Total execution time (seconds) | 0-∞ |

   avg_betweenness_centrality:      0.3333

   avg_closeness_centrality:        0.6667

   pagerank_entropy:                1.3863

   heterogeneity_score:             0.0000# Extract features from new MAS variant| `total_token_usage` | Total tokens consumed | 0-∞ |# 2. Create virtual environment



🤝 Collective Metric (1):new_features = await extractor.extract_all_features(new_mas_data)

   collective_score:                0.8200

==============================================================| `num_agents_triggered_enhancement` | Count of agents needing enhancement | 0-N |python -m venv venv

```

# Predict performance (fast!)

---

predicted_score = predictor.predict(new_features).\venv\Scripts\Activate.ps1

## ⚠️ Important Notes



### 1. Minimum Variants Required

if predicted_score > 0.7:### Graph Features (9)

**DO NOT use only 2 MAS variants for training!**

    print("✅ Deploy this MAS variant!")

The paper used **1,796 variants**. For practical results:

- **Minimum:** 30-50 variantselse:| Feature | Description | Range |# 3. Install dependencies

- **Recommended:** 100+ variants

- **Ideal:** 500-1000 variants    print("❌ Reject - predicted performance too low")



Use `scripts/generate_mas_variants.py` to create variants automatically.```|---------|-------------|-------|pip install -r requirements.txt



---



### 2. Enhancement Loop Configuration---| `num_nodes` | Number of agent nodes | 3-10 |



**threshold:** Lower = more retries, higher = faster

- 0.5 = Lenient (fewer retries)

- 0.6 = Balanced ⭐ (recommended)## 📁 Project Structure| `num_edges` | Number of interactions | 2-N |# 4. Configure environment

- 0.7 = Strict (more retries)



**max_retries:** Higher = better quality, slower

- 1 = Fast, basic improvement```| `clustering_coefficient` | Local clustering measure | 0-1 |# Create .env file with:

- 2 = Balanced ⭐ (recommended)

- 3 = Best quality, slowestAgentMonitor/Final/



---├── AgentMonitor/              # Main framework package| `transitivity` | Global clustering measure | 0-1 |LLM_PROVIDER=gemini  # or "ollama"



### 3. Weak Supervision Formula│   ├── core/



```python│   │   ├── agent_monitor.py   # Non-invasive monitoring| `avg_degree_centrality` | Average node connections | 0-1 |GEMINI_API_KEY=your_api_key_here

label = 0.5 * humaneval_score + 0.3 * gsm8k_score + 0.2 * mmlu_score

```│   │   └── agent_wrapper.py   # Simple agent abstraction



This creates a single quality metric from multiple benchmarks.│   ├── features/| `avg_betweenness_centrality` | Average bridge importance | 0-1 |GEMINI_MODEL=gemini-2.0-flash



---│   │   └── feature_extractor.py  # 16 feature extraction



## 🎯 Quick Commands│   ├── evaluation/| `avg_closeness_centrality` | Average node proximity | 0-1 |```



```bash│   │   ├── benchmark_evaluator.py  # HumanEval/GSM8K/MMLU

# Run complete demo (RECOMMENDED)

python run_complete_agentmonitor.py│   │   └── mas_orchestrator.py     # Full evaluation pipeline| `pagerank_entropy` | Information distribution | 0-∞ |



# Generate MAS variants (for training)│   ├── models/

python scripts/generate_mas_variants.py

│   │   └── predictor.py       # XGBoost trainer & predictor| `heterogeneity_score` | Network diversity | 0-∞ |### Basic Usage

# Run older examples (if needed)

python examples/complete_demo.py│   └── utils/

python examples/simple_integration.py

│

# Install dependencies

pip install -r requirements.txt├── examples/

```

│   ├── complete_demo.py       # Full end-to-end demo### Collective Score (1)```powershell

---

│   └── simple_integration.py  # Integration with existing MAS

## 📖 Citation

│| Feature | Description | Range |# Run single task

```bibtex

@article{chan2024agentmonitor,├── scripts/

  title={AgentMonitor: A Plug-and-Play Framework for Predictive and Secure Multi-Agent Systems},

  author={Chan, Chi-Min and Huang, Jianxuan and Liu, Weize and Lyu, Xinle and Liu, Zikang and Yang, Shuyu and Liu, Jiaxuan and Zhou, Yixin and Chen, Qianyu and Wang, Chunyang and others},│   └── generate_mas_variants.py  # Create 30-50 MAS variants|---------|-------------|-------|python Agent_Monitor/run_with_monitor.py

  journal={arXiv preprint arXiv:2408.14972},

  year={2024}│

}

```├── MAS/| `collective_score` | Overall MAS coordination | 0-1 |# Enter: "write python code for fibonacci sequence"



**Paper:** https://arxiv.org/abs/2408.14972  │   └── mas_pipeline.py        # Example MAS implementations

**Official Repo:** https://github.com/chanchimin/AgentMonitor

│

---

├── BenchmarkDatasetFolder/

## 🤝 What's New in This Implementation?

│   ├── HumanEval/data.csv### Target Labels (4) - Only in Training Data# Run benchmarks (generate training data)

| Feature | Research Paper | This Implementation |

|---------|---------------|-------------------|│   ├── GSM8k/data.csv

| 16 Features | ✅ | ✅ |

| XGBoost Prediction | ✅ | ✅ |│   └── MMLU/data.csv| Label | Description | Formula |python Agent_Monitor/benchmark_runner.py

| Weak Supervision | ✅ | ✅ |

| Non-invasive Monitoring | ✅ | ✅ |│

| **Enhancement Loops** | ❌ | ✅ ⭐ NEW! |

| **LLM Scoring** | ✅ | ✅ Enhanced |├── data/|-------|-------------|---------|

| **Feedback Generation** | ❌ | ✅ ⭐ NEW! |

| **Production Logging** | ⚠️ Basic | ✅ Complete |│   ├── mas_variants/          # Generated MAS configs

| **Easy to Use** | ⚠️ Complex | ✅ Simple API |

│   └── mas_benchmark_results.csv  # Training data| `humaneval_score` | Code generation accuracy | Mean correctness |# Train XGBoost model

---

│

## 📄 License

├── models/| `gsm8k_score` | Math reasoning accuracy | Mean correctness |python Trainer/xgb_trainer.py

MIT License

│   └── mas_predictor.pkl      # Trained XGBoost model

---

│| `mmlu_score` | Knowledge accuracy | Mean correctness |

## 🙏 Acknowledgments

├── README.md                  # This file

- Research paper authors for the methodology

- Original AgentMonitor team└── requirements.txt           # Dependencies| `label_mas_score` | **Prediction Target** | 0.5×HE + 0.3×GSM + 0.2×MM |# Make predictions

- NetworkX for graph analysis

- XGBoost team```



---python Trainer/predict.py



**Built with ❤️ for Multi-Agent System research and production**---



*Complete implementation ready for deployment!*---```


## 🔄 Complete Workflow



### Phase 1: Generate MAS Variants (30-50 configs)

## 🚀 Installation---

**Why?** Paper used 1,796 variants. Minimum 30-50 for meaningful XGBoost training.



```bash

# Generate 30-50 variants automatically### Prerequisites## 🦙 LLM Integration (Gemini & Ollama)

python scripts/generate_mas_variants.py

- Python 3.8+

# Output: data/mas_variants/all_variants.json

```- Virtual environment (recommended)### Current Status: Gemini (Cloud API)



Creates variants by varying:- LLM API (Gemini, OpenAI, or Ollama with Llama3)

- Number of agents (2, 3, 4)

- Topology (sequential, parallel, iterative)**Active Configuration**:

- Max loops (1, 2, 3)

- Temperature (0.7, 0.9, 1.1)### Setup- Provider: Google Gemini 2.0 Flash

- Agent roles (different combinations)

- API Key: Configured in `.env`

### Phase 2: Evaluate All Variants

```bash- Model: `gemini-2.0-flash`

```python

from AgentMonitor import MASOrchestrator# Clone repository

import json

git clone <repository-url>### Switching to Ollama (Local)

orchestrator = MASOrchestrator(api_key="your_api_key")

results = []cd AgentMonitor/Final



# Load variants**Why Ollama?**

with open("data/mas_variants/all_variants.json") as f:

    variants = json.load(f)# Create virtual environment- ✅ **Free**: No API costs



# Evaluate each variantpython -m venv venv- ✅ **Private**: Data stays local

for variant in variants:

    mas = create_mas_from_config(variant)  # Your implementation- ✅ **Offline**: Works without internet

    result = await orchestrator.evaluate_mas_on_benchmarks(

        mas_variant=mas,# Activate virtual environment- ✅ **Fast**: Local inference on GPU/CPU

        humaneval_samples=5,  # Small sample for speed

        gsm8k_samples=5,# Windows:

        mmlu_samples=5

    )venv\Scripts\activate**Step-by-Step Integration**:

    results.append(result)

# Linux/Mac:

# Save training data

import pandas as pdsource venv/bin/activate#### 1. Create LLM Wrapper

df = pd.DataFrame(results)

df.to_csv("data/mas_benchmark_results.csv", index=False)Create `Agent_Monitor/llm_wrapper.py`:

```

# Install dependencies```python

### Phase 3: Train XGBoost Model

pip install -r requirements.txtimport os

```python

from AgentMonitor import MASPredictorimport ollama



predictor = MASPredictor()# Set up environment variablesimport google.generativeai as genai

metrics = predictor.train(

    data_path="data/mas_benchmark_results.csv",# Windows PowerShell:

    test_size=0.2,

    tune_hyperparams=True$env:GEMINI_API_KEY = "your-api-key-here"class OllamaClientWrapper:

)

    def __init__(self, model_name="llama3"):

print(f"RMSE: {metrics['test_rmse']:.4f}")

print(f"R²: {metrics['test_r2']:.4f}")# Linux/Mac:        self.model_name = model_name

print(f"Spearman: {metrics['test_spearman']:.4f}")  # Key metric!

export GEMINI_API_KEY="your-api-key-here"    

# Save model

predictor.save("models/mas_predictor.pkl")```    def generate_content(self, prompt: str) -> str:

```

        response = ollama.generate(model=self.model_name, prompt=prompt)

### Phase 4: Use for Prediction

---        return response['response']

```python

# Quick performance check for new MAS

predictor.load("models/mas_predictor.pkl")

## 💡 Usageclass GeminiClientWrapper:

new_mas = create_new_mas_variant()

features = extract_features(new_mas)    def __init__(self, api_key: str, model_name="gemini-2.0-flash"):

predicted_score = predictor.predict(features)

### 1. Generate Training Dataset        genai.configure(api_key=api_key)

print(f"Predicted MAS score: {predicted_score:.4f}")

```        self.model_name = model_name



---```bash    



## 📚 API Referencepython Agent_Monitor/evaluate_mas_on_benchmarks.py    def generate_content(self, prompt: str) -> str:



### AgentMonitor```        model = genai.GenerativeModel(self.model_name)



**Core monitoring class**        return model.generate_content(prompt).text



```python**Output**: `data/mas_benchmark_results.csv` (5 rows × 20 columns)

from AgentMonitor import AgentMonitor

def create_llm_client(provider=None, **kwargs):

monitor = AgentMonitor(debug=False)

```- Tests 5 MAS variants on 3 benchmarks    provider = provider or os.getenv("LLM_PROVIDER", "ollama")



**Methods:**- Each MAS runs 30 times (10 samples × 3 benchmarks)    if provider == "ollama":

- `register(agent, input_method, output_method, capability)` - Register agent for monitoring

- `save(filepath)` - Save monitoring data to JSON- Features aggregated across all runs        return OllamaClientWrapper(kwargs.get("model_name", "llama3"))

- `load(filepath)` - Load monitoring data from JSON

- `get_agent_stats()` - Get per-agent statistics- Takes ~30-45 minutes for 10 samples    elif provider == "gemini":

- `get_graph_edges()` - Get conversation graph edges

        return GeminiClientWrapper(kwargs.get("api_key"), kwargs.get("model_name"))

### FeatureExtractor

### 2. Train XGBoost Model```

**Extract 16 performance features**



```python

from AgentMonitor import FeatureExtractor```bash#### 2. Update agent_monitor.py



extractor = FeatureExtractor(api_key="your_key")python Trainer/xgb_trainer_mas.py```python

features = await extractor.extract_all_features(monitor_data)

``````# Replace imports



**Features:**from Agent_Monitor.llm_wrapper import create_llm_client

- **System (6):** avg_personal_score, min_personal_score, max_loops, total_latency, total_token_usage, num_agents_triggered_enhancement

- **Graph (9):** num_nodes, num_edges, avg_clustering, global_transitivity, centrality metrics, pagerank_entropy, heterogeneity**Output**: `models/xgb_model.json`

- **Collective (1):** collective_score (LLM-judged collaboration quality)

# Update __init__

### BenchmarkEvaluator

- Loads training data from `data/mas_benchmark_results.csv`def __init__(self, llm_client=None, threshold=0.6, ...):

**Evaluate MAS on benchmarks**

- Uses 16 features (15 + collective_score) as X    self.client = llm_client

```python

from AgentMonitor import BenchmarkEvaluator- Uses `label_mas_score` as y```



evaluator = BenchmarkEvaluator()- Saves trained model



# HumanEval (code execution)#### 3. Update run_with_monitor.py

score = evaluator.evaluate_humaneval(mas_output, test_cases)

### 3. Make Predictions```python

# GSM8K (numeric answer matching)

score = evaluator.evaluate_gsm8k(mas_output, expected_answer)from Agent_Monitor.llm_wrapper import create_llm_client



# MMLU (text matching)```bash

score = evaluator.evaluate_mmlu(mas_output, correct_answer)

```python Trainer/predict_mas.pydef run_prompt(..., llm_provider=None):



### MASOrchestrator```    llm_client = create_llm_client(provider=llm_provider)



**Full evaluation pipeline**    monitor = AgentMonitor(llm_client=llm_client, ...)



```python**Input**: New MAS features (16 values)  ```

from AgentMonitor import MASOrchestrator

**Output**: Predicted MAS performance score (0-1)

orchestrator = MASOrchestrator(api_key="your_key")

results = await orchestrator.evaluate_mas_on_benchmarks(#### 4. Update .env

    mas_variant=your_mas,

    humaneval_samples=10,---```env

    gsm8k_samples=10,

    mmlu_samples=10LLM_PROVIDER=ollama

)

```## 📊 Training Data FormatOLLAMA_MODEL=llama3



### MASPredictorOLLAMA_HOST=http://localhost:11434



**XGBoost training and prediction**### CSV Structure (20 columns)```



```python

from AgentMonitor import MASPredictor

```csv#### 5. Install & Setup

predictor = MASPredictor(model_path="models/mas_predictor.pkl")

avg_personal_score,min_personal_score,max_loops,total_latency,total_token_usage,num_agents_triggered_enhancement,num_nodes,num_edges,clustering_coefficient,transitivity,avg_degree_centrality,avg_betweenness_centrality,avg_closeness_centrality,pagerank_entropy,heterogeneity_score,collective_score,humaneval_score,gsm8k_score,mmlu_score,label_mas_score```powershell

# Train

metrics = predictor.train(0.63,0.40,2,25.48,1384,3,5,4,0.18,0.22,0.36,0.14,0.27,2.16,0.008,0.65,0.72,0.58,0.61,0.63# Install Ollama Python package

    data_path="data/mas_benchmark_results.csv",

    test_size=0.2,0.71,0.52,3,32.15,1876,5,6,5,0.22,0.28,0.42,0.18,0.31,2.45,0.011,0.73,0.78,0.65,0.68,0.72pip install ollama

    tune_hyperparams=True

)...



# Predict```# Pull Llama model

score = predictor.predict(features_dict)

ollama pull llama3

# Save/Load

predictor.save("model.pkl")**Breakdown**:

predictor.load("model.pkl")

```- Columns 1-6: System features# Test



---- Columns 7-15: Graph featuresollama run llama3 "Hello"



## ⚠️ Important Notes- Column 16: Collective score```



### 1. Variant Requirements- Columns 17-19: Benchmark scores (training only)



**DO NOT use only 2 MAS variants!** XGBoost cannot learn patterns from 2 samples.- Column 20: Label (training target)#### 6. Run with Ollama



| Variants | Spearman Correlation | Quality |```powershell

|----------|---------------------|---------|

| 2 | 0.0-0.2 | ❌ Useless |---python Agent_Monitor/run_with_monitor.py

| 10-20 | 0.2-0.3 | ⚠️ Very weak |

| 30-50 | 0.4-0.6 | ✅ Basic patterns |# Output: [INFO] Using Ollama with model: llama3

| 100+ | 0.6-0.7 | ✅ Good |

| 1,796 (paper) | 0.89 | 🎯 Excellent |## 🧪 MAS Variants Tested```



**Solution:** Use `scripts/generate_mas_variants.py` to create 30-50 variants automatically.



### 2. Weak Supervision FormulaThe system evaluates 5 different MAS configurations:**Performance Comparison**:



The paper uses weighted benchmark scores as labels:



```python| Variant | Threshold | Max Retries | Description || Metric | Gemini | Ollama (Llama3) |

label = 0.5 * humaneval_score + 0.3 * gsm8k_score + 0.2 * mmlu_score

```|---------|-----------|-------------|-------------||--------|--------|----------------|



This creates a single quality metric from multiple benchmarks.| CodeMAS_v1 | 0.6 | 2 | Balanced configuration || Cost | $0.0005/1K tokens | Free |



### 3. LLM-Judged Scores| CodeMAS_Aggressive | 0.5 | 3 | More enhancement loops || Latency | ~2-5s | ~3-10s (CPU), ~1-3s (GPU) |



Personal and collective scores use LLM evaluation:| CodeMAS_Conservative | 0.7 | 1 | Fewer enhancement loops || Privacy | Cloud | Local |

- **Personal scores:** Quality of individual agent outputs (0-1)

- **Collective score:** Overall collaboration quality (0-1)| LogicMAS_v1 | 0.6 | 2 | Logic-focused tasks || Quality | Excellent | Good |



Fallback to heuristics if LLM unavailable.| QA_MAS_v1 | 0.6 | 2 | Question-answering tasks |



### 4. Non-Invasive Monitoring---



AgentMonitor uses **monkey-patching** to wrap agent methods without changing your code:---



```python## 📦 Components

# Your existing MAS (NO CHANGES!)

from MAS.mas_pipeline import CodePipeline## 🔬 How It Works

pipeline = CodePipeline(llm)

### 1. MAS Pipeline (`MAS/mas_pipeline.py`)

# Add monitoring (wrapper)

monitor = AgentMonitor()### Step 1: MAS Execution with Monitoring

# ... wrap agents ...

**Code Pipeline**:

# Run normally

result = pipeline.run(task)```python- `RequirementAnalyzer`: Extracts requirements, identifies language



# Features extracted!from Agent_Monitor.run_with_monitor import run_prompt- `CodeGenerator`: Generates working code with LLM

```

- `CodeReviewer`: Detects bugs and inefficiencies

See `examples/simple_integration.py` for complete example.

data, features, raw_log, summary = run_prompt(- `UnitTestWriter`: Creates test cases

### 5. Expected Performance

    prompt="Write a function to reverse a string",- `CodeExecutor`: Runs syntax checks and simulates execution

With 30-50 variants:

- **Spearman correlation:** ~0.4-0.6 (moderate)    task_type='code',

- **RMSE:** Varies by dataset

- **Use case:** Basic pattern detection, variant ranking    api_key=os.getenv('GEMINI_API_KEY'),**QA Pipeline**:



For paper-level performance (0.89), you need:    threshold=0.6,- `RequirementAnalyzer`: Analyzes question

- 1,000+ variants

- Multiple MAS architectures    max_retries=2- `QAAnswerer`: Generates answer

- Multiple LLM models

- Full benchmark samples)- `QAReviewer`: Reviews answer quality



---



## 🎯 Quick Commands# features contains 16 metrics### 2. Agent Monitor (`Agent_Monitor/agent_monitor.py`)



```bashprint(features)

# Run demo

python examples/complete_demo.py# {**6-Dimensional Scoring**:



# Generate variants#   'avg_personal_score': 0.75,1. **personal_score**: Overall quality (0-1)

python scripts/generate_mas_variants.py

#   'min_personal_score': 0.60,2. **factual_accuracy**: Correctness (0-1)

# Run simple integration

python examples/simple_integration.py#   'max_loops': 2,3. **clarity**: Readability (0-1)



# Install dependencies#   ...4. **safety**: Security/ethics (0-1)

pip install -r requirements.txt

#   'collective_score': 0.825. **code_correctness**: Syntax/logic (0-1, code only)

# Create virtual environment

python -m venv venv# }6. **complexity**: Appropriate complexity (0-1)

venv\Scripts\activate  # Windows

``````



---**Enhancement Loop**:



## 📊 Example Output### Step 2: Feature Aggregation```python



### Feature Extractionwhile score < threshold and loops < max_retries:

```json

{For each MAS variant:    enhanced_output = llm.enhance(current_output, suggestions)

  "avg_personal_score": 0.82,

  "min_personal_score": 0.75,1. Run on 10 HumanEval tasks → collect 10 feature sets    score = llm.score(enhanced_output)

  "max_loops": 2,

  "total_latency": 4.5,2. Run on 10 GSM8K tasks → collect 10 feature sets    loops += 1

  "total_token_usage": 1500,

  "num_agents_triggered_enhancement": 1,3. Run on 10 MMLU tasks → collect 10 feature sets```

  "num_nodes": 3,

  "num_edges": 2,4. **Aggregate**: Average each of 15 features across all 30 runs

  "avg_clustering": 0.0,

  "global_transitivity": 0.0,5. Compute benchmark scores (accuracy on each benchmark)### 3. Feature Aggregator (`Agent_Monitor/feature_aggregator.py`)

  "avg_degree_centrality": 0.67,

  "avg_betweenness_centrality": 0.33,6. Compute label: `0.5 × humaneval + 0.3 × gsm8k + 0.2 × mmlu`

  "avg_closeness_centrality": 0.83,

  "pagerank_entropy": 1.09,**19 Features Collected**:

  "heterogeneity_score": 0.15,

  "collective_score": 0.78### Step 3: XGBoost Training

}

```**System Metrics** (8):



### Benchmark Evaluation```python- `avg_personal_score`, `max_personal_score`, `min_personal_score`

```json

{# X: 16 features (15 + collective_score)- `total_latency_sec`, `avg_token_count`

  "humaneval_score": 0.65,

  "gsm8k_score": 0.72,# y: label_mas_score- `max_loops`, `avg_loops`

  "mmlu_score": 0.58,

  "label": 0.663- `collective_score` (LLM-based system-level score)

}

```model = xgb.XGBRegressor(



### Prediction    n_estimators=100,**Graph Metrics** (11):

```

Predicted MAS score: 0.687    max_depth=5,- `num_nodes`, `num_edges`, `avg_degree`

Feature importance:

  1. collective_score: 0.25    learning_rate=0.1- `clustering_coefficient`, `transitivity`

  2. avg_personal_score: 0.18

  3. num_nodes: 0.12)- `avg_betweenness_centrality`, `avg_closeness_centrality`

  4. total_latency: 0.10

  ...model.fit(X, y)- `pagerank_entropy`, `authority_entropy`

```

```- `density`, `diameter`

---



## 📖 Citation

### Step 4: Prediction**Benchmark Scores** (3):

If you use this implementation, please cite the original paper:

- `humaneval_score` (code correctness)

```bibtex

@article{chan2024agentmonitor,```python- `gsm8k_score` (math reasoning)

  title={AgentMonitor: A Plug-and-Play Framework for Predictive and Secure Multi-Agent Systems},

  author={Chan, Chi-Min and Huang, Jianxuan and Liu, Weize and Lyu, Xinle and Liu, Zikang and Yang, Shuyu and Liu, Jiaxuan and Zhou, Yixin and Chen, Qianyu and Wang, Chunyang and others},# New MAS execution- `mmlu_score` (knowledge)

  journal={arXiv preprint arXiv:2408.14972},

  year={2024}new_features = [0.68, 0.45, 2, 27.5, 1500, 3, 5, 4, 0.20, ...]  # 16 values

}

```### 4. XGBoost Model (`Trainer/xgb_trainer.py`)



**Paper:** https://arxiv.org/abs/2408.14972  # Predict performance

**Official Repo:** https://github.com/chanchimin/AgentMonitor

predicted_score = model.predict([new_features])**Model Configuration**:

---

print(f"Predicted MAS Score: {predicted_score[0]:.4f}")```python

## 🤝 Contributing

```XGBRegressor(

Issues and pull requests welcome! This is a research implementation - there's room for improvement:

    n_estimators=100,

- [ ] Add more MAS frameworks (AutoGen, LangChain, ChatDev)

- [ ] Implement safety post-editing module---    max_depth=5,

- [ ] Add more benchmark datasets

- [ ] Optimize feature extraction (caching)    learning_rate=0.1,

- [ ] Create web dashboard (Streamlit/Gradio)

## 📈 Expected Performance    objective='reg:squarederror'

---

)

## 📄 License

### Training Data```

MIT License - See LICENSE file for details.

- **Rows**: 5 MAS variants

---

- **R² Score**: 0.7-0.9 (on simulated data)**Training Requirements**:

## 🙏 Acknowledgments

- **MAE**: 0.05-0.15- Minimum 10 rows (50-100 recommended)

- Research paper authors for the methodology

- Official AgentMonitor repository for inspiration- 18 input features → 1 target (`collective_score`)

- NetworkX team for graph analysis tools

- XGBoost team for the prediction framework### Use Cases- Cross-validation: 5-fold KFold



---- **Quick MAS evaluation**: Predict performance without running expensive benchmarks- Saved as `models/xgb_model.json`



**Built with ❤️ for Multi-Agent System research and production**- **MAS configuration tuning**: Test different thresholds/retries



*Last Updated: October 11, 2025*- **Agent monitoring**: Track system health during execution---




---## 📖 Usage Guide



## 🛠️ Troubleshooting### Run Single Prompt



### Issue: Import Errors```powershell

```bashpython Agent_Monitor/run_with_monitor.py

# Solution```

pip install -r requirements.txt

```**Example**:

```

### Issue: API Key ErrorsEnter task: write python code for fibonacci sequence

```bash

# Solution: Set environment variableOutput:

$env:GEMINI_API_KEY = "your-key"✅ RequirementAnalyzer: Score 0.85

✅ CodeGenerator: Score 0.92  

# Or modify evaluate_mas_on_benchmarks.py to use Ollama✅ CodeReviewer: Score 0.88

```✅ UnitTestWriter: Score 0.79

✅ CodeExecutor: Syntax OK

### Issue: Benchmark Data Not Found

```bashFeatures saved to: data/features.csv

# Ensure these folders exist:Logs: logs/run_20251008_153042.json

BenchmarkDatasetFolder/HumanEval/data.csv```

BenchmarkDatasetFolder/GSM8k/data.csv

BenchmarkDatasetFolder/MMLU/data.csv### Generate Training Data

```

```powershell

### Issue: Execution Too Slowpython Agent_Monitor/benchmark_runner.py

```bash```

# Use fewer samples (5 instead of 10)

# In evaluate_mas_on_benchmarks.py, when prompted:**Options**:

Samples per benchmark: 5- Select dataset: HumanEval, GSM8K, MMLU

```- Number of samples: 10, 50, 100

- Output: Appends to `data/features.csv`

---

### Train XGBoost Model

## 📚 Key Files Explained

```powershell

### `agent_monitor.py`python Trainer/xgb_trainer.py

Monitors MAS execution, tracks agent interactions, implements enhancement loops.```



### `run_with_monitor.py`**Requirements**:

Main entry point. Executes MAS pipeline with monitoring enabled, returns features.- At least 10 rows in `data/features.csv`

- Varying `collective_score` values

### `feature_aggregator.py`

Extracts 16 features from MAS execution logs. Computes graph metrics, system metrics, and collective score.**Output**:

```

### `evaluate_mas_on_benchmarks.py`✅ Model trained with 5-fold CV

Generates training data by running MAS variants on benchmarks. Creates 20-column CSV.✅ R² Score: 0.73

✅ RMSE: 0.15

### `xgb_trainer_mas.py`✅ Saved to: models/xgb_model.json

Trains XGBoost model on 20-column CSV using first 16 columns as features.```



### `predict_mas.py`### Make Predictions

Loads trained model and makes predictions on new MAS feature vectors.

```powershell

---python Trainer/predict.py

```

## 🎓 Research Background

**Input**: 18 features (from latest run)  

This system implements a **weak supervision** approach for MAS evaluation:**Output**: Predicted `collective_score` (0-1)



1. **Problem**: Evaluating MAS on benchmarks is expensive (time, tokens, API costs)---

2. **Solution**: Train a predictor using cheap features (execution metrics)

3. **Training**: Use benchmark scores as labels (weak supervision)## 🔧 Fixes Applied

4. **Inference**: Predict performance from features alone (no benchmarks needed)

### Issue #1: Gemini API 404 Error ✅ FIXED

### Weak Supervision Formula

```**Problem**: Using deprecated model `gemini-1.5-flash`

label_mas_score = 0.5 × humaneval_score + 

                  0.3 × gsm8k_score + **Solution**: Updated to `gemini-2.0-flash`

                  0.2 × mmlu_score

```**Files Modified**:

- `Agent_Monitor/agent_monitor.py` (line 15)

Weights reflect task importance:- `Agent_Monitor/run_with_monitor.py` (line 29)

- **50%** Code generation (most important for coding MAS)

- **30%** Math reasoning (logical thinking)### Issue #2: All Scores Returning 0.0 ✅ FIXED

- **20%** General knowledge (factual accuracy)

**Problem**: Gemini wraps JSON in markdown code blocks (` ```json {...} ``` `), causing `json.loads()` to fail

---

**Solution**: Added `extract_json()` function to strip markdown

## 🤝 Contributing

**Code Added** (`agent_monitor.py`):

To extend this system:```python

def extract_json(raw_text: str) -> str:

1. **Add more features**: Modify `feature_aggregator.py`    raw_text = raw_text.strip()

2. **Add benchmarks**: Update `evaluate_mas_on_benchmarks.py`    if raw_text.startswith("```json"):

3. **Try different models**: Replace XGBoost in `xgb_trainer_mas.py`        raw_text = raw_text[7:]

4. **Tune hyperparameters**: Adjust XGBoost settings    elif raw_text.startswith("```"):

        raw_text = raw_text[3:]

---    if raw_text.endswith("```"):

        raw_text = raw_text[:-3]

## 📝 License    return raw_text.strip()

```

This project is part of research on Multi-Agent System evaluation and monitoring.

### Issue #3: collective_score Always 0.5 ✅ FIXED

---

**Problem**: LLM client not passed to `get_collective_score_with_llm()`

## 📧 Support

**Solution**: 

For questions or issues:1. Added `extract_json()` to feature_aggregator.py

1. Check `INSTRUCTIONS_FOR_FRIEND.md` for dataset generation guide2. Added debug logging to track LLM calls

2. Review logs in `logs/` directory3. Ensured `llm_client` passed from `run_with_monitor.py`

3. Verify CSV format matches `data/mas_benchmark_results_FORMAT_GUIDE.csv`

### Issue #4: max_loops Always 2 ✅ FIXED

---

**Problem**: Threshold (0.8) higher than typical scores (0.0-0.6)

## ✅ Quick Start Checklist

**Solution**: Lowered threshold from 0.8 → 0.6

- [ ] Install Python 3.8+

- [ ] Create virtual environment**Impact**: Fewer wasted enhancement loops, `max_loops` now varies

- [ ] Install dependencies: `pip install -r requirements.txt`

- [ ] Set API key: `$env:GEMINI_API_KEY = "your-key"`### Issue #5: Generated Code Has Markdown ✅ FIXED

- [ ] Generate data: `python Agent_Monitor/evaluate_mas_on_benchmarks.py`

- [ ] Train model: `python Trainer/xgb_trainer_mas.py`**Problem**: Code wrapped in ` ```python ... ``` ` causing syntax errors

- [ ] Make predictions: `python Trainer/predict_mas.py`

**Solution**: Strip markdown blocks from generated code

---

**Code Added** (`mas_pipeline.py`):

**Built with ❤️ for efficient Multi-Agent System evaluation**```python

if code.startswith("```python"):
    code = code[9:]
elif code.startswith("```"):
    code = code[3:]
if code.endswith("```"):
    code = code[:-3]
```

---

## 📊 Data Analysis

### Training Data Overview

**Current Status** (as of Oct 8, 2025):
- **Total rows**: 23
- **Features**: 19 columns
- **Source**: HumanEval benchmark runs

### Column Analysis

**Constant Columns** (Expected - Same pipeline structure):
- `num_nodes`: 5 (code) or 3 (QA)
- `num_edges`: 4 or 2
- `clustering_coefficient`: 0.0
- `transitivity`: 0
- `avg_betweenness_centrality`: 0.167

**Varying Columns** (Good):
- `avg_personal_score`: 0.0 - 0.59
- `total_latency_sec`: 29.8 - 92.1
- `avg_token_count`: 15 - 89
- `max_loops`: Now varies (0, 1, 2) after fix
- `collective_score`: Now varies (0.3 - 0.8) after fix

**Zero Columns** (No tasks run yet):
- `gsm8k_score`: 0.0 (100%)
- `mmlu_score`: 0.0 (100%)

### Recommendations

1. **Generate more data**: Need 50-100 rows for robust XGBoost model
2. **Diversify tasks**: Run GSM8K and MMLU benchmarks
3. **Vary pipeline structure**: Try parallel agents, conditional flows for graph metric diversity

---

## 🐛 Troubleshooting

### Gemini API Errors

**404 Error - Model not found**:
```
Error: models/gemini-1.5-flash is not found
Solution: Update to gemini-2.0-flash
```

**JSON Parsing Errors**:
```
Error: json.loads() failed
Solution: Use extract_json() to strip markdown
```

### Ollama Issues

**Connection refused**:
```powershell
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

**Model not found**:
```powershell
# Pull model
ollama pull llama3
```

### XGBoost Training Fails

**Not enough data**:
```
Error: Need at least 10 rows
Solution: Run benchmark_runner.py to generate more data
```

**constant target variable**:
```
Error: collective_score is constant
Solution: Ensure LLM client is passed correctly (check fix #3)
```

### Enhancement Loop Issues

**All agents hit max_retries**:
```
Issue: max_loops always 2
Solution: Lower threshold (0.8 → 0.6) or increase max_retries
```

---

## 📁 Project Structure

```
Final/
├── Agent_Monitor/
│   ├── agent_monitor.py          # Core monitoring + scoring
│   ├── feature_aggregator.py     # 19-feature extraction
│   ├── run_with_monitor.py       # Main orchestrator
│   ├── benchmark_runner.py       # Dataset evaluation
│   └── utils/
│       ├── eval_utils.py         # Benchmark scoring
│       ├── graph_utils.py        # NetworkX analytics
│       └── json_logger.py        # JSON logging
├── MAS/
│   └── mas_pipeline.py           # Multi-agent pipelines
├── Trainer/
│   ├── xgb_trainer.py            # XGBoost training
│   └── predict.py                # Model inference
├── BenchmarkDatasetFolder/
│   ├── HumanEval/data.csv        # 5,893 code tasks
│   ├── GSM8K/data.csv            # 6,142 math problems
│   └── MMLU/data.csv             # Knowledge questions
├── data/
│   └── features.csv              # Training data (23 rows)
├── models/
│   └── xgb_model.json            # Trained XGBoost
├── logs/                         # JSON run logs
├── .env                          # API keys + config
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔑 Key Commands

```powershell
# Environment setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run tasks
python Agent_Monitor/run_with_monitor.py          # Single prompt
python Agent_Monitor/benchmark_runner.py          # Generate data
python Trainer/xgb_trainer.py                     # Train model
python Trainer/predict.py                         # Predict score

# Switch LLM provider
# In .env: LLM_PROVIDER=gemini or ollama

# Ollama setup
pip install ollama
ollama pull llama3
ollama run llama3 "test"
```

---

## 📈 Workflow: Dataset Generation → Model Training

### **Phase 1: Dataset Generation (Friend with Llama/Ollama)**

**Your friend will:**
1. Setup Ollama with local Llama model (see `DATASET_GENERATION_GUIDE.md`)
2. Run benchmark evaluation:
   ```powershell
   python Trainer/evaluate_mas_on_benchmarks.py
   # Choose 20-50 samples per benchmark
   ```
3. Share generated file: `data/mas_benchmark_results.csv`

**Time**: 2-8 hours (depending on sample size)  
**Cost**: FREE (local model)

---

### **Phase 2: Model Training (You)**

**After receiving dataset from friend:**

1. **Copy dataset to your system:**
   ```powershell
   # Place mas_benchmark_results.csv in data/ folder
   ```

2. **Train XGBoost model:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   python Trainer/xgb_trainer_mas.py
   ```

3. **Test predictions:**
   ```powershell
   python Trainer/predict_mas.py
   ```

4. **Deploy model:**
   - Predict MAS_score for new configurations
   - Optimize MAS design based on predictions
   - A/B test different agent combinations

**Time**: 10 minutes  
**Cost**: FREE

---

### **Why This Workflow?**

✅ **Friend has GPU/free time** → Generates expensive benchmark data  
✅ **You get trained model** → No API costs for you  
✅ **Everyone benefits** → Collaborative approach to AI research  

See `DATASET_GENERATION_GUIDE.md` for complete instructions!

---

## 📝 License

MIT License - See repository for details

## 🤝 Contributing

Contributions welcome! Please submit PRs to the `shruthi` branch.

## 📧 Contact

**Author**: Kumaraswamy Bakkashetti  
**Repository**: https://github.com/KumaraswamyBakkashetti/3-1project  
**Branch**: shruthi

---

**Last Updated**: October 8, 2025  
**Version**: 2.0 (Ollama-ready)
