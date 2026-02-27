---
name: oauth2-context7
description: Token-efficient OAuth 2.0 documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for OAuth 2.0 flows (Authorization Code, PKCE, Client Credentials, Device Flow), OpenID Connect (OIDC), JWT, token management, and popular OAuth libraries (authlib, oauthlib, oauth4webapi, passport.js, golang.org/x/oauth2). Use when users ask about OAuth 2.0 implementation, PKCE flow, refresh tokens, JWT validation, OIDC setup, social login integration, or securing APIs with OAuth. Triggers include questions like "How do I implement OAuth 2.0 PKCE", "Show me Authorization Code flow", "OAuth refresh token examples", "OIDC setup with Python", "JWT validation", or any OAuth 2.0 / OpenID Connect documentation request.
---

# OAuth 2.0 Context7 Documentation Fetcher

Fetch OAuth 2.0 and OpenID Connect documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Using authlib (Python - comprehensive OAuth 2.0 + OIDC)
bash scripts/fetch-docs.sh --library authlib --topic <topic>

# Using oauthlib (Python - core OAuth 2.0)
bash scripts/fetch-docs.sh --library oauthlib --topic <topic>

# Using oauth4webapi (JavaScript/TypeScript)
bash scripts/fetch-docs.sh --library oauth4webapi --topic <topic>

# Using golang.org/x/oauth2 (Go)
bash scripts/fetch-docs.sh --library "golang oauth2" --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library authlib --topic "authorization code"
bash scripts/fetch-docs.sh --library authlib --topic "PKCE"
bash scripts/fetch-docs.sh --library authlib --topic "client credentials"
bash scripts/fetch-docs.sh --library oauth4webapi --topic "refresh token"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

### 1. Identify Library + Topic

| Use Case | Recommended Library |
|----------|-------------------|
| Python OAuth 2.0 + OIDC | `authlib` |
| Python OAuth 2.0 core | `oauthlib` |
| JavaScript/TypeScript | `oauth4webapi` |
| Go | `golang oauth2` |
| Node.js Passport | `passport` |

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library <library> --topic <topic> --verbose
```

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (934 tokens, stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content (205 tokens to Claude)

## Parameters

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required (pick one):**
- `--library <name>` - Library name (auto-resolved via Context7)
- `--library-id <id>` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific feature/flow to focus on
- `--mode <code|info>` - `code` for examples (default), `info` for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

## Library IDs (for faster lookup)

```bash
authlib:        /lepture/authlib
oauthlib:       /oauthlib-team/oauthlib
oauth4webapi:   /panva/oauth4webapi
```

## Common OAuth 2.0 Topics

| Topic | Description |
|-------|-------------|
| `authorization code` | Authorization Code Grant flow |
| `PKCE` | Proof Key for Code Exchange (RFC 7636) |
| `client credentials` | Machine-to-machine OAuth 2.0 |
| `device flow` | Device Authorization Grant (RFC 8628) |
| `refresh token` | Token refresh and rotation |
| `introspection` | Token introspection (RFC 7662) |
| `revocation` | Token revocation (RFC 7009) |
| `JWT` | JSON Web Tokens, JWK, JWS |
| `OIDC` | OpenID Connect discovery, userinfo |
| `resource server` | Protecting APIs with Bearer tokens |
| `social login` | GitHub, Google, Facebook OAuth |
| `scope` | OAuth scopes and permissions |
| `state` | CSRF protection with state parameter |
| `nonce` | Replay protection for OIDC |

## Workflow Patterns

### Pattern 1: Authorization Code + PKCE (Web/SPA/Mobile)

User asks: "How do I implement OAuth 2.0 PKCE flow?"

```bash
# Step 1: Get PKCE overview
bash scripts/fetch-docs.sh --library authlib --topic "PKCE" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library authlib --topic "PKCE authorization code"
```

### Pattern 2: Client Credentials (API-to-API)

User asks: "Show me OAuth 2.0 client credentials flow"

```bash
bash scripts/fetch-docs.sh --library authlib --topic "client credentials" --verbose
```

### Pattern 3: JWT Validation

User asks: "How do I validate JWTs in Python?"

```bash
bash scripts/fetch-docs.sh --library authlib --topic "JWT validation"
bash scripts/fetch-docs.sh --library authlib --topic "JWK JWKS"
```

### Pattern 4: OpenID Connect

User asks: "How do I set up OIDC with authlib?"

```bash
# Discovery + setup
bash scripts/fetch-docs.sh --library authlib --topic "OIDC discovery"

# UserInfo endpoint
bash scripts/fetch-docs.sh --library authlib --topic "userinfo"
```

### Pattern 5: Resource Server (API Protection)

User asks: "How do I protect my API with Bearer tokens?"

```bash
bash scripts/fetch-docs.sh --library authlib --topic "resource server bearer token"
```

### Pattern 6: JavaScript/TypeScript

User asks: "OAuth 2.0 PKCE in TypeScript"

```bash
bash scripts/fetch-docs.sh --library oauth4webapi --topic "authorization code PKCE"
bash scripts/fetch-docs.sh --library oauth4webapi --topic "refresh token"
```

### Pattern 7: Go OAuth 2.0

User asks: "OAuth 2.0 in Go"

```bash
bash scripts/fetch-docs.sh --library "golang oauth2" --topic "authorization code"
bash scripts/fetch-docs.sh --library "golang oauth2" --topic "client credentials"
```

## OAuth 2.0 Flow Reference

### Authorization Code + PKCE (Recommended for public clients)

```
1. Generate code_verifier + code_challenge (S256)
2. Redirect to authorization endpoint with code_challenge
3. User authenticates + authorizes
4. Receive authorization_code at redirect_uri
5. Exchange code + code_verifier for tokens
6. Validate id_token (OIDC) / use access_token
```

### Client Credentials (Machine-to-machine)

```
1. POST /token with client_id + client_secret + grant_type=client_credentials
2. Receive access_token (no refresh_token)
3. Use access_token as Bearer in API requests
```

### Token Refresh

```
1. Detect access_token expiry (check exp claim or 401 response)
2. POST /token with grant_type=refresh_token + refresh_token
3. Receive new access_token (and optionally new refresh_token)
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

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Library not found | Try `--library-id` with direct Context7 ID |
| Topic not found | Try broader terms or use `--mode info` |
| Need more examples | Use `--page 2` or `--page 3` |
| OIDC vs OAuth confusion | Use `--mode info` for conceptual overview first |

## References

- [references/context7-tools.md](references/context7-tools.md) - Complete Context7 tool reference
- [references/oauth2-patterns.md](references/oauth2-patterns.md) - OAuth 2.0 code patterns by language

## Implementation Notes

**Components (for reference only, use fetch-docs.sh):**
- `mcp-client.py` - Universal MCP client (foundation)
- `fetch-raw.sh` - MCP wrapper
- `extract-code-blocks.sh` - Code example filter (awk)
- `extract-signatures.sh` - API signature filter (awk)
- `extract-notes.sh` - Important notes filter (grep)
- `fetch-docs.sh` - **Main orchestrator (ALWAYS USE THIS)**
