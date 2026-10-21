#!/usr/bin/env bash
#SBATCH --job-name=res_eco_40
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/fau_hpc_40_%j.out
#SBATCH --error=logs/fau_hpc_40_%j.err

# ============================================================================
# FAU Research Computing (HPC SLURM + Workstation) Experiment Dispatcher
# Topic: Autonomous Graph-Loop Synthesis: Multi-Node Speculative Decoding on FAU SLURM + Homelab GraphRAG
# ============================================================================
set -euo pipefail
mkdir -p logs

echo "[FAU-HPC] Starting experiment for Paper 40: Autonomous Graph-Loop Synthesis: Multi-Node Speculative Decoding on FAU SLURM + Homelab GraphRAG"
echo "[FAU-HPC] Host: $(hostname) | GPUs: 2 | CPUs: 16 | Mem: 64G"

python3 -m research_ecosystem.cli verify-all --json > logs/empirical_results_40.json
echo "[FAU-HPC] Completed empirical benchmark sweep."
