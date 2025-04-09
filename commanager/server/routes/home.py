# from flask import Flask, render_template
# from supabase import create_client
# import config

# app = Flask(__name__)

# # Set up Supabase client
# supabase = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

# @app.route('/')
# def home():
#     # Query the "users" table from Supabase
#     response = supabase.table("users").select("*").execute()
#     users = response.data  # this will be a list of dicts
#     return render_template("home.html", users=users)

# if __name__ == '__main__':
#     app.run(debug=True)