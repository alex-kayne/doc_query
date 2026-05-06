from hashlib import sha256


class DocumentParser:

    @staticmethod
    def _normalize_text(text: str) -> str:
        return text

    @staticmethod
    def _calc_text_hash(normalized_text: str) -> str:
        return sha256(normalized_text.encode()).hexdigest()

    @staticmethod
    def _parse_docx(text: str, ) -> tuple[str, str]:
        normalized_text = DocumentParser._normalize_text(text)
        text_hash = DocumentParser._calc_text_hash(normalized_text)
        return normalized_text, text_hash

    @staticmethod
    def parse(text: str, content_type: str) -> tuple[str, str]:
        try:
            return strategy[content_type](text)
        except KeyError:
            raise ValueError(f"Не поддерживаем тип контента: {content_type}")

strategy = {
        "docx": DocumentParser._parse_docx,
    }
