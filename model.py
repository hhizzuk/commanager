"""eecs497 models."""

from supabase import create_client, Client
from config import (SUPABASE_URL, SUPABASE_ANON_KEY,)
from uuid import uuid4

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

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

# def create_message(sender_id, receiver_id, message_content):
#     """Creates a new message in the 'messages' table."""
#     response = (
#         supabase.table("messages")
#         .insert(
#             {
#                 "sender_id": sender_id,
#                 "receiver_id": receiver_id,
#                 "content": message_content,
#                 "id": str(uuid4()),
#             }
#         )
#         .execute()
#     )
#     if response.error:
#         print(f"supabase error: {response.error}")
#     return response