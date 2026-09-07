import asyncio

class AIProviderError(Exception):
    pass

class FakeAIProvider:
    def __init__(self, *, should_fail: bool = False):
        self.should_fail = should_fail

    async def execute(self, *, prompt: str) -> str:
        await asyncio.sleep(2)

        if self.should_fail:
            raise AIProviderError("Fake Provider failure")

        
        return f"Fake AI result for: {prompt}"