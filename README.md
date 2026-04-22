# doc_query

`doc_query` — это backend-сервис для загрузки, фоновой обработки, индексации и последующего поиска по документам. Проект разрабатывается как production-like pet-project с AI-функциональностью для демонстрации backend engineering подхода к построению RAG-систем.

## Цель проекта

Собрать не просто демо с вызовом LLM, а полноценный backend-сервис, в котором есть:

- API для загрузки и управления документами
- фоновая обработка через очередь задач
- pipeline парсинга и индексации
- semantic search / hybrid retrieval
- ответы на вопросы по документам
- измеримые метрики производительности и качества retrieval

Проект ориентирован на демонстрацию навыков Python backend engineer c AI integrations.

---

## Ключевые возможности

### Уже реализуемые / базовые
- FastAPI backend
- PostgreSQL как основное хранилище
- Redis + ARQ для фоновых задач
- Alembic для миграций
- lifecycle документов и задач
- базовые ingestion-метрики
- загрузка документов и импорт из URL / docs sources
- parsing и очистка текста
- chunking
- embeddings и vector index
- lexical retrieval + dense retrieval
- hybrid retrieval через Reciprocal Rank Fusion (RRF)
- question answering с цитированием источников
- оценка retrieval quality через Recall@k и MRR
- логирование, retries, timeout policies, benchmarking

---

## Архитектурная идея

Сервис строится по принципу разделения API и тяжёлой фоновой обработки.

### Основной pipeline
1. Клиент создаёт dataset
2. Клиент загружает документ
3. Документ получает статус `queued`
4. В очередь ставится задача обработки
5. Worker обрабатывает документ
6. В дальнейшем документ будет проходить этапы:
   - parsing
   - cleaning
   - chunking
   - embeddings
   - indexing

---

## Технологический стек

- **Python 3.12+**
- **FastAPI**
- **PostgreSQL**
- **Redis**
- **ARQ**
- **SQLAlchemy 2.x**
- **Alembic**
- **Docker Compose**

Планируемо:
- **pgvector**
- embedding / LLM provider через абстракцию клиентов
- retrieval evaluation scripts

---
