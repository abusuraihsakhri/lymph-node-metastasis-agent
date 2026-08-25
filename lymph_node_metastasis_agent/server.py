"""
FastAPI REST Application & Webhooks for LymphSentinel: Autonomous Sentinel Node Micrometastasis & ITC Detector.
"""
from typing import Dict, Any, Optional
from .models import ClinicalCasePayload
from .agents import LymphCoordinator

coordinator = LymphCoordinator()

def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel

        app = FastAPI(
            title="LymphSentinel: Autonomous Sentinel Node Micrometastasis & ITC Detector",
            description="Automated system classifying sentinel lymph node metastases into Isolated Tumor Cells (ITC <=0.2mm), Micrometastases (0.2-2mm), and Macromets (>2mm).",
            version="2.0.0-PRO",
        )

        class AuditRequest(BaseModel):
            case_id: str = "CASE-2026-001"
            patient_synthetic_id: str = "SYNTH-PT-881"
            primary_metric: float = 24.5
            secondary_metric: float = 14.0
            status_flag: str = "DISCORDANT"
            is_stat: bool = True
            clinical_notes: str = ""
            biomarkers: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "lymph-node-metastasis-agent", "domain": "Digital Pathology", "version": "2.0.0-PRO"}

        @app.post("/api/audit")
        def api_audit(req: AuditRequest):
            payload = ClinicalCasePayload(
                case_id=req.case_id,
                patient_synthetic_id=req.patient_synthetic_id,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_flag=req.status_flag,
                is_stat=req.is_stat,
                clinical_notes=req.clinical_notes,
                biomarkers=req.biomarkers,
            )
            return coordinator.process_case(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
