import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

SHOP_ID = os.getenv("SHOP_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DOMAIN = os.getenv("DOMAIN")

REDIRECT_URI = f"https://{DOMAIN}/callback"
LOGOUT_URL = f"https://{DOMAIN}/logout"
SCOPE = quote("openid email https://api.customers.com/auth/customer.graphql")

def get_shop_id():
    return SHOP_ID

def get_domain():
    return DOMAIN

def get_client_id():
    return CLIENT_ID

def get_client_secret():
    return CLIENT_SECRET

def get_redirect_uri():
    return REDIRECT_URI

def get_logout_url():
    return LOGOUT_URL

def get_scope():
    return SCOPE
