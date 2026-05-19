import re
from collections.abc import Iterator
from app.schemas.chunk import ChunkCreate
from hashlib import sha256
from collections import deque


class DocumentChunker:
    chunk_size = 200
    overlap = 40
    cur_overlap = 0
    new_overlap_queue = deque()
    old_overlap_queue = deque()

    @staticmethod
    def iter_sentences(normalized_text: str) -> Iterator[str]:
        pattern = r"(?<=[.!?])\s+"

        for sentence in re.split(pattern, normalized_text):
            sentence = sentence.strip()
            if sentence:
                yield sentence

    def _modify_overlap(self, sentence: str) -> None:
        if self.cur_overlap < self.overlap:
            self.cur_overlap += len(sentence)
        else:
            self.cur_overlap -= len(self.overlap_queue.popleft())
        self.overlap_queue.append(sentence)

    def _add_chunk(self, token_count: int, text: str, chunk_index: int,
                   chunks: list) -> None:
        if chunk_index == 1:
            chunk_text = text
        else:
            chunk_text = " ".join(self.old_overlap_queue) + text
        self.old_overlap_queue = self.new_overlap_queue.copy()
        chunks.append(
            ChunkCreate(chunk_index=chunk_index,
                        chunk_text=chunk_text,
                        chunk_hash=sha256(chunk_text.encode()).hexdigest(),
                        token_count=token_count))
        return None

    def chunk(self, normalized_text: str) -> list[ChunkCreate]:
        chunks = []
        chunk_index = 1
        token_count = 0
        text = ""

        for sentence in self.iter_sentences(normalized_text):
            if token_count > self.chunk_size:
                self._add_chunk(token_count, text, chunk_index, chunks)
                chunk_index += 1
                text = ""
                self.cur_overlap = 0
                self.overlap_queue = deque()
                token_count = 0

            token_count += len(sentence.split())
            text += f"{sentence} "
            self._modify_overlap(sentence)

        self._add_chunk(token_count, text, chunk_index, chunks)

        return chunks
