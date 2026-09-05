"""
Automated Pytest for lymph-node-metastasis-agent Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    OverviewEngine,
    Enrichment1TumorBurdenQuantificationAgent,
    ImplementationEngine,
    Enrichment2CapLymphNodeExamComplianceScorerEngine,
    Enrichment3ExtranodalExtensionEneDetectionAndGradingEngine,
    Enrichment4MicrometastasisVsIsolatedTumorCellItcDifferentiationEngine,
    LymphnodemetastasisagentEnrichmentSuite,
    enrichment_suite,
    EnrichmentResult,
)

def test_enrichment_suite_execution():
    suite = LymphnodemetastasisagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 1
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = LymphnodemetastasisagentEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0


def test_enrichment_suite_unique_keys():
    """Verify all enrichment suite result keys are unique (no overwrites)."""
    suite = LymphnodemetastasisagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    expected_keys = {
        "OverviewEngine",
        "Enrichment1TumorBurdenQuantificationAgent",
        "ImplementationEngine_TumorBurden",
        "Enrichment2CapLymphNodeExamComplianceScorerEngine",
        "ImplementationEngine_CapCompliance",
        "Enrichment3ExtranodalExtensionEneDetectionAndGradingEngine",
        "ImplementationEngine_EneneDetection",
        "Enrichment4MicrometastasisVsIsolatedTumorCellItcDifferentiationEngine",
    }
    assert set(res.keys()) == expected_keys
    assert len(res) == 8  # No duplicate keys overwritten


def test_enrichment_result_types():
    """Verify all results are EnrichmentResult instances."""
    suite = LymphnodemetastasisagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    for k, v in res.items():
        assert isinstance(v, EnrichmentResult)
        assert v.feature_name != ""
