from pydantic import BaseModel


class Config(BaseModel):
    admin_as_group_admin: bool = False

    class Config:
        extra = "ignore"
