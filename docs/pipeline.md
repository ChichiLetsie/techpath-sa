# TechPath SA - Data Pipeline Architecture

The pipeline follows a robust **ETL / ELT** architectural pattern executed via `python pipeline/run_pipeline.py`.

## Stages

1. **Extract**
   - Independent modules scrape public sources or ingest curated feeds.
   - Fault-isolated try/except blocks guarantee that if one source fails, remaining collectors proceed unaffected.
   - Raw records are timestamped and archived under `data/raw/`.

2. **Transform**
   - Normalises skill nomenclature (e.g., `Amazon Web Services` → `AWS`).
   - Standardises South African cities and remote flags.
   - Strips corporate noise from company names and eliminates duplicates.

3. **Validate**
   - Pydantic models (`ValidatedJob`, `ValidatedOpportunity`) verify data types, required strings, and structure prior to insertion.

4. **Load**
   - Inserts clean records into PostgreSQL via SQLAlchemy.
   - Performs duplicate checks against existing records before committing.