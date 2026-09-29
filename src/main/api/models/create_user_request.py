from src.main.api.models.base_model import BaseModel
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule

class CreateUserRequest(BaseModel):
    username: str
    password: Annotated[str, CreationRule(regex=r"^[A-Z][0-9][a-z]{5}!$")]
    role: Annotated[str, CreationRule(regex=r"^ROLE_(USER)$")]