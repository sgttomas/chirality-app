# Neo4j Queries Reference (Archived for v2)

Note: Archived for v2.0.0. The current app does not ship graph features. This reference is retained for future work behind an optional feature flag.

## Schema Overview

### Core Node Types
```cypher
// Document metadata (source of truth: files)
(:Document {id, kind, slug, title, updatedAt, selection_v})

// Selected high-value components 
(:Component {id, type, title, anchor, order, score})

// CF14 semantic matrices (external framework integration)
(:CFMatrix {id, kind, name, createdAt})
(:CFNode {id, term, station, score, payload})
```

### Relationship Types
```cypher
// Document structure
(doc:Document)-[:CONTAINS]->(comp:Component)

// Inter-document references
(doc1:Document)-[:REFERENCES]->(doc2:Document)  

// Document lineage
(derived:Document)-[:DERIVED_FROM]->(source:Document)

// CF14 semantic relationships
(matrix:CFMatrix)-[:CONTAINS]->(node:CFNode)
(node1:CFNode)-[:RELATES_TO]->(node2:CFNode)
```

## Document Operations

### Basic Document Queries

#### Find Document by ID
```cypher
MATCH (d:Document {id: $documentId})
RETURN d;
```

#### List All Documents by Type
```cypher
MATCH (d:Document {kind: $documentType})
RETURN d.id, d.title, d.updatedAt
ORDER BY d.updatedAt DESC;
```

#### Get Document with Components
```cypher
MATCH (d:Document {id: $documentId})
OPTIONAL MATCH (d)-[:CONTAINS]->(c:Component)
RETURN d, collect(c) as components;
```

### Document Relationship Queries

#### Find Referenced Documents
```cypher
MATCH (source:Document {id: $documentId})-[:REFERENCES]->(target:Document)
RETURN target.id, target.title, target.kind
ORDER BY target.kind, target.title;
```

#### Get Document Lineage (Dependencies)
```cypher
MATCH (derived:Document {id: $documentId})-[:DERIVED_FROM*1..3]->(source:Document)
RETURN source.id, source.title, source.kind
ORDER BY source.updatedAt;
```

#### Find Documents Referencing Current
```cypher
MATCH (referencing:Document)-[:REFERENCES]->(target:Document {id: $documentId})
RETURN referencing.id, referencing.title, referencing.kind;
```

## Component Operations

### Component Selection Queries

#### High-Value Components (Score-Based)
```cypher
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE c.score >= $minScore
RETURN d.id as docId, d.title as docTitle, 
       collect({id: c.id, title: c.title, score: c.score}) as components
ORDER BY d.kind, d.title;
```

#### Components with Cross-References
```cypher
MATCH (d1:Document)-[:CONTAINS]->(c:Component)
WHERE EXISTS {
  MATCH (d1)-[:REFERENCES]->(d2:Document)
  WHERE c.title CONTAINS 'ref:' OR c.title CONTAINS 'cite:'
}
RETURN d1.id, c.id, c.title, c.score
ORDER BY c.score DESC;
```

#### Search Components by Content
```cypher
MATCH (c:Component)
WHERE toLower(c.title) CONTAINS toLower($searchTerm)
WITH c, c.parent as doc
RETURN c.id, c.title, c.type, doc.id as docId, doc.title as docTitle
ORDER BY c.score DESC
LIMIT $limit;
```

### Component Analysis Queries

#### Component Distribution by Document Type
```cypher
MATCH (d:Document)-[:CONTAINS]->(c:Component)
RETURN d.kind, count(c) as componentCount, avg(c.score) as avgScore
ORDER BY componentCount DESC;
```

#### Top Scoring Components Across All Documents
```cypher
MATCH (d:Document)-[:CONTAINS]->(c:Component)
RETURN d.kind, d.title, c.title, c.score
ORDER BY c.score DESC
LIMIT $topN;
```

## CF14 Matrix Integration

### Matrix Discovery Queries

#### List Available Matrices
```cypher
MATCH (m:CFMatrix)
RETURN m.id, m.kind, m.name, m.createdAt
ORDER BY m.kind, m.createdAt DESC;
```

#### Matrix with Node Count
```cypher
MATCH (m:CFMatrix)
OPTIONAL MATCH (m)-[:CONTAINS]->(n:CFNode)
RETURN m.id, m.kind, m.name, count(n) as nodeCount
ORDER BY nodeCount DESC;
```

#### Find Matrix by Kind
```cypher
MATCH (m:CFMatrix {kind: $matrixKind})
OPTIONAL MATCH (m)-[:CONTAINS]->(n:CFNode)
RETURN m, collect(n)[0..10] as sampleNodes; // First 10 nodes
```

### Semantic Node Queries

#### Search Nodes by Term
```cypher
MATCH (n:CFNode)
WHERE toLower(n.term) CONTAINS toLower($searchTerm)
OPTIONAL MATCH (n)-[:RELATES_TO]->(related:CFNode)
RETURN n.id, n.term, n.station, n.score,
       collect(related.term)[0..5] as relatedTerms
ORDER BY n.score DESC
LIMIT $limit;
```

#### Node Relationships
```cypher
MATCH (source:CFNode {id: $nodeId})
OPTIONAL MATCH (source)-[:RELATES_TO]->(target:CFNode)
RETURN source, collect({
  id: target.id,
  term: target.term, 
  station: target.station,
  score: target.score
}) as relatedNodes;
```

#### High-Value Semantic Connections
```cypher
MATCH (n1:CFNode)-[r:RELATES_TO]->(n2:CFNode)
WHERE n1.score >= $minScore AND n2.score >= $minScore
RETURN n1.term, n2.term, n1.station, n2.station
ORDER BY n1.score + n2.score DESC
LIMIT $limit;
```

## Mirror Synchronization Operations

### Document Upsert (Idempotent)
```cypher
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
```

### Component Batch Upsert
```cypher
UNWIND $components as comp
MERGE (c:Component {id: comp.id})
ON CREATE SET 
  c.type = comp.type,
  c.title = comp.title,
  c.anchor = comp.anchor,
  c.order = comp.order,
  c.score = comp.score
ON MATCH SET
  c.title = comp.title,
  c.order = comp.order,
  c.score = comp.score
WITH c, comp
MATCH (d:Document {id: comp.docId})
MERGE (d)-[:CONTAINS]->(c);
```

### Stale Component Cleanup
```cypher
// Remove components no longer in current selection
MATCH (d:Document {id: $docId})-[:CONTAINS]->(c:Component)
WHERE NOT c.id IN $currentComponentIds
DETACH DELETE c;
```

### Reference Relationship Management
```cypher
// Create document references
MATCH (source:Document {id: $sourceId})
MATCH (target:Document {id: $targetId})
MERGE (source)-[:REFERENCES]->(target);

// Create derivation relationships  
MATCH (derived:Document {id: $derivedId})
MATCH (source:Document {id: $sourceId})
MERGE (derived)-[:DERIVED_FROM]->(source);
```

## Analysis and Reporting Queries

### System Health Queries

#### Database Statistics
```cypher
MATCH (d:Document)
OPTIONAL MATCH (d)-[:CONTAINS]->(c:Component)
OPTIONAL MATCH (m:CFMatrix)
OPTIONAL MATCH (n:CFNode)
RETURN 
  count(DISTINCT d) as documentCount,
  count(DISTINCT c) as componentCount,
  count(DISTINCT m) as matrixCount,
  count(DISTINCT n) as nodeCount;
```

#### Selection Version Audit
```cypher
MATCH (d:Document)
RETURN d.selection_v as version, count(d) as documentCount
ORDER BY version;
```

#### Orphaned Components (Quality Check)
```cypher
MATCH (c:Component)
WHERE NOT EXISTS((d:Document)-[:CONTAINS]->(c))
RETURN c.id, c.title, c.type;
```

### Document Quality Metrics

#### Cross-Reference Density
```cypher
MATCH (d:Document)
OPTIONAL MATCH (d)-[:REFERENCES]->(ref:Document)
RETURN d.id, d.title, d.kind, count(ref) as referenceCount
ORDER BY referenceCount DESC;
```

#### Component Score Distribution
```cypher
MATCH (d:Document {kind: $documentKind})-[:CONTAINS]->(c:Component)
WITH d, c.score as score
RETURN d.id, d.title,
       min(score) as minScore,
       max(score) as maxScore, 
       avg(score) as avgScore,
       count(*) as componentCount;
```

#### Most Connected Documents
```cypher
MATCH (d:Document)
OPTIONAL MATCH (d)-[:REFERENCES]->(out:Document)
OPTIONAL MATCH (in:Document)-[:REFERENCES]->(d)
RETURN d.id, d.title, d.kind,
       count(DISTINCT out) as outgoingRefs,
       count(DISTINCT in) as incomingRefs,
       count(DISTINCT out) + count(DISTINCT in) as totalConnections
ORDER BY totalConnections DESC
LIMIT $topN;
```

## Advanced Analysis Queries

### Document Similarity (Shared References)
```cypher
MATCH (d1:Document)-[:REFERENCES]->(shared:Document)<-[:REFERENCES]-(d2:Document)
WHERE d1.id < d2.id  // Avoid duplicates
WITH d1, d2, count(shared) as sharedRefs
WHERE sharedRefs >= $minSharedRefs
RETURN d1.id, d1.title, d2.id, d2.title, sharedRefs
ORDER BY sharedRefs DESC;
```

### Component Influence Analysis  
```cypher
MATCH (d:Document)-[:CONTAINS]->(c:Component)
OPTIONAL MATCH (d)-[:REFERENCES]->(referencedDoc:Document)
RETURN c.id, c.title, c.score,
       d.id as parentDoc,
       count(referencedDoc) as documentInfluence,
       c.score * count(referencedDoc) as weightedInfluence
ORDER BY weightedInfluence DESC
LIMIT $topInfluential;
```

### CF14 Matrix Integration Analysis
```cypher
// Find documents that could benefit from CF14 context
MATCH (d:Document {kind: $documentKind})
MATCH (n:CFNode)
WHERE toLower(d.title) CONTAINS toLower(n.term)
   OR toLower(n.term) CONTAINS toLower($problemKeyword)
RETURN d.id, d.title,
       collect({term: n.term, station: n.station, score: n.score})[0..5] as potentialMatches
ORDER BY size(potentialMatches) DESC;
```

## Performance Optimization Queries

### Index Creation
```cypher
// Essential indexes for performance
CREATE INDEX document_id IF NOT EXISTS FOR (d:Document) ON (d.id);
CREATE INDEX document_kind IF NOT EXISTS FOR (d:Document) ON (d.kind);
CREATE INDEX component_id IF NOT EXISTS FOR (c:Component) ON (c.id);
CREATE INDEX component_score IF NOT EXISTS FOR (c:Component) ON (c.score);
CREATE INDEX cfnode_term IF NOT EXISTS FOR (n:CFNode) ON (n.term);
CREATE INDEX cfmatrix_kind IF NOT EXISTS FOR (m:CFMatrix) ON (m.kind);
```

### Query Performance Analysis
```cypher
// Identify slow relationship patterns
CALL apoc.meta.stats() YIELD labelCount, relTypeCount, propertyKeyCount
RETURN labelCount, relTypeCount, propertyKeyCount;

// Check relationship cardinalities
MATCH ()-[r]->()
RETURN type(r), count(r) as relationshipCount
ORDER BY relationshipCount DESC;
```

## Maintenance Operations

### Data Cleanup

#### Remove Orphaned Components
```cypher
MATCH (c:Component)
WHERE NOT EXISTS((d:Document)-[:CONTAINS]->(c))
DETACH DELETE c;
```

#### Clean Broken References
```cypher
MATCH (d1:Document)-[r:REFERENCES]->(d2:Document)
WHERE d2 IS NULL
DELETE r;
```

#### Archive Old Selection Versions
```cypher
MATCH (d:Document)
WHERE d.selection_v < $currentVersion 
  AND d.updatedAt < datetime() - duration('P30D')
DETACH DELETE d;
```

### Bulk Operations

#### Batch Component Score Update
```cypher
CALL apoc.periodic.iterate(
  "MATCH (c:Component) WHERE c.score IS NULL RETURN c",
  "SET c.score = 0",
  {batchSize: 1000}
);
```

#### Recompute All Document References
```cypher
MATCH (d:Document)
DETACH DELETE (d)-[:REFERENCES]->()
WITH d
// Recompute references based on component content
MATCH (d)-[:CONTAINS]->(c:Component)
WHERE c.title CONTAINS 'ref:'
WITH d, extract(ref IN split(c.title, 'ref:') | trim(ref)) as refs
UNWIND refs as refId
MATCH (target:Document {id: refId})
MERGE (d)-[:REFERENCES]->(target);
```

## Development and Debugging

### Schema Inspection
```cypher
// View all node labels and counts
CALL apoc.meta.stats() YIELD labels
RETURN labels;

// View all relationship types
CALL db.relationshipTypes() YIELD relationshipType
RETURN relationshipType;

// Sample data inspection
MATCH (d:Document)
RETURN d.kind, count(d) as count, 
       collect(d.title)[0..3] as sampleTitles
ORDER BY count DESC;
```

### Query Performance Testing
```cypher
// Test complex query performance
PROFILE
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE c.score > $threshold
OPTIONAL MATCH (d)-[:REFERENCES]->(ref:Document)
RETURN d.id, d.title, count(c) as components, count(ref) as references
ORDER BY components DESC, references DESC
LIMIT 10;
```

### Data Validation
```cypher
// Validate component scores are within expected range
MATCH (c:Component)
WHERE c.score < -10 OR c.score > 100
RETURN c.id, c.title, c.score, 'Invalid score range' as issue;

// Check for missing required properties
MATCH (d:Document)
WHERE d.id IS NULL OR d.kind IS NULL OR d.title IS NULL
RETURN d, 'Missing required properties' as issue;

// Verify relationship consistency
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE NOT EXISTS((d:Document {id: d.id}))
RETURN c.id, 'Orphaned component' as issue;
```

## Advanced Analysis

### Document Network Analysis
```cypher
// Find most central documents (highest degree)
MATCH (d:Document)
OPTIONAL MATCH (d)-[:REFERENCES]->(out:Document)
OPTIONAL MATCH (in:Document)-[:REFERENCES]->(d)
WITH d, count(DISTINCT out) + count(DISTINCT in) as degree
RETURN d.id, d.title, d.kind, degree
ORDER BY degree DESC
LIMIT 10;
```

### Component Clustering
```cypher
// Group components by shared reference patterns
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE c.title CONTAINS 'ref:'
WITH d.kind, extract(ref IN split(c.title, 'ref:') | trim(ref)) as refs
UNWIND refs as ref
WITH d.kind, ref, count(*) as frequency
WHERE frequency >= $minFrequency
RETURN d.kind, ref, frequency
ORDER BY d.kind, frequency DESC;
```

### Quality Metrics
```cypher
// Document quality indicators
MATCH (d:Document)
OPTIONAL MATCH (d)-[:CONTAINS]->(c:Component)
OPTIONAL MATCH (d)-[:REFERENCES]->(ref:Document)
WITH d, count(c) as components, count(ref) as references,
     avg(c.score) as avgComponentScore
RETURN d.id, d.title, d.kind,
       components,
       references, 
       round(avgComponentScore, 2) as avgScore,
       round(references * avgComponentScore / components, 2) as qualityMetric
ORDER BY qualityMetric DESC;
```

## CF14 Integration Queries

### Matrix-Document Alignment
```cypher
// Find CF14 nodes that align with document content
MATCH (d:Document {id: $documentId})-[:CONTAINS]->(c:Component)
MATCH (n:CFNode)
WHERE toLower(c.title) CONTAINS toLower(n.term)
   OR toLower(n.term) CONTAINS toLower($searchKeyword)
RETURN c.id, c.title, 
       collect({
         nodeId: n.id, 
         term: n.term, 
         station: n.station, 
         score: n.score
       }) as alignedNodes
ORDER BY size(alignedNodes) DESC;
```

### Semantic Enhancement Opportunities
```cypher
// Documents that could benefit from CF14 enhancement
MATCH (d:Document)-[:CONTAINS]->(c:Component)
WHERE c.score < $lowScoreThreshold
MATCH (n:CFNode)
WHERE n.score > $highCF14Threshold
  AND (toLower(n.term) CONTAINS toLower($problemDomain)
       OR n.station CONTAINS $relevantStation)
RETURN d.id, d.title, c.id, c.title, c.score,
       collect({
         enhancement: n.term,
         station: n.station,
         score: n.score
       })[0..3] as enhancementOpportunities;
```

## Security and Access Control

### Read-Only Query Validation
```cypher
// Ensure queries are read-only (no writes)
// This check is performed at the GraphQL layer
// No MERGE, CREATE, SET, DELETE, or REMOVE operations allowed
```

### Query Complexity Limits
```cypher
// Automatic complexity analysis (handled by graphql-validation-complexity)
// Max depth: 6 levels
// Max complexity cost: 1000 points
// Timeout: 5 seconds per query
```

### Rate Limiting Queries
```cypher
// Track query frequency by user/session
// (Implemented at application layer, not database)
MATCH (log:QueryLog {session: $sessionId})
WHERE log.timestamp > datetime() - duration('PT1M')
RETURN count(log) as recentQueries;
```

## Backup and Maintenance

### Data Export
```cypher
// Export all documents and relationships
CALL apoc.export.cypher.all("backup.cypher", {
  format: "neo4j-shell",
  useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
});
```

### Index Maintenance
```cypher
// Rebuild indexes for performance
CALL apoc.schema.assert({}, {
  Document: ['id', 'kind'],
  Component: ['id', 'score'], 
  CFNode: ['term'],
  CFMatrix: ['kind']
});
```

---

*Neo4j Cypher query reference for Chirality AI App graph integration layer with document metadata mirroring and CF14 semantic enhancement.*
