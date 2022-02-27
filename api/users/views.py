from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.contrib import messages
from rest_framework import generics, permissions, response, status, views

from accounts.extensions import generate_otp, is_verified_otp, send_otp
from blog.models import User

from . import permissions as custom_permission
from .serializers import UserSerializer, CustomRegisterSerializer, OTPSerializer
from .messages import ViewMessages


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return response.Response({
            'message': ViewMessages.USER_REGISTERED_SUCCESSFULLY.value,
            'verify_url': request.build_absolute_uri(reverse('api-user:verify-user'))
        })


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          custom_permission.IsUserVerified, ]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          custom_permission.IsUserVerified,
                          custom_permission.IsSelfOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(cache_page(60*60), name='post')
class OTPVerifyUser(views.APIView):
    """Verify the user with OTP"""
    serializer_class = OTPSerializer

    def get(self, request, *args, **kwargs):
        """GET method will generate OTP for this user with their phone_number
        proccess:
            1. checking that user is not verified already
            2. generate OTP for user
            3. get the counter and remain_attmepts
            4. checking remain any attempts
            5. send the OTP for phone_number or email of user 
            6. leave a message to sending the password that has been sent
        """
        user = request.user
        if user.is_verified:
            return response.Response({
                'message': ViewMessages.ALREADY_VERIFIED_USER.value
            },
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = generate_otp(user)
        counter = cache.get('%s-counter' % user.phone_number, 0)
        remain_attmepts = cache.get('%s-remain' % user.phone_number, 0)

        if remain_attmepts >= 3:
            return response.Response({
                'message': ViewMessages.ATTEMPTS_HAS_BEEN_FINISHED.value
            },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        cache.set('%s-%s-otp' % (user.phone_number, counter), otp.at(counter))
        send_otp(
            otp=otp.at(counter),
            from_email='niceblog@gmail.com',
            user_phone_number=user.phone_number,
            user_email=user.email,
            verify_url=request.build_absolute_uri(
                reverse('api-user:verify-user'))
        )
        # print(cache.get('%s-%s-otp' % (user.phone_number, counter)), counter)

        return response.Response({
            'message': ViewMessages.OTP_SENT_SUCCESSFULLY.value
        })

    def post(self, request, *args, **kwargs):
        """ Post method will take the OTP from the user and validate that 
        if correct user will be verified otherwise if remained any attempts it will let user to send again """
        user = request.user
        if user.is_verified:
            return response.Response({
                'message': ViewMessages.ALREADY_VERIFIED_USER.value
            },
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = request.data.get('otp')
        if not otp:  # would be filled in POST dictionary :)
            otp = request.POST.get('otp')

        if not otp:
            return response.Response({
                'message': ViewMessages.OTP_IS_REQUIRED.value
            },
                status=status.HTTP_400_BAD_REQUEST,
            )
        counter = cache.get('%s-counter' % user.phone_number, 0)
        remain_attmepts = cache.get('%s-remain' % user.phone_number, 0)
        if remain_attmepts >= 3:
            return response.Response({
                'message': ViewMessages.ATTEMPTS_HAS_BEEN_FINISHED.value
            },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        if counter is not None:
            is_verified = is_verified_otp(user, otp, counter)
            if is_verified:
                user.is_verified = True
                user.save()
                text = ViewMessages.USER_VERIFIED.value
                messages.add_message(request, messages.SUCCESS, text)
                return redirect('accounts:profile')
            else:
                cache.set('%s-remain' % user.phone_number,
                          remain_attmepts+1)  # one more attempts
                return response.Response({
                    'message': ViewMessages.INVALID_OTP.value,
                    'remain_attmepts': 3 - cache.get('%s-remain' % user.phone_number)
                },
                    status=status.HTTP_200_OK,
                )
        return response.Response({
            'message': ViewMessages.SOMETHING_WENT_WRONG.value
        },
            status=status.HTTP_400_BAD_REQUEST,
        )
