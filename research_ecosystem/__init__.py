"""
research_ecosystem: 36 Research Paper Implementations Across Edge Agents,
Graph-Loop Creative Pipelines, and Network Economics Distributions.
"""

from .catalog import (
    PAPERS_CATALOG,
    get_paper,
    list_papers,
    run_paper,
    run_pillar,
    run_scenario,
    verify_all_systems,
)

__version__ = "0.1.0"
__all__ = [
    "PAPERS_CATALOG",
    "get_paper",
    "list_papers",
    "run_paper",
    "run_pillar",
    "run_scenario",
    "verify_all_systems",
]
