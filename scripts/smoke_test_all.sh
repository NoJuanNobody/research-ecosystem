#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Validating Python Test Harnesses (All 36 Papers & Scenarios A/B/C) ==="
python3 -m unittest discover -v -s tests

echo "=== 2. Running End-to-End Pipeline Smoke Test ==="
python3 scripts/benchmark_edge_throughput.py --target-tok-per-sec 100

echo "=== 3. Running CLI Verification Across All 36 Systems ==="
python3 -m research_ecosystem.cli verify-all

if command -v cargo >/dev/null 2>&1; then
  echo "=== 4. Validating Rust Crates ==="
  cargo test --workspace --all-targets
fi

echo "=== ALL 36 RESEARCH SYSTEMS VERIFIED SUCCESSFULLY ==="
