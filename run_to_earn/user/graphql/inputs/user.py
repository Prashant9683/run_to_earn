import strawberry
from typing import Optional


@strawberry.input
class ProfileInput:
    first_name: str
    last_name: str
    phone_number: Optional[str] = None