import re
from collections import deque
from copy import copy
from hashlib import sha256
from typing import Generator

from app.schemas.chunk import ChunkCreate


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

    def chunk(self, normalized_text: str) -> list[ChunkCreate]:
        chunks = []
        chunk_index = 1
        text = ""
        chunk_size = 0
        overlap_size = 0
        overlap_queue = deque()
        overlap_to_add = None

        for sentence, sentence_len in self.iter_sentences(normalized_text):
            text = text + sentence
            chunk_size += sentence_len
            if overlap_size < self.overlap:
                overlap_size += sentence_len
            else:
                del_sentence, del_sentence_len = overlap_queue.popleft()
                overlap_size -= del_sentence_len + sentence_len

            overlap_queue.append((sentence, sentence_len,))

            if chunk_size > self.chunk_size:
                if chunk_index != 1:
                    chunk_size += overlap_size
                    text = " ".join([seq for seq, _ in overlap_to_add]) + " " + text

                chunks.append(ChunkCreate(chunk_index=chunk_index,
                                          chunk_text=text,
                                          chunk_hash=sha256(text.encode()).hexdigest(),
                                          token_count=chunk_size))
                chunk_index += 1
                chunk_size = 0
                text = ""
                overlap_to_add = copy(overlap_queue)

        return chunks
