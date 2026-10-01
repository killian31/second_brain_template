### Obsidian

The user browses this vault in Obsidian. Nothing agents do depends on it. `.obsidian/` holds its configuration, so leave it alone unless asked. If `Home.md` exists at the root, it is the human dashboard (Dataview queries, styled by `.obsidian/snippets/home.css`); it renders only inside Obsidian, so agents use [[INDEX]] instead and never hand-edit its query results.
