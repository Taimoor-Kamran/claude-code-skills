#!/bin/bash
# Fetch raw documentation from Context7 MCP
# Output: JSON response (stays in shell, doesn't enter Claude context)
#
# Updated for Context7 MCP v2 API:
# - Tool: query-docs (renamed from get-library-docs)
# - Parameters: libraryId, query (simplified from context7CompatibleLibraryID, topic, mode, page)

set -euo pipefail

LIBRARY_ID="${1:?Error: Library ID required}"
QUERY="${2:-}"

# Build query from topic - make it more descriptive for better results
if [ -z "$QUERY" ]; then
  QUERY="documentation and code examples"
fi

# Build parameters JSON for query-docs
PARAMS=$(cat <<JSON
{
  "libraryId": "$LIBRARY_ID",
  "query": "$QUERY"
}
JSON
)

# Call MCP server (response stays in this subprocess!)
python3 "$(dirname "$0")/mcp-client.py" call \
  -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p "$PARAMS" 2>/dev/null
