# Lymph Node Metastasis Agent

A collection of Python demonstration engines and a standalone browser interface for exploring **rule-based flagging of numeric inputs**. The browser and Python implementations use illustrative thresholds; they do **not** analyze histology images or calculate validated pathologic staging.

## Browser demonstration

Open [web/index.html](web/index.html) locally in a modern browser. The interface works without Python, a backend, a build step, login, or API keys.

- Enter synthetic task IDs, two unitless metrics, an optional status keyword, and a priority flag.
- Evaluate three deterministic rules: primary metric **>25**, secondary metric **>12** or priority flag, and configured descriptor keywords.
- Inspect the output and download a JSON result.
- Validation rejects malformed identifiers, negative/non-finite metrics, and unsupported descriptor characters.

The static browser tool reproduces the **generic worker trigger rules** in `agents/workers.py`; it does not execute Python or cryptographically sign results. Browser data remains in the current page/session and is not sent to a server or written to browser storage. Do not enter patient information.

## Clinical limitations

**For research and software demonstration only—not for patient care.** The repository contains generic thresholds, simulated worker alerts, and legacy clinical-themed modules. No diagnostic performance, tissue image interpretation, ITC/micrometastasis classification, pN staging, CAP protocol compliance, or HIPAA compliance has been established or validated. Thresholds such as 25 and 12 have **no defined clinical units or guideline support**. Consult the applicable current, site-specific staging protocols and a qualified pathologist for actual clinical decisions.

## Python installation

Python 3.10 or newer is required. Clone the repository and install the appropriate extras:

```bash
git clone https://github.com/abusuraihsakhri/lymph-node-metastasis-agent.git
cd lymph-node-metastasis-agent
python -m pip install -e ".[api]"
```

For Python tests, also install `python -m pip install -e ".[test]"`.

### Generic worker CLI and API

The root-level `cli.py` uses `agents/` and writes **in-memory HMAC-SHA256 audit entries**. Set a unique key before invoking audit operations:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py audit --task-id TASK-001 --target SAMPLE-001 --primary 28 --secondary 14 --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py serve --host 127.0.0.1 --port 8000
```

The REST service exposes `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. Interactive API documentation is available at `http://127.0.0.1:8000/docs` while the server runs.

Audit entries are **volatile**: they do not persist across process restarts and are not a durable or HIPAA-certified record. `verify-audit` verifies only entries in the current running process. A missing `AUDIT_SECRET_KEY` prevents audit operations. The PHI patterns are limited screening checks, not reliable de-identification.

### Legacy interfaces

The repository also preserves independent example entry points:

```bash
python -m lymph_node_metastasis_agent.cli audit --case-id CASE-001 --primary 2 --secondary 1
python lymph_sentinel.py audit --case-id CASE-001 --primary 2 --secondary 1
python simulator.py 100
```

These modules implement different historical rule sets and outputs. Do not assume equivalence with `agents/` or the browser demo; no actual histology classifier, trained image model, or robust staging algorithm is bundled.

## Docker

With `AUDIT_SECRET_KEY` set in the environment:

```bash
docker compose up --build
```

Compose binds the API to `127.0.0.1:8000` by default. There is **no** bundled secret; use a generated secret, do not commit it, and protect the API with appropriate access controls before exposing it beyond the local machine.

## Testing

```bash
python -m pip install -e ".[test]"
export AUDIT_SECRET_KEY="test-only-key-do-not-use-in-production"
python -m pytest -q
node --check web/app.js
node --test web/app.test.cjs
```

GitHub Actions checks Python 3.10–3.12 and browser rule tests. The web app is dependency-free vanilla HTML, CSS, and JavaScript and is intended for current desktop/mobile browsers. The REST service uses FastAPI, Pydantic v2, and Uvicorn. Server and browser modes do not require external LLM services; the `mock` responder is deterministic.

## Privacy and security

The static page makes no HTTP requests from its application code and has no analytics, external fonts, cookies, or local storage. Python tools can retain synthetic task identifiers and in-memory audit metadata while running; do not submit real patient identifiers. The API has **no authentication** and should not be publicly exposed. The audit chain authenticates metadata fields with HMAC-SHA256 but is not persistent; it does not prove that upstream inputs are accurate.

## License

[MIT](LICENSE).
