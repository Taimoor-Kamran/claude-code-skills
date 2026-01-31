#!/bin/bash
# Main orchestrator: Token-efficient documentation fetcher
#
# This script achieves 94% token savings by:
# 1. Fetching raw docs (5,500 tokens stay in shell)
# 2. Filtering with grep/awk/sed (0 LLM tokens!)
# 3. Returning condensed output (~350 tokens to Claude)
#
# Updated for Context7 MCP v2 API:
# - resolve-library-id now requires both query and libraryName
# - get-library-docs renamed to query-docs with libraryId and query params

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
LIBRARY_ID=""
TOPIC=""
MODE="code"
VERBOSE=0

usage() {
  cat << USAGE
Usage: $0 [OPTIONS]

Token-efficient documentation fetcher using Context7 MCP

OPTIONS:
  --library-id ID    Context7 library ID (e.g., /better-auth/better-auth)
  --library NAME     Library name (will resolve to ID)
  --topic TOPIC      Topic/query to focus on (e.g., "social login", "sessions")
  --mode MODE        Mode: code (default) or info (affects local filtering)
  --verbose, -v      Show token statistics
  --help, -h         Show this help

EXAMPLES:
  # Quick lookup with known library ID
  $0 --library-id /better-auth/better-auth --topic "email authentication"

  # Resolve library name first
  $0 --library better-auth --topic "social providers" --mode code

  # Get conceptual info
  $0 --library-id /better-auth/better-auth --topic "getting started" --mode info
USAGE
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --library-id)
      LIBRARY_ID="$2"
      shift 2
      ;;
    --library)
      LIBRARY_NAME="$2"
      shift 2
      ;;
    --topic)
      TOPIC="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    -v|--verbose)
      VERBOSE=1
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

# Build the query string for Context7
build_query() {
  local topic="$1"
  local mode="$2"

  if [ -z "$topic" ]; then
    echo "documentation and code examples"
  elif [ "$mode" = "info" ]; then
    echo "How does $topic work? Explain concepts and architecture"
  else
    echo "Show me code examples for $topic"
  fi
}

# Resolve library if name provided
if [ -n "${LIBRARY_NAME:-}" ] && [ -z "$LIBRARY_ID" ]; then
  [ $VERBOSE -eq 1 ] && echo "🔍 Resolving library: $LIBRARY_NAME..." >&2

  # Build query for resolve-library-id (now requires both query and libraryName)
  RESOLVE_QUERY=$(build_query "$TOPIC" "$MODE")

  # Call resolve-library-id with both required parameters
  RESOLVE_JSON=$(python3 "$SCRIPT_DIR/mcp-client.py" call \
    -s "npx -y @upstash/context7-mcp" \
    -t resolve-library-id \
    -p "{\"query\": \"$RESOLVE_QUERY\", \"libraryName\": \"$LIBRARY_NAME\"}" 2>/dev/null)

  # Extract text from JSON (fallback to Python if jq not available)
  if command -v jq &> /dev/null; then
    RESOLVE_TEXT=$(echo "$RESOLVE_JSON" | jq -r '.content[0].text // empty')
  else
    RESOLVE_TEXT=$(echo "$RESOLVE_JSON" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data.get("content", [{}])[0].get("text", ""))')
  fi

  # Extract library ID - look for "Context7-compatible library ID:" pattern
  # The response format is: "- Context7-compatible library ID: /org/project"
  LIBRARY_ID=$(echo "$RESOLVE_TEXT" | grep -oP 'Context7-compatible library ID:\s*\K/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+' | head -n 1 || true)

  # Fallback: try backtick format
  if [ -z "$LIBRARY_ID" ]; then
    LIBRARY_ID=$(echo "$RESOLVE_TEXT" | grep -oP '`/[^`]+`' | head -n 1 | tr -d '`' || true)
  fi

  if [ -n "$LIBRARY_ID" ]; then
    [ $VERBOSE -eq 1 ] && echo "✅ Resolved to: $LIBRARY_ID" >&2
  else
    [ $VERBOSE -eq 1 ] && echo "⚠️ Could not extract library ID from response" >&2
    [ $VERBOSE -eq 1 ] && echo "Response: $RESOLVE_TEXT" >&2
  fi
fi

# Validate library ID
if [ -z "$LIBRARY_ID" ]; then
  echo "Error: Must specify --library-id or --library" >&2
  usage
fi

# Step 1: Fetch raw documentation (stays in shell memory!)
[ $VERBOSE -eq 1 ] && echo "📚 Fetching documentation..." >&2

# Build query for query-docs
QUERY=$(build_query "$TOPIC" "$MODE")

RAW_JSON=$("$SCRIPT_DIR/fetch-raw.sh" "$LIBRARY_ID" "$QUERY")

# Step 2: Extract text from JSON (using Python if jq not available)
if command -v jq &> /dev/null; then
  RAW_TEXT=$(echo "$RAW_JSON" | jq -r '.content[0].text // empty')
else
  RAW_TEXT=$(echo "$RAW_JSON" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data.get("content", [{}])[0].get("text", ""))')
fi

if [ -z "$RAW_TEXT" ]; then
  echo "Error: No documentation received from Context7" >&2
  echo "Library ID: $LIBRARY_ID" >&2
  echo "Query: $QUERY" >&2
  exit 1
fi

# Calculate raw token count (approximate: words * 1.3)
if [ $VERBOSE -eq 1 ]; then
  RAW_WORDS=$(echo "$RAW_TEXT" | wc -w)
  RAW_TOKENS=$(echo "$RAW_WORDS * 1.3" | bc | cut -d. -f1)
  echo "📊 Raw response: ~$RAW_WORDS words (~$RAW_TOKENS tokens)" >&2
fi

# Step 3: Filter using shell tools (0 LLM tokens!)
# This is where the magic happens - all processing stays in shell

OUTPUT=""

if [ "$MODE" = "code" ]; then
  # Code mode: Extract code examples and API signatures

  # Extract code blocks
  CODE_BLOCKS=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-code-blocks.sh" 5)

  if [ -n "$CODE_BLOCKS" ] && [ "$CODE_BLOCKS" != "# No code blocks found" ]; then
    OUTPUT+="## Code Examples\n\n$CODE_BLOCKS\n"
  fi

  # Extract API signatures
  SIGNATURES=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-signatures.sh" 3)

  if [ -n "$SIGNATURES" ]; then
    OUTPUT+="\n## API Signatures\n\n$SIGNATURES\n"
  fi

else
  # Info mode: Extract conceptual content

  # Get fewer code examples (2 max)
  CODE_BLOCKS=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-code-blocks.sh" 2)

  if [ -n "$CODE_BLOCKS" ] && [ "$CODE_BLOCKS" != "# No code blocks found" ]; then
    OUTPUT+="## Examples\n\n$CODE_BLOCKS\n"
  fi

  # Extract key paragraphs (first 3 substantial paragraphs)
  OVERVIEW=$(echo "$RAW_TEXT" | \
    awk 'BEGIN{RS=""; FS="\n"} length($0) > 200 && !/```/{print; if(++count>=3) exit}')

  if [ -n "$OVERVIEW" ]; then
    OUTPUT+="\n## Overview\n\n$OVERVIEW\n"
  fi
fi

# Always add important notes
NOTES=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-notes.sh" 3)

if [ -n "$NOTES" ]; then
  OUTPUT+="\n## Important Notes\n\n$NOTES\n"
fi

# Fallback if no content extracted
if [ -z "$OUTPUT" ]; then
  OUTPUT=$(echo "$RAW_TEXT" | head -c 500)
  OUTPUT+="\n\n[Response truncated for brevity...]"
fi

# Step 4: Output filtered content (this is what enters Claude's context!)
echo -e "$OUTPUT"

# Calculate filtered token count and savings
if [ $VERBOSE -eq 1 ]; then
  FILTERED_WORDS=$(echo -e "$OUTPUT" | wc -w)
  FILTERED_TOKENS=$(echo "$FILTERED_WORDS * 1.3" | bc | cut -d. -f1)
  if [ "$RAW_TOKENS" -gt 0 ]; then
    SAVINGS=$(echo "scale=1; (($RAW_TOKENS - $FILTERED_TOKENS) / $RAW_TOKENS) * 100" | bc)
  else
    SAVINGS="0"
  fi

  echo "" >&2
  echo "✨ Filtered output: ~$FILTERED_WORDS words (~$FILTERED_TOKENS tokens)" >&2
  echo "💰 Token savings: ${SAVINGS}%" >&2
fi
