from typing import Protocol

import hashlib


class EmbeddingProvider(Protocol):

    async def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class FakeEmbeddingProvider:
    @staticmethod
    async def embed(texts: list[str]) -> list[list[float]]:
        return [[ord(char) * 1.13 for char in hashlib.sha256(string.encode("utf-8")).hexdigest()] for string in texts]


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(FakeEmbeddingProvider().embed(["foo", "bar"])))
