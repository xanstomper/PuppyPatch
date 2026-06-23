from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json

@dataclass
class Event:
    type: str
    payload: dict[str, Any]
    source: str = "horus"
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps({"ts": self.ts, "source": self.source, "type": self.type, "payload": self.payload}, ensure_ascii=False)
