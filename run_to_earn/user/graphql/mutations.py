import strawberry

from run_to_earn.utils.email import send_verification_email
from user.graphql.inputs.user import ProfileInput


@strawberry.type
class UserMutations:

    @strawberry.mutation
    def signup(self, info, password: str, email: str, profile: ProfileInput) -> int:
        from user.models import User
        import re

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not regex.match(email):
            raise Exception('Invalid Email')

        user = User(
            email=email,
            first_name=profile.first_name,
            last_name=profile.last_name
        )
        username = email.split("@")[0]
        user.username = username
        user.set_password(password)
        user.save()

        if not send_verification_email(user.id, email, profile.first_name):
            user.delete()
            raise Exception("Unable to send verification email")

        return True

    @strawberry.mutation
    def verify_email(self, info, email: str, otp: str) -> bool:
        from user.models import VerificationOTP
        try:
            otp = VerificationOTP.objects.get(user__email=email, otp=otp)
        except VerificationOTP.DoesNotExist:
            raise Exception("Invalid OTP")
        user = otp.user
        user.isVerified = True
        user.save()
        otp.delete()
        return True

    @strawberry.mutation
    def login(self, info, email: str, password: str) -> bool:
        from django.contrib.auth import authenticate
        user = authenticate(email=email, password=password)
        if user is None:
            raise Exception("Invalid credentials")
        if not user.isVerified:
            raise Exception("Email not verified")
        setattr(info.context, "userID", user.id)
        setattr(info.context.request, "issueNewTokens", True)
        setattr(info.context.request, "clientID", user.id)
        return True

    @strawberry.mutation
    def logout(self, info) -> bool:
        setattr(info.context.request, "revokeTokens", True)
        return True


__all__ = ["UserMutations"]
