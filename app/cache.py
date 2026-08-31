
from langsmith._openapi_client.types import run_select_field
import hashlib
import time
from typing import Optional

class ResponseCache:
    """
    In-memory response cache with TTL (time-to-live).
    
    In production, replace this with Redis for:
    - Persistence across multiple instances
    - Shared cache across multiple instances
    - Built-in TTL management
    """

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._cache: dict[str, dict] = {}
        self._hits = 0
        self._misses = 0

    def _make_key(self, query: str) -> str:
        """Create a cache key from the normalized query."""
        normalized = query.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()

    def get(self, query: str) -> Optional [str]:
        """Get cached response if it exists and hasn't expired.
        Returns None on cache miss.
        """
        key = self._make_key(query)
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                self._hits += 1
                return entry["response"]
            else:
                # Entry expired, remove it
                del self._cache[key]
        self._misses += 1
        return None

    @property
    def stats(self) -> dict:
        """Cache performance statistics."""
        total = self.hits + self._misses
        hit_rate = self.hits / total if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.1%}",
            "cached_entries": len(self._cache),
        }