#!/bin/bash
# Token-efficient SQLModel documentation fetcher via Context7 MCP
#
# Uses the fixed SQLModel library ID (/fastapi/sqlmodel) for direct, fast lookups.
# Fetches and filters official docs — only essential content enters Claude's context.
#
# Usage:
#   bash scripts/fetch-sqlmodel-docs.sh --topic <topic> [OPTIONS]
#
# Examples:
#   bash scripts/fetch-sqlmodel-docs.sh --topic "create models"
#   bash scripts/fetch-sqlmodel-docs.sh --topic "relationships" --mode info
#   bash scripts/fetch-sqlmodel-docs.sh --topic "select where" --verbose

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT7_SCRIPT_DIR="$(dirname "$SCRIPT_DIR")/../context7-efficient/scripts"

# SQLModel's fixed Context7 library ID
SQLMODEL_LIB_ID="/fastapi/sqlmodel"

TOPIC=""
MODE="code"
PAGE=1
VERBOSE=0

usage() {
  cat << USAGE
Usage: $0 --topic <topic> [OPTIONS]

Fetch official SQLModel documentation via Context7 MCP (token-efficient)

OPTIONS:
  --topic TOPIC    Topic to look up (e.g., "create models", "relationships")
  --mode MODE      code (default) or info
  --page NUM       Page number 1-10 (default: 1)
  --verbose, -v    Show token savings statistics
  --help, -h       Show this help

COMMON TOPICS:
  "create models"           Model definition, table=True, fields
  "session"                 Session, engine, context manager
  "select where"            Querying with select() and where()
  "relationships"           One-to-many, many-to-many, back_populates
  "FastAPI integration"     Lifespan, session dependency, router setup
  "create update delete"    CRUD write operations
  "Alembic migration"       Database migrations
USAGE
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --topic)     TOPIC="$2";   shift 2 ;;
    --mode)      MODE="$2";    shift 2 ;;
    --page)      PAGE="$2";    shift 2 ;;
    -v|--verbose) VERBOSE=1;   shift ;;
    -h|--help)   usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$TOPIC" ]; then
  echo "Error: --topic is required" >&2
  usage
fi

# Locate mcp-client.py — prefer context7-efficient's copy, fall back to local
MCP_CLIENT=""
if [ -f "$CONTEXT7_SCRIPT_DIR/mcp-client.py" ]; then
  MCP_CLIENT="$CONTEXT7_SCRIPT_DIR/mcp-client.py"
elif [ -f "$SCRIPT_DIR/mcp-client.py" ]; then
  MCP_CLIENT="$SCRIPT_DIR/mcp-client.py"
else
  echo "Error: mcp-client.py not found. Install context7-efficient skill or add mcp-client.py to scripts/." >&2
  exit 1
fi

[ $VERBOSE -eq 1 ] && echo "📚 Fetching SQLModel docs: topic='$TOPIC' mode='$MODE' page=$PAGE" >&2

# Fetch raw documentation
RAW_JSON=$(python3 "$MCP_CLIENT" call \
  -s "npx -y @upstash/context7-mcp" \
  -t get-library-docs \
  -p "{\"context7CompatibleLibraryID\": \"$SQLMODEL_LIB_ID\", \"topic\": \"$TOPIC\", \"tokens\": 5000}" \
  2>/dev/null)

# Extract text from JSON
if command -v jq &> /dev/null; then
  RAW_TEXT=$(echo "$RAW_JSON" | jq -r '.content[0].text // empty')
else
  RAW_TEXT=$(echo "$RAW_JSON" | python3 -c \
    'import sys, json; data=json.load(sys.stdin); print(data.get("content", [{}])[0].get("text", ""))')
fi

if [ -z "$RAW_TEXT" ]; then
  echo "Error: No documentation received. Check your Context7 MCP setup." >&2
  exit 1
fi

if [ $VERBOSE -eq 1 ]; then
  RAW_WORDS=$(echo "$RAW_TEXT" | wc -w)
  RAW_TOKENS=$(echo "$RAW_WORDS * 1.3" | bc | cut -d. -f1)
  echo "📊 Raw: ~$RAW_TOKENS tokens" >&2
fi

OUTPUT=""

if [ "$MODE" = "code" ]; then
  # Extract code blocks (up to 6)
  CODE_BLOCKS=$(echo "$RAW_TEXT" | awk '
    /^```/{
      if (in_block) {
        print $0; in_block=0; count++
        if (count >= 6) exit
      } else {
        in_block=1; print $0
      }
      next
    }
    in_block { print }
  ')
  [ -n "$CODE_BLOCKS" ] && OUTPUT+="## Code Examples\n\n$CODE_BLOCKS\n"

  # Extract function/class signatures
  SIGS=$(echo "$RAW_TEXT" | grep -E '^\s*(def |class |async def )' | head -10)
  [ -n "$SIGS" ] && OUTPUT+="\n## Signatures\n\n\`\`\`python\n$SIGS\n\`\`\`\n"
else
  # Info mode: first 2 code blocks + prose paragraphs
  CODE_BLOCKS=$(echo "$RAW_TEXT" | awk '
    /^```/{
      if (in_block) {
        print $0; in_block=0; count++
        if (count >= 2) exit
      } else {
        in_block=1; print $0
      }
      next
    }
    in_block { print }
  ')
  [ -n "$CODE_BLOCKS" ] && OUTPUT+="## Examples\n\n$CODE_BLOCKS\n"

  OVERVIEW=$(echo "$RAW_TEXT" | awk 'BEGIN{RS=""; FS="\n"} length($0) > 150 && !/```/{print; if(++c>=3) exit}')
  [ -n "$OVERVIEW" ] && OUTPUT+="\n## Overview\n\n$OVERVIEW\n"
fi

# Always extract important notes/warnings
NOTES=$(echo "$RAW_TEXT" | grep -iE '^\s*[>*-]?\s*(note|warning|tip|important):' | head -5)
[ -n "$NOTES" ] && OUTPUT+="\n## Notes\n\n$NOTES\n"

# Fallback: first 600 chars if nothing extracted
if [ -z "$OUTPUT" ]; then
  OUTPUT=$(echo "$RAW_TEXT" | head -c 600)
  OUTPUT+="\n\n[Truncated — try a more specific --topic]"
fi

echo -e "$OUTPUT"

if [ $VERBOSE -eq 1 ]; then
  FILTERED_WORDS=$(echo -e "$OUTPUT" | wc -w)
  FILTERED_TOKENS=$(echo "$FILTERED_WORDS * 1.3" | bc | cut -d. -f1)
  SAVINGS=$(echo "scale=1; (($RAW_TOKENS - $FILTERED_TOKENS) / $RAW_TOKENS) * 100" | bc 2>/dev/null || echo "N/A")
  echo "" >&2
  echo "✨ Filtered: ~$FILTERED_TOKENS tokens | Savings: ${SAVINGS}%" >&2
fi
