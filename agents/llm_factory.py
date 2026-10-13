"""
Deterministic mock responder; external LLM providers are not implemented.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Lymph Node Metastasis Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} Deterministic Verification Engine]: No clinical analysis or external LLM inference was performed. Query preview: '{prompt[:60]}...'. This is a demonstration response."


class LLMFactory:
    """Creates the available deterministic mock responder."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Lymph Node Metastasis Agent"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(
            f"Provider {provider!r} is not implemented. "
            "Only 'mock', 'deterministic', and 'test' are supported."
        )
