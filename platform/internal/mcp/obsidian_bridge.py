"""Obsidian MCP integration for persistent brain/memory."""

import json
import os
import time
from pathlib import Path
from typing import Optional


class ObsidianBrain:
    """Bridge between red team platform and Obsidian vault via MCP."""

    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or os.environ.get("OBSIDIAN_VAULT", str(Path.home() / "redteam-brain"))
        self.notes_dir = Path(self.vault_path)
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        (self.notes_dir / "knowledge").mkdir(exist_ok=True)
        (self.notes_dir / "sessions").mkdir(exist_ok=True)
        (self.notes_dir / "skills").mkdir(exist_ok=True)
        (self.notes_dir / "findings").mkdir(exist_ok=True)
        self.connected = False

    def connect(self) -> bool:
        """Connect to Obsidian vault."""
        try:
            from mcp_obsidian import ObsidianMCP
            self.mcp = ObsidianMCP(vault_path=self.vault_path)
            self.connected = True
            return True
        except ImportError:
            # Fall back to file-based sync
            self.connected = False
            return False

    def store(self, category: str, title: str, content: str, tags: list = None) -> str:
        """Store content as an Obsidian note."""
        safe_title = title.replace(" ", "_").replace("/", "-")[:100]
        note_path = self.notes_dir / category / f"{safe_title}.md"

        tags_str = " ".join(f"#{t}" for t in (tags or []))
        frontmatter = f"---\ntags: [{', '.join(tags or [])}]\ncreated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"

        with open(note_path, "w") as f:
            f.write(frontmatter)
            f.write(content)
            if tags_str:
                f.write(f"\n\n{tags_str}")

        return str(note_path)

    def load(self, category: str, title: str) -> Optional[str]:
        """Load content from an Obsidian note."""
        safe_title = title.replace(" ", "_").replace("/", "-")[:100]
        note_path = self.notes_dir / category / f"{safe_title}.md"
        if note_path.exists():
            return note_path.read_text()
        return None

    def search(self, query: str) -> list:
        """Search notes in vault."""
        results = []
        for md_file in self.notes_dir.rglob("*.md"):
            content = md_file.read_text()
            if query.lower() in content.lower():
                results.append({
                    "path": str(md_file),
                    "title": md_file.stem,
                    "preview": content[:200].replace("---\n", "").strip()
                })
        return results

    def sync_from_db(self):
        """Sync SQLite knowledge base to Obsidian vault."""
        from pkg.db.memory import memory

        # Sync knowledge entries
        for row in memory.conn.execute("SELECT * FROM knowledge"):
            self.store("knowledge", row["title"], row["content"],
                      json.loads(row["tags"]) if row["tags"] else [])

        # Sync attack patterns
        for row in memory.conn.execute("SELECT * FROM attack_patterns"):
            content = f"## {row['name']}\n\n**Type:** {row['type']}\n**Target:** {row.get('target_type', 'N/A')}\n\n### Template\n```\n{row['prompt_template']}\n```\n\n**Effectiveness:** {row['effectiveness']:.0%}"
            self.store("skills", f"attack_{row['name']}", content, [row['type'], 'attack'])

        return {"synced": True}


def get_brain() -> ObsidianBrain:
    brain = ObsidianBrain()
    brain.connect()
    return brain
