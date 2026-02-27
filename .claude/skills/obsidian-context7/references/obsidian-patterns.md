# Obsidian Plugin Common Patterns

## Plugin Entry Point

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    await this.loadSettings();
    this.addCommand({ ... });
    this.addSettingTab(new MySettingTab(this.app, this));
    this.addRibbonIcon('dice', 'My Plugin', () => { ... });
  }

  onunload() {
    // cleanup
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

## Commands

```typescript
this.addCommand({
  id: 'my-command',
  name: 'My Command',
  hotkeys: [{ modifiers: ['Mod'], key: 'k' }],
  callback: () => {
    new Notice('Hello!');
  },
  // editorCallback: (editor: Editor) => { ... }  // for editor-only commands
  // checkCallback: (checking: boolean) => { ... }  // for conditional commands
});
```

## Vault API – File Operations

```typescript
// Read a file
const content = await this.app.vault.read(file);  // TFile

// Write/modify a file
await this.app.vault.modify(file, newContent);

// Create a file
await this.app.vault.create('path/to/note.md', 'content');

// Rename/move
await this.app.fileManager.renameFile(file, 'new/path/note.md');

// Delete
await this.app.vault.trash(file, true);  // true = use system trash

// Get all markdown files
const files = this.app.vault.getMarkdownFiles();

// Get file by path
const file = this.app.vault.getAbstractFileByPath('path/to/note.md');
```

## Workspace API

```typescript
// Get active editor
const view = this.app.workspace.getActiveViewOfType(MarkdownView);
if (view) {
  const editor = view.editor;
}

// Open a file
await this.app.workspace.openLinkText('note name', '', false);

// Get active file
const file = this.app.workspace.getActiveFile();

// Listen to file open events
this.registerEvent(
  this.app.workspace.on('file-open', (file) => { ... })
);
```

## Editor API

```typescript
// Get cursor position
const cursor = editor.getCursor();  // { line: number, ch: number }

// Get selection
const selected = editor.getSelection();

// Replace selection
editor.replaceSelection('new text');

// Get entire content
const content = editor.getValue();

// Set content
editor.setValue('new content');

// Get line
const line = editor.getLine(0);

// Move cursor
editor.setCursor({ line: 0, ch: 0 });
```

## Settings Tab

```typescript
import { App, PluginSettingTab, Setting } from 'obsidian';

class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName('Setting Name')
      .setDesc('Description')
      .addText(text => text
        .setPlaceholder('Enter value')
        .setValue(this.plugin.settings.mySetting)
        .onChange(async (value) => {
          this.plugin.settings.mySetting = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.enabled)
        .onChange(async (value) => {
          this.plugin.settings.enabled = value;
          await this.plugin.saveSettings();
        }));
  }
}
```

## Modal

```typescript
import { App, Modal } from 'obsidian';

class MyModal extends Modal {
  constructor(app: App) {
    super(app);
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.setText('Hello!');
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

// Usage
new MyModal(this.app).open();
```

## FuzzySuggestModal (Quick Switcher-style)

```typescript
import { FuzzySuggestModal } from 'obsidian';

class MyFuzzyModal extends FuzzySuggestModal<string> {
  getItems(): string[] {
    return ['item1', 'item2', 'item3'];
  }

  getItemText(item: string): string {
    return item;
  }

  onChooseItem(item: string, evt: MouseEvent | KeyboardEvent): void {
    new Notice(`Selected: ${item}`);
  }
}
```

## Events

```typescript
// Register events (auto-cleaned on unload)
this.registerEvent(
  this.app.vault.on('create', (file) => { ... })
);
this.registerEvent(
  this.app.vault.on('modify', (file) => { ... })
);
this.registerEvent(
  this.app.vault.on('delete', (file) => { ... })
);
this.registerEvent(
  this.app.vault.on('rename', (file, oldPath) => { ... })
);
this.registerEvent(
  this.app.workspace.on('active-leaf-change', (leaf) => { ... })
);
```

## MetadataCache (Frontmatter & Tags)

```typescript
// Get file metadata
const cache = this.app.metadataCache.getFileCache(file);
const frontmatter = cache?.frontmatter;  // parsed YAML frontmatter
const tags = cache?.tags;  // array of TagCache
const links = cache?.links;  // outgoing links

// Get all tags in vault
const allTags = Object.keys(this.app.metadataCache.getTags());

// Resolve a link to a file
const resolvedFile = this.app.metadataCache.getFirstLinkpathDest('note name', '');
```

## Custom View (Pane)

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';

export const MY_VIEW_TYPE = 'my-view';

class MyView extends ItemView {
  getViewType() { return MY_VIEW_TYPE; }
  getDisplayText() { return 'My View'; }

  async onOpen() {
    this.containerEl.children[1].createEl('h2', { text: 'My View' });
  }

  async onClose() {}
}

// Register view
this.registerView(MY_VIEW_TYPE, (leaf) => new MyView(leaf));

// Activate view
async activateView() {
  this.app.workspace.detachLeavesOfType(MY_VIEW_TYPE);
  await this.app.workspace.getRightLeaf(false).setViewState({
    type: MY_VIEW_TYPE,
    active: true,
  });
  this.app.workspace.revealLeaf(
    this.app.workspace.getLeavesOfType(MY_VIEW_TYPE)[0]
  );
}
```

## Markdown Rendering

```typescript
import { MarkdownRenderer, Component } from 'obsidian';

// Render markdown into a container element
await MarkdownRenderer.render(
  this.app,
  '**bold** and [[wikilink]]',
  containerEl,
  sourcePath,   // path of current file for resolving links
  new Component()
);
```

## Status Bar

```typescript
const statusBarItem = this.addStatusBarItem();
statusBarItem.setText('My Plugin Active');
```

## Context Menu

```typescript
import { Menu } from 'obsidian';

this.registerEvent(
  this.app.workspace.on('file-menu', (menu, file) => {
    menu.addItem((item) => {
      item
        .setTitle('My Action')
        .setIcon('pencil')
        .onClick(async () => { ... });
    });
  })
);
```

## Interval (auto-cleared)

```typescript
this.registerInterval(
  window.setInterval(() => { ... }, 5 * 60 * 1000)
);
```

## Key Topics by Use Case

| Use Case | Topics to Fetch |
|----------|----------------|
| Build a plugin scaffold | `plugin lifecycle`, `plugin class` |
| Work with notes/files | `vault api`, `vault read write` |
| Interact with editor | `editor api`, `editor cursor` |
| Add commands | `commands`, `hotkeys` |
| Add settings | `settings tab`, `pluginsettingtab` |
| Show dialogs | `modal`, `fuzzysuggestmodal` |
| Custom side pane | `itemview`, `workspace leaf` |
| React to file changes | `events`, `vault on modify` |
| Read frontmatter | `metadatacache`, `frontmatter` |
| Render markdown | `markdownrenderer` |
