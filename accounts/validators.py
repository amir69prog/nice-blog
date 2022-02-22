from django.core.validators import RegexValidator

PhoneNumberValidator = RegexValidator(
    regex=r'^(0|\+98|0098)9[0-9]{9}$',
    message='Phone number is not correct',
    code='phone_number_validator'
)
