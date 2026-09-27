# Enterprise Network Knowledge & Troubleshooting Assistant

A progressive learning project for building an enterprise Agentic AI network troubleshooting assistant using **Python, FastAPI, Google Gemini, LangGraph, MCP/FastMCP, RAG, PostgreSQL and pgvector**.

The project is intentionally implemented in versions so each architectural layer is understood before introducing the next one.

> **LLM provider:** Google Gemini in every version.
> **Package manager:** `uv` (not `pip`).
> **MCP server framework:** FastMCP, using `from fastmcp import FastMCP`.

---

## 1. Project Goal

Build an AI assistant that can investigate network issues using two distinct evidence sources:

### Operational evidence

Accessed through MCP tools:

- Device status
- CPU and memory
- Interfaces
- Interface errors
- BGP neighbors
- Alerts
- Telemetry
- Configuration and diagnostics in later versions

### Knowledge evidence

Accessed through RAG:

- Troubleshooting runbooks
- Operational procedures
- Network documentation
- Design guidance
- Incident knowledge in later versions

The final system will combine both sources using LangGraph orchestration and Gemini reasoning.

---

## 2. Core Design Principle

> **Gemini reasons about what needs to happen; deterministic tools perform infrastructure operations; RAG supplies documented knowledge; LangGraph controls workflow and state.**

This separation is intentional:

```text
Gemini       = reasoning
MCP          = standardized capability protocol
FastMCP      = MCP server implementation
RAG          = knowledge retrieval
pgvector     = vector similarity search
LangGraph    = workflow/state orchestration
FastAPI      = application/API layer
```

---

## 3. Final Target Architecture

```text
                                USER
                                  |
                                  v
                           +--------------+
                           |   FastAPI    |
                           |   AI Gateway |
                           +------+-------+
                                  |
                                  v
                         +------------------+
                         |    LangGraph     |
                         |    Supervisor    |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             +-------------+              +-------------+
             |  Knowledge  |              |   Network   |
             |    Agent    |              | Investigation|
             +------+------+              +------+------+
                    |                            |
                    v                            v
                  RAG                          MCP
                    |                            |
                    v                            v
             PostgreSQL/                 FastMCP Server
               pgvector                       |
                    |                 +---------+---------+
                    |                 |         |         |
                    v                 v         v         v
                Runbooks          Status     Alerts    Telemetry
                    |                 |
                    +---------+-------+
                              |
                              v
                           Gemini
                              |
                              v
                        Grounded Answer
```

---

## 4. Progressive Roadmap

| Version | Main capability | Status |
|---|---|---|
| V1 | FastAPI network simulator | Completed |
| V2 | Gemini-powered network assistant | Completed |
| V3 | Gemini function/tool calling | Completed |
| V4 | MCP + FastMCP network tools | Implemented / debugging |
| V5 | RAG + Gemini Embeddings + PostgreSQL/pgvector | In progress |
| V6 | LangGraph orchestration + specialized agents | Planned |
| V7 | Complete multi-agent troubleshooting assistant | Planned |
| V8 | Validation, HITL, audit, evaluation, failure handling | Planned |

The README is a **living project document** and should be updated whenever a future version changes the architecture, files, dependencies, commands, tests, or implementation status.

---

## 5. Technology Stack

### Core

- Python 3.11
- `uv`
- FastAPI
- Pydantic
- pytest

### AI

- Google Gemini
- `google-genai`
- Gemini function calling
- Gemini Embeddings

### Agent orchestration

- LangGraph
- LangChain where useful

### MCP

- MCP protocol
- FastMCP
- MCP Python client/session

### RAG

- Gemini Embeddings
- PostgreSQL
- pgvector
- cosine similarity
- HNSW vector index

### Local infrastructure

- Docker
- Docker Compose

---

## 6. Current Project Structure

```text
enterprise-network-ai/
|
+-- .env
+-- .gitignore
+-- docker-compose.yml
+-- pyproject.toml
+-- README.md
|
+-- knowledge/
|   +-- bgp_troubleshooting.md
|   +-- high_cpu_troubleshooting.md
|   +-- interface_errors.md
|
+-- sql/
|   +-- schema.sql
|
+-- scripts/
|   +-- init_db.py
|   +-- ingest_knowledge.py
|   +-- test_mcp_server.py
|   +-- test_gemini_mcp.py
|   +-- test_rag.py
|
+-- src/
|   +-- enterprise_network_ai/
|       +-- __init__.py
|       +-- main.py
|       +-- models.py
|       +-- data.py
|       +-- network_tools.py
|       +-- mcp_server.py
|       +-- gemini_mcp.py
|       +-- embeddings.py
|       +-- vector_store.py
|       +-- rag.py
|
+-- tests/
    +-- test_api.py
    +-- test_network_tools.py
    +-- test_mcp_server.py
    +-- test_chunking.py
    +-- test_rag_api.py
```

File names may change in V6-V8 as the architecture evolves. Keep this section synchronized with the actual repository.

---

# 7. Environment Setup

## Create the project

If starting from scratch:

```powershell
uv init --package enterprise-network-ai
cd enterprise-network-ai
uv sync
```

Optional Windows activation:

```powershell
.venv\Scripts\activate
```

The project uses `uv run` for execution, so activation is not required for normal commands.

---

## Dependencies

Install using `uv`:

```powershell
uv add fastapi uvicorn pydantic
uv add google-genai python-dotenv
uv add "fastmcp>=4,<5"
uv add "psycopg[binary]" pgvector
uv add --dev pytest
```

Do not use `pip` for this project.

---

## `.env`

Create `.env` in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.7-flash

GEMINI_EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=1536

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/network_ai
```

Keep model names configurable so they can be changed without modifying application code.

Never commit `.env` to Git.

---

# 8. V1 — FastAPI Network Simulator

## Objective

Build a deterministic network API before introducing AI.

### Architecture

```text
User
 |
 v
FastAPI
 |
 v
Simulated network data
 |
 v
JSON response
```

### Simulated device

```text
Device: R1
Vendor: Cisco
Model: ASR1001-X
Status: up
CPU: 91%
Memory: 62%
```

### Endpoints

```text
GET /devices/{device_id}/status
GET /devices/{device_id}/alerts
```

### Run

```powershell
uv run uvicorn src.enterprise_network_ai.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Concepts learned

- FastAPI application structure
- HTTP endpoints
- Pydantic models
- Request/response validation
- 404 handling
- Separation of data and API logic

---

# 9. V2 — Gemini Network Assistant

## Objective

Introduce Gemini reasoning without tools.

### Architecture

```text
User
 |
 v
FastAPI
 |
 v
Network context
 |
 v
Gemini
 |
 v
Natural-language answer
```

The model only knows information explicitly included in the prompt.

### Main concepts

- `google-genai`
- Gemini API
- Environment variables
- Prompt construction
- Grounded prompting
- LLM integration separation

### Key lesson

V2 is primarily an **LLM application**, not a full agent. Gemini cannot independently retrieve current device state.

---

# 10. V3 — Gemini Function Calling

## Objective

Allow Gemini to request network operations.

### Architecture

```text
User
 |
 v
FastAPI
 |
 v
Gemini
 |
 | Function Call
 v
Tool Registry
 |
 v
Python network tool
 |
 v
Network data
 |
 v
Function response
 |
 v
Gemini
 |
 v
Final answer
```

### Tools

```text
get_device_status
get_device_alerts
get_interface_status
get_bgp_neighbors
```

### Core loop

```text
Reason
  |
  v
Request tool
  |
  v
Execute
  |
  v
Observe result
  |
  v
Reason again
```

### Important distinction

Gemini does not directly execute Python. It produces a structured function-call request. The application validates the requested tool, executes it, and sends the result back to Gemini.

### Testing principle

Unit tests mock Gemini. Real model/API calls are performed separately as integration tests.

---

# 11. V4 — MCP + FastMCP

## Objective

Move network capabilities behind an MCP server.

### V3

```text
Gemini
 |
 v
Python tool registry
 |
 v
Python function
```

### V4

```text
Gemini
 |
 v
MCP client
 |
 v
MCP protocol
 |
 v
FastMCP server
 |
 v
Network tools
```

### MCP server tools

```text
get_device_status
get_device_alerts
get_interface_status
get_bgp_neighbors
```

### FastMCP pattern

```python
from fastmcp import FastMCP

mcp = FastMCP("Enterprise Network Tools")

@mcp.tool
def get_device_status(device_id: str) -> dict:
    ...
```

### MCP client operations

Tool discovery:

```python
await client.list_tools()
```

Tool invocation:

```python
await client.call_tool(
    "get_device_status",
    {"device_id": "R1"},
)
```

### Separation of concerns

```text
network_tools.py
    |
    +-- domain/business logic

mcp_server.py
    |
    +-- MCP protocol adapter
```

---

## V4 Gemini/MCP integration notes

The project encountered compatibility issues with the Gemini SDK's direct built-in MCP integration.

### Issue 1

```text
TypeError: cannot pickle '_asyncio.Task' object
```

Cause: a live MCP `ClientSession` was placed inside a typed Gemini configuration object and the SDK's copying behavior interacted badly with live asyncio state.

### Issue 2

```text
AttributeError: 'bool' object has no attribute 'items'
```

Cause: the Gemini SDK's MCP schema conversion encountered a JSON Schema field such as `additionalProperties: false` and treated the boolean as a dictionary.

### Current design

The project therefore uses an explicit adapter:

```text
FastMCP
 |
 v
MCP tool schema
 |
 v
Schema sanitizer/adapter
 |
 v
Gemini FunctionDeclaration
 |
 v
Gemini function call
 |
 v
MCP ClientSession.call_tool()
 |
 v
FastMCP
```

This makes the protocol boundaries explicit and avoids depending on the problematic direct SDK MCP conversion path.

---

# 12. V5 — RAG + Gemini Embeddings + PostgreSQL/pgvector

## Objective

Add network documentation and semantic retrieval.

MCP answers:

> What is happening on the network?

RAG answers:

> What does our documented knowledge say about this problem?

### Architecture

```text
Question
 |
 v
Gemini Embedding
 |
 v
Vector
 |
 v
PostgreSQL + pgvector
 |
 v
Top-K relevant chunks
 |
 v
Grounding context
 |
 v
Gemini
 |
 v
Answer + sources
```

---

## V5 embedding configuration

```env
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=1536
```

Database column:

```sql
embedding VECTOR(1536)
```

Similarity uses cosine distance.

---

## V5 database

Docker image:

```text
pgvector/pgvector:pg18-trixie
```

For PostgreSQL 18+, the recommended volume mount is:

```yaml
volumes:
  - network_ai_pgdata:/var/lib/postgresql
```

rather than mounting `/var/lib/postgresql/data` directly.

### Start

```powershell
docker compose up -d
```

### Check

```powershell
docker compose ps
```

### Logs

```powershell
docker logs enterprise-network-postgres
```

---

## V5 database schema

Table:

```text
knowledge_chunks
```

Columns:

```text
id
document_name
title
chunk_index
content
metadata
embedding
created_at
```

Vector column:

```sql
embedding VECTOR(1536)
```

Vector index:

```sql
USING hnsw (embedding vector_cosine_ops)
```

---

## Initialize database

```powershell
uv run python scripts/init_db.py
```

Verify tables:

```powershell
docker exec enterprise-network-postgres `
    psql -U postgres -d network_ai `
    -c "\dt"
```

Verify pgvector:

```powershell
docker exec enterprise-network-postgres `
    psql -U postgres -d network_ai `
    -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';"
```

---

## V5 knowledge corpus

Initial files:

```text
knowledge/
|
+-- bgp_troubleshooting.md
+-- high_cpu_troubleshooting.md
+-- interface_errors.md
```

Later versions may support additional formats and knowledge sources.

---

## V5 chunking

Current implementation:

```text
chunk_size = 180 words
overlap = 40 words
```

Chunking is a tunable retrieval-quality parameter, not a universal constant.

---

## V5 ingestion

Run:

```powershell
uv run python scripts/ingest_knowledge.py
```

Pipeline:

```text
Markdown
 |
 v
Normalization
 |
 v
Chunking
 |
 v
Gemini Embedding
 |
 v
1536-dimensional vector
 |
 v
PostgreSQL/pgvector
```

---

## V5 retrieval test

Run:

```powershell
uv run python scripts/test_rag.py
```

Example queries:

```text
How should I troubleshoot BGP flapping?
What should I check for high CPU?
What can cause interface errors?
```

The first purpose of this test is retrieval quality. Verify that semantically relevant chunks are returned before evaluating generated answers.

---

## V5 API

Expected endpoints:

```text
GET  /knowledge/search
POST /knowledge/ask
```

Example request:

```json
{
  "question": "How should I troubleshoot BGP flapping?",
  "top_k": 3
}
```

The response contains the generated answer and source metadata.

---

## V5 RAG concepts

### Embedding

A numerical representation of text used for semantic similarity.

### Chunk

A smaller unit of a document that can be retrieved independently.

### Retrieval

Finding relevant chunks for a query.

### Top-K

Number of nearest chunks returned.

### Grounding

Constraining the generated answer to retrieved evidence.

### Retrieval quality vs answer quality

A correct retriever can still be followed by a poor generation step, and a poor retriever can produce an answer that sounds plausible. These are separate evaluation problems.

---

## V5 known troubleshooting status

A PostgreSQL authentication issue has been encountered:

```text
FATAL: password authentication failed for user "postgres"
```

The application attempted:

```text
postgresql://postgres:postgres@localhost:5432/network_ai
```

This means the server is reachable on the target address/port but the credentials accepted by that PostgreSQL instance do not match the connection string.

Useful diagnostics:

```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
```

```powershell
docker port enterprise-network-postgres
```

```powershell
netstat -ano | findstr :5432
```

Test from inside the container:

```powershell
docker exec -it enterprise-network-postgres `
    env PGPASSWORD=postgres `
    psql -h 127.0.0.1 -U postgres -d network_ai `
    -c "SELECT current_user, current_database();"
```

A possible clean local configuration, if Windows port 5432 is already used by another PostgreSQL instance, is:

```yaml
ports:
  - "5433:5432"
```

with:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/network_ai
```

Do not destroy an existing database unless its data is known to be disposable.

---

# 13. Testing Strategy

The project uses layered testing.

## Unit tests

Fast, deterministic, external services mocked where appropriate:

```powershell
uv run pytest -v
```

Examples:

- network tools
- chunking
- API validation
- mocked Gemini interactions

## MCP integration

```powershell
uv run python scripts/test_mcp_server.py
```

Flow:

```text
MCP Client
 |
 v
FastMCP Server
 |
 v
Network tools
```

## Gemini + MCP integration

```powershell
uv run python scripts/test_gemini_mcp.py
```

Flow:

```text
Gemini
 |
 v
Gemini tool declaration
 |
 v
MCP client/session
 |
 v
FastMCP
 |
 v
Network tool
 |
 v
Gemini final answer
```

## RAG integration

```powershell
uv run python scripts/test_rag.py
```

Flow:

```text
Gemini embedding
 |
 v
pgvector
 |
 v
semantic retrieval
```

---

# 14. Recommended Debugging Order

When an end-to-end test fails, isolate layers in this order:

```text
1. Python import
2. Domain/network function
3. PostgreSQL connectivity
4. pgvector schema
5. Embedding API
6. Vector insertion
7. Vector search
8. MCP server
9. MCP client
10. Gemini
11. End-to-end FastAPI
```

Avoid debugging all layers simultaneously.

---

# 15. V6 — Planned: LangGraph

## Objective

Introduce explicit workflow and state orchestration.

Target architecture:

```text
                    User
                     |
                     v
                Supervisor
                /         \
               /           \
              v             v
     Knowledge Agent   Network Agent
              |             |
              v             v
             RAG           MCP
              |             |
              +------+------+
                     |
                     v
                   Gemini
                     |
                     v
                  Answer
```

Concepts to learn:

- Graph
- Node
- Edge
- State
- Conditional routing
- Supervisor
- Specialized agents
- Tool nodes
- Multi-step investigation

Key question:

> When should the assistant use RAG, MCP, or both?

---

# 16. V7 — Planned: Complete Troubleshooting Assistant

Combine:

```text
FastAPI
+
Gemini
+
LangGraph
+
MCP
+
FastMCP
+
RAG
+
PostgreSQL/pgvector
```

Example request:

> R1 has high CPU and interface errors. Investigate the problem and tell me what I should check first.

Target flow:

```text
Supervisor
 |
 +-- Network Agent
 |      |
 |      +-- Device status
 |      +-- Interface errors
 |      +-- Alerts
 |      +-- BGP state
 |
 +-- Knowledge Agent
        |
        +-- High CPU runbook
        +-- Interface troubleshooting
        +-- BGP guidance
 |
v
Combined evidence
 |
v
Gemini
 |
v
Grounded diagnosis
```

---

# 17. V8 — Planned: Production Hardening

Final hardening topics:

```text
Tool validation
Authorization
Structured outputs
Human-in-the-loop
Audit logging
Failure handling
Retries/timeouts
Evaluation
Groundedness checks
Retrieval evaluation
Tool-selection evaluation
Agent execution evaluation
```

Target execution:

```text
Gemini
 |
v
Agent decision
 |
v
Tool validation
 |
v
Authorization
 |
+---- no ----> Reject
|
+---- yes
|
v
Human approval when required
 |
v
Tool execution
 |
v
Audit event
 |
v
Evaluation/monitoring
```

These capabilities should not be described as implemented until they are actually built and tested.

---

# 18. Security Principles

The project intentionally starts with **read-only** network tools.

Allowed examples:

```text
get_device_status
get_device_alerts
get_interface_status
get_bgp_neighbors
```

Avoid exposing a generic arbitrary command executor to the model.

Future mutating operations must consider:

- authentication
- authorization
- input validation
- allow-lists
- human approval
- audit logs
- rollback/failure handling

---

# 19. Development Principles

1. Add one architectural capability at a time.
2. Keep domain logic separate from framework/protocol code.
3. Prefer explicit interfaces over hidden magic.
4. Test each layer independently.
5. Mock expensive/external dependencies in unit tests.
6. Keep secrets in environment variables.
7. Keep infrastructure access read-only initially.
8. Measure retrieval and answer quality before calling a RAG system reliable.
9. Do not claim production-ready capabilities until they are implemented and tested.

---

# 20. Useful Commands

## Run tests

```powershell
uv run pytest -v
```

## Run FastAPI

```powershell
uv run uvicorn src.enterprise_network_ai.main:app --reload
```

## Start PostgreSQL

```powershell
docker compose up -d
```

## Stop PostgreSQL

```powershell
docker compose down
```

## Remove the project's Docker volume

```powershell
docker compose down -v
```

Use `-v` only when deleting the disposable learning database is intentional.

## Inspect PostgreSQL logs

```powershell
docker logs enterprise-network-postgres
```

---

# 21. Learning Milestones

## Milestone 1

```text
FastAPI
Pydantic
HTTP
Data layer
```

## Milestone 2

```text
Gemini
Prompts
LLM integration
Grounded prompting
```

## Milestone 3

```text
Function calling
Tool registry
Tool execution
Agent loop
```

## Milestone 4

```text
MCP
MCP client
MCP server
FastMCP
tool discovery
tool invocation
```

## Milestone 5

```text
Embeddings
Chunking
pgvector
Semantic search
RAG
Grounding
```

## Milestone 6

```text
LangGraph
State
Nodes
Edges
Supervisor
Multi-agent routing
```

## Milestone 7

```text
Combined operational + knowledge investigation
```

## Milestone 8

```text
Reliability
Safety
HITL
Audit
Evaluation
Production controls
```

---

# 22. Final Interview Narrative

A concise description of the project after the full implementation is completed:

> Built an Agentic AI network troubleshooting assistant using Python, FastAPI, Google Gemini, LangGraph, MCP/FastMCP, RAG, PostgreSQL and pgvector. The system separates operational investigation from knowledge retrieval, uses MCP tools for controlled access to network telemetry and diagnostics, uses RAG for runbooks and documentation, and uses LangGraph to orchestrate specialized knowledge and network investigation agents.

The wording should always match the capabilities actually implemented and tested.

---

# 23. README Maintenance Rule

This `README.md` is a **living project document**.

For every future version, update the appropriate sections.

### V6

Update:

- architecture
- folder structure
- dependencies
- setup/run/test commands
- LangGraph state and nodes
- supervisor behavior
- troubleshooting issues

### V7

Update:

- complete architecture
- agent routing
- MCP + RAG interaction
- end-to-end scenarios
- tests

### V8

Update:

- production controls
- HITL
- audit logging
- evaluation
- failure handling
- reliability and security decisions

The README should reflect the **actual implementation status**, not planned functionality presented as completed functionality.

---

# 24. Current Status

```text
V1  ████████████████████ Completed
V2  ████████████████████ Completed
V3  ████████████████████ Completed
V4  ███████████████░░░░░ Implemented / debugging
V5  ███████████░░░░░░░░ In progress
V6  ░░░░░░░░░░░░░░░░░░░ Planned
V7  ░░░░░░░░░░░░░░░░░░░ Planned
V8  ░░░░░░░░░░░░░░░░░░░ Planned
```

Immediate V5 work remaining at the time of this README update:

1. Confirm the Docker PostgreSQL host port and credentials.
2. Make the Python `DATABASE_URL` connection succeed.
3. Initialize the `knowledge_chunks` schema.
4. Ingest knowledge documents.
5. Verify semantic retrieval.
6. Verify the `/knowledge/search` and `/knowledge/ask` endpoints.

---

# 25. Project Philosophy

The project is intentionally built from the fundamentals upward:

```text
API
  |
  v
LLM
  |
  v
Tools
  |
  v
MCP
  |
  v
RAG
  |
  v
LangGraph
  |
  v
Multi-Agent
  |
  v
Production controls
```

The goal is not only to make the system work.

The goal is to understand:

> **what each component does, why it exists, what problem it solves, what happens without it, and how the components interact in a real Agentic AI architecture.**
