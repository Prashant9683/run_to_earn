from typing import Optional
import strawberry
from users.graphql.types.user import UserType
from users.models import User


@strawberry.type
class UserQueries:

    @strawberry.field
    def user(self, id: int) -> Optional[UserType]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None