from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from fastapi import status
from app.ai.provider import FakeAIProvider
from app.executions.schemas import ExecutionCreate, ExecutionResponse

from app.executions.service import create_execution, run_execution

router = APIRouter(
    prefix="/executions",
    tags=["executions"]
)

@router.post("", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution_endpoint(payload: ExecutionCreate, session: AsyncSession = Depends(get_session)) -> ExecutionResponse:
    execution = await create_execution(session, prompt=payload.prompt)
    provider = FakeAIProvider()

    await run_execution(session, execution=execution, provider=provider)

    return execution
