# DOMAIN Knowledge Indexing Plan

## Status

Deferred for later design and implementation.

This note captures the current intent so the idea can be resumed without
reconstructing the discussion.

## Purpose

Use the DOMAIN decomposition and its resulting workspace contents to create
queryable derived indexes so information can be retrieved without manually
searching through folders.

The intended outcome is not to replace the filesystem as authority. The
filesystem remains authoritative. The indexes are derived query layers.

## Core Idea

Build two complementary derived indexes over the DOMAIN workspace:

1. A structural index:
   - hypergraph representation of Categories, Knowledge Types, Knowledge
     Subjects / Knowledge Artifacts, objectives, units, and their bindings
   - used for explicit relationship queries

2. A semantic index:
   - embeddings derived from the textual contents of each KTY's production
     documents
   - used for semantic retrieval over the authored knowledge

These two indexes should work together rather than being collapsed into one
database model.

## Architectural Position

- Authoritative source:
  - DOMAIN decomposition files
  - Category / Knowledge Type folders
  - production documents inside each KTY folder

- Derived structural layer:
  - hypergraph snapshot built from the workspace
  - read-only derivation
  - suitable for structural traversal and scoped retrieval

- Derived semantic layer:
  - vector index built from chunked KTY production-document content
  - every embedded chunk must preserve provenance back to source files

## Existing Fit With Current Pipeline

The repo already contains a DOMAIN hypergraph concept and agent:

- `DOMAIN_HYPERGRAPH` derives normalized tables and JSON from the DOMAIN
  workspace
- this is the existing starting point for the structural index

The missing future layer is the semantic indexing stage:

- chunk the textual contents of KTY production documents
- generate embeddings
- store them in a vector database with provenance and structural references

## Recommended Representation Split

### Hypergraph layer

Store explicit structure such as:

- `CATEGORY`
- `KNOWLEDGE_TYPE`
- `KNOWLEDGE_ARTIFACT`
- `ATOMIC_UNIT`
- `OBJECTIVE`

And explicit bindings such as:

- `IN_CATEGORY`
- `HAS_ARTIFACT`
- `LEDGER_ROW`
- `KTY_SUPPORTS_OBJ`

Use the hypergraph for questions like:

- Which Knowledge Types support a given objective?
- Which artifacts belong to a given KTY?
- Which Categories contain KTYs related to a given unit or objective?

### Vector layer

Store semantic content for retrieval, not structure.

Preferred embedding scope:

- `Scoping.md` sections
- each `KA-*.md` artifact
- or smaller heading / paragraph chunks within each `KA-*.md`

Avoid embedding only one vector per whole KTY folder, because that is likely
too coarse for useful retrieval.

## Provenance Requirements For Embedded Chunks

Each embedded chunk should preserve, at minimum:

- `CategoryID`
- `KnowledgeTypeID`
- `SubjectID` when available
- artifact filename
- source path
- section / heading reference
- chunk ordinal
- source text or a stable source-text pointer

This allows semantic retrieval results to be expanded back into filesystem
context and structural context.

## Query Modes To Support Later

### Structural query

Examples:

- "Which KTYs support objective OBJ-X?"
- "What artifacts belong to KTY-CC-TT?"

Primary engine:

- hypergraph layer

### Semantic query

Examples:

- "What does the domain say about onboarding exceptions?"
- "Find guidance related to escalation thresholds."

Primary engine:

- vector layer

### Hybrid query

Examples:

- semantically retrieve relevant chunks, then expand to neighboring KTY /
  objective / category nodes
- structurally narrow the scope to a Category or KTY set, then perform vector
  retrieval only within that scoped subset

Primary engine:

- both layers together

## Important Constraints

- Do not make the database authoritative.
- Do not treat the hypergraph or vector store as replacements for the source
  files.
- Do not try to store all text content as hypergraph structure.
- Do not rely on whole-KTY embeddings as the only semantic representation.

## Suggested Implementation Order For Later

1. Finalize DOMAIN decomposition and KTY document generation.
2. Run and validate `DOMAIN_HYPERGRAPH` as the structural index.
3. Define chunking rules for KTY production documents.
4. Define the embedding record schema with provenance fields.
5. Build a vector indexing pipeline over the chunked artifacts.
6. Design hybrid query workflows that combine graph scope with semantic
   retrieval.
7. Only after the query model is proven, decide whether a specialized graph
   or hypergraph database is actually needed.

## Deferred Decisions

These decisions remain open:

- exact storage engine for the hypergraph
- exact storage engine for the vector index
- chunk size and chunk boundary policy
- whether to embed `Scoping.md`, `KA-*.md`, or both
- whether to maintain incremental indexing or only rebuild snapshots
- how hybrid retrieval should rank / merge graph and vector results

## Short Summary

The intended future design is:

- filesystem = authority
- hypergraph = structural query index
- vector database = semantic retrieval index
- hybrid query = graph scoping + vector retrieval + provenance back to source

This work is intentionally deferred until the DOMAIN structure and contents are
stable enough to index usefully.
