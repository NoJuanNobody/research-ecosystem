#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if command -v tectonic >/dev/null 2>&1; then
    tectonic main.tex
elif command -v pdflatex >/dev/null 2>&1; then
    pdflatex -interaction=nonstopmode main.tex
    bibtex main || true
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
else
    echo "LaTeX source (main.tex + references.bib) generated. Install tectonic or MacTeX/pdflatex to render main.pdf."
fi
