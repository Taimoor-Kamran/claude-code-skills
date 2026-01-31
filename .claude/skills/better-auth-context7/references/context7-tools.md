# Context7 MCP Tools (v2 API)

*2 tools available*

## `resolve-library-id`

Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

You MUST call this function before 'query-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

### Selection Process

1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
   - Name similarity to the query (exact matches prioritized)
   - Description relevance to the query's intent
   - Documentation coverage (prioritize libraries with higher Code Snippet counts)
   - Source reputation (consider libraries with High or Medium reputation more authoritative)
   - Benchmark Score: Quality indicator (100 is the highest score)

### Parameters

- **`query`** (`string`) *(required)*: The user's original question or task. This is used to rank library results by relevance to what the user is trying to accomplish. Do not include sensitive information.

- **`libraryName`** (`string`) *(required)*: Library name to search for and retrieve a Context7-compatible library ID.

### Response Format

Returns a list of matching libraries with:
- Title
- Context7-compatible library ID (e.g., `/better-auth/better-auth`)
- Code Snippets count
- Source Reputation (High/Medium/Low)
- Benchmark Score
- Description

### Examples

```bash
# Find Better Auth library
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t resolve-library-id \
  -p '{"query": "authentication with social providers", "libraryName": "better-auth"}'

# Find React library
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t resolve-library-id \
  -p '{"query": "React hooks examples", "libraryName": "react"}'
```

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The user's original question or task. Used to rank library results by relevance."
    },
    "libraryName": {
      "type": "string",
      "description": "Library name to search for and retrieve a Context7-compatible library ID."
    }
  },
  "required": ["query", "libraryName"]
}
```
</details>

## `query-docs`

Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework.

You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

### Parameters

- **`libraryId`** (`string`) *(required)*: Exact Context7-compatible library ID (e.g., '/better-auth/better-auth', '/mongodb/docs', '/vercel/next.js') retrieved from 'resolve-library-id' or directly from user query.

- **`query`** (`string`) *(required)*: The question or task you need help with. Be specific and include relevant details. Good examples: 'How to set up authentication with email/password' or 'Social provider OAuth configuration'. Bad examples: 'auth' or 'login'.

### Examples

```bash
# Get Better Auth authentication documentation
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/better-auth/better-auth", "query": "How to set up email password authentication"}'

# Get social login examples
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/better-auth/better-auth", "query": "GitHub OAuth configuration and sign in"}'

# Get session management info
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/better-auth/better-auth", "query": "Session management and cookie configuration"}'
```

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "libraryId": {
      "type": "string",
      "description": "Exact Context7-compatible library ID retrieved from 'resolve-library-id' or directly from user query."
    },
    "query": {
      "type": "string",
      "description": "The question or task you need help with. Be specific and include relevant details."
    }
  },
  "required": ["libraryId", "query"]
}
```
</details>

## Usage Patterns

### Pattern 1: Unknown Library

When you don't know the exact library ID:

```bash
# Step 1: Resolve library name
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t resolve-library-id \
  -p '{"query": "email password authentication setup", "libraryName": "better-auth"}'

# Step 2: Use returned ID to fetch docs
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/better-auth/better-auth", "query": "email password sign up and sign in"}'
```

### Pattern 2: Known Library ID

When you know the library ID:

```bash
# Direct fetch (skip resolve step)
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/better-auth/better-auth", "query": "two factor authentication setup"}'
```

### Pattern 3: Using fetch-docs.sh (Recommended)

The fetch-docs.sh script handles resolution automatically and filters output for token efficiency:

```bash
# Automatic resolution
bash scripts/fetch-docs.sh --library better-auth --topic "social providers"

# With known ID (faster)
bash scripts/fetch-docs.sh --library-id /better-auth/better-auth --topic "sessions"

# With verbose output
bash scripts/fetch-docs.sh --library better-auth --topic "2fa" --verbose
```

## Common Library IDs

Quick reference for popular libraries:

| Library | Context7 ID |
|---------|-------------|
| Better Auth | `/better-auth/better-auth` |
| React | `/reactjs/react.dev` |
| Next.js | `/vercel/nextjs.org` |
| Express | `/expressjs/expressjs.com` |
| MongoDB | `/mongodb/docs` |
| Prisma | `/prisma/docs` |
| Supabase | `/supabase/supabase` |

## Tips

1. **Library Resolution**: Always use `resolve-library-id` first unless you have the exact ID
2. **Specific Queries**: More specific queries yield better results
3. **Use fetch-docs.sh**: The shell script handles everything automatically with token savings
4. **Fallback**: If results are insufficient, try rephrasing your query
5. **Limit Calls**: Don't call tools more than 3 times per question
