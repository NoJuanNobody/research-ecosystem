"""
Complete Structured Metadata Catalog & Cross-Pillar Orchestrator for all 36 Research Papers.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from .pillar1_edge import PILLAR_1_RUNNERS
from .pillar2_creative import PILLAR_2_RUNNERS
from .pillar3_economics import PILLAR_3_RUNNERS

PAPERS_CATALOG: List[Dict[str, object]] = [
    # Pillar I: AI Edge Agents (01-12)
    {
        "id": "01",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Sub-4-Bit Speculative Streaming on Edge Silicon",
        "runtime": "C++ / Metal / NEON / Rust",
        "target_metric": ">120 tok/s on 8GB",
        "work_package_files": ["crates/edge_inference/src/lib.rs", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "02",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Stateful Delta-KV Cache Compression Hierarchy",
        "runtime": "Rust / llama.cpp",
        "target_metric": "<50MB RAM for 30d",
        "work_package_files": ["crates/kv_cache/src/lib.rs", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "03",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Micro-LoRA Swarms: Dynamic NPU Hot-Swapping",
        "runtime": "Python / C++ (ONNX)",
        "target_metric": "<5ms swap latency",
        "work_package_files": ["python/micro_lora/adapter_pool.py", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "04",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Edge-to-Edge Gossip Consensus in Ephemeral Meshes",
        "runtime": "Rust (libp2p / BLE)",
        "target_metric": "0-cloud sync; 99% C",
        "work_package_files": ["crates/edge_mesh/src/lib.rs", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "05",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Neuro-Symbolic Guardrails on Microcontrollers",
        "runtime": "Embedded C / Rust (#![no_std])",
        "target_metric": "<200us check latency",
        "work_package_files": ["embedded/guardrails/src/lib.rs", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "06",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Asymmetric VLM Distillation for Edge Robotics",
        "runtime": "PyTorch / TensorRT",
        "target_metric": "60 fps @ <10W power",
        "work_package_files": ["python/robotics_vlm/asymmetric_vlm.py", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "07",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Differentially Private Federated DPO at Edge",
        "runtime": "Python / PySyft",
        "target_metric": "eps <= 1.5; delta 1e-5",
        "work_package_files": ["python/federated_dpo/dp_trainer.py", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "08",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Thermal-Aware Adaptive Token Budgeting on Mobile",
        "runtime": "C++ / Swift / Kotlin / Python",
        "target_metric": "Zero thermal throttle",
        "work_package_files": ["python/thermal_controller/controller.py", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "09",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Edge-Native Vector Indexing in SQLite MMap",
        "runtime": "C / SQLite Extension",
        "target_metric": "<1ms top-k RAG search",
        "work_package_files": ["sqlite_ext/vss_pq.c", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "09" if False else "10",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Fault-Tolerant Speculative Agent Tool Sandboxing",
        "runtime": "Rust / WASM / btrfs",
        "target_metric": "Zero dirty mutations",
        "work_package_files": ["crates/sandbox/src/lib.rs", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "11",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Acoustic Cascades for Zero-Shot Ambient Agents",
        "runtime": "C / CMSIS-DSP",
        "target_metric": "<1mW always-on idle",
        "work_package_files": ["embedded/acoustic_cascade/src/acoustic_cascade.c", "research_ecosystem/pillar1_edge.py"],
    },
    {
        "id": "12",
        "pillar": 1,
        "pillar_name": "AI Edge Agents",
        "title": "Grammar-Guided BNF Decoding for Logit Constraints",
        "runtime": "C++ / llama.cpp",
        "target_metric": "0% JSON syntax error",
        "work_package_files": ["research_ecosystem/pillar1_edge.py"],
    },
    # Pillar II: Graph-Loop Creative Pipelines (13-24)
    {
        "id": "13",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Deterministic Time-Indexed Frame Synthesis Engine",
        "runtime": "TypeScript / Canvas",
        "target_metric": "Hash-identical runs",
        "work_package_files": ["packages/motion_engine/src/index.ts", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "14",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Persistent Identity Latent Anchoring in Panels",
        "runtime": "PyTorch / FLUX / IP",
        "target_metric": ">95% face similarity",
        "work_package_files": ["python/creative_pipeline/identity_anchor.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "15",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Non-Executive World Bible Consistency Monitors",
        "runtime": "Python / LangGraph",
        "target_metric": "0 lore contradictions",
        "work_package_files": ["python/creative_pipeline/bible_monitor.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "16",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Constraint Layout Optimization via ILP Graphs",
        "runtime": "Python / OR-Tools",
        "target_metric": "0 panel text overflow",
        "work_package_files": ["python/layout_engine/solver.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "17",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Audio-Driven Visual Seam Smoothing in Loops",
        "runtime": "Python (librosa)",
        "target_metric": "0-jitter loop seam",
        "work_package_files": ["python/motion_audio/seam_smoother.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "18",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Delaunay Triangulation for Comic Lettering Tails",
        "runtime": "TypeScript / Canvas",
        "target_metric": "0 balloon collisions",
        "work_package_files": ["packages/lettering/src/index.ts", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "19",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Dual-Loop Hierarchical Narrative Script Graphs",
        "runtime": "Python / Pydantic",
        "target_metric": "Pacing score >= 8.5",
        "work_package_files": ["python/creative_pipeline/narrative_graph.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "20",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Harmonic Mood Palettes & Dirty Gradient Shading",
        "runtime": "Python / OpenCV",
        "target_metric": "Strict ASE/ACO match",
        "work_package_files": ["python/color_lab/dirty_gradient.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "21",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Forensic Prompt Manifest Compilers from Beats",
        "runtime": "Python / Jinja2",
        "target_metric": "100% prompt determinism",
        "work_package_files": ["python/creative_pipeline/prompt_compiler.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "22",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Automated Visual QA via Multi-Scale Distance",
        "runtime": "Python (ArcFace/CLIP)",
        "target_metric": "<2% undetected drift",
        "work_package_files": ["python/creative_pipeline/visual_qa.py", "research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "23",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "3D Wireframe Blockout Guidance for Spaces",
        "runtime": "Blender Python API",
        "target_metric": "100% perspective sync",
        "work_package_files": ["research_ecosystem/pillar2_creative.py"],
    },
    {
        "id": "24",
        "pillar": 2,
        "pillar_name": "Graph-Loop Creative Pipelines",
        "title": "Autonomous Narrative Pacing & Beat Graph Pruning",
        "runtime": "Python / NetworkX",
        "target_metric": "0 flat narrative acts",
        "work_package_files": ["python/creative_pipeline/graph_pruner.py", "research_ecosystem/pillar2_creative.py"],
    },
    # Pillar III: Network Economics Distributions (25-36)
    {
        "id": "25",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Proof-of-Creative-Attribution DAG Ledgers",
        "runtime": "Rust / Merkle DAG / Solidity",
        "target_metric": "O(1) royalty lookup",
        "work_package_files": ["contracts/ProofOfAttribution.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "26",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Dynamic Bonding Curves for Content Syndication",
        "runtime": "Solidity / Foundry",
        "target_metric": "Zero slippage drain",
        "work_package_files": ["contracts/BondingCurveSyndication.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "27",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Decentralized Bandwidth Swarms for Diffusion P2P",
        "runtime": "Rust (libp2p / bitswap)",
        "target_metric": ">80% bandwidth saved",
        "work_package_files": ["crates/swarm_sync/src/lib.rs", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "28",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Agent-to-Agent Micro-Streaming State Channels",
        "runtime": "Rust / L2 Lightning",
        "target_metric": "<1ms settlement, $0 fee",
        "work_package_files": ["crates/micro_channel/src/lib.rs", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "29",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Proof-of-Human-In-The-Loop Staked Consensus",
        "runtime": "Solidity / Web3 / TypeScript",
        "target_metric": ">99% BFT accuracy",
        "work_package_files": [
            "contracts/CuratorConsensus.sol",
            "packages/web_curator/src/index.ts",
            "research_ecosystem/pillar3_economics.py",
        ],
    },
    {
        "id": "30",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Zero-Knowledge Model Fingerprint Verification",
        "runtime": "Circom / snarkjs / Solidity",
        "target_metric": "zk-SNARK proof <200B",
        "work_package_files": ["contracts/ZKModelVerifier.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "31",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Prediction Market Orchestration of Franchises",
        "runtime": "Solidity (AMM Gnosis / LMSR)",
        "target_metric": "Efficient price disc",
        "work_package_files": ["contracts/NarrativePredictionMarket.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "32",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Algorithmic Scarcity & Editioning Protocols",
        "runtime": "Solidity / Chainlink VRF",
        "target_metric": "Verifiable VRF runs",
        "work_package_files": ["contracts/AlgorithmicEditioning.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "33",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Decentralized Storage Pinning Smart Escrows",
        "runtime": "EVM / Filecoin / Arweave",
        "target_metric": "100% data durability",
        "work_package_files": ["contracts/StoragePinningEscrow.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "34",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Anti-Sybil Proof-of-Compute for Edge Agent Swarms",
        "runtime": "C++ / Rust (Hashcash)",
        "target_metric": "0 spam / 0 API keys",
        "work_package_files": ["crates/pow_limiter/src/lib.rs", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "35",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Dynamic Royalty Cascades for Derivative Remixes",
        "runtime": "Solidity / Foundry",
        "target_metric": "Arbitrary depth tree",
        "work_package_files": ["contracts/RoyaltyCascadeTree.sol", "research_ecosystem/pillar3_economics.py"],
    },
    {
        "id": "36",
        "pillar": 3,
        "pillar_name": "Network Economics Distributions",
        "title": "Nash Equilibrium in Autonomous Agent Labor Market",
        "runtime": "Python / Rust (Double Auction)",
        "target_metric": "Stable market clear",
        "work_package_files": ["crates/agent_market/src/lib.rs", "research_ecosystem/pillar3_economics.py"],
    },
]

ALL_RUNNERS: Dict[str, Callable[[], Dict[str, object]]] = {
    **PILLAR_1_RUNNERS,
    **PILLAR_2_RUNNERS,
    **PILLAR_3_RUNNERS,
}

SCENARIO_DEFINITIONS: Dict[str, Dict[str, object]] = {
    "A": {
        "scenario_id": "A",
        "name": "The Autonomous 1-Person Animation Studio",
        "papers": ["19", "15", "21", "01", "23", "14", "22", "16", "13", "17", "25", "28"],
        "description": (
            "End-to-end autonomous pipeline from Dual-Loop Script (19) and Bible Gate (15) "
            "through Prompt Compiler (21), Sub-4-Bit Edge Streamer (01), 3D Blockout (23), "
            "Identity Anchor (14), Visual QA (22), Constraint Layout (16), Frame Engine f(t) (13), "
            "Audio Seam Loop (17), and Proof-of-Attribution + Micro-Channel settlement (25, 28)."
        ),
    },
    "B": {
        "scenario_id": "B",
        "name": "Distributed Edge Intelligence with Zero Central Cloud",
        "papers": ["01", "02", "05", "10", "04", "28"],
        "description": (
            "On-device agent executing via Sub-4-Bit Speculative Streaming (01) and Delta-KV Cache (02), "
            "protected by Microcontroller DFA Guardrails (05) and CoW Transactional Sandbox (10), "
            "coordinating over Ephemeral Gossip CRDT Mesh (04) and settling via L2 State Channels (28)."
        ),
    },
    "C": {
        "scenario_id": "C",
        "name": "Community-Driven Franchise Syndication",
        "papers": ["31", "19", "15", "29", "26", "35"],
        "description": (
            "Audience greenlights story arcs via LMSR Prediction Markets (31), triggering Dual-Loop "
            "Script (19) and Bible Gate (15), audited by Schelling-Point Staked Curators (29), "
            "published on Dynamic Bonding Curves (26), and splitting remix revenue via Royalty Cascades (35)."
        ),
    },
}


def normalize_paper_id(paper_id: str | int) -> str:
    return f"{int(str(paper_id).strip()):02d}"


def get_paper(paper_id: str | int) -> Dict[str, object]:
    pid = normalize_paper_id(paper_id)
    for entry in PAPERS_CATALOG:
        if entry["id"] == pid:
            return entry
    raise KeyError(f"Paper ID '{paper_id}' not found (valid range: 01..36)")


def list_papers(pillar: Optional[int] = None) -> List[Dict[str, object]]:
    if pillar is None:
        return list(PAPERS_CATALOG)
    return [entry for entry in PAPERS_CATALOG if entry["pillar"] == pillar]


def run_paper(paper_id: str | int) -> Dict[str, object]:
    pid = normalize_paper_id(paper_id)
    if pid not in ALL_RUNNERS:
        raise KeyError(f"Runner for Paper ID '{pid}' not found")
    return ALL_RUNNERS[pid]()


def run_pillar(pillar: str | int) -> List[Dict[str, object]]:
    p_str = str(pillar).strip().lower()
    if p_str == "all":
        return [ALL_RUNNERS[f"{i:02d}"]() for i in range(1, 37)]
    p_int = int(p_str)
    if p_int == 1:
        return [PILLAR_1_RUNNERS[f"{i:02d}"]() for i in range(1, 13)]
    if p_int == 2:
        return [PILLAR_2_RUNNERS[f"{i:02d}"]() for i in range(13, 25)]
    if p_int == 3:
        return [PILLAR_3_RUNNERS[f"{i:02d}"]() for i in range(25, 37)]
    raise ValueError(f"Invalid pillar '{pillar}'; expected 1, 2, 3, or all")


def run_scenario(scenario_id: str) -> Dict[str, object]:
    sid = scenario_id.strip().upper()
    if sid not in SCENARIO_DEFINITIONS:
        raise KeyError(f"Unknown scenario '{scenario_id}' (expected A, B, or C)")
    spec = SCENARIO_DEFINITIONS[sid]
    paper_ids: List[str] = list(spec["papers"])
    step_results = [run_paper(pid) for pid in paper_ids]
    all_passed = all(bool(r.get("passed")) for r in step_results)
    return {
        "scenario_id": sid,
        "name": spec["name"],
        "description": spec["description"],
        "papers_executed": paper_ids,
        "steps": step_results,
        "passed": all_passed,
    }


def verify_all_systems() -> Dict[str, object]:
    paper_results = run_pillar("all")
    scenario_results = {sid: run_scenario(sid) for sid in ("A", "B", "C")}
    passed_papers = sum(1 for r in paper_results if r.get("passed"))
    passed_scenarios = sum(1 for s in scenario_results.values() if s.get("passed"))
    return {
        "total_papers": len(paper_results),
        "passed_papers": passed_papers,
        "total_scenarios": len(scenario_results),
        "passed_scenarios": passed_scenarios,
        "all_passed": passed_papers == 36 and passed_scenarios == 3,
        "papers": paper_results,
        "scenarios": scenario_results,
    }
