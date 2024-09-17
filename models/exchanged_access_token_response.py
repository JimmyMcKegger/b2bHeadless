from typing import Optional
from pydantic import BaseModel


class ExchangedAccessTokenResponse(BaseModel):
    access_token: str
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    issued_token_type: Optional[str] = None

    def __repr__(self):
        return f"ExchangedAccessTokenResponse<access_token='{self.access_token}', token_type='{self.token_type}', expires_in='{self.expires_in}', scope='{self.scope}'>"
