"""
CLI entry point (`research-ecosystem`) for inspecting, running, and verifying all 36 research papers.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .catalog import (
    get_paper,
    list_papers,
    run_paper,
    run_pillar,
    run_scenario,
    verify_all_systems,
)
from .latex_publisher import LatexManuscriptCompiler
from .research_graph_loop import AutonomousResearchGraphLoop


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-ecosystem",
        description="36 Research Paper Implementations Across Edge Agents, Creative Graph-Loops, and Network Economics",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all 36 research papers or filter by pillar (1, 2, 3)")
    p_list.add_argument("--pillar", type=int, choices=[1, 2, 3], default=None, help="Filter by pillar")
    p_list.add_argument("--json", action="store_true", help="Output as JSON")

    p_inspect = sub.add_parser("inspect", help="Inspect metadata and execute verification for a paper ID (01..36)")
    p_inspect.add_argument("paper_id", help="Paper ID (01..36)")
    p_inspect.add_argument("--json", action="store_true", help="Output as JSON")

    p_run = sub.add_parser("run-pillar", help="Run all papers in Pillar 1, 2, 3, or all")
    p_run.add_argument("pillar", choices=["1", "2", "3", "all"], help="Pillar to execute")
    p_run.add_argument("--json", action="store_true", help="Output as JSON")

    p_scen = sub.add_parser("scenario", help="Run cross-pillar integration scenario (A, B, or C)")
    p_scen.add_argument("scenario_id", choices=["A", "B", "C", "a", "b", "c"], help="Scenario ID")
    p_scen.add_argument("--json", action="store_true", help="Output as JSON")

    p_ver = sub.add_parser("verify-all", help="Verify all 36 papers and 3 cross-pillar integration scenarios")
    p_ver.add_argument("--json", action="store_true", help="Output as JSON")

    p_latex = sub.add_parser("latex", help="Compile a paper (01..36) into a publication-ready LaTeX + BibTeX manuscript bundle")
    p_latex.add_argument("paper_id", help="Paper ID (01..36)")
    p_latex.add_argument("--out-dir", default="./papers_latex", help="Output directory for LaTeX bundle")

    p_loop = sub.add_parser(
        "graph-loop",
        help="Run the 5-stage Autonomous Research Graph Loop (Lab Scanner -> Council Discussion -> FAU HPC/Homelab Experiment -> Critique Gate -> LaTeX Publication)",
    )
    p_loop.add_argument(
        "--topic",
        default="Speculative GraphRAG Distillation & Sub-4-Bit Edge Verification",
        help="Seed research topic to investigate",
    )
    p_loop.add_argument(
        "--compute-target",
        choices=["fau_hpc", "homelab", "edge_local"],
        default="fau_hpc",
        help="Target compute fabric (fau_hpc SLURM cluster, homelab silo, or edge_local)",
    )
    p_loop.add_argument("--out-dir", default="./papers_latex", help="Output directory for SLURM script and LaTeX paper")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        papers = list_papers(pillar=args.pillar)
        if args.json:
            print(json.dumps(papers, indent=2))
        else:
            for p in papers:
                print(
                    f"[{p['id']}] Pillar {p['pillar']} ({p['pillar_name']}): "
                    f"{p['title']} | {p['runtime']} | Target: {p['target_metric']}"
                )
        return 0

    if args.command == "inspect":
        meta = get_paper(args.paper_id)
        execution = run_paper(args.paper_id)
        payload = {"metadata": meta, "execution": execution}
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"Paper {meta['id']}: {meta['title']}")
            print(f"  Pillar:        {meta['pillar']} ({meta['pillar_name']})")
            print(f"  Runtime:       {meta['runtime']}")
            print(f"  Target Metric: {meta['target_metric']}")
            print(f"  Work Package:  {', '.join(meta['work_package_files'])}")
            print(f"  Verification:  {'PASS' if execution.get('passed') else 'FAIL'}")
            print(f"  Metrics:       {json.dumps(execution)}")
        return 0 if execution.get("passed") else 1

    if args.command == "run-pillar":
        results = run_pillar(args.pillar)
        all_ok = all(bool(r.get("passed")) for r in results)
        if args.json:
            print(json.dumps({"pillar": args.pillar, "all_passed": all_ok, "results": results}, indent=2))
        else:
            for r in results:
                status = "PASS" if r.get("passed") else "FAIL"
                print(f"[{r['paper_id']}] {status} - {r['title']}")
        return 0 if all_ok else 1

    if args.command == "scenario":
        res = run_scenario(args.scenario_id)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            status = "PASS" if res.get("passed") else "FAIL"
            print(f"Scenario {res['scenario_id']}: {res['name']} [{status}]")
            print(f"  Chain: {' -> '.join(res['papers_executed'])}")
        return 0 if res.get("passed") else 1

    if args.command == "verify-all":
        summary = verify_all_systems()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print(
                f"Verified {summary['passed_papers']}/{summary['total_papers']} papers and "
                f"{summary['passed_scenarios']}/{summary['total_scenarios']} cross-pillar scenarios."
            )
            if summary["all_passed"]:
                print("=== ALL 36 RESEARCH SYSTEMS VERIFIED SUCCESSFULLY ===")
        return 0 if summary["all_passed"] else 1

    if args.command == "latex":
        compiler = LatexManuscriptCompiler()
        bundle = compiler.compile_paper(args.paper_id, out_root=args.out_dir)
        print(json.dumps(bundle.to_dict(), indent=2))
        return 0

    if args.command == "graph-loop":
        loop = AutonomousResearchGraphLoop(out_dir=args.out_dir)
        result = loop.run_cycle(seed_topic=args.topic, compute_target=args.compute_target)
        print(json.dumps(result, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
