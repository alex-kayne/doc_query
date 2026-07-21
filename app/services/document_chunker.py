import re
from collections import deque
from copy import copy
from hashlib import sha256
from typing import Generator
from app.services.embedding_provider import FakeEmbeddingProvider
from app.schemas.chunk import ChunkCreate
from tenacity import retry, stop_after_attempt, wait_exponential


class DocumentChunker:
    chunk_size = 200
    overlap = 40  # 40 слов

    @staticmethod
    def iter_sentences(normalized_text: str) -> Generator[tuple[str, int]]:
        pattern = r"(?<=[.!?])\s+"

        for sentence in re.split(pattern, normalized_text):
            sentence = sentence.strip()
            if sentence:
                yield sentence, sentence.count(" ") + 1

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _create_chunks(self, chunk_size: int, chunk_inx: int, sentence_list: list[str],
                             overlap_to_add: deque | None) -> ChunkCreate:
        if chunk_inx != 1:
            text = " ".join(sentence_list)
            for seq, seq_len in reversed(overlap_to_add or []):
                text = seq + " " + text
                chunk_size += seq_len
        else:
            text = " ".join(sentence_list)

        embedding = await FakeEmbeddingProvider.embed(sentence_list)

        return ChunkCreate(chunk_index=chunk_inx,
                           chunk_text=text,
                           chunk_hash=sha256(text.encode()).hexdigest(),
                           token_count=chunk_size,
                           embedding=embedding)

    async def chunk(self, normalized_text: str) -> list[ChunkCreate]:
        chunks = []
        chunk_index = 1
        sentence_list = []
        chunk_size = 0
        overlap_size = 0
        overlap_queue = deque()
        overlap_to_add = None

        for sentence, sentence_len in self.iter_sentences(normalized_text):
            sentence_list.append(sentence)
            chunk_size += sentence_len

            if overlap_size > self.overlap:
                del_sentence, del_sentence_len = overlap_queue.popleft()
                overlap_size -= del_sentence_len

            overlap_size += sentence_len
            overlap_queue.append((sentence, sentence_len,))

            if chunk_size > self.chunk_size:
                chunks.append(
                    await self._create_chunks(chunk_size, chunk_index, sentence_list, overlap_to_add))
                chunk_index += 1
                chunk_size = 0
                sentence_list = []
                overlap_to_add = copy(overlap_queue)

        if sentence_list:
            chunks.append(await self._create_chunks(chunk_size, chunk_index, sentence_list, overlap_to_add))

        return chunks
