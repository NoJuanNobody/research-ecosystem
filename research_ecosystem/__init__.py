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
from .latex_publisher import LatexManuscriptBundle, LatexManuscriptCompiler
from .research_graph_loop import AutonomousResearchGraphLoop, ResearchGraphNode

__version__ = "0.2.0"
__all__ = [
    "PAPERS_CATALOG",
    "get_paper",
    "list_papers",
    "run_paper",
    "run_pillar",
    "run_scenario",
    "verify_all_systems",
    "LatexManuscriptBundle",
    "LatexManuscriptCompiler",
    "ResearchGraphNode",
    "AutonomousResearchGraphLoop",
]
