from typing import Optional
import strawberry
from user.graphql.types.user import UserType
from user.models import User


@strawberry.type
class UserQueries:

    @strawberry.field
    def user(self, id: int) -> Optional[UserType]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None