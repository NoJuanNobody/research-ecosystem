#!/usr/bin/env python3
"""
Automated performance and throughput benchmark suite for Pillar I Edge Inference (Paper 01)
and full 36-paper ecosystem verification.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_ecosystem.catalog import verify_all_systems
from research_ecosystem.pillar1_edge import run_paper_01


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark Edge Speculative Streaming Throughput")
    parser.add_argument("--target-tok-per-sec", type=float, default=100.0)
    args = parser.parse_args()

    p01 = run_paper_01()
    tok_s = float(p01["sustained_tok_per_sec"])
    summary = verify_all_systems()

    report = {
        "paper_01_tok_per_sec": tok_s,
        "target_tok_per_sec": args.target_tok_per_sec,
        "throughput_target_met": tok_s >= args.target_tok_per_sec,
        "papers_verified": f"{summary['passed_papers']}/{summary['total_papers']}",
        "scenarios_verified": f"{summary['passed_scenarios']}/{summary['total_scenarios']}",
        "all_passed": summary["all_passed"] and (tok_s >= args.target_tok_per_sec),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
