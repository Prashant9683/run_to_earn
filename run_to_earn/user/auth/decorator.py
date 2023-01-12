from functools import wraps


def login_required(resolver):
    @wraps(resolver)
    def wrapper(parent, info, *args, **kwargs):
        userID = getattr(info.context, "userID", None)
        if userID is not None:
            return resolver(parent, info, *args, **kwargs)
        return None
    return wrapper


def admin_required(resolver):
    @wraps(resolver)
    def wrapper(parent, info, *args, **kwargs):
        try:
            from users.models import User
            user = User.objects.get(id=info.context.userID)
            if user.role == "admin":
                return resolver(parent, info, *args, **kwargs)
        except User.DoesNotExist:
            pass
        return None
    return wrapper
