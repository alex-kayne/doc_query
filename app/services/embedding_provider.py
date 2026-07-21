import hashlib
from typing import Protocol

from tenacity import retry, stop_after_attempt, wait_exponential


class EmbeddingProvider(Protocol):

    async def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class FakeEmbeddingProvider:

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def embed(text: list[str]) -> list[list[float]]:
        return [[char * 1.13 for char in hashlib.sha256(chunk_text.encode("utf-8")).digest()] for chunk_text in text]


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(FakeEmbeddingProvider().embed(["foo", "bar",])))
