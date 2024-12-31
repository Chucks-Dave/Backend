from django.shortcuts import render
from .serializers import GraduateRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .otp import generate_otp, send_otp_email
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class GraduateCreateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = GraduateRegistrationSerializer(data=request.data)
        if serializer.is_valid():

            gradauate = serializer.save()
            # print("***************************hahahahahah|", gradauate)
            user = gradauate.user
            otp = generate_otp()
            user.otp = otp
            user.is_verified = False
            user.save()
            send_otp_email(user.email, otp)
            print("hahahahahahah*************|", user)
            refresh = RefreshToken.for_user(user)

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Build a response payload that combines
            # the serialized graduate data with the tokens
            data = {
                'message': 'User registered successfully. OTP sent to your email.',
                'graduate': serializer.data,  # or any representation you prefer
                'access': access_token,
                'refresh': refresh_token,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        if not email or not otp_entered:
            return Response({'detail': 'Missing email or otp'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            user = CustomUser.objects.get(email=email, otp=otp_entered)
            user.is_verified = True
            user.otp = None
            user.save()

            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
