from pydantic import BaseModel, Field


class DeviceStatus(BaseModel):
    hostname: str
    vendor: str
    model: str
    status: str
    cpu: float
    memory: float


class Alert(BaseModel):
    severity: str
    message: str


class KnowledgeSearchResponse(BaseModel):
    document_name: str
    title: str
    chunk_index: int
    content: str
    similarity: float


class KnowledgeAskRequest(BaseModel):
    question: str = Field(
        min_length=3,
        description="Question about network documentation",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of knowledge chunks to retrieve",
    )


class KnowledgeSource(BaseModel):
    document_name: str
    title: str
    similarity: float


class KnowledgeAskResponse(BaseModel):
    answer: str
    sources: list[KnowledgeSource]