"""SQLite memory system with live learning, skill acquisition, and agent training."""

import sqlite3
import json
import time
import hashlib
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


class MemoryDB:
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.executescript("""
            PRAGMA journal_mode=WAL;
            PRAGMA foreign_keys=ON;

            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                model TEXT,
                provider TEXT,
                config TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                last_active REAL,
                trust_score REAL DEFAULT 0.5,
                skill_level TEXT DEFAULT 'novice'
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                session_id TEXT,
                created_at REAL NOT NULL,
                updated_at REAL,
                summary TEXT,
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tokens INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            );

            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                prompt_template TEXT,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                updated_at REAL,
                source TEXT DEFAULT 'learned',
                metadata TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS agent_skills (
                agent_id TEXT NOT NULL,
                skill_id TEXT NOT NULL,
                proficiency REAL DEFAULT 0.0,
                practice_count INTEGER DEFAULT 0,
                last_practiced REAL,
                PRIMARY KEY (agent_id, skill_id),
                FOREIGN KEY (agent_id) REFERENCES agents(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id)
            );

            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                category TEXT,
                tags TEXT DEFAULT '[]',
                embedding BLOB,
                created_at REAL NOT NULL,
                updated_at REAL,
                access_count INTEGER DEFAULT 0,
                relevance_score REAL DEFAULT 0.0
            );

            CREATE TABLE IF NOT EXISTS attack_patterns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                target_type TEXT,
                prompt_template TEXT,
                effectiveness REAL DEFAULT 0.0,
                detection_rate REAL DEFAULT 0.0,
                created_at REAL NOT NULL,
                metadata TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS redteam_sessions (
                id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                agent_id TEXT,
                status TEXT DEFAULT 'active',
                started_at REAL NOT NULL,
                completed_at REAL,
                findings INTEGER DEFAULT 0,
                summary TEXT,
                config TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                type TEXT NOT NULL,
                severity TEXT DEFAULT 'medium',
                title TEXT NOT NULL,
                description TEXT,
                payload TEXT,
                cvss REAL DEFAULT 0.0,
                cwe TEXT,
                remediation TEXT,
                created_at REAL NOT NULL,
                verified INTEGER DEFAULT 0,
                FOREIGN KEY (session_id) REFERENCES redteam_sessions(id)
            );

            CREATE TABLE IF NOT EXISTS learning_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT DEFAULT 'system',
                event_type TEXT NOT NULL,
                context TEXT,
                outcome TEXT,
                reward REAL DEFAULT 0.0,
                created_at REAL NOT NULL,
                FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_knowledge_tags ON knowledge(tags);
            CREATE INDEX IF NOT EXISTS idx_findings_session ON findings(session_id);
            CREATE INDEX IF NOT EXISTS idx_learning_agent ON learning_log(agent_id);
        """)
        self.conn.commit()
        self._ensure_system_agent()

    def _ensure_system_agent(self):
        self.conn.execute(
            "INSERT OR IGNORE INTO agents (id, name, created_at) VALUES (?,?,?)",
            ('system', 'System', time.time())
        )
        self.conn.commit()

    # --- Agent Management ---
    def register_agent(self, name: str, model: str = None, provider: str = None, config: dict = None) -> str:
        import uuid
        agent_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO agents (id, name, model, provider, config, created_at, last_active) VALUES (?,?,?,?,?,?,?)",
            (agent_id, name, model, provider, json.dumps(config or {}), time.time(), time.time())
        )
        self.conn.commit()
        return agent_id

    def update_agent_trust(self, agent_id: str, delta: float):
        self.conn.execute(
            "UPDATE agents SET trust_score = MIN(1.0, MAX(0.0, trust_score + ?)), last_active = ? WHERE id = ?",
            (delta, time.time(), agent_id)
        )
        self.conn.commit()

    # --- Skill System ---
    def learn_skill(self, name: str, category: str, prompt_template: str, description: str = None, source: str = "learned") -> str:
        import uuid
        skill_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO skills (id, name, category, description, prompt_template, created_at, source) VALUES (?,?,?,?,?,?,?)",
            (skill_id, name, category, description, prompt_template, time.time(), source)
        )
        self.conn.commit()
        self._log_learning(None, "skill_learned", {"skill": name, "category": category}, "success", 0.5)
        return skill_id

    def practice_skill(self, agent_id: str, skill_id: str, success: bool):
        now = time.time()
        self.conn.execute("""
            INSERT INTO agent_skills (agent_id, skill_id, proficiency, practice_count, last_practiced)
            VALUES (?,?,?,1,?)
            ON CONFLICT(agent_id, skill_id) DO UPDATE SET
                proficiency = MIN(1.0, proficiency + ?),
                practice_count = practice_count + 1,
                last_practiced = ?
        """, (agent_id, skill_id, 0.1 if success else -0.05, now, 0.05 if success else -0.05, now))

        self.conn.execute("UPDATE skills SET usage_count = usage_count + 1, success_rate = (success_rate * usage_count + ?) / (usage_count + 1) WHERE id = ?",
                         (1.0 if success else 0.0, skill_id))
        self.conn.commit()
        self._log_learning(agent_id, "skill_practice", {"skill_id": skill_id}, "success" if success else "fail", 0.3 if success else -0.2)

    def get_agent_skills(self, agent_id: str) -> list:
        return [dict(r) for r in self.conn.execute("""
            SELECT s.*, a.proficiency, a.practice_count, a.last_practiced
            FROM skills s JOIN agent_skills a ON s.id = a.skill_id
            WHERE a.agent_id = ? ORDER BY a.proficiency DESC
        """, (agent_id,)).fetchall()]

    # --- Knowledge Base ---
    def store_knowledge(self, title: str, content: str, category: str = None, tags: list = None, source: str = None):
        import uuid
        kid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO knowledge (id, title, content, source, category, tags, created_at) VALUES (?,?,?,?,?,?,?)",
            (kid, title, content, source, category, json.dumps(tags or []), time.time())
        )
        self.conn.commit()
        return kid

    def search_knowledge(self, query: str, category: str = None, limit: int = 10) -> list:
        sql = "SELECT * FROM knowledge WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        if category:
            sql += " AND category = ?"
            params.append(category)
        sql += " ORDER BY relevance_score DESC, access_count DESC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(sql, params).fetchall()
        for r in rows:
            self.conn.execute("UPDATE knowledge SET access_count = access_count + 1 WHERE id = ?", (r["id"],))
        self.conn.commit()
        return [dict(r) for r in rows]

    # --- Attack Patterns ---
    def register_attack(self, name: str, ptype: str, prompt_template: str, target_type: str = None) -> str:
        import uuid
        aid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO attack_patterns (id, name, type, target_type, prompt_template, created_at) VALUES (?,?,?,?,?,?)",
            (aid, name, ptype, target_type, prompt_template, time.time())
        )
        self.conn.commit()
        return aid

    def get_attacks_by_type(self, ptype: str) -> list:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM attack_patterns WHERE type = ? ORDER BY effectiveness DESC", (ptype,)
        ).fetchall()]

    # --- Red Team Sessions ---
    def create_session(self, target: str, agent_id: str = None, config: dict = None) -> str:
        import uuid
        sid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO redteam_sessions (id, target, agent_id, started_at, config) VALUES (?,?,?,?,?)",
            (sid, target, agent_id, time.time(), json.dumps(config or {}))
        )
        self.conn.commit()
        return sid

    def add_finding(self, session_id: str, ftype: str, title: str, description: str = None,
                    severity: str = "medium", payload: str = None, cvss: float = 0.0, cwe: str = None):
        self.conn.execute(
            "INSERT INTO findings (session_id, type, severity, title, description, payload, cvss, cwe, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (session_id, ftype, severity, title, description, payload, cvss, cwe, time.time())
        )
        self.conn.execute("UPDATE redteam_sessions SET findings = findings + 1 WHERE id = ?", (session_id,))
        self.conn.commit()

    def get_session_findings(self, session_id: str) -> list:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM findings WHERE session_id = ? ORDER BY cvss DESC", (session_id,)
        ).fetchall()]

    # --- Learning System ---
    def _log_learning(self, agent_id: str, event_type: str, context: dict, outcome: str, reward: float = 0.0):
        self.conn.execute(
            "INSERT INTO learning_log (agent_id, event_type, context, outcome, reward, created_at) VALUES (?,?,?,?,?,?)",
            (agent_id or 'system', event_type, json.dumps(context), outcome, reward, time.time())
        )
        self.conn.commit()

    def reinforce(self, agent_id: str, event_type: str, context: dict, reward: float):
        self._log_learning(agent_id or 'system', event_type, context, "reinforced", reward)
        if agent_id:
            self.update_agent_trust(agent_id, reward * 0.1)

    def get_learning_summary(self, agent_id: str, days: int = 7) -> dict:
        cutoff = time.time() - (days * 86400)
        rows = self.conn.execute(
            "SELECT event_type, outcome, COUNT(*) as cnt, AVG(reward) as avg_reward FROM learning_log WHERE agent_id = ? AND created_at > ? GROUP BY event_type, outcome",
            (agent_id, cutoff)
        ).fetchall()
        return {
            "total_events": sum(r["cnt"] for r in rows),
            "avg_reward": float(np.mean([r["avg_reward"] for r in rows])) if rows else 0,
            "breakdown": [dict(r) for r in rows]
        }

    # --- Live Learning (reinforcement from outcomes) ---
    def live_learn(self, agent_id: str, action: str, outcome: dict):
        """Real-time learning from action outcomes."""
        reward = 0.0
        if outcome.get("success"):
            reward += 0.3
        if outcome.get("efficiency", 0) > 0.5:
            reward += 0.2
        if outcome.get("novelty"):
            reward += 0.4

        self.reinforce(agent_id, f"action_{action}", outcome, reward)

        # Auto-skill generation if high novelty
        if outcome.get("novelty") and reward > 0.5:
            skill_name = f"auto_{action}_{int(time.time())}"
            self.learn_skill(skill_name, "auto_learned", outcome.get("prompt", ""),
                           f"Auto-generated from {action}", source="reinforcement")
            return {"learned": True, "skill": skill_name, "reward": reward}
        return {"learned": False, "reward": reward}


memory = MemoryDB()
