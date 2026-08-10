Purpose
-------
A minimal service that ingests booking data, detects duplicates, indexes searchable representations, and exposes one-off operational scripts for maintenance.

Layers (dependency order)
-------------------------
- scripts: entry-point and operational orchestration (CLIs, scheduled jobs). Instantiate dependencies and call into `core`.
- core: application business logic and domain rules (grouped by domain subfolders such as `core/ingestion/`, `core/dedup/`, `core/ranking/`, `core/similarity/`, `core/geo/`, and `core/sitemap/`). Declares abstract interfaces for external interactions — no concrete clients here.
- mappers: translation layer between domain objects and external storage/index formats (marshal/unmarshal, schema mappings).
- clients: concrete integrations with external systems (DynamoDB, Elasticsearch, Qdrant, S3, embedding services).

Hard rule (ideal) and current exception
-------------------------------------
Dependencies must flow downward through interfaces: `core/` should not import concrete `clients/` implementations directly. Core must depend only on abstract contracts (or function parameters) that `clients/` implement. All wiring of concrete implementations belongs in `scripts/` (or a DI/bootstrap module).

Practical note: the current codebase contains one exception — `core/dedup/duplicate_detector.py` imports `generate_embedding` from `clients/embedding_client.py` and calls it directly. This violates the hard rule. Recommended quick fixes:
- Preferred: extract an abstract embedding interface in `core/` (or accept an `embedding_fn` parameter), then have `scripts/` pass `clients.embedding_client.generate_embedding` at runtime.
- Shorter change: modify `find_duplicates(...)` to accept an `embedding_fn` argument and remove the direct import from `core/`.


Request flow example — duplicate detection (file-by-file)
-------------------------------------------------------
1. `scripts/detect_duplicates.py` — CLI: parses args, constructs concrete clients and mappers, injects them, calls `DuplicateDetector`.
2. `core/dedup/duplicate_detector.py` — business logic: `DuplicateDetector` uses abstract interfaces (e.g., storage/embedding interfaces) to fetch candidates and compute similarity; it emits duplicate decisions as domain objects.
3. `mappers/dynamodb_document_mapper.py` — translates domain objects/rows to DynamoDB item shapes used by `clients/`.
4. `clients/dynamodb_client.py` — concrete network/IO implementation that executes DynamoDB calls and returns raw data to `mappers/`.

Implementation reality for duplicate detection (current run-time path):
1. `scripts/detect_duplicates.py` — constructs concrete clients (e.g., `clients.spark_session`, `clients.embedding_client`) and calls `core.find_duplicates()`.
2. `core/dedup/duplicate_detector.py` — currently imports `clients.embedding_client.generate_embedding` directly and uses it inside `text_similarity()`; it performs the comparison logic and returns matches.
3. `mappers/dynamodb_document_mapper.py` — mapping helpers (when persisting or reading tracked domain objects).
4. `clients/dynamodb_client.py` — concrete DynamoDB I/O used elsewhere by scripts.

Where new code goes
-------------------
- New business logic → put under `core/`, grouped by domain subfolder (e.g., `core/dedup/`, `core/ingestion/`, `core/similarity/`), export clear interfaces.
- New external system → add a `clients/` implementation plus a matching `mappers/` entry to adapt its data model into existing domain objects.
- One-off operational task → add to `scripts/` (small, focused CLIs or scheduled jobs). Keep `scripts/` responsible for wiring concrete implementations and bootstrap logic.

Reviewer rules (quick checklist)
------------------------------
- Does `core/` import concrete `clients/`? If yes, reject and require interface extraction.
- Is each client accompanied by a mapper when it persists or reads domain-shaped entities? Prefer small, testable mappers.
- Are bootstrap/wiring steps in `scripts/` and not duplicated inside core logic?

That's all — follow the downward-only dependency rule and group domain code inside `core/` subfolders.
