"""
Comprehensive test suite verifying all 36 Research Paper implementations across:
  - Pillar I: AI Edge Agents (Papers 01–12)
  - Pillar II: Graph-Loop Creative Pipelines (Papers 13–24)
  - Pillar III: Network Economics Distributions (Papers 25–36)
  - Cross-Pillar Scenarios A, B, and C
  - Monorepo scaffold file existence (Rust, TypeScript, Solidity, Embedded C/Rust, SQLite, Python)
  - CLI subcommands (`list`, `inspect`, `run-pillar`, `scenario`, `verify-all`)
"""

from __future__ import annotations

import io
import json
import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from research_ecosystem.catalog import (
    PAPERS_CATALOG,
    get_paper,
    list_papers,
    run_paper,
    run_pillar,
    run_scenario,
    verify_all_systems,
)
from research_ecosystem.cli import main as cli_main
from research_ecosystem.pillar1_edge import (
    run_paper_01,
    run_paper_02,
    run_paper_03,
    run_paper_04,
    run_paper_05,
    run_paper_06,
    run_paper_07,
    run_paper_08,
    run_paper_09,
    run_paper_10,
    run_paper_11,
    run_paper_12,
)
from research_ecosystem.pillar2_creative import (
    run_paper_13,
    run_paper_14,
    run_paper_15,
    run_paper_16,
    run_paper_17,
    run_paper_18,
    run_paper_19,
    run_paper_20,
    run_paper_21,
    run_paper_22,
    run_paper_23,
    run_paper_24,
)
from research_ecosystem.pillar3_economics import (
    run_paper_25,
    run_paper_26,
    run_paper_27,
    run_paper_28,
    run_paper_29,
    run_paper_30,
    run_paper_31,
    run_paper_32,
    run_paper_33,
    run_paper_34,
    run_paper_35,
    run_paper_36,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPillar1EdgeAgents(unittest.TestCase):
    def test_paper_01_speculative_streaming(self) -> None:
        res = run_paper_01()
        self.assertTrue(res["passed"])
        self.assertGreater(res["sustained_tok_per_sec"], 120.0)
        self.assertEqual(res["accepted_tokens"], [11, 22, 33, 44, 77])

    def test_paper_02_delta_kv_cache(self) -> None:
        res = run_paper_02()
        self.assertTrue(res["passed"])
        self.assertEqual(res["sink_count"], 4)
        self.assertGreater(res["cosine_similarity"], 0.98)
        self.assertLess(res["ram_footprint_mb"], 50.0)

    def test_paper_03_micro_lora_hot_swap(self) -> None:
        res = run_paper_03()
        self.assertTrue(res["passed"])
        self.assertLess(res["max_swap_latency_ms"], 5.0)
        self.assertNotEqual(res["output_reviewer"], res["output_safety"])

    def test_paper_04_edge_gossip_crdt(self) -> None:
        res = run_paper_04()
        self.assertTrue(res["passed"])
        self.assertTrue(res["all_nodes_converged"])
        self.assertEqual(res["converged_set"], ["task_alpha", "task_gamma"])

    def test_paper_05_microcontroller_dfa_guardrail(self) -> None:
        res = run_paper_05()
        self.assertTrue(res["passed"])
        self.assertEqual(res["safe_verdict"], "GUARD_PASS")
        self.assertEqual(res["injection_verdict"], "GUARD_TRAP")
        self.assertEqual(res["overflow_verdict"], "GUARD_BUFFER_OVERFLOW")

    def test_paper_06_asymmetric_vlm_distillation(self) -> None:
        res = run_paper_06()
        self.assertTrue(res["passed"])
        self.assertGreaterEqual(res["inference_fps"], 60.0)
        self.assertLess(res["power_watts"], 10.0)

    def test_paper_07_dp_federated_dpo(self) -> None:
        res = run_paper_07()
        self.assertTrue(res["passed"])
        self.assertLessEqual(res["privacy_epsilon"], 1.5)
        self.assertAlmostEqual(res["clipped_grad_norm"], 1.0, places=4)

    def test_paper_08_thermal_adaptive_budgeting(self) -> None:
        res = run_paper_08()
        self.assertTrue(res["passed"])
        self.assertGreater(res["cool_schedule"]["active_layers"], res["warm_schedule"]["active_layers"])
        self.assertEqual(res["hot_schedule"]["active_layers"], 8)

    def test_paper_09_sqlite_vss_pq_adc(self) -> None:
        res = run_paper_09()
        self.assertTrue(res["passed"])
        self.assertEqual(res["top_results"][0][0], 101)

    def test_paper_10_transactional_cow_sandbox(self) -> None:
        res = run_paper_10()
        self.assertTrue(res["passed"])
        self.assertFalse(res["bad_turn_committed"])
        self.assertTrue(res["byte_exact_rollback"])

    def test_paper_11_acoustic_cascade(self) -> None:
        res = run_paper_11()
        self.assertTrue(res["passed"])
        self.assertEqual(res["stages_triggered"], [1, 2, 3])
        self.assertLess(res["average_idle_power_mw"], 1.0)

    def test_paper_12_bnf_grammar_logit_mask(self) -> None:
        res = run_paper_12()
        self.assertTrue(res["passed"])
        self.assertEqual(res["decoded_json"], '{"action":"search"}')
        self.assertEqual(res["syntax_error_rate"], 0.0)


class TestPillar2CreativePipelines(unittest.TestCase):
    def test_paper_13_deterministic_frame_engine(self) -> None:
        res = run_paper_13()
        self.assertTrue(res["passed"])
        self.assertTrue(res["hash_identical_runs"])
        self.assertLess(res["seam_position_error"], 1e-9)

    def test_paper_14_identity_latent_anchoring(self) -> None:
        res = run_paper_14()
        self.assertTrue(res["passed"])
        self.assertGreater(res["char1_face_similarity"], 0.95)
        self.assertGreater(res["char2_face_similarity"], 0.95)
        self.assertLess(res["identity_cross_bleed"], 0.05)

    def test_paper_15_non_executive_bible_monitor(self) -> None:
        res = run_paper_15()
        self.assertTrue(res["passed"])
        self.assertEqual(res["caught_violations_count"], 3)
        self.assertEqual(res["bad_route"], "script_agent")
        self.assertEqual(res["good_route"], "art_agent")

    def test_paper_16_constraint_layout_ilp(self) -> None:
        res = run_paper_16()
        self.assertTrue(res["passed"])
        self.assertEqual(res["overflow_incidents"], 0)

    def test_paper_17_audio_visual_seam_smoother(self) -> None:
        res = run_paper_17()
        self.assertTrue(res["passed"])
        self.assertEqual(res["post_smooth_seam_jitter"], 0.0)

    def test_paper_18_delaunay_balloon_router(self) -> None:
        res = run_paper_18()
        self.assertTrue(res["passed"])
        self.assertEqual(res["obstacle_collisions"], 0)

    def test_paper_19_dual_loop_narrative_graph(self) -> None:
        res = run_paper_19()
        self.assertTrue(res["passed"])
        self.assertGreaterEqual(res["pacing_score"], 8.5)

    def test_paper_20_dirty_gradient_colorizer(self) -> None:
        res = run_paper_20()
        self.assertTrue(res["passed"])
        self.assertTrue(res["strict_swatch_match"])

    def test_paper_21_forensic_prompt_compiler(self) -> None:
        res = run_paper_21()
        self.assertTrue(res["passed"])
        self.assertTrue(res["denoise_contract_satisfied"])
        self.assertGreaterEqual(res["m1_denoise"], 0.35)
        self.assertLessEqual(res["m1_denoise"], 0.48)

    def test_paper_22_automated_visual_qa_gate(self) -> None:
        res = run_paper_22()
        self.assertTrue(res["passed"])
        self.assertTrue(res["clean_panel_passed"])
        self.assertFalse(res["corrupted_panel_passed"])

    def test_paper_23_wireframe_blockout_guidance(self) -> None:
        res = run_paper_23()
        self.assertTrue(res["passed"])
        self.assertEqual(res["reprojection_error_px"], 0.0)

    def test_paper_24_editorial_beat_graph_pruner(self) -> None:
        res = run_paper_24()
        self.assertTrue(res["passed"])
        self.assertEqual(res["kept_beats"], ["b1_hook", "b3_betrayal", "b5_climax"])


class TestPillar3NetworkEconomics(unittest.TestCase):
    def test_paper_25_proof_of_attribution_dag(self) -> None:
        res = run_paper_25()
        self.assertTrue(res["passed"])
        self.assertAlmostEqual(res["total_distributed"], 1000.0, places=2)

    def test_paper_26_bancor_bonding_curve(self) -> None:
        res = run_paper_26()
        self.assertTrue(res["passed"])
        self.assertLess(res["solvency_error"], 1e-9)

    def test_paper_27_bitswap_bandwidth_swarm(self) -> None:
        res = run_paper_27()
        self.assertTrue(res["passed"])
        self.assertGreater(res["origin_bandwidth_saved_pct"], 80.0)

    def test_paper_28_l2_micro_state_channel(self) -> None:
        res = run_paper_28()
        self.assertTrue(res["passed"])
        self.assertEqual(res["settled_sequence_k"], 100)

    def test_paper_29_schelling_curator_consensus(self) -> None:
        res = run_paper_29()
        self.assertTrue(res["passed"])
        self.assertEqual(res["consensus_outcome"], 1)
        self.assertEqual(res["slashed_nodes"], ["malicious_cartel"])

    def test_paper_30_zk_model_fingerprint_verifier(self) -> None:
        res = run_paper_30()
        self.assertTrue(res["passed"])
        self.assertTrue(res["licensed_verified"])
        self.assertTrue(res["pirated_rejected"])
        self.assertLess(res["proof_bytes"], 200)

    def test_paper_31_lmsr_prediction_market(self) -> None:
        res = run_paper_31()
        self.assertTrue(res["passed"])
        self.assertAlmostEqual(res["prob_sum"], 1.0, places=5)
        self.assertEqual(res["funded_branches"], [0])

    def test_paper_32_vrf_scarcity_editioner(self) -> None:
        res = run_paper_32()
        self.assertTrue(res["passed"])
        self.assertTrue(res["cap_enforced"])
        self.assertEqual(res["minted_count"], 3)

    def test_paper_33_perpetual_storage_endowment(self) -> None:
        res = run_paper_33()
        self.assertTrue(res["passed"])
        self.assertTrue(res["perpetually_solvent"])

    def test_paper_34_hashcash_anti_sybil_pow(self) -> None:
        res = run_paper_34()
        self.assertTrue(res["passed"])
        self.assertTrue(res["verified"])
        self.assertGreater(res["updated_difficulty"], 8.0)

    def test_paper_35_royalty_cascade_tree(self) -> None:
        res = run_paper_35()
        self.assertTrue(res["passed"])
        self.assertAlmostEqual(res["total_payout"], 100.0, places=3)

    def test_paper_36_agent_labor_double_auction(self) -> None:
        res = run_paper_36()
        self.assertTrue(res["passed"])
        self.assertEqual(res["matched_trades"], 3)
        self.assertEqual(res["clearing_price"], 8.0)


class TestCrossPillarScenariosAndMonorepo(unittest.TestCase):
    def test_scenarios_a_b_c(self) -> None:
        for sid in ("A", "B", "C"):
            res = run_scenario(sid)
            self.assertTrue(res["passed"], f"Scenario {sid} failed")
            self.assertGreaterEqual(len(res["steps"]), 6)

    def test_catalog_and_verify_all(self) -> None:
        self.assertEqual(len(PAPERS_CATALOG), 36)
        self.assertEqual(len(list_papers(1)), 12)
        self.assertEqual(len(list_papers(2)), 12)
        self.assertEqual(len(list_papers(3)), 12)
        summary = verify_all_systems()
        self.assertTrue(summary["all_passed"])
        self.assertEqual(summary["passed_papers"], 36)
        self.assertEqual(summary["passed_scenarios"], 3)

    def test_monorepo_scaffold_files_exist(self) -> None:
        required_files = [
            "Cargo.toml",
            "package.json",
            "pyproject.toml",
            "setup.py",
            "SKILL.md",
            "README.md",
            "HANDOFF_36_PAPERS.md",
            "crates/edge_inference/src/lib.rs",
            "crates/kv_cache/src/lib.rs",
            "crates/edge_mesh/src/lib.rs",
            "crates/sandbox/src/lib.rs",
            "crates/swarm_sync/src/lib.rs",
            "crates/micro_channel/src/lib.rs",
            "crates/pow_limiter/src/lib.rs",
            "crates/agent_market/src/lib.rs",
            "packages/motion_engine/src/index.ts",
            "packages/lettering/src/index.ts",
            "packages/web_curator/src/index.ts",
            "contracts/ProofOfAttribution.sol",
            "contracts/BondingCurveSyndication.sol",
            "contracts/CuratorConsensus.sol",
            "contracts/ZKModelVerifier.sol",
            "contracts/NarrativePredictionMarket.sol",
            "contracts/AlgorithmicEditioning.sol",
            "contracts/StoragePinningEscrow.sol",
            "contracts/RoyaltyCascadeTree.sol",
            "embedded/guardrails/src/lib.rs",
            "embedded/acoustic_cascade/src/acoustic_cascade.c",
            "sqlite_ext/vss_pq.c",
            "scripts/smoke_test_all.sh",
            "scripts/benchmark_edge_throughput.py",
        ]
        for rel in required_files:
            full = REPO_ROOT / rel
            self.assertTrue(full.is_file(), f"Missing required monorepo file: {rel}")

    def test_cli_subcommands(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli_main(["list", "--pillar", "1", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(len(data), 12)

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli_main(["inspect", "15", "--json"])
        self.assertEqual(rc, 0)
        inspected = json.loads(buf.getvalue())
        self.assertEqual(inspected["metadata"]["id"], "15")
        self.assertTrue(inspected["execution"]["passed"])

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli_main(["scenario", "A", "--json"])
        self.assertEqual(rc, 0)
        scen = json.loads(buf.getvalue())
        self.assertTrue(scen["passed"])

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli_main(["verify-all", "--json"])
        self.assertEqual(rc, 0)
        ver = json.loads(buf.getvalue())
        self.assertTrue(ver["all_passed"])


if __name__ == "__main__":
    unittest.main()
