"""Regression coverage for boolean CSV flags and finite metric validation."""
import csv
import math

import pytest

from lymph_node_metastasis_agent.cli import main as packaged_main
from lymph_node_metastasis_agent.models import ClinicalCasePayload
from lymph_sentinel import main as legacy_main


def test_packaged_csv_false_does_not_escalate(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    source.write_text(
        "case_id,patient_synthetic_id,primary_metric,secondary_metric,is_stat,status_flag\n"
        "TEST-1,SYNTH-1,1,1,False,NORMAL\n",
        encoding="utf-8",
    )
    # Strings above must contain real newline escapes when parsed by Python.
    assert packaged_main(["batch", "-i", str(source), "-o", str(dest)]) == 0
    with dest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["overall_status"] == "CONCORDANT_NORMAL"


def test_legacy_csv_false_does_not_escalate(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    source.write_text(
        "case_id,metric_primary,metric_secondary,critical_flag,status_text\n"
        "TEST-1,1,1,False,NORMAL\n",
        encoding="utf-8",
    )
    assert legacy_main(["batch", "-i", str(source), "-o", str(dest)]) == 0
    with dest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["overall_status"] == "CONCORDANT_NORMAL"


@pytest.mark.parametrize("value", [math.inf, math.nan, -1.0])
def test_dataclass_rejects_invalid_metrics(value):
    with pytest.raises(ValueError):
        ClinicalCasePayload("C1", "SYNTH1", value, 1.0, "NORMAL")
