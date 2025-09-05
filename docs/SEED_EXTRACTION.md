# Seed Extraction Documentation

The seed extraction system enables the Chirality App to extract and use text content from chirality-framework matrix cells as "seeds of thought" for semantic valley traversal.

## Overview

Seed extraction transforms matrix cells (C, D, X, E) from a framework run into compact text arrays that can be injected into LLM prompts as `initialVector` guidance. This provides deterministic scaffolding for document generation while maintaining flexibility for AI creativity.

## Architecture

### Core Components

1. **Seed Extractor** (`lib/seeds/seedExtractor.ts`)
   - Extracts text from normalized matrix cells
   - Applies configurable heuristics (trimming, deduplication, length limits)
   - Handles missing/invalid matrices gracefully
   - Collates warnings for soft failures

2. **Streaming Ingestion** (`lib/framework/ingest.ts`)
   - Uses Node.js readline for memory-efficient JSONL parsing
   - Supports large matrix files (10k+ lines) without memory overflow
   - Configurable checksum verification

3. **Cache System** (`runs/<runId>/seeds.json`)
   - Validates freshness using file mtime and size
   - Best-effort persistence with graceful failure handling
   - Cache metadata (sourceMtime/sourceSize) is stored under `seeds.metadata`

4. **API Integration** (`/api/export/run?include=seeds`)
   - Cache-aware extraction with automatic invalidation
   - Returns structured response per specification
   - Soft failure mode with warnings

## Configuration

Environment variables control seed extraction behavior:

```bash
# Enable text processing heuristics (trimming, deduplication)
SEEDS_ENABLE_HEURISTICS=false

# Item count constraints per matrix
SEEDS_MIN_ITEMS=6
SEEDS_MAX_ITEMS=12

# Maximum text length per item (characters)
SEEDS_MAX_LEN=120

# Verify file checksums during ingestion
SEEDS_VERIFY_CHECKSUMS=true

# Persist extracted seeds to cache
SEEDS_PERSIST=true

# Base directory for framework runs
CHIRALITY_RUNS_DIR=runs
```

## API Usage

### Extract Seeds from a Framework Run

```bash
GET /api/export/run?runId=run_123456_abcd&include=seeds
```

### Response Structure

```json
{
  "runId": "run_123456_abcd",
  "files": {
    "runJson": "runs/run_123456_abcd/run.json",
    "packetsJsonl": "runs/run_123456_abcd/packets.jsonl"
  },
  "size": {
    "runJson": 1234,
    "packetsJsonl": 5678,
    "total": 6912
  },
  "seeds": {
    "initialVector": {
      "matrixC": ["text1", "text2", "..."],
      "matrixD": ["text3", "text4", "..."],
      "matrixX": ["text5", "text6", "..."],
      "matrixE": ["text7", "text8", "..."]
    },
    "metadata": {
      "runId": "run_123456_abcd",
      "extractedAt": "2025-01-01T12:00:00.000Z",
      "totalCells": 48,
      "counts": { "C": 12, "D": 12, "X": 12, "E": 12 },
      "preHeuristicsCounts": { "C": 20, "D": 20, "X": 15, "E": 18 },
      "postHeuristicsCounts": { "C": 12, "D": 12, "X": 12, "E": 12 },
      "preHeuristicsTotal": 73,
      "postHeuristicsTotal": 48,
      "sourceFiles": ["snapshots/C.jsonl", "snapshots/D.jsonl", "snapshots/X.jsonl", "snapshots/E.jsonl"],
      "checksumVerified": true,
      "checksums": { "C": "ok", "D": "ok", "X": "ok", "E": "ok" },
      "warnings": []
    }
  }
}
```

### Error Handling

Soft failures return `200 OK` with `seeds: null` (warnings are logged server-side; when seeds are present, warnings appear in `metadata.warnings`):

```json
{
  "runId": "run_123456_abcd",
  "files": { "...": "..." },
  "size": { "...": 0 },
  "seeds": null
}
```

Hard failures (e.g., invalid runId) return appropriate HTTP error codes.

## UI Integration

The `ProblemForm` component includes:

1. **Framework Run ID Input**: Text field for entering run ID
2. **Load Seeds Button**: Fetches seeds via API and displays status
3. **Seed Status Display**: Shows loaded seed counts and any warnings
4. **Automatic Injection**: Loaded seeds are passed to traversal as `initialVector`

### User Flow

1. User enters Framework Run ID (e.g., `run_1234567890_abcd12`)
2. User clicks "Load Seeds" button
3. System fetches seeds from `/api/export/run?runId=...&include=seeds`
4. If successful, displays seed counts (e.g., "✓ Seeds loaded: 48 total items")
5. If warnings exist, displays them in yellow warning box
6. When user submits form, seeds are included in traversal request

## Cache Management

### Cache Structure

Seeds are cached at `runs/<runId>/seeds.json`:

```json
{
  "seeds": {
    "initialVector": { "...": ["..."] },
    "metadata": {
      "...": "...",
      "sourceMtime": { "snapshots/C.jsonl": 1234567890 },
      "sourceSize": { "snapshots/C.jsonl": 12345 }
    }
  }
}
```

### Cache Validation

Cache is considered valid if:
- File exists and is readable
- Source file mtimes match cached values
- Source file sizes match cached values

If any validation fails, fresh extraction occurs.

## Heuristics

When `SEEDS_ENABLE_HEURISTICS=true`, the following transformations are applied:

1. **Trimming**: Remove leading/trailing whitespace
2. **Filtering**: Remove empty strings and normalize whitespace
3. **Length Limiting**: Truncate to `SEEDS_MAX_LEN` characters
4. **Deduplication**: Case-insensitive (keep first)
5. **Count Constraints**: Clamp to `SEEDS_MAX_ITEMS`; if < `SEEDS_MIN_ITEMS`, do not pad — include a warning

## Performance Considerations

### Memory Usage

- Streaming JSONL parsing keeps memory usage below 150MB for 50k line files
- Matrix cells are processed incrementally, not loaded all at once
- Cache reduces redundant processing for repeated requests

### Optimization Tips

1. Enable caching (`SEEDS_PERSIST=true`) for production
2. Use checksum verification (`SEEDS_VERIFY_CHECKSUMS=true`) in production
3. Adjust `SEEDS_MAX_ITEMS` based on LLM context window limits
4. Monitor warnings for missing matrices or checksum mismatches

## Troubleshooting

### Common Issues

**Seeds not loading:**
- Verify framework run exists at `runs/<runId>/`
- Check that `index.json` manifest is present
- Ensure matrix snapshot files (.jsonl) are accessible

**Cache not updating:**
- Delete `runs/<runId>/seeds.json` to force refresh
- Check file permissions for write access
- Verify `SEEDS_PERSIST=true` is set

**Memory issues with large files:**
- Streaming should handle files up to 50k lines
- Check Node.js heap size if issues persist
- Consider splitting very large matrices

**Checksum mismatches:**
- Set `SEEDS_VERIFY_CHECKSUMS=false` for development
- Regenerate framework run if checksums are outdated
- Check for file corruption if persistent

## Testing

### Unit Tests
```bash
npm test -- seeds.test.ts
```

Tests cover:
- Text extraction from matrix cells
- Heuristic application
- Cache validation logic
- Error handling for missing files

### Integration Tests
```bash
npm test -- integration/seeds.test.ts
```

Tests cover:
- End-to-end API flow
- Cache persistence and retrieval
- Large file handling (performance test)
- Framework run with missing matrices

### Manual Testing

1. Create a test framework run:
```bash
cp -r fixtures/runs/sample_happy_001 runs/test_run_001
```

2. Test seed extraction:
```bash
curl "http://localhost:3001/api/export/run?runId=test_run_001&include=seeds" | jq
```

3. Verify cache creation:
```bash
ls runs/test_run_001/seeds.json
```

4. Test cache invalidation:
```bash
touch runs/test_run_001/snapshots/C.jsonl
curl "http://localhost:3001/api/export/run?runId=test_run_001&include=seeds" | jq
```

## Future Enhancements

1. **Smart Selection**: Use embeddings to select most relevant seeds
2. **Cross-Matrix Relationships**: Preserve cell relationships during extraction
3. **Incremental Updates**: Support partial matrix updates without full re-extraction
4. **Compression**: Store cached seeds in compressed format for space efficiency
5. **Metrics**: Track extraction performance and cache hit rates
