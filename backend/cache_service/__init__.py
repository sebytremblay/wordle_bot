"""
Cache service package for Wordle hint caching using Supabase.
"""

from .supabase_client import get_supabase_client
from .hint_cache import HintCache

__all__ = ['get_supabase_client', 'HintCache']
