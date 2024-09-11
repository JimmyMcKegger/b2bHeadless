from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import base64
import secrets
import httpx
from models import InitialAccessTokenResponse, ExchangedAccessTokenResponse
from .dependencies import (
    get_redirect_uri,
    get_shop_id,
    get_domain,
    get_scope,
    get_client_secret,
    get_client_id,
    get_logout_url,
)

from dotenv import load_dotenv

load_dotenv()

SHOP_ID = get_shop_id()
CLIENT_ID = get_client_id()
CLIENT_SECRET = get_client_secret()
DOMAIN = get_domain()
REDIRECT_URI = get_redirect_uri()
LOGOUT_URL = get_logout_url()
SCOPE = get_scope()
TOKEN_URL = f"https://shopify.com/{SHOP_ID}/auth/oauth/token"
CUSTOMER_API_URL = f"https://shopify.com/{SHOP_ID}/account/customer/api/2024-07/graphql"

credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
ENCODED_CREDENTIALS = base64.b64encode(credentials.encode()).decode()
TOKEN_EXHANGE_HEADERS = {
    "Authorization": f"Basic {ENCODED_CREDENTIALS}",
    "Content-Type": "application/x-www-form-urlencoded",
}

templates = Jinja2Templates(directory="./templates")

router = APIRouter()


@router.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/login")


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    authorization_url = (
        f"https://shopify.com/{SHOP_ID}/auth/oauth/authorize?"
        f"scope={SCOPE}&"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"state={state}&"
        f"nonce={nonce}&"
        f"ui_locales=en"
    )

    response = templates.TemplateResponse(
        "index.html", {"request": request, "auth_url": authorization_url}
    )
    response.set_cookie(key="myCookie", value="yabbadabbadoo")
    return response


@router.get("/callback", response_class=JSONResponse)
async def callback(request: Request):
    try:
        params = request.query_params
        code = params.get("code", None)
        print(f"CODE: {code}")

        # Obtain initial access token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": CLIENT_ID,
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                },
                headers=TOKEN_EXHANGE_HEADERS,
            )
            INITIAL_ACCESS_TOKEN = InitialAccessTokenResponse(**response.json())

            print("INITIAL ACCESS TOKEN RESPONSE:", INITIAL_ACCESS_TOKEN)

        # Exchange access token to use it
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "code": "ODh3WlJtNDJWYmpkcVhKRmtqbWRGMW5wY2xqQlcvTU9XUnhSZzZwL1NPUW9QVURBbzdoSEljaVhDa3U2Y2ZheEVSTlNmYjU4cUdSc2N0eHVZL1FtSSs2WW1SVVo5MnUvc3JJNENmMmJJbnJTejBkUEtDZzQ1ZVdpRjRNak11ZDUzcWlkM0h1MWVFYmxMejlLMXlZM2VxM0JCSUtha2QrTDFXMWlWcTRtRXd1TlYwZUJqRXVsU2M5VjN2NDVZbU5aUFdlMWQ3WEJzcUdmNGVwUWJoZEJZQnJPQmMvczJSOTJWL3VjVk1xSGdmTDZVUE5nWVJ4MWdHa0NyblhqQjhSTkszcExhNlZ2Q01pMGVaRzM0Nk1ubGd0TFRvT1ZPMnpzeno2TEJ6dVZScFNQVnlidTBXWHNLN1dYVmVXS0V2RnRTTTRIeDdEN2R4UDBHZz09LS1tUU4wSFI0THZEWXBBbkc0LS1oeGdyVUtZL2JEaWJYRkdkc2ZpMGh3PT0",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "audience": "30243aa5-17c1-465a-8493-944bcc4e88aa",
            "subject_token": INITIAL_ACCESS_TOKEN.access_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "scopes": "openid email https://api.customers.com/auth/customer.graphql",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL, headers=TOKEN_EXHANGE_HEADERS, data=data
            )

        if response.status_code == 200:
            EXCHANGED_ACCESS_TOKEN = ExchangedAccessTokenResponse(**response.json())
            print("EXCHANGED ACCESS TOKEN RESPONSE:", EXCHANGED_ACCESS_TOKEN)
        else:
            print("Error:", response.status_code, response.text)

        # set cookies
        tokens = {
            "id_token": INITIAL_ACCESS_TOKEN.id_token,
            "access_token": EXCHANGED_ACCESS_TOKEN.access_token,
            "refresh_token": INITIAL_ACCESS_TOKEN.refresh_token,
        }

        response = RedirectResponse(url="/account")

        for key, value in tokens.items():
            response.set_cookie(key=key, value=value, path="/")

        return response

    except Exception as e:
        print(f"An error occurred: {e}")

        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "details": str(e)},
        )


@router.get("/account")
async def account(request: Request):
    access_token = request.cookies.get("access_token")
    print("account page access Token: ", access_token)
    if not access_token:
        return {"error": "No access token found. User may not be logged in."}

    query = """
    {
    shop {
        id
    }
    customer{
        id
        emailAddress{
            emailAddress
        }
        creationDate
        displayName
        firstName
        tags
        }
    }
    """


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{access_token}",
    }
    print(f"API URL: {CUSTOMER_API_URL}")
    print("Headers:", headers)

    async with httpx.AsyncClient() as client:
        response = await client.post(CUSTOMER_API_URL, json={"query": query}, headers=headers)
        account_info = response.json()

    print("Account Info:", account_info)
    if "errors" in account_info:
        return {
            "error": "Failed to fetch account info",
            "details": account_info["errors"],
        }

    return templates.TemplateResponse(
        "account.html", {"request": request, "account_info": account_info}
    )


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    id_token = request.cookies.get("id_token")
    if not id_token:
        return RedirectResponse(url="/logout/confirmation")

    logout_url = (
        f"https://shopify.com/{SHOP_ID}/auth/logout?id_token_hint={id_token}&"
        f"post_logout_redirect_uri=https://{DOMAIN}/logout/confirmation"
    )

    response = RedirectResponse(url=logout_url)
    response.delete_cookie(key="id_token")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return response


@router.get("/logout/confirmation", response_class=HTMLResponse)
async def logout_confirmation(request: Request):
    return "<h1>You have been logged out successfully.</h1><br><button onclick=\"window.location.href='/login'\">Log Back In</button>"
