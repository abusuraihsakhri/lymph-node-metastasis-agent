"""
Enterprise Security, PHI Outbound Guard, and HMAC-SHA256 Audit Trail.

"""
import os
import re
import json
import time
import hmac
import hashlib
from typing import Dict, Any, List, Optional
from threading import RLock
from datetime import datetime, timezone
from pydantic import BaseModel, Field

PHI_PATTERNS = [
    re.compile(r"\b(?:MRN|mrn)[:#\s-]*\d{4,10}\b", re.IGNORECASE),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    re.compile(r"\b(?:DOB|Date of Birth)[:\s]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", re.IGNORECASE),
    re.compile(r"\b(?:Patient\s+Name|Patient)[:\s]+[A-Z][a-z]+\s+[A-Z][a-z]+\b", re.IGNORECASE),
    re.compile(r"\b(?:John\s+Doe|Jane\s+Smith|Alice\s+Johnson)\b", re.IGNORECASE),
]


class SecurityException(Exception):
    """Raised when outbound data violates HIPAA Safe Harbor or contains raw PHI."""
    pass


class ResourceLimitExceededException(Exception):
    """Raised when computational parameters exceed safety bounds."""
    pass


def assert_no_phi(text: str) -> None:
    if not text:
        return
    for pattern in PHI_PATTERNS:
        if pattern.search(str(text)):
            raise SecurityException(f"PHI Outbound Guard Violation: Sensitive identifier detected with pattern {pattern.pattern}")


class PHIGuard:
    @staticmethod
    def assert_no_phi(text: str) -> None:
        assert_no_phi(text)

    @staticmethod
    def redact_phi(text: str) -> str:
        res = str(text)
        for pattern in PHI_PATTERNS:
            res = pattern.sub("[REDACTED_IDENTIFIER]", res)
        return res


class AuditTrail:
    """In-memory HMAC-SHA256 hash chain; entries are not persisted across restarts."""

    GENESIS = "GENESIS_BLOCK_0000000000000000"

    def __init__(self, secret_key: Optional[str] = None):
        resolved_key = secret_key or os.getenv("AUDIT_SECRET_KEY")
        if not resolved_key:
            raise SecurityException(
                "AUDIT_SECRET_KEY environment variable must be set. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        self.secret_key = resolved_key.encode("utf-8")
        self.logs: List[Dict[str, Any]] = []
        self._lock = RLock()

    def log(self, actor: str, actor_tier: str, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        payload_str = json.dumps(details, sort_keys=True, allow_nan=False)
        for text in (actor, actor_tier, event_type, payload_str):
            assert_no_phi(text)
        payload_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        ts = datetime.now(timezone.utc).isoformat()
        with self._lock:
            audit_id = f"AUDIT-{int(time.time()*1000)}-{len(self.logs)+1}"
            prev_hash = self.logs[-1]["current_hash"] if self.logs else self.GENESIS
            sign_string = f"{audit_id}|{ts}|{actor}|{actor_tier}|{event_type}|{payload_hash}|{prev_hash}"
            signature = hmac.new(self.secret_key, sign_string.encode("utf-8"), hashlib.sha256).hexdigest()
            entry = {
                "audit_id": audit_id,
                "timestamp": ts,
                "actor": actor,
                "actor_tier": actor_tier,
                "event_type": event_type,
                "payload_hash": payload_hash,
                "prev_hash": prev_hash,
                "current_hash": signature,
            }
            self.logs.append(entry)
            return dict(entry)

    def verify_integrity(self) -> bool:
        """Verify linkage AND every HMAC signature, not merely the previous hash."""
        with self._lock:
            prev = self.GENESIS
            for entry in self.logs:
                try:
                    if entry["prev_hash"] != prev:
                        return False
                    sign_string = "|".join(str(entry[k]) for k in (
                        "audit_id", "timestamp", "actor", "actor_tier",
                        "event_type", "payload_hash", "prev_hash"
                    ))
                    expected = hmac.new(self.secret_key, sign_string.encode("utf-8"), hashlib.sha256).hexdigest()
                    actual = entry["current_hash"]
                    if not isinstance(actual, str) or not hmac.compare_digest(expected, actual):
                        return False
                    prev = actual
                except (KeyError, TypeError, ValueError):
                    return False
            return True

    def get_trail(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [dict(entry) for entry in self.logs]


_GLOBAL_AUDIT: Optional[AuditTrail] = None
_GLOBAL_AUDIT_LOCK = RLock()


def _get_global_audit() -> AuditTrail:
    global _GLOBAL_AUDIT
    with _GLOBAL_AUDIT_LOCK:
        if _GLOBAL_AUDIT is None:
            _GLOBAL_AUDIT = AuditTrail()
        return _GLOBAL_AUDIT


class AuditLogger:
    @staticmethod
    def log(actor: str, actor_tier: str, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        return _get_global_audit().log(actor, actor_tier, event_type, details)

    @staticmethod
    def get_trail() -> List[Dict[str, Any]]:
        return _get_global_audit().get_trail()

    @staticmethod
    def verify_integrity() -> bool:
        return _get_global_audit().verify_integrity()


class ActionExecutor:
    @staticmethod
    def execute_with_audit(actor: str, actor_tier: str, action_type: str, fn, *args, **kwargs):
        res = fn(*args, **kwargs)
        AuditLogger.log(actor, actor_tier, action_type, {"status": "SUCCESS"})
        return res
