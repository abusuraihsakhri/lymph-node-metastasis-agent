"""Regression tests for audit-chain integrity and caller isolation."""
import pytest

from agents.base import AuditTrail, SecurityException


def test_hmac_detects_modified_fields():
    trail = AuditTrail(secret_key="unit-test-only")
    trail.log("worker", "supervisor", "EVENT", {"measurement": 1})
    trail.log("worker", "supervisor", "EVENT", {"measurement": 2})
    assert trail.verify_integrity()
    trail.logs[0]["actor"] = "attacker"
    assert not trail.verify_integrity()


def test_hmac_detects_forged_chain():
    trail = AuditTrail(secret_key="unit-test-only")
    trail.log("worker", "supervisor", "EVENT", {"measurement": 1})
    trail.logs[0]["current_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_get_trail_is_defensive_copy():
    trail = AuditTrail(secret_key="unit-test-only")
    trail.log("worker", "supervisor", "EVENT", {"measurement": 1})
    external = trail.get_trail()
    external[0]["actor"] = "attacker"
    assert trail.verify_integrity()


def test_metadata_cannot_contain_detected_phi():
    trail = AuditTrail(secret_key="unit-test-only")
    with pytest.raises(SecurityException):
        trail.log("MRN-123456", "worker", "EVENT", {"measurement": 1})
    assert not trail.get_trail()


def test_no_audit_key_needed_to_import_package(monkeypatch):
    monkeypatch.delenv("AUDIT_SECRET_KEY", raising=False)
    with pytest.raises(SecurityException):
        AuditTrail()
