from app.executions.model import ExecutionStatus
from pydantic import BaseModel, ConfigDict

from datetime import datetime
from uuid import UUID



class ExecutionCreate(BaseModel):
    prompt: str


class ExecutionResponse(BaseModel):
    id: UUID
    prompt: str
    status: ExecutionStatus

    result: str | None
    error: str | None

    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = ConfigDict(from_attributes=True)