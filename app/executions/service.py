from sqlalchemy.ext.asyncio import AsyncSession
from app.executions.model import Execution, ExecutionStatus
from sqlalchemy import func
from app.ai.provider import FakeAIProvider

class InvalidExecutionStateTransitionError(Exception):
        pass

class AIProviderError(Exception):
    pass

async def create_execution(session: AsyncSession, *, prompt: str) -> Execution:
    new_execution = Execution(
        prompt=prompt
    )

    async with session.begin():
        session.add(new_execution)
        await session.flush()

    return new_execution

async def mark_execution_running(session: AsyncSession, *, execution: Execution) -> None:
    async with session.begin():
        if execution.status != ExecutionStatus.PENDING:
            raise InvalidExecutionStateTransitionError()

        execution.status = ExecutionStatus.RUNNING
        execution.started_at = func.now()


async def mark_execution_succeeded(session: AsyncSession, *, execution: Execution, result: str) -> None:
     async with session.begin():
        if execution.status != ExecutionStatus.RUNNING:
            raise InvalidExecutionStateTransitionError()
        
        execution.status = ExecutionStatus.SUCCEEDED
        execution.result = result
        execution.error = None
        execution.finished_at = func.now()

async def mark_execution_failed(session: AsyncSession, *, execution: Execution, error: str) -> None:
     async with session.begin():
        if execution.status != ExecutionStatus.RUNNING:
            raise InvalidExecutionStateTransitionError()
        
        execution.status = ExecutionStatus.FAILED
        execution.result = None
        execution.error = error
        execution.finished_at = func.now()

async def run_execution(session: AsyncSession, *, execution: Execution, provider: FakeAIProvider) -> None:

    await mark_execution_running(session, execution=execution)
    try:
        result = await provider.execute(prompt=execution.prompt)
    except AIProviderError as exc:
        await mark_execution_failed(session, execution=execution, error=str(exc))
        raise 
    
    await mark_execution_succeeded(session, execution=execution, result=result)

        