"""Local, synthetic demonstration pipeline for the public portfolio."""

from .models import Posting
from .pipeline import run_pipeline

__all__ = ["Posting", "run_pipeline"]
