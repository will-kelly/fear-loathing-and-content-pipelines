"""Content Pipeline Agent.

A five-stage, claims-first editorial pipeline on the Claude API:

    intake -> claims -> draft -> review -> package

Every stage writes its output to disk before the next stage runs, so a
run is inspectable, resumable, and diffable. See ARCHITECTURE.md.
"""

from .pipeline import Pipeline, PipelineRun

__all__ = ["Pipeline", "PipelineRun"]
__version__ = "0.1.0"
