from __future__ import annotations
from pathlib import Path
from typing import Any
import sqlite3, json, time

class MemoryStore:
    def __init__(self, path: str = ".horus/memory.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._init()
    def _init(self) -> None:
        cur = self.conn.cursor()
        cur.execute("create table if not exists events(id integer primary key, ts real, type text, scope text, content text, meta text)")
        cur.execute("create virtual table if not exists memory_fts using fts5(content, type, scope, content='events', content_rowid='id')")
        self.conn.commit()
    def add(self, type: str, content: str, scope: str = "session", meta: dict[str, Any] | None = None) -> int:
        cur = self.conn.cursor()
        cur.execute("insert into events(ts,type,scope,content,meta) values(?,?,?,?,?)", (time.time(), type, scope, content, json.dumps(meta or {})))
        rowid = int(cur.lastrowid)
        cur.execute("insert into memory_fts(rowid,content,type,scope) values(?,?,?,?)", (rowid, content, type, scope))
        self.conn.commit()
        return rowid
    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("select e.id,e.ts,e.type,e.scope,e.content,e.meta from memory_fts f join events e on e.id=f.rowid where memory_fts match ? limit ?", (query, limit))
        return [{"id":r[0],"ts":r[1],"type":r[2],"scope":r[3],"content":r[4],"meta":json.loads(r[5] or '{}')} for r in cur.fetchall()]
    def summarize(self, scope: str = "session") -> str:
        cur = self.conn.cursor()
        cur.execute("select type,content from events where scope=? order by id desc limit 20", (scope,))
        rows = cur.fetchall()
        return "\n".join([f"- {t}: {c[:160]}" for t,c in rows])
    def export_jsonl(self, path: str) -> None:
        cur = self.conn.cursor()
        with open(path, "w", encoding="utf-8") as f:
            for r in cur.execute("select id,ts,type,scope,content,meta from events order by id"):
                f.write(json.dumps({"id":r[0],"ts":r[1],"type":r[2],"scope":r[3],"content":r[4],"meta":json.loads(r[5] or '{}')}) + "\n")
