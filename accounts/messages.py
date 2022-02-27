from enum import Enum


class UserMessage(Enum):
    PHONE_NUMBER_HELP_TEXT = 'Please enter your phone number as a following template\n\
use one of these: [09120000000 | +9891200000000 | 00989120000000]'
    PROFILE_UPDATED_SUCCESSFULLY = 'Your account has been updated successfully.'
    
