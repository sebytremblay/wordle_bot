"""
Hint caching service implementation using Supabase.
"""

import json
import hashlib
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass

from .supabase_client import get_supabase_client, SupabaseConnectionError


@dataclass
class CacheEntry:
    """Data class representing a cache entry."""
    hint: str
    solver_type: str


class HintCacheError(Exception):
    """Base exception for hint cache errors."""
    pass


class HintCache:
    """Service for caching and retrieving Wordle game hints."""

    @staticmethod
    def _generate_state_hash(game_state: Dict[str, Any]) -> str:
        """
        Generate a deterministic hash for a game state.

        Args:
            game_state: Dictionary containing game state information

        Returns:
            str: SHA-256 hash of the canonicalized game state
        """
        # Create a canonical representation of the game state
        # Sort dictionary keys to ensure consistent ordering
        canonical_state = json.dumps(game_state['history'], sort_keys=True)
        return hashlib.sha256(canonical_state.encode()).hexdigest()

    @staticmethod
    def get_cached_hint(game_state: Dict[str, Any], solver_type: str) -> Optional[CacheEntry]:
        """
        Retrieve a cached hint for the given game state and solver type.

        Args:
            game_state: Current game state dictionary
            solver_type: Type of solver used (e.g., 'naive', 'greedy', 'mcts')

        Returns:
            Optional[CacheEntry]: Cache entry if found, None otherwise

        Raises:
            HintCacheError: If there's an error accessing the cache
        """
        try:
            client = get_supabase_client()
            state_hash = HintCache._generate_state_hash(game_state)

            response = (client.table('hint_cache')
                        .select('hint, solver_type')
                        .eq('game_state_hash', state_hash)
                        .eq('solver_type', solver_type)
                        .limit(1)
                        .execute())

            if response.data and len(response.data) > 0:
                entry = response.data[0]
                return CacheEntry(
                    hint=entry['hint'],
                    solver_type=entry['solver_type']
                )
            return None

        except Exception as e:
            raise HintCacheError(f"Failed to retrieve cached hint: {str(e)}")

    @staticmethod
    def cache_hint(game_state: Dict[str, Any], hint: str, solver_type: str) -> None:
        """
        Cache a hint for the given game state and solver type.

        Args:
            game_state: Current game state dictionary
            hint: The computed hint to cache
            solver_type: Type of solver used

        Raises:
            HintCacheError: If there's an error storing the hint
        """
        try:
            client = get_supabase_client()
            state_hash = HintCache._generate_state_hash(game_state)

            # Prepare cache entry with only the fields in our schema
            cache_data = {
                'game_state_hash': state_hash,
                'solver_type': solver_type,
                'hint': hint
                # created_at will be handled by the database default value
            }

            # Upsert the cache entry based on composite primary key
            client.table('hint_cache').upsert(
                cache_data,
                on_conflict='game_state_hash,solver_type'  # Specify composite key columns
            ).execute()

        except Exception as e:
            raise HintCacheError(f"Failed to cache hint: {str(e)}")

    @staticmethod
    def get_or_compute_hint(
        game_state: Dict[str, Any],
        solver_type: str,
        compute_fn: callable
    ) -> Tuple[str, bool]:
        """
        Get a cached hint or compute and cache a new one.

        Args:
            game_state: Current game state dictionary
            solver_type: Type of solver to use
            compute_fn: Function to compute a new hint if not cached

        Returns:
            Tuple[str, bool]: (hint, was_cached)

        Raises:
            HintCacheError: If there's an error with the cache operations
        """
        try:
            # Try to get cached hint
            cached = HintCache.get_cached_hint(game_state, solver_type)
            if cached:
                return cached.hint, True

            # Compute new hint
            hint = compute_fn()

            # Cache the new hint
            HintCache.cache_hint(game_state, hint, solver_type)

            return hint, False

        except Exception as e:
            raise HintCacheError(f"Failed to get or compute hint: {str(e)}")
