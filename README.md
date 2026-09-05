# Lymph Node Metastasis Agent

> **Domain:** Digital Pathology & Quantitative Histopathology  
> **Reference Guidelines & Standards:** College of American Pathologists (CAP) Synoptic Protocols & DICOM WSI

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Lymph Node Metastasis Agent** is an advanced analytical and computational platform implementing Sentinel Node Micrometastasis & ITC Staging Agent. It evaluates lymph node measurements against clinical thresholds and generates consensus dossiers with tamper-evident audit trails.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`MetastasisDimensionAgent`**: Specialized Sub-Agent 1 for lymph-node-metastasis-agent
- **`ExtracapsularExtensionAgent`**: Specialized Sub-Agent 2 for lymph-node-metastasis-agent
- **`pNStageSynthesizerAgent`**: Specialized Sub-Agent 3 for lymph-node-metastasis-agent

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/lymph-node-metastasis-agent.git
cd lymph-node-metastasis-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Set required environment variable for audit security
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-2026-001 --primary 28.5 --secondary 14.2 --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "Explain specifications"
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task/case identifier | TASK-2026-001 |
| `--target` | Entity or target identifier | KEY-TARGET-01 |
| `--primary` | Primary measurement value (float) | 28.5 |
| `--secondary` | Secondary measurement value (float) | 14.2 |
| `--critical` | Flag for critical escalation | False |
| `--status` | Status descriptor (NOMINAL, DISCORDANT, etc.) | DISCORDANT |

### Input Data Schema (CSV)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Entity/target identifier | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Optional |
| `status_descriptor` | Status code (NOMINAL, DISCORDANT, etc.) | Optional |
| `is_critical_flag` | Critical escalation flag (true/false) | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. Requires `AUDIT_SECRET_KEY` environment variable.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
# Set test audit key (tests use a deterministic key)
export AUDIT_SECRET_KEY="test-audit-key-for-development-only"

# Run all tests
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t lymph-node-metastasis-agent .
docker run -e AUDIT_SECRET_KEY=your-secret-key -p 8000:8000 lymph-node-metastasis-agent
```

---

## 📁 Project Structure

```
lymph-node-metastasis-agent/
├── agents/                    # Core agent modules
│   ├── __init__.py
│   ├── api.py                 # FastAPI REST endpoints
│   ├── base.py                # Security, PHI guard, audit trail
│   ├── learning.py            # Bayesian calibration engine
│   ├── llm_factory.py         # LLM provider factory
│   ├── metrics.py             # Prometheus metrics collector
│   ├── models.py              # Pydantic data models
│   ├── streamer.py            # WebSocket telemetry
│   ├── supervisor.py          # Master orchestrator
│   └── workers.py             # Domain worker agents
├── tests/                     # Test suite
│   ├── test_enrichment.py
│   └── test_lymph_node_metastasis_agent.py
├── cli.py                     # Command-line interface
├── enrichment.py              # Enrichment feature engines
├── lymph_sentinel.py          # LymphSentinel clinical engine
├── simulator.py               # High-throughput simulator
├── sample.csv                 # Sample input data
├── sample_payload.json        # Sample API payload
├── pyproject.toml             # Project configuration
├── Dockerfile                 # Container definition
└── web/                       # Web interface
    └── index.html
```

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
