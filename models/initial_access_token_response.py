from pydantic import BaseModel


class InitialAccessTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str

    def __repr__(self):
        return f"InitialAccessTokenResponse<access_token='{self.access_token}',\nexpires_in={self.expires_in},\nid_token='{self.id_token}',\nrefresh_token='{self.refresh_token}'>"

    def __str__(self):
        return f"InitialAccessTokenResponse<access_token='{self.access_token}',\nexpires_in={self.expires_in},\nid_token='{self.id_token}',\nrefresh_token='{self.refresh_token}'>"
