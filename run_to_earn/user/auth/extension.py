import jwt
from strawberry.extensions import Extension
from strawberry.types import ExecutionContext

from user.auth import auth_settings


class JWTExtension(Extension):

    def __init__(self, execution_context: ExecutionContext):
        super().__init__(execution_context=execution_context)
        self.userID = None
        self.request = None
        self.response = None
        self.issueNewTokens = False
        self.revokeTokens = False

    def get_token_payload(self, tokenName):
        try:
            return jwt.decode(
                jwt=self.request.COOKIES[tokenName],
                key=auth_settings.SECRET_KEY,
                algorithms=["HS256"],  # todo: 1.make this dynamic 2. add nfb and leeway
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def validate_access_token(self):
        if 'JWT_ACCESS_TOKEN' in self.request.COOKIES and self.request.COOKIES['JWT_ACCESS_TOKEN']:
            tokenPayload = self.get_token_payload(tokenName="JWT_ACCESS_TOKEN")
            if tokenPayload and 'userID' in tokenPayload:
                self.userID = tokenPayload['userID']
                return True
            return False

    def validate_refresh_token(self):
        if 'JWT_REFRESH_TOKEN' in self.request.COOKIES and self.request.COOKIES['JWT_REFRESH_TOKEN']:
            token_payload = self.get_token_payload(tokenName="JWT_REFRESH_TOKEN")
            if token_payload and token_payload is not None:
                try:
                    from user.models import RefreshTokens
                    refreshTokenObj = RefreshTokens.objects.get(refreshToken=self.request.COOKIES['JWT_REFRESH_TOKEN'])
                    # refreshTokenObj = RefreshTokens.objects.get(refreshToken=token_payload["refreshToken"])
                    print("refreshTokenObj", refreshTokenObj)
                    if refreshTokenObj:
                        self.userID = refreshTokenObj.user.id
                        return True
                except RefreshTokens.DoesNotExist:
                    print("refreshTokenObj does not exist")
                    pass
            print("refresh token invalid !!!!!!!!!!!!")
            self.revokeTokens = True
            return False

    def on_request_start(self):
        self.request = self.execution_context.context["request"]
        print("on_request_start", self.request.COOKIES)
        if self.validate_access_token():
            pass
        elif self.validate_refresh_token():
            print("refresh token validated")
            self.issueNewTokens = True

    def resolve(self, _next, root, info, *args, **kwargs):
        setattr(info.context, "userID", self.userID)
        if self.issueNewTokens:
            print(self.userID)
            setattr(info.context.request, "issueNewTokens", self.issueNewTokens)
            setattr(info.context.request, "clientID", self.userID)
        if self.revokeTokens:
            print("revokeTokens")
            setattr(info.context.request, "revokeTokens", self.revokeTokens)
        return _next(root, info, **kwargs)
