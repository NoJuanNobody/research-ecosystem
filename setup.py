from setuptools import find_packages, setup

setup(
    name="research-ecosystem",
    version="0.1.0",
    description="36 Research Paper Implementations Across Edge Agents, Graph-Loop Creative Pipelines, and Network Economics Distributions",
    packages=find_packages(include=["research_ecosystem", "research_ecosystem.*"]),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "research-ecosystem = research_ecosystem.cli:main",
        ],
    },
)
