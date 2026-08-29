from sqlalchemy.ext.asyncio import AsyncSession
from app.executions.model import Execution

async def create_execution(session: AsyncSession, *, prompt: str) -> Execution:
    new_execution = Execution(
        prompt=prompt
    )

    async with session.begin():
        session.add(new_execution)
        await session.flush()
