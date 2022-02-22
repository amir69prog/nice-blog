from datetime import datetime
import base64

from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.core.mail import send_mail

from .models import CustomUser

import pyotp


def generate_key(phone: str) -> str:
    """ Generate key for crating an hash """
    return phone + str(datetime.now().timestamp()) + get_random_string(30)


def generate_otp(user: CustomUser) -> str:
    """ Genrate OTP password for users """
    key = base64.b32encode(generate_key(user.phone_number).encode())
    OTP = pyotp.HOTP(key)
    return OTP


def is_verified_otp(user: CustomUser, otp, counter):
    """ Checking the user counter chached OTP with password has been sending """
    cached_otp = cache.get('%s-%s-otp' % (user.phone_number, counter))
    print(cached_otp)
    if otp == cached_otp:
        return True
    return False


def send_otp(otp: int, from_email: str = None, user_phone_number: str = None, user_email: str = None, verify_url: str = None) -> bool:
    """ Send OTPassword to the user_phone_number or user_email """
    try:
        if user_email:
            subject = 'OTP from Niceblog website'
            message = '''The OTP has been sent to you\nKey: %(otp)s\nplease send this key at %(verify_url)s url\n\nThanks to join us :)'''
            from_email = from_email
            recipient_list = [user_email, ]

            send_mail(
                subject=subject,
                message=message % {'otp': otp, 'verify_url': verify_url},
                from_email=from_email,
                recipient_list=recipient_list
            )

        elif user_phone_number:
            print('OTP has been sent to %s phone number' % user_phone_number)
    except Exception as err:
        print(str(err))
        return False
    else:
        return True
