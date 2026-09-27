from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .data import devices as DEVICES
from .gemini_mcp import ask_network_assistant
from .models import Alert, DeviceStatus

from .rag import (
    ask_knowledge_question,
    retrieve_knowledge,
)
from .models import (
    Alert,
    DeviceStatus,
    KnowledgeAskRequest,
    KnowledgeAskResponse,
    KnowledgeSearchResponse,
)


app = FastAPI(
    title="Enterprise Network AI Assistant",
    version="4.0.0",
)


class TroubleshootingRequest(BaseModel):
    device_id: str = Field(
        min_length=1,
        description="Network device identifier",
    )

    question: str = Field(
        min_length=3,
        description="Network troubleshooting question",
    )


class TroubleshootingResponse(BaseModel):
    device_id: str
    question: str
    answer: str


@app.get(
    "/devices/{device_id}/status",
    response_model=DeviceStatus,
)
def get_device_status(device_id: str):

    device = DEVICES.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return {
        "device_id": device_id,
        "hostname": device["hostname"],
        "vendor": device["vendor"],
        "model": device["model"],
        "status": device["status"],
        "cpu": device["cpu"],
        "memory": device["memory"],
    }


@app.get(
    "/devices/{device_id}/alerts",
    response_model=list[Alert],
)
def get_device_alerts(device_id: str):

    device = DEVICES.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device["alerts"]


@app.post(
    "/troubleshoot",
    response_model=TroubleshootingResponse,
)
async def troubleshoot(
    request: TroubleshootingRequest,
):

    if request.device_id not in DEVICES:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    question = (
        f"Investigate device {request.device_id}.\n"
        f"User question: {request.question}"
    )

    try:

        answer = await ask_network_assistant(
            question=question,
        )

        return TroubleshootingResponse(
            device_id=request.device_id,
            question=request.question,
            answer=answer,
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get(
    "/knowledge/search",
    response_model=list[KnowledgeSearchResponse],
)
def search_knowledge(
    q: str,
    top_k: int = 5,
):

    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    if top_k < 1 or top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10.",
        )

    results = retrieve_knowledge(
        question=q,
        top_k=top_k,
    )

    return [
        KnowledgeSearchResponse(
            document_name=result[
                "document_name"
            ],
            title=result["title"],
            chunk_index=result[
                "chunk_index"
            ],
            content=result["content"],
            similarity=result[
                "similarity"
            ],
        )
        for result in results
    ]


@app.post(
    "/knowledge/ask",
    response_model=KnowledgeAskResponse,
)
def ask_knowledge(
    request: KnowledgeAskRequest,
):

    try:

        result = ask_knowledge_question(
            question=request.question,
            top_k=request.top_k,
        )

        return KnowledgeAskResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc