from typing import Protocol

import hashlib


class EmbeddingProvider(Protocol):

    async def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class FakeEmbeddingProvider:

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[ord(char) * 1.13 for char in string] for string in texts]


if __name__ == '__main__':
    import asyncio
    print(asyncio.run(FakeEmbeddingProvider().embed(["foo", "bar"])))
