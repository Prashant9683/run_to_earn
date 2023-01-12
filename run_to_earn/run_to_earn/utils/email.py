import string
import random


def send_verification_email(
        userID: int,
        email: str,
        name: str,
):
    generate_pass = ''.join([random.choice(string.ascii_uppercase +
                                           string.ascii_lowercase +
                                           string.digits)
                             for n in range(8)])
    print(generate_pass)
    from user.models import VerificationOTP
    VerificationOTP.objects.create(user_id=userID, otp=generate_pass)
    return True
