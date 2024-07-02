from supabase import Client, create_client
from dotenv import load_dotenv
import os

class SupabaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        load_dotenv()
        api_url: str = os.getenv('SUPABASE_URL')
        key: str = os.getenv('SUPABASE_KEY')
        self.client: Client = create_client(api_url, key)

    def get_client(self):
        return self.client

# Usage
def get_supabase_client():
    return SupabaseClient().get_client()