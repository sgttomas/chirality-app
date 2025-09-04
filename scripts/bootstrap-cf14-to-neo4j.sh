#!/usr/bin/env bash
set -euo pipefail

echo "▶ Starting Neo4j (if not already)..."
pushd /Users/ryan/Desktop/ai-env/chirality-app >/dev/null
docker compose -f docker-compose.neo4j.yml up -d
until curl -s http://localhost:7474 >/dev/null; do sleep 1; done
npm install >/dev/null 2>&1 || true
npx tsx scripts/init-graph-constraints.ts || true
popd >/dev/null

echo "▶ Ensuring CF14 constraints..."
cat > /tmp/cf14-indexes.cypher <<'CYPHER'
CREATE CONSTRAINT cf_matrix_id IF NOT EXISTS FOR (m:CFMatrix) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT cf_node_id   IF NOT EXISTS FOR (n:CFNode)   REQUIRE n.id IS UNIQUE;
CREATE INDEX     cf_term_idx   IF NOT EXISTS FOR (n:CFNode)   ON (n.term);
CYPHER
echo "Open http://localhost:7474 and run /tmp/cf14-indexes.cypher if needed."

echo "▶ Running CF14 pipeline with Neo4j export..."
pushd /Users/ryan/Desktop/ai-env/chirality-framework >/dev/null
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m chirality.cli run \
  --thread "demo:test" \
  --A chirality/tests/fixtures/A.json \
  --B chirality/tests/fixtures/B.json \
  --resolver echo \
  --write-cf14-neo4j
popd >/dev/null

echo "✅ Done. Query via the app:"
echo "   cd /Users/ryan/Desktop/ai-env/chirality-app && npm run dev"
echo "   curl -s -H 'Authorization: Bearer dev-super-secret' -H 'Content-Type: application/json' \\"
echo "     -d '{\"query\":\"{ cfMatrices(kind:\\\"A\\\"){ id kind nodes(limit:5){ id term } } }\"}' \\"
echo "     http://localhost:3001/api/v1/graph/graphql | jq ."