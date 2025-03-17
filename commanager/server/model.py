"""commanager model database."""

from supabase import create_client, Client
from commanager.config import (SUPABASE_URL, SUPABASE_ANON_KEY,)
from uuid import uuid4


def get_db():
    """Open a new database connection.
    """
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Supabase URL and Key must be set as environment variables.")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    return supabase

# def get_user_by_id(user_id):
#     """Retrieves a user from the Supabase 'users' table by ID."""
#     response = supabase.table("users").select("*").eq("id", user_id).execute()
#     if response.error:
#         print(f"Supabase error: {response.error}")
#         return None
#     if response.data:
#         return response.data[0]
#     return None

# def create_commission(artist_id, client_id, description, price, drive_folder_id, paypal_order_id):
#     """Creates a new commission in the Supabase 'commissions' table."""
#     response = (
#         supabase.table("commissions")
#         .insert(
#             {
#                 "artist_id": artist_id,
#                 "client_id": client_id,
#                 "description": description,
#                 "price": price,
#                 "drive_folder_id": drive_folder_id,
#                 "paypal_order_id": paypal_order_id,
#                 "status": "pending",
#                 "id": str(uuid4()), # Creates unique id
#             }
#         )
#         .execute()
#     )
#     if response.error:
#         print(f"supabase error: {response.error}")
#     return response
