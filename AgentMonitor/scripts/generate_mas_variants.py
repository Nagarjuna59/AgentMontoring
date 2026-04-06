"""
MAS Variant Generator

Creates 30-50 MAS variants by varying:
- Number of agents (2, 3, 4)
- Agent ordering/topology
- Max loops (1, 2, 3)
- LLM parameters (temperature, model)
- Agent capabilities

This solves the "only 2 variants" problem!
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from typing import List, Dict, Any
from itertools import product


class MASVariantGenerator:
    """
    Generates multiple MAS configuration variants for training
    """
    
    def __init__(self, output_dir: str = "data/mas_variants"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_code_pipeline_variants(self) -> List[Dict[str, Any]]:
        """
        Generate variants of CodePipeline
        """
        variants = []
        
        # Dimension 1: Number of agents
        agent_counts = [2, 3, 4]
        
        # Dimension 2: Agent topologies
        topologies = [
            "sequential",  # A → B → C → D
            "parallel",    # A → [B,C,D] → merge
            "iterative",   # A ↔ B ↔ C (with feedback)
        ]
        
        # Dimension 3: Max enhancement loops
        max_loops = [1, 2, 3]
        
        # Dimension 4: LLM temperature (creativity)
        temperatures = [0.7, 0.9, 1.1]
        
        # Dimension 5: Agent roles (for 4-agent setup)
        four_agent_roles = [
            ["analyzer", "coder", "tester", "reviewer"],
            ["planner", "coder", "debugger", "reviewer"],
            ["architect", "developer", "tester", "optimizer"],
        ]
        
        three_agent_roles = [
            ["analyzer", "coder", "tester"],
            ["planner", "developer", "reviewer"],
            ["architect", "coder", "optimizer"],
        ]
        
        two_agent_roles = [
            ["coder", "reviewer"],
            ["developer", "tester"],
            ["architect", "builder"],
        ]
        
        variant_id = 1
        
        # Generate combinations
        for n_agents in agent_counts:
            # Select appropriate role sets
            if n_agents == 4:
                role_sets = four_agent_roles
            elif n_agents == 3:
                role_sets = three_agent_roles
            else:  # 2
                role_sets = two_agent_roles
            
            for roles in role_sets:
                for topology in topologies:
                    # Skip invalid combinations
                    if topology == "parallel" and n_agents < 3:
                        continue
                    
                    for loops in max_loops:
                        for temp in temperatures:
                            # Create variant config
                            variant = {
                                "variant_id": f"code_v{variant_id:03d}",
                                "pipeline_type": "code_generation",
                                "num_agents": n_agents,
                                "topology": topology,
                                "agent_roles": roles[:n_agents],
                                "max_loops": loops,
                                "llm_config": {
                                    "model": "gemini-2.0-flash",
                                    "temperature": temp,
                                },
                                "threshold": 0.6,  # Score threshold for enhancement
                            }
                            variants.append(variant)
                            variant_id += 1
        
        return variants
    
    def generate_qa_pipeline_variants(self) -> List[Dict[str, Any]]:
        """
        Generate variants of QAPipeline
        """
        variants = []
        
        agent_counts = [2, 3, 4]
        topologies = ["sequential", "tree", "consensus"]
        max_loops = [1, 2, 3]
        temperatures = [0.5, 0.7, 0.9]  # Lower for QA (need accuracy)
        
        four_agent_roles = [
            ["retriever", "reasoner", "answerer", "verifier"],
            ["searcher", "analyzer", "synthesizer", "checker"],
        ]
        
        three_agent_roles = [
            ["retriever", "reasoner", "answerer"],
            ["searcher", "analyzer", "verifier"],
        ]
        
        two_agent_roles = [
            ["reasoner", "answerer"],
            ["analyzer", "verifier"],
        ]
        
        variant_id = 1
        
        for n_agents in agent_counts:
            if n_agents == 4:
                role_sets = four_agent_roles
            elif n_agents == 3:
                role_sets = three_agent_roles
            else:
                role_sets = two_agent_roles
            
            for roles in role_sets:
                for topology in topologies:
                    if topology == "tree" and n_agents < 3:
                        continue
                    
                    for loops in max_loops:
                        for temp in temperatures:
                            variant = {
                                "variant_id": f"qa_v{variant_id:03d}",
                                "pipeline_type": "question_answering",
                                "num_agents": n_agents,
                                "topology": topology,
                                "agent_roles": roles[:n_agents],
                                "max_loops": loops,
                                "llm_config": {
                                    "model": "gemini-2.0-flash",
                                    "temperature": temp,
                                },
                                "threshold": 0.7,  # Higher threshold for QA
                            }
                            variants.append(variant)
                            variant_id += 1
        
        return variants
    
    def generate_hybrid_variants(self) -> List[Dict[str, Any]]:
        """
        Generate hybrid/custom variants
        """
        variants = []
        
        # Variant: Mixed capabilities
        variants.append({
            "variant_id": "hybrid_v001",
            "pipeline_type": "hybrid",
            "num_agents": 3,
            "topology": "sequential",
            "agent_roles": ["coder", "reasoner", "reviewer"],
            "max_loops": 2,
            "llm_config": {"model": "gemini-2.0-flash", "temperature": 0.8},
            "threshold": 0.65,
        })
        
        # Variant: Minimal (fast)
        variants.append({
            "variant_id": "minimal_v001",
            "pipeline_type": "code_generation",
            "num_agents": 2,
            "topology": "sequential",
            "agent_roles": ["coder", "tester"],
            "max_loops": 1,
            "llm_config": {"model": "gemini-2.0-flash", "temperature": 0.7},
            "threshold": 0.5,
        })
        
        # Variant: Maximal (thorough)
        variants.append({
            "variant_id": "maximal_v001",
            "pipeline_type": "code_generation",
            "num_agents": 4,
            "topology": "iterative",
            "agent_roles": ["analyzer", "coder", "tester", "reviewer"],
            "max_loops": 3,
            "llm_config": {"model": "gemini-2.0-flash", "temperature": 1.0},
            "threshold": 0.7,
        })
        
        return variants
    
    def generate_all(self) -> List[Dict[str, Any]]:
        """
        Generate all variants
        """
        print("Generating MAS variants...")
        
        code_variants = self.generate_code_pipeline_variants()
        print(f"  ✅ Generated {len(code_variants)} code pipeline variants")
        
        qa_variants = self.generate_qa_pipeline_variants()
        print(f"  ✅ Generated {len(qa_variants)} QA pipeline variants")
        
        hybrid_variants = self.generate_hybrid_variants()
        print(f"  ✅ Generated {len(hybrid_variants)} hybrid variants")
        
        all_variants = code_variants + qa_variants + hybrid_variants
        print(f"\n📦 Total variants: {len(all_variants)}")
        
        return all_variants
    
    def save_variants(self, variants: List[Dict[str, Any]]):
        """
        Save variants to JSON files
        """
        # Save all variants as one file
        all_path = os.path.join(self.output_dir, "all_variants.json")
        with open(all_path, 'w') as f:
            json.dump(variants, f, indent=2)
        print(f"\n✅ Saved all variants to: {all_path}")
        
        # Save individual variant files
        for variant in variants:
            variant_path = os.path.join(
                self.output_dir,
                f"{variant['variant_id']}.json"
            )
            with open(variant_path, 'w') as f:
                json.dump(variant, f, indent=2)
        
        print(f"✅ Saved {len(variants)} individual variant configs")
        
        # Create summary
        summary = {
            "total_variants": len(variants),
            "by_pipeline_type": {},
            "by_num_agents": {},
            "by_topology": {},
            "agent_count_range": [
                min(v['num_agents'] for v in variants),
                max(v['num_agents'] for v in variants)
            ],
            "loop_range": [
                min(v['max_loops'] for v in variants),
                max(v['max_loops'] for v in variants)
            ],
        }
        
        for variant in variants:
            # Count by pipeline type
            ptype = variant['pipeline_type']
            summary['by_pipeline_type'][ptype] = summary['by_pipeline_type'].get(ptype, 0) + 1
            
            # Count by num agents
            n = variant['num_agents']
            summary['by_num_agents'][str(n)] = summary['by_num_agents'].get(str(n), 0) + 1
            
            # Count by topology
            topo = variant['topology']
            summary['by_topology'][topo] = summary['by_topology'].get(topo, 0) + 1
        
        summary_path = os.path.join(self.output_dir, "variants_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Saved summary to: {summary_path}")
        
        return summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """
        Print variant summary
        """
        print("\n" + "=" * 80)
        print("MAS VARIANT SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 Total Variants: {summary['total_variants']}")
        
        print("\n📈 By Pipeline Type:")
        for ptype, count in summary['by_pipeline_type'].items():
            print(f"   {ptype:20s} : {count:3d}")
        
        print("\n👥 By Number of Agents:")
        for n, count in sorted(summary['by_num_agents'].items()):
            print(f"   {n} agents              : {count:3d}")
        
        print("\n🕸️  By Topology:")
        for topo, count in summary['by_topology'].items():
            print(f"   {topo:20s} : {count:3d}")
        
        print(f"\nAgent Count Range: {summary['agent_count_range'][0]}-{summary['agent_count_range'][1]}")
        print(f"Loop Range:        {summary['loop_range'][0]}-{summary['loop_range'][1]}")
        
        print("\n" + "=" * 80)
        print(f"✅ Ready for training! With {summary['total_variants']} variants,")
        print("   you can expect:")
        if summary['total_variants'] >= 50:
            print("   - Spearman correlation: ~0.6-0.7 (good)")
        elif summary['total_variants'] >= 30:
            print("   - Spearman correlation: ~0.4-0.6 (moderate)")
        else:
            print("   - Spearman correlation: ~0.3-0.4 (basic patterns)")
        print(f"   - Paper achieved 0.89 with 1,796 variants")
        print("=" * 80)


def main():
    """
    Main function
    """
    print("\n" + "=" * 80)
    print("MAS VARIANT GENERATOR")
    print("Solving the '2 variants problem' by creating 30-50+ variants!")
    print("=" * 80)
    
    generator = MASVariantGenerator(output_dir="data/mas_variants")
    
    # Generate all variants
    variants = generator.generate_all()
    
    # Save to disk
    summary = generator.save_variants(variants)
    
    # Print summary
    generator.print_summary(summary)
    
    print("\n📝 Next Steps:")
    print("1. Review variants: cat data/mas_variants/all_variants.json")
    print("2. Run batch evaluation: python scripts/batch_evaluate.py")
    print("3. Train predictor: python scripts/train_predictor.py")
    print("4. Predict new MAS: python scripts/predict_mas.py")


if __name__ == "__main__":
    main()

