# Enterprise Network AI

A FastAPI-based enterprise network troubleshooting assistant that uses Google Gemini with tool calling and a local MCP server to inspect network telemetry and answer operational questions from a simulated enterprise environment.

## Overview

This project demonstrates a network operations AI workflow in which an LLM can:

- inspect a simulated inventory of network devices
- query device status, alerts, interface health, and BGP neighbors
- reason over the observed telemetry
- provide troubleshooting guidance without changing network configuration

The application is designed to be read-only and safe by default. It uses a controlled tool registry and an MCP-based tool layer to keep model access limited to approved network diagnostics.

## Architecture

The current design is the V4 flow:

```text
User
  |
  v
FastAPI API
  |
  v
Gemini LLM
  |
  v
MCP Client
  |
  v
MCP Protocol
  |
  v
FastMCP Server
  |
  v
Read-only Network Tools
```

The key components are:

- `src/enterprise_network_ai/main.py` — FastAPI application and API routes
- `src/enterprise_network_ai/llm.py` — Gemini function-calling logic and tool execution
- `src/enterprise_network_ai/gemini_mcp.py` — MCP client for connecting to a local FastMCP server
- `src/enterprise_network_ai/mcp_server.py` — FastMCP server exposing network tools
- `src/enterprise_network_ai/network_tools.py` — read-only device and interface telemetry functions
- `src/enterprise_network_ai/data.py` — simulated network inventory and alerts

## Features

- Device status lookup
- Alert retrieval for network devices
- Interface health checks
- BGP neighbor inspection
- Troubleshooting endpoint powered by Gemini + tool calling
- Strict read-only tooling for safe operations

## Prerequisites

- Python 3.11+
- A Google Gemini API key
- `uv` recommended for running the project

## Setup

1. Clone the repository.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

4. Create a `.env` file in the project root with your Gemini credentials:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Run the API

```bash
uv run uvicorn enterprise_network_ai.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Get device status

```http
GET /devices/{device_id}/status
```

Example:

```bash
curl http://127.0.0.1:8000/devices/R1/status
```

### Get device alerts

```http
GET /devices/{device_id}/alerts
```

Example:

```bash
curl http://127.0.0.1:8000/devices/R1/alerts
```

### Troubleshoot a device

```http
POST /troubleshoot
```

Request body:

```json
{
  "device_id": "R1",
  "question": "Why is CPU utilization elevated on this device?"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/troubleshoot \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "R1",
    "question": "Why is the CPU high?"
  }'
```

## Network Tools Exposed

The MCP server exposes read-only diagnostics such as:

- `get_device_status(device_id)`
- `get_device_alerts(device_id)`
- `get_interface_status(device_id, interface_name)`
- `get_bgp_neighbors(device_id)`

These tools are intentionally limited to inspection and analysis.

## Example Device Data

The sample catalog ships with a single simulated router:

- Device ID: `R1`
- Vendor: `Cisco`
- Model: `ASR1001-X`
- Status: `up`
- CPU: `91%`
- Memory: `62%`

## Testing

Run the project tests with:

```bash
pytest
```

The suite currently covers:

- network tool behavior
- API behavior for successful and missing-device requests

## Project Structure

```text
enterprise-network-ai/
├── src/
│   └── enterprise_network_ai/
│       ├── __init__.py
│       ├── data.py
│       ├── gemini_mcp.py
│       ├── llm.py
│       ├── main.py
│       ├── mcp_server.py
│       ├── network_tools.py
│       └── tools.py
├── tests/
│   ├── test_api.py
│   ├── test_llm.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── scripts/
    ├── test_gemini_mcp.py
    ├── test_gemini_tools.py
    └── test_mcp_server.py
```

## Notes

This project is an educational and demonstration implementation of AI-assisted network troubleshooting. It uses simulated network data rather than live production telemetry, so it is suitable for local development, experimentation, and learning about agentic LLM integration with network APIs and MCP tools.
