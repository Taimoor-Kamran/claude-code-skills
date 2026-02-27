---
name: obsidian-context7
description: Token-efficient Obsidian Plugin API documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for building Obsidian plugins including Plugin lifecycle, Vault API, Workspace API, Editor API, Commands, Settings, Modals, Views, Events, and Markdown rendering. Use when users ask about Obsidian plugin development, need code examples for the Obsidian API, want to build custom plugins, work with files/notes programmatically, create ribbon icons, register commands, add settings tabs, or any Obsidian plugin development task. Triggers include questions like "How do I create an Obsidian plugin", "Show me Vault API examples", "Obsidian command registration", "How to add a settings tab in Obsidian", or any Obsidian plugin API documentation request.
---

# Obsidian Plugin API Context7 Documentation Fetcher

Fetch Obsidian Plugin API documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library obsidian --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library obsidian --topic "plugin lifecycle"
bash scripts/fetch-docs.sh --library obsidian --topic "vault api"
bash scripts/fetch-docs.sh --library obsidian --topic "editor commands"
bash scripts/fetch-docs.sh --library obsidian --topic "settings tab"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Obsidian Plugin API documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific API area (vault, workspace, editor, commands, settings, modals, views, events, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library obsidian --topic <topic> --verbose
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
- `--library obsidian` - Uses Obsidian library
- `--library-id /obsidianmd/obsidian-api` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific API area to focus on
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

## Obsidian Library ID

Use `--library-id` for faster lookup (skips resolution):

```bash
Obsidian API:   /obsidianmd/obsidian-api
```

## Common Obsidian Topics

| Topic | Description |
|-------|-------------|
| `plugin lifecycle` | onload, onunload, Plugin class setup |
| `vault api` | File/folder CRUD, read, write, rename, delete |
| `workspace api` | Leaves, views, split panes, active editor |
| `editor api` | Cursor, selection, text manipulation, CodeMirror |
| `commands` | registerCommand, addCommand, hotkeys |
| `settings` | PluginSettingTab, addSettingTab, loadData, saveData |
| `modals` | Modal class, SuggestModal, FuzzySuggestModal |
| `views` | ItemView, custom panes, icon registration |
| `events` | on, off, trigger, EventRef patterns |
| `markdown` | MarkdownRenderer, renderMarkdown, MarkdownView |
| `notice` | Notice class, status bar items |
| `ribbon` | addRibbonIcon, ribbon actions |
| `menu` | Menu class, addMenuItem, context menus |
| `file manager` | FileManager, rename, trash, create |
| `metadata` | MetadataCache, frontmatter, getAllTags |
| `search` | SearchComponent, prepareQuery |
| `keymap` | Hotkey registration, modifier keys |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me how to register a command in Obsidian"

```bash
bash scripts/fetch-docs.sh --library obsidian --topic "commands" --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning an API Area

User asks: "How do I work with files in Obsidian plugins?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library obsidian --topic "vault api" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library obsidian --topic "vault read write" --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How do I create a settings tab?"

```bash
bash scripts/fetch-docs.sh --library-id /obsidianmd/obsidian-api --topic "settings tab"
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library obsidian --topic "workspace" --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library obsidian --topic "workspace" --page 2
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

## Obsidian-Specific Examples

### Plugin Setup

```bash
# Plugin lifecycle
bash scripts/fetch-docs.sh --library obsidian --topic "plugin onload"

# Manifest and main entry
bash scripts/fetch-docs.sh --library obsidian --topic "plugin class"
```

### Vault & File Operations

```bash
# Read/write files
bash scripts/fetch-docs.sh --library obsidian --topic "vault read write"

# List files and folders
bash scripts/fetch-docs.sh --library obsidian --topic "vault getFiles"

# Create and delete
bash scripts/fetch-docs.sh --library obsidian --topic "vault create delete"
```

### Editor & Workspace

```bash
# Active editor access
bash scripts/fetch-docs.sh --library obsidian --topic "workspace activeEditor"

# Editor cursor and selection
bash scripts/fetch-docs.sh --library obsidian --topic "editor cursor selection"

# Open files in panes
bash scripts/fetch-docs.sh --library obsidian --topic "workspace openLinkText"
```

### UI Components

```bash
# Settings tab
bash scripts/fetch-docs.sh --library obsidian --topic "settings tab addSetting"

# Modal dialogs
bash scripts/fetch-docs.sh --library obsidian --topic "modal open close"

# Notice / toast messages
bash scripts/fetch-docs.sh --library obsidian --topic "notice"

# Ribbon icons
bash scripts/fetch-docs.sh --library obsidian --topic "ribbon icon"
```

### Metadata & Search

```bash
# Frontmatter access
bash scripts/fetch-docs.sh --library obsidian --topic "metadata frontmatter"

# Cache and tags
bash scripts/fetch-docs.sh --library obsidian --topic "metadatacache tags"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Topic not found | Try name variations or use broader search term |
| No results | Use `--mode info` or broader topic |
| Need more examples | Increase page: `--page 2` |
| Want full context | Use `--mode info` for explanations |
| Library not resolving | Use `--library-id /obsidianmd/obsidian-api` directly |

## References

For detailed Context7 MCP tool documentation and Obsidian patterns, see:
- [references/context7-tools.md](references/context7-tools.md) - Complete tool reference
- [references/obsidian-patterns.md](references/obsidian-patterns.md) - Common Obsidian plugin patterns

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
