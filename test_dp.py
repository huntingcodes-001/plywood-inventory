import os
import sys

# Temporarily add backend config path to load .env
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

from supabase import create_client, Client
from config import settings


def test_connection():
    # These values are loaded from your .env file via settings
    url = settings.supabase_url
    key = settings.supabase_service_key

    print(f"--- Testing Supabase Connection ---")
    print(f"URL: {url}")
    print(f"Key Prefix: {key[:10]}...")

    try:
        # Attempt to create the client
        client: Client = create_client(url, key)

        # Attempt a simple query to confirm connectivity
        result = client.rpc('version').execute()

        if result:
            print("\n✅ CONNECTION SUCCESSFUL!")
            print(f"Database response received: {result}")
        else:
            print("\n❌ CONNECTION FAILED: Query returned no data.")

    except Exception as e:
        print("\n❌ CONNECTION FAILED: An exception occurred during client creation or connection.")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    test_connection()
