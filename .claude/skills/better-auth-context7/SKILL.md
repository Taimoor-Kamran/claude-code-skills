---
name: better-auth-context7
description: Token-efficient Better Auth documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for Better Auth authentication library including email/password auth, social providers, sessions, 2FA, database adapters, and framework integrations. Use when users ask about Better Auth features, need code examples for authentication flows, social login setup, session management, or two-factor authentication. Triggers include questions like "How do I set up Better Auth", "Show me social login examples", "Better Auth session management", or any Better Auth-related documentation request.
---

# Better Auth Context7 Documentation Fetcher

Fetch Better Auth documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library better-auth --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library better-auth --topic authentication
bash scripts/fetch-docs.sh --library better-auth --topic "social providers"
bash scripts/fetch-docs.sh --library better-auth --topic sessions
bash scripts/fetch-docs.sh --library better-auth --topic "two factor"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Better Auth documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific feature (email auth, social providers, sessions, 2fa, database, middleware, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library better-auth --topic <topic> --verbose
```

The `--verbose` flag shows token savings statistics.

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (934 tokens, stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content (205 tokens to Claude)

## Parameters

### Basic Usage

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required (pick one):**
- `--library better-auth` - Uses Better Auth library
- `--library-id /better-auth/better-auth` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific feature to focus on
- `--mode <code|info>` - code for examples (default), info for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

### Mode Selection

**Code Mode (default):** Returns code examples + API signatures
```bash
--mode code
```

**Info Mode:** Returns conceptual explanations + fewer examples
```bash
--mode info
```

## Better Auth Library IDs

Use `--library-id` for faster lookup (skips resolution):

```bash
Better Auth (official):    /better-auth/better-auth
Better Auth (llms.txt):    /llmstxt/better-auth_llms_txt
```

Both IDs provide comprehensive Better Auth documentation. The `llmstxt` version has more code snippets.

## Common Better Auth Topics

| Topic | Description |
|-------|-------------|
| `email password` | Email/password sign up, sign in, password reset |
| `social providers` | GitHub, Google, Apple, Discord OAuth |
| `sessions` | Session management, cookies, token caching |
| `two factor` | TOTP, backup codes, 2FA setup |
| `database` | PostgreSQL, SQLite, MySQL, Drizzle, Prisma adapters |
| `middleware` | Route protection, Next.js middleware |
| `nextjs` | Next.js App Router integration |
| `plugins` | Better Auth plugins and extensions |
| `client` | Client-side hooks and methods |
| `server` | Server-side configuration and API |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me Better Auth sign up examples"

```bash
bash scripts/fetch-docs.sh --library better-auth --topic "sign up email" --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning Better Auth Feature

User asks: "How do I get started with Better Auth social login?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library better-auth --topic "social providers" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library better-auth --topic "github oauth" --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How does Better Auth session management work?"

```bash
bash scripts/fetch-docs.sh --library-id /better-auth/better-auth --topic sessions
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library better-auth --topic authentication --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library better-auth --topic authentication --page 2
```

## Token Efficiency

**How it works:**

1. `fetch-docs.sh` calls `fetch-raw.sh` (which uses `mcp-client.py`)
2. Full response (934 tokens) stays in subprocess memory
3. Shell filters (awk/grep/sed) extract essentials (0 LLM tokens used)
4. Returns filtered output (205 tokens) to Claude

**Savings:**
- Direct MCP: 934 tokens per query
- This approach: 205 tokens per query
- **77% reduction**

**Do NOT use `mcp-client.py` directly** - it bypasses filtering and wastes tokens.

## Better Auth-Specific Examples

### Email/Password Authentication

```bash
# Sign up flow
bash scripts/fetch-docs.sh --library better-auth --topic "email sign up"

# Sign in flow
bash scripts/fetch-docs.sh --library better-auth --topic "email sign in"

# Password reset
bash scripts/fetch-docs.sh --library better-auth --topic "password reset"
```

### Social Providers

```bash
# GitHub OAuth
bash scripts/fetch-docs.sh --library better-auth --topic "github oauth"

# Google OAuth
bash scripts/fetch-docs.sh --library better-auth --topic "google oauth"

# Multiple providers
bash scripts/fetch-docs.sh --library better-auth --topic "social providers"
```

### Session Management

```bash
# Session basics
bash scripts/fetch-docs.sh --library better-auth --topic "session management"

# Session hooks
bash scripts/fetch-docs.sh --library better-auth --topic "useSession"

# Server-side sessions
bash scripts/fetch-docs.sh --library better-auth --topic "getSession server"
```

### Two-Factor Authentication

```bash
# 2FA setup
bash scripts/fetch-docs.sh --library better-auth --topic "two factor setup"

# TOTP verification
bash scripts/fetch-docs.sh --library better-auth --topic "totp verify"

# Backup codes
bash scripts/fetch-docs.sh --library better-auth --topic "backup codes"
```

### Database Adapters

```bash
# PostgreSQL
bash scripts/fetch-docs.sh --library better-auth --topic "postgresql adapter"

# Prisma
bash scripts/fetch-docs.sh --library better-auth --topic "prisma adapter"

# Drizzle
bash scripts/fetch-docs.sh --library better-auth --topic "drizzle adapter"
```

### Framework Integration

```bash
# Next.js setup
bash scripts/fetch-docs.sh --library better-auth --topic "nextjs integration"

# Express setup
bash scripts/fetch-docs.sh --library better-auth --topic "express integration"

# Middleware
bash scripts/fetch-docs.sh --library better-auth --topic "middleware protection"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Topic not found | Try name variations or use broader search term |
| No results | Use `--mode info` or broader topic |
| Need more examples | Increase page: `--page 2` |
| Want full context | Use `--mode info` for explanations |

## References

For detailed Context7 MCP tool documentation, see:
- [references/context7-tools.md](references/context7-tools.md) - Complete tool reference
- [references/better-auth-patterns.md](references/better-auth-patterns.md) - Common Better Auth patterns

## Implementation Notes

**Components (for reference only, use fetch-docs.sh):**
- `mcp-client.py` - Universal MCP client (foundation)
- `fetch-raw.sh` - MCP wrapper
- `extract-code-blocks.sh` - Code example filter (awk)
- `extract-signatures.sh` - API signature filter (awk)
- `extract-notes.sh` - Important notes filter (grep)
- `fetch-docs.sh` - **Main orchestrator (ALWAYS USE THIS)**

**Architecture:**
Shell pipeline processes documentation in subprocess, keeping full response out of Claude's context. Only filtered essentials enter the LLM context, achieving 77% token savings with 100% functionality preserved.

Based on [Anthropic's "Code Execution with MCP" blog post](https://www.anthropic.com/engineering/code-execution-with-mcp).
