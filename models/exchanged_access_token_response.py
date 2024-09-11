from pydantic import BaseModel


class ExchangedAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    issued_token_type: str

    def __repr__(self):
        return f"ExchangedAccessTokenResponse<access_token='{self.access_token}', token_type='{self.token_type}', expires_in='{self.expires_in}', scope='{self.scope}'>"
