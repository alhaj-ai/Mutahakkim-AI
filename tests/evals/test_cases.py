from __future__ import annotations

from computer_use.evals import run_evals


def test_eval_harness_exports_runner():
    assert callable(run_evals)
