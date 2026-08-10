Purpose
-------
This repository implements a lightweight data pipeline and search/indexing platform for booking/ accommodation data. It supports ingestion, transformation, deduplication, vector embedding, indexing (search + vector stores), and a set of operational scripts for one-off and scheduled maintenance tasks.

High-level goals
----------------
- Make core business logic independent of transport and storage implementations.
- Keep `scripts/` responsible for wiring concrete clients, orchestration, and CLI entry points.
- Keep mappings and persistence concerns in `mappers/` and `clients/` respectively.
- Support local developer workflows (docker-compose & local emulators) and production-ready deployment patterns.

Repository layout (summary)
--------------------------
- `src/clients/` : concrete connectors to external systems (DynamoDB, Elasticsearch, Qdrant, S3-local, SQS, embeddings, Spark session, etc.).
- `src/core/` : domain logic grouped by domain subpackages (`ingestion`, `dedup`, `ranking`, `similarity`, `sitemap`, `geo`). Core should express interfaces/abstract contracts and pure business rules.
- `src/mappers/` : translation between domain objects and external storage/index shapes.
- `src/scripts/` : CLI and operational programs that bootstrap clients, configure mappers, and run domain workflows (detect duplicates, export data, generate sitemaps, sync jobs).
- `src/utils/` : support utilities (configuration, logging, retry, time helpers, custom exceptions).
- `data/` : local data snapshots, export logs, and static JSON files used for mapping and tests.
- `tests/` : unit tests grouped parallel to the code structure.

Runtime components and services
------------------------------
- DynamoDB (local or AWS): primary source/target for structured booking data and domain records. Mapped by `mappers/dynamodb_document_mapper.py` and accessed via `clients/dynamodb_client.py`.
- Elasticsearch: text search index and some aggregations. Mapped via `mappers/es_document_mapper.py` and accessed via `clients/es_client.py`.
- Qdrant: vector store for embeddings-based similarity and nearest-neighbour search. Accessed via `clients/qdrant_client.py` and mapped in `mappers/qdrant_document_mapper.py`.
- Embedding service: external (or local) embedding generator used to convert text into vectors. Implemented in `clients/embedding_client.py`.
- S3-local: local filesystem-backed S3 for storing artifacts, snapshots, and static blobs. `clients/s3_local_client.py` handles access.
- Spark (optional): `clients/spark_session.py` provides a Spark session where heavy ETL or large-scale ingestion jobs run.
- Localstack / test infra: used in CI/local dev to emulate AWS services.

Data flow (typical pipelines)
-----------------------------
1. Ingestion: raw files (CSV/JSON/Iceberg snapshots) are read (scripts like `run_sync.py` / `sync_iceberg.py`) and normalized into domain objects in `core/ingestion/`.
2. Mapping & persistence: domain objects are translated into storage shapes by `mappers/` and persisted via `clients/` (DynamoDB, S3).
3. Embedding & similarity: text fields are passed through the embedding function (pluggable) and results are stored in Qdrant; `core/similarity/` contains the logic for computing candidate sets and scoring.
4. Deduplication: `core/dedup/` orchestrates candidate generation, vector/text similarity, and dedup decisioning. It must depend only on abstract embedding and storage interfaces (see "Best practices").
5. Indexing & ranking: `core/ranking/` prepares documents for ES and vector store indexing; `scripts/export_to_qdrant.py` and `scripts/export_to_s3_local.py` perform the writes.
6. Operational outputs: sitemap generation, export logs, and other artifacts land in `data/` or S3-local buckets.

Deployment & local development
------------------------------
- `docker-compose.yml` and `Dockerfile` configure a development stack (Elasticsearch, Qdrant, DynamoDB-local, Localstack, and optional Spark). Use `docker-compose up` for a local environment.
- `pyproject.toml` + `requirements.txt` manage Python dependencies. `requirements-ci.txt` contains pinned deps for CI runs.
- Local persisted volumes: `data/`, `s3_local/`, `es_data/`, `qdrant_data/` — help reproduce state between runs and are used by the local compose stack.

Key design rules and recommendations
-----------------------------------
- Dependency direction: `scripts/` → `core/` → `mappers/` → `clients/` (wiring in `scripts/`, business rules in `core/`).
- Pluggable embedding: never call a concrete `clients.embedding_client` directly from `core/`. Instead:
	- Preferred: define an abstract embedding interface in `core/` (or accept an `embedding_fn` parameter) and have scripts pass the concrete function at runtime.
	- Short-term: add an `embedding_fn` parameter to dedup/similarity entry points and remove direct imports from `core/`.
- Small mappers: each client that transforms domain-shaped data should have a corresponding `mappers/` entry to keep conversion logic testable and contained.
- Idempotent scripts: design `scripts/` to be idempotent and safe to retry for operational reliability.

Testing and CI
--------------
- Unit tests live under `tests/unit` and exercise `core/`, `mappers/`, and `clients/` in isolation using fixtures and small local emulators.
- Integration smoke tests should run against the `docker-compose` stack (Elasticsearch + Qdrant + DynamoDB-local). CI jobs should bring up these services and run a small end-to-end scenario.

Observability and ops
---------------------
- Logging: use `src/utils/logging.py` for standardized logs across scripts and clients.
- Monitoring: add simple metrics (counts of ingested records, index latencies, dedup decisions) and export them to the host metrics collector (Prometheus/Grafana) if available in production.
- Backups & snapshots: maintain snapshots for ES and Qdrant; use `s3_local/` for local artifact storage and mirror to durable backup in production.

Security and credentials
------------------------
- Prefer environment-based credentials for production (IAM, secrets manager). For local development, use `localstack` or environment variables pointing to local emulators.
- Do not check secrets into the repository. Use `.env` (gitignored) for local overrides.

Common operational scripts (what's already present)
--------------------------------------------------
- `scripts/detect_duplicates.py` — dedup detection runner.
- `scripts/export_to_dynamodb.py`, `export_to_qdrant.py`, `export_to_s3_local.py` — export jobs.
- `scripts/generate_nearby_sitemap.py`, `generate_property_sitemap.py`, `generate_root_sitemap_index.py` — sitemap generation.
- `scripts/run_sync.py`, `scripts/sync_iceberg.py` — sync/ingest orchestrators.

Next actionable improvements
--------------------------
1. Remove direct embedding imports from `core/` and make embedding pluggable (high priority for testability).
2. Add lightweight integration tests that bring up `docker-compose` stack and validate end-to-end ingest → embed → index → query.
3. Add README sections for local dev: `docker-compose up`, how to populate `s3_local/`, and how to run dedup flows.

Contact / maintainers
---------------------
See repository README.md for maintainers and contribution guidelines.

Appendix: Quick checklist for reviewers
------------------------------------
- `core/` must not import `clients/` directly.
- Every client used for persisting domain shaped entities should have a `mappers/` counterpart.
- Scripts should contain wiring only; business logic belongs in `core/`.

