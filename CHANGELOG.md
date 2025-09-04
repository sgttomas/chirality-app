# Changelog

All notable changes to Chirality AI App are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documentation consolidation from 25+ files to essential minimal set
- Comprehensive troubleshooting guide with systematic debugging procedures
- Enhanced contributing guidelines with testing requirements and code standards
- Matrix integration test coverage with dynamic fixture generation

### Changed
- Updated README.md to focus on three-pass orchestration and matrix integration
- Improved CONTRIBUTING.md with comprehensive development workflow
- Enhanced ROADMAP.md with strategic priorities and success metrics
- Standardized TROUBLESHOOTING.md with complete diagnostic procedures

## [1.0.0] - 2025-09-01

### Added
- **Three-Pass Matrix-Driven Orchestration System**
  - V1→V2→V3 iterative refinement with convergence tracking
  - Matrix integration using external chirality-framework as "seeds of thought"
  - Deterministic scaffolding with stable ordering (meta.order then id)
  - RAG pipeline serving generated documents as "seeds of evidence"

- **Enterprise-Grade Production Features**
  - RBAC with approver role requirements for document exports
  - SOC2 compliance with structured audit logging 
  - Streaming export using PassThrough to avoid memory issues
  - Comprehensive test coverage (52 tests passing)

- **Framework Integration Layer**
  - External framework ingestion with JSONL parsing and version validation
  - Matrix-to-document generation mappings (C→DS, D→SP, X+E→X, E→M)
  - Triple structure compliance with text, terms_used, warnings
  - Agent orchestration with precise phase timing and V1/V2/V3 hashing

- **Advanced API Endpoints**
  - `POST /api/agent/run` - External framework run processing with matrix integration
  - `GET /api/agent/export/[runId]` - Streaming export with RBAC validation
  - `POST /api/agent/sign/[runId]` - Approver role requirement for finalization
  - Enhanced error handling with production-ready safeguards

### Fixed
- TypeScript strict mode compliance removing all `as any` shortcuts
- Jest configuration error (`moduleNameMappers` → `moduleNameMapper`)
- Generator collection bug only gathering `refs` but not `citations`
- Ingestion tests with dynamic fixture generation replacing static files
- MatrixCell interface compliance with `row` and `col` fields per specification

### Performance
- Atomic file operations with lockfile resilience for concurrent access
- Streaming export implementation preventing memory exhaustion
- Optimized matrix ingestion with comprehensive validation
- Enhanced error recovery with graceful degradation patterns

## [0.9.0] - 2025-08-17

### Added
- **Two-Pass Semantic Document Generation System**
  - Sequential generation of DS/SP/X/M documents with dependency management
  - Cross-referential refinement using insights from all documents
  - Final resolution creating comprehensive X document
  - Real-time progress tracking through generation process

- **RAG-Enhanced Streaming Chat Interface** 
  - Server-sent events for real-time chat responses
  - Automatic document context injection for grounded responses
  - Command recognition (`set problem:`, `generate DS/SP/X/M`)
  - Citation support referencing generated document content

- **Complete Next.js Architecture**
  - App Router with React 18 and TypeScript strict mode
  - API routes for document generation and chat functionality  
  - File-based state persistence with atomic operations
  - Component library with error boundaries and responsive design

### Changed
- Migrated from planned GraphQL/Neo4j to simplified file-based approach
- Focused on single-user experience with clear multi-user upgrade path
- Prioritized development velocity over complex infrastructure

### Performance
- Document generation: 45-90 seconds for complete two-pass process
- Chat response: <2 seconds first token, 20-50 tokens/second streaming
- State operations: Sub-second response with atomic file locking

## [0.8.0] - 2025-08-01

### Added
- Document validation system with flexible string/array handling
- Enhanced context injection for better RAG performance
- State consistency validation and recovery mechanisms
- Comprehensive error handling with graceful degradation

### Fixed
- Document validation edge cases with mixed formats
- Context injection failures with malformed structures
- State synchronization during rapid generation
- Memory leaks in streaming responses

### Performance  
- 25% reduction in generation latency through prompt optimization
- Improved streaming token buffering
- Optimized file I/O operations

## [0.7.0] - 2025-07-15

### Added
- Next.js App Router migration with React Server Components
- Reusable component library with consistent patterns
- RESTful API architecture with comprehensive error handling
- Mobile and tablet responsive design optimization

### Changed
- Complete migration from Pages Router to App Router
- Enhanced TypeScript integration with stricter checking
- Improved component imports for better tree shaking

### Removed
- Legacy Pages Router components and configuration
- Deprecated API patterns and unused dependencies

## [0.6.0] - 2025-07-01

### Added
- File-based state management system
- Direct OpenAI API integration (gpt-4.1-nano)
- Streamlined architecture focused on core functionality
- Cost-optimized prompt engineering

### Changed
- Architecture simplification from planned GraphQL/database to REST/file approach
- Eliminated external database requirements for easier deployment

## [0.5.0] - 2025-06-15

### Added
- Initial DS/SP/X/M document type system
- Basic sequential generation workflow
- React chat interface with OpenAI integration
- Document context injection experiments

---

*For detailed release information, see individual release notes. This changelog maintains complete project evolution history following Keep a Changelog conventions.*