from app.db.base import Base
from enum import StrEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class ExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class Execution(Base):

    __tablename__ = "executions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    prompt: Mapped[str] = mapped_column(Text)
    status: Mapped[ExecutionStatus] = mapped_column(Enum(ExecutionStatus, name="execution_status", values_callable=lambda enum_cls: [
        member.value for member in enum_cls
    ]), server_default=ExecutionStatus.PENDING.value, default=ExecutionStatus.PENDING)
    
    result: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

