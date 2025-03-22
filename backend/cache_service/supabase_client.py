"""
Supabase client configuration and management.
"""

import os
from typing import Optional
from functools import lru_cache
from supabase import create_client, Client
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()


class SupabaseConnectionError(Exception):
    """Raised when there are issues connecting to Supabase."""
    pass


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Get or create a Supabase client instance.
    Uses lru_cache to maintain a single instance throughout the application.

    Returns:
        Client: Configured Supabase client instance

    Raises:
        SupabaseConnectionError: If required environment variables are missing or connection fails
    """
    url: Optional[str] = os.getenv('SUPABASE_URL')
    key: Optional[str] = os.getenv('SUPABASE_KEY')

    if not url or not key:
        raise SupabaseConnectionError(
            "Missing required Supabase configuration. "
            "Please ensure SUPABASE_URL and SUPABASE_KEY are set in your .env file."
        )

    try:
        return create_client(url, key)
    except Exception as e:
        raise SupabaseConnectionError(
            f"Failed to initialize Supabase client: {str(e)}")


def verify_table_exists() -> bool:
    """
    Verify that the hint_cache table exists in the Supabase database.

    Returns:
        bool: True if table exists and is accessible

    Raises:
        SupabaseConnectionError: If table verification fails
    """
    try:
        client = get_supabase_client()
        # Attempt to query the table
        client.table('hint_cache').select('id').limit(1).execute()
        return True
    except Exception as e:
        raise SupabaseConnectionError(
            f"Failed to verify hint_cache table: {str(e)}")
