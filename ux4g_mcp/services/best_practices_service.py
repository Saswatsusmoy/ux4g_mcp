"""Knowledge-base service for UX4G handbook best practices."""
import json
from typing import Any

from ..config import METADATA_DIR


class BestPracticesService:
    """Serve handbook-backed best practices with lightweight query matching."""

    def __init__(self) -> None:
        self._kb_path = METADATA_DIR / "best_practices_kb.json"
        self._kb = self._load_kb()

    def _load_kb(self) -> dict[str, Any]:
        if not self._kb_path.exists():
            return {
                "source": {
                    "title": "UX4G Handbook",
                    "url": "https://www.ux4g.gov.in/assets/img/pdf/UX4G-Handbook.pdf",
                },
                "practices": [],
            }
        with open(self._kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def query(self, user_query: str | None = None, limit: int = 10) -> dict[str, Any]:
        practices = self._kb.get("practices", [])
        query = (user_query or "").strip().lower()

        if not query:
            selected = practices[: max(1, limit)]
        else:
            scored: list[tuple[int, dict[str, Any]]] = []
            terms = [t for t in query.split() if t]
            for item in practices:
                text = " ".join(
                    [
                        item.get("topic", ""),
                        item.get("title", ""),
                        item.get("guidance", ""),
                        " ".join(item.get("keywords", [])),
                    ]
                ).lower()
                score = sum(1 for term in terms if term in text)
                if score > 0:
                    scored.append((score, item))

            scored.sort(key=lambda s: s[0], reverse=True)
            selected = [item for _, item in scored[: max(1, limit)]]

            if not selected:
                selected = practices[: min(5, len(practices))]

        return {
            "source": self._kb.get("source", {}),
            "query": user_query or "",
            "result_count": len(selected),
            "practices": selected,
        }
