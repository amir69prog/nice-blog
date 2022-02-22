from enum import Enum


class ViewMessages(Enum):
    USER_REGISTERED_SUCCESSFULLY = 'You have been registered successfully. Please verify your phone'
    OTP_SENT_SUCCESSFULLY = 'The OTP has been sent successfully. please check your email or phone then send it to us.'
    ALREADY_VERIFIED_USER = 'Your account is already verified.'
    OTP_IS_REQUIRED = 'The otp field must be filled.'
    USER_VERIFIED = 'Your account has been verified successfully.'
    ATTEMPTS_HAS_BEEN_FINISHED = 'Your allowed attempts are over. Please come back in an hour'
    SOMETHING_WENT_WRONG = 'Something went wrong!'
    INVALID_OTP = 'Your OTP is not valid. Please try again.'
    USER_IS_NOT_VERIFIED = 'Your account is not verified.'
