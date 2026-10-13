"""
Specialized Domain Worker Agents for Lymph Node Metastasis Agent.
Domain: Digital Pathology & Histology Systems
Standard: CAP Cancer Protocols / DICOM WSI PS3.16
"""
import uuid
from typing import List
from .models import SystemTaskPayload, AgentAlert, UrgencyLevel


class InvariantQCWorker:
    """Worker 1: Primary Mathematical & Protocol Boundary Auditor."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        if payload.primary_metric > 25.0:
            alerts.append(AgentAlert(
                alert_id=f"QC-{uuid.uuid4().hex[:6]}",
                origin_worker="InvariantQCWorker",
                urgency=UrgencyLevel.ELEVATED,
                summary="Primary Metric Threshold Exceeded",
                technical_details=f"Primary measurement ({payload.primary_metric:.2f}) exceeds configured demonstration threshold (25.00); not a clinical reference interval.",
                actionable_remediation="Review the unitless demonstration inputs and threshold configuration.",
            ))
        return alerts


class SafetyEscalationWorker:
    """Worker 2: Safety Boundary, Toxicity & Emergency Interlock Worker."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        if payload.is_critical_flag or payload.secondary_metric > 12.0:
            alerts.append(AgentAlert(
                alert_id=f"SAFE-{uuid.uuid4().hex[:6]}",
                origin_worker="SafetyEscalationWorker",
                urgency=UrgencyLevel.CRITICAL_STAT if payload.is_critical_flag else UrgencyLevel.ELEVATED,
                summary="Priority Flag or Secondary Threshold Triggered",
                technical_details=f"CriticalFlag={payload.is_critical_flag} with secondary index {payload.secondary_metric:.2f}.",
                actionable_remediation="Review the demonstration rule flags; no clinical escalation is initiated.",
            ))
        return alerts


class ProtocolConformanceWorker:
    """Worker 3: Spec Conformance, Anomaly Triage & Discordance Checker."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        desc_upper = str(payload.status_descriptor).upper()
        if any(w in desc_upper for w in ["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"]):
            alerts.append(AgentAlert(
                alert_id=f"CONF-{uuid.uuid4().hex[:6]}",
                origin_worker="ProtocolConformanceWorker",
                urgency=UrgencyLevel.ELEVATED,
                summary="Protocol Conformance Discordance Detected",
                technical_details=f"Descriptor '{payload.status_descriptor}' matched a demonstration keyword; this does not establish clinical discordance.",
                actionable_remediation="Review the descriptor and application rule configuration.",
            ))
        return alerts
