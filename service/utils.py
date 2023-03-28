from fastapi import HTTPException, Security
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())


API_KEY = os.environ.get("APPLICATION_API_KEY","*uLRc*0Vj:v];zAjHVQp")
API_KEY_NAME = "access_token"

ADMIN_API_KEY = os.environ.get("APPLICATION_API_KEY_ADMIN")
ADMIN_API_KEY_NAME="admin_access_token"



api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


admin_api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
admin_api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
admin_api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

async def get_admin_api_key(
    api_key_query: str = Security(admin_api_key_query),
    api_key_header: str = Security(admin_api_key_header),
    api_key_cookie: str = Security(admin_api_key_cookie),
):

    if api_key_query == ADMIN_API_KEY:
        return api_key_query
    elif api_key_header == ADMIN_API_KEY:
        return api_key_header
    elif api_key_cookie == ADMIN_API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Only admin can access this endpoint"
        )