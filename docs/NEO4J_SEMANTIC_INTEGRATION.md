# Neo4j Semantic Integration (Archived for v2)

Note: This document is archived for v2.0.0. The current app does not depend on Neo4j. Graph integration may return in a future release behind a feature flag.

Technical specification for the graph-based metadata mirror system that enhances document discoverability while maintaining files as the source of truth.

## Architecture Philosophy

### Files as Source of Truth
The Neo4j graph serves as a **metadata mirror only**:
- **Complete document bodies** remain in file system (`store/state.json`)
- **Selected high-value components** mirrored to graph for discovery
- **Document relationships** tracked for enhanced navigation
- **CF14 semantic matrices** integrated for external framework alignment

### Non-Blocking Integration
Graph operations never block core functionality:
- **Async mirroring** via `queueMicrotask()` after successful file writes
- **Feature flagged** via `FEATURE_GRAPH_ENABLED` environment variable
- **Graceful degradation** when graph is unavailable
- **Zero impact** on document generation performance

## Component Selection Algorithm

### Scoring Logic
Rule-based algorithm identifies high-value document sections:

```typescript
function scoreComponent(section: DocumentSection, context: ScoringContext): number {
  let score = 0;
  
  // Cross-references boost value significantly
  const crossRefCount = countCrossReferences(section.content);
  score += crossRefCount * 3; // +3 per cross-reference
  
  // High-value keywords in headings
  const hasHighValueKeywords = /^(key|critical|important|required|must)/i.test(section.heading);
  if (hasHighValueKeywords) score += 2;
  
  // Size penalty for very long sections with few references  
  if (section.content.length > 500 && crossRefCount === 0) {
    score -= 2;
  }
  
  return Math.max(0, score); // Never negative
}
```

### Selection Criteria
Components are mirrored if they meet threshold requirements:
- **Score ≥ 3**: Generally mirrored (has cross-references or high-value keywords)
- **Score < 3**: Not mirrored unless explicitly required
- **Always mirror**: Document titles, section headings, reference lists

## Graph Schema Design

### Node Types
```cypher
// Primary document metadata
(:Document {
  id: string,           // SHA1 hash of document slug
  kind: string,         // DS | SP | X | M
  slug: string,         // Document identifier
  title: string,        // Human-readable title
  updatedAt: datetime,  // Last modification timestamp
  selection_v: string   // Selection algorithm version
})

// High-value document components
(:Component {
  id: string,           // SHA1 hash of content + position
  type: string,         // section | list_item | reference
  title: string,        // Component heading or identifier
  anchor: string,       // URL fragment for navigation
  order: int,           // Position within parent document
  score: int            // Selection algorithm score
})

// CF14 semantic matrices (external framework)
(:CFMatrix {
  id: string,           // Matrix identifier from framework
  kind: string,         // A | B | C | D | F | J
  name: string,         // Matrix display name
  createdAt: datetime   // Creation timestamp
})

// CF14 semantic nodes
(:CFNode {
  id: string,           // Node identifier from framework
  term: string,         // Semantic term
  station: string,      // Station context from CF14
  score: int,           // CF14 computed score
  payload: string       // Additional CF14 metadata
})
```

### Relationship Types
```cypher
// Document structure
(doc:Document)-[:CONTAINS]->(comp:Component)

// Inter-document references
(doc1:Document)-[:REFERENCES]->(doc2:Document)

// Document lineage and derivation
(derived:Document)-[:DERIVED_FROM]->(source:Document)

// CF14 semantic structure
(matrix:CFMatrix)-[:CONTAINS]->(node:CFNode)
(node1:CFNode)-[:RELATES_TO]->(node2:CFNode)

// Cross-integration (planned)
(doc:Document)-[:ENHANCED_BY]->(matrix:CFMatrix)
(comp:Component)-[:RELATES_TO]->(node:CFNode)
```

## Mirror Synchronization Process

### Document Write Flow
```typescript
export async function mirrorAfterWrite(bundle: DocumentBundle) {
  if (process.env.FEATURE_GRAPH_ENABLED !== "true") return;
  
  // 1. Select components using scoring algorithm
  const selection = selectForMirror(bundle, config);
  
  // 2. Queue non-blocking mirror operation
  queueMicrotask(() => 
    mirrorGraph({ 
      selection_v: "1.0.0", 
      docs: selection.docs,
      components: selection.components,
      references: selection.references,
      derived: selection.derived
    }).catch(err => console.warn("Mirror deferred failed", err))
  );
}
```

### Idempotent Graph Operations
```cypher
-- Document upsert (safe for concurrent operations)
MERGE (d:Document {id: $docId})
ON CREATE SET 
  d.kind = $kind,
  d.slug = $slug, 
  d.title = $title,
  d.updatedAt = $timestamp,
  d.selection_v = $selectionVersion
ON MATCH SET
  d.title = $title,
  d.updatedAt = $timestamp,
  d.selection_v = $selectionVersion
RETURN d;

-- Component batch upsert with relationship management
UNWIND $components as comp
MERGE (c:Component {id: comp.id})
ON CREATE SET c = comp
ON MATCH SET c = comp
WITH c, comp
MATCH (d:Document {id: comp.docId})
MERGE (d)-[:CONTAINS]->(c);

-- Stale component cleanup (set difference approach)
MATCH (d:Document {id: $docId})-[:CONTAINS]->(c:Component)
WHERE NOT c.id IN $currentComponentIds
DETACH DELETE c;
```

## CF14 Framework Integration

### Matrix Ingestion Pipeline
CF14 matrices from external chirality-framework are ingested as semantic enhancement:

```typescript
interface CFMatrixIngestion {
  matrixId: string;     // Framework-generated matrix ID
  kind: 'A' | 'B' | 'C' | 'D' | 'F' | 'J';
  nodes: CFNodeData[];  // Semantic nodes with term/station/score
  relationships: CFRelationship[]; // Inter-node semantic relationships
  metadata: {
    createdAt: string;
    framework_version: string;
    problem_context: string;
  };
}
```

### Semantic Alignment Process
```cypher
-- Align document components with CF14 nodes
MATCH (d:Document)-[:CONTAINS]->(c:Component)
MATCH (n:CFNode)
WHERE toLower(c.title) CONTAINS toLower(n.term)
   OR edit_distance(c.title, n.term) <= 3
WITH c, n, edit_distance(c.title, n.term) as similarity
WHERE similarity <= 3
MERGE (c)-[:RELATES_TO {similarity: similarity, method: 'term_alignment'}]->(n);
```

## GraphQL API Layer

### Type Definitions
```graphql
type Document {
  id: ID!
  kind: String!       # DS | SP | X | M
  slug: String!
  title: String!
  updatedAt: String
  components: [Component!]! @relationship(type: "CONTAINS", direction: OUT)
  references: [Document!]! @relationship(type: "REFERENCES", direction: OUT) 
  derivedFrom: [Document!]! @relationship(type: "DERIVED_FROM", direction: OUT)
}

type Component {
  id: ID!
  type: String!       # section | list_item | reference
  title: String!
  anchor: String      # URL fragment
  order: Int
  score: Int
  parent: Document! @relationship(type: "CONTAINS", direction: IN)
}

type CFMatrix {
  id: ID!
  kind: String!       # A | B | C | D | F | J  
  name: String
  createdAt: String
  nodes(limit: Int = 50): [CFNode!]!
}

type CFNode {
  id: ID!
  term: String!
  station: String
  score: Int
  payload: String
  relatesTo(limit: Int = 50): [CFNode!]!
}
```

### Query Complexity Management
```typescript
// Depth limiting (max 6 levels)
import depthLimit from "graphql-depth-limit";

// Complexity cost limiting (max 1000 points)
import { createComplexityLimitRule } from "graphql-validation-complexity";

const validationRules = [
  depthLimit(6),
  createComplexityLimitRule(1000, {
    onCost: () => void 0,
    formatErrorMessage: (cost: number) => `Query too complex: ${cost}`
  })
];
```

### Security Model
```typescript
// Bearer token authentication
const auth = req.headers.get("authorization") || "";
const authorized = auth === `Bearer ${process.env.GRAPHQL_BEARER_TOKEN}`;

// CORS configuration
const corsOrigins = process.env.GRAPHQL_CORS_ORIGINS?.split(',') || ['*'];

// Read-only operations only (no mutations that modify core data)
```

## Performance Optimization

### Index Strategy
```cypher
-- Essential indexes for query performance
CREATE INDEX document_id IF NOT EXISTS FOR (d:Document) ON (d.id);
CREATE INDEX document_kind IF NOT EXISTS FOR (d:Document) ON (d.kind);
CREATE INDEX document_updated IF NOT EXISTS FOR (d:Document) ON (d.updatedAt);
CREATE INDEX component_score IF NOT EXISTS FOR (c:Component) ON (c.score);
CREATE INDEX component_type IF NOT EXISTS FOR (c:Component) ON (c.type);
CREATE INDEX cfnode_term IF NOT EXISTS FOR (n:CFNode) ON (n.term);
CREATE INDEX cfmatrix_kind IF NOT EXISTS FOR (m:CFMatrix) ON (m.kind);
```

### Query Optimization Patterns
```cypher
-- Use LIMIT consistently to prevent runaway queries
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE c.score >= $threshold
RETURN d, c
ORDER BY c.score DESC
LIMIT 100; -- Always include reasonable limits

-- Use index-friendly WHERE clauses
MATCH (d:Document {kind: $documentType}) -- Uses index
WHERE d.updatedAt >= $sinceDate         -- Additional filter
RETURN d;

-- Avoid expensive operations in WHERE
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WITH d, count(c) as componentCount       -- Aggregate first
WHERE componentCount >= $minComponents   -- Then filter
RETURN d, componentCount;
```

## Monitoring and Observability

### Health Check Queries
```cypher
-- Database connectivity and basic statistics
MATCH (d:Document)
OPTIONAL MATCH (d)-[:CONTAINS]->(c:Component)
OPTIONAL MATCH (m:CFMatrix)
RETURN {
  connected: true,
  documents: count(DISTINCT d),
  components: count(DISTINCT c), 
  matrices: count(DISTINCT m),
  lastDocument: max(d.updatedAt)
} as health;
```

### Performance Monitoring
```cypher
-- Query performance analysis
CALL apoc.meta.stats() YIELD 
  labelCount, 
  relTypeCount, 
  propertyKeyCount,
  nodeCount,
  relCount
RETURN {
  labels: labelCount,
  relationshipTypes: relTypeCount,
  properties: propertyKeyCount,
  nodes: nodeCount,
  relationships: relCount
} as dbStats;
```

### Error Detection
```cypher
-- Detect data integrity issues
MATCH (c:Component)
WHERE NOT EXISTS((d:Document)-[:CONTAINS]->(c))
RETURN count(c) as orphanedComponents;

-- Check for selection algorithm inconsistencies  
MATCH (d:Document)
WHERE d.selection_v IS NULL OR d.selection_v <> $currentVersion
RETURN count(d) as staleDocs;
```

## Configuration Management

### Environment Variables
```bash
# Core graph settings
FEATURE_GRAPH_ENABLED=true
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j  
NEO4J_PASSWORD=your-secure-password

# API security
GRAPHQL_BEARER_TOKEN=your-secure-random-token
GRAPHQL_CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# Performance tuning
GRAPH_QUERY_TIMEOUT_MS=5000
GRAPH_CONNECTION_POOL_SIZE=10
SELECTION_SCORE_THRESHOLD=3

# CF14 integration
CF14_MATRIX_SYNC_ENABLED=true
CF14_ALIGNMENT_THRESHOLD=0.8
```

### Neo4j Configuration
```bash
# neo4j.conf optimizations
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=1G
dbms.tx_log.rotation.retention_policy=2 days
dbms.security.auth_enabled=true
```

## Development Workflow

### Local Development Setup
```bash
# 1. Start Neo4j via Docker Compose
docker compose up neo4j -d

# 2. Wait for startup (health check)
until curl -f http://localhost:7474/browser/; do sleep 2; done

# 3. Apply schema constraints
npm run init:graph:constraints

# 4. Enable graph features
echo "FEATURE_GRAPH_ENABLED=true" >> .env.local

# 5. Start development server
npm run dev
```

### Testing Integration
```typescript
// Graph integration test pattern
describe('Neo4j Integration', () => {
  beforeEach(async () => {
    // Clear test data
    await clearGraphData();
    
    // Set up test fixtures
    await createTestDocuments();
  });
  
  it('mirrors documents after file write', async () => {
    // Generate documents
    const result = await orchestrate(testProblem);
    
    // Verify file write
    expect(await readState()).toContain(result.finals);
    
    // Wait for async mirror
    await waitForMirrorCompletion();
    
    // Verify graph mirror
    const graphDocs = await queryGraphDocuments();
    expect(graphDocs).toHaveLength(4); // DS, SP, X, M
  });
});
```

## Migration and Versioning

### Schema Evolution Strategy
```cypher
-- Version-aware schema updates
MATCH (d:Document)
WHERE d.selection_v < $newVersion
SET d.needsUpdate = true;

-- Gradual migration approach
CALL apoc.periodic.iterate(
  "MATCH (d:Document) WHERE d.needsUpdate = true RETURN d",
  "CALL apoc.custom.updateSelection(d) YIELD result RETURN result",
  {batchSize: 100, parallel: false}
);
```

### Backup Strategy
```bash
#!/bin/bash
# Daily backup with rotation
DATE=$(date +%Y%m%d)
docker exec neo4j-graph neo4j-admin database dump \
  --to-path=/backups/chirality-graph-${DATE}.dump neo4j

# Keep last 7 days
find /backups -name "chirality-graph-*.dump" -mtime +7 -delete
```

## Error Handling and Recovery

### Connection Resilience
```typescript
import { Neo4jError } from 'neo4j-driver';
import { retry, stop_after_attempt, wait_exponential } from 'async-retry';

export async function withRetry<T>(operation: () => Promise<T>): Promise<T> {
  return retry(operation, {
    retries: 3,
    factor: 2,
    minTimeout: 1000,
    maxTimeout: 5000,
    onRetry: (error, attempt) => {
      console.warn(`Graph operation retry ${attempt}:`, error.message);
    }
  });
}
```

### Graceful Degradation
```typescript
export async function mirrorGraph(selection: ComponentSelection): Promise<void> {
  try {
    await withRetry(() => syncToGraph(selection));
  } catch (error) {
    // Log but don't throw - mirror failures shouldn't break core functionality
    console.warn('Graph mirror failed, continuing with file-only operation:', error);
    
    // Optionally emit metrics for monitoring
    if (process.env.NODE_ENV === 'production') {
      emitMetric('graph.mirror.failure', 1, { error: error.message });
    }
  }
}
```

### Data Validation
```cypher
-- Integrity checks for automated monitoring
MATCH (d:Document)
WHERE d.id IS NULL OR d.kind IS NULL OR d.title IS NULL
RETURN d as invalidDocument;

MATCH (c:Component)
WHERE NOT EXISTS((d:Document)-[:CONTAINS]->(c))
RETURN c.id as orphanedComponent;

MATCH (d:Document)-[:REFERENCES]->(target:Document)
WHERE target IS NULL
RETURN d.id as brokenReference;
```

## Security Considerations

### Access Control
- **Read-only GraphQL API**: No mutations allowed that modify document content
- **Bearer token authentication**: Required for all graph API access
- **CORS restrictions**: Configurable allowed origins
- **Query complexity limits**: Prevent resource exhaustion attacks

### Data Privacy
- **Metadata only**: No sensitive document content in graph
- **Audit logging**: All graph operations logged for SOC2 compliance
- **Secure connections**: TLS required for production Neo4j connections
- **Token rotation**: Regular bearer token updates

### Query Safety
```typescript
// Input validation for GraphQL queries
const FORBIDDEN_PATTERNS = [
  /MERGE|CREATE|SET|DELETE|REMOVE/i,  // Write operations
  /apoc\.load/i,                       // External data loading
  /dbms\./i,                           // Database admin functions
  /\/\*/,                              // Comment injection
];

export function validateQuery(query: string): boolean {
  return !FORBIDDEN_PATTERNS.some(pattern => pattern.test(query));
}
```

## Troubleshooting

### Common Issues

#### Graph Not Connecting
```bash
# Check Neo4j status
docker compose ps neo4j

# Verify connection parameters
echo "NEO4J_URI: $NEO4J_URI"
echo "NEO4J_USER: $NEO4J_USER"

# Test basic connectivity
curl -u neo4j:$NEO4J_PASSWORD \
  -X POST http://localhost:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"RETURN 1 as test"}]}'
```

#### Mirror Synchronization Failures
```bash
# Check graph API health
curl http://localhost:3001/api/v1/graph/health

# Verify component selection is working
node -e "
const { selectForMirror } = require('./lib/graph/select');
const testBundle = { /* test data */ };
console.log(JSON.stringify(selectForMirror(testBundle, {}), null, 2));
"
```

#### Performance Issues
```cypher
-- Identify expensive queries
CALL apoc.monitor.kernel() YIELD kernelAvailableMemory, kernelFreeMemory, kernelTotalMemory
RETURN kernelAvailableMemory, kernelFreeMemory, kernelTotalMemory;

-- Check for missing indexes
CALL db.indexes() YIELD labelsOrTypes, properties, state
WHERE state <> 'ONLINE'
RETURN labelsOrTypes, properties, state;
```

### Debugging Tools
```bash
# Enable debug logging
DEBUG=graph:* npm run dev

# Monitor graph operations
tail -f logs/graph-mirror.log

# Test component selection algorithm
npm run test:graph:selection
```

## Future Enhancements

### Planned Features
- **Vector similarity search**: Semantic search within graph
- **Advanced CF14 alignment**: Machine learning for term matching
- **Real-time subscriptions**: WebSocket updates for graph changes
- **Batch optimization**: Bulk mirror operations for performance

### Research Directions
- **Graph neural networks**: Enhanced component scoring
- **Semantic clustering**: Automatic document grouping
- **Knowledge graph reasoning**: Inference over document relationships
- **Federated graphs**: Multi-instance knowledge sharing

---

*Technical specification for Neo4j-based metadata mirroring system enabling enhanced document discovery while preserving file-based source of truth.*
