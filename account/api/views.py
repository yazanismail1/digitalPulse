from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from account.api.serializers import CustomUserSerializer, UserProfileSerializer
from account.models import CustomUser, UserProfile
from custom.customClasses import CustomAPIView
from custom.functions import is_valid_email

# ---------- CustomUserView ---------- #
class SignupView(CustomAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    model = CustomUser.objects
    not_allowed_actions = ["get", "put"]
    
    def post(self, request):
        data = request.data
        data["username"] = data.get("username", None).lower() if data.get("username", None) else None

        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if get_user_model().objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if data.get("email", None):
                if is_valid_email(data.get("email")):
                    if UserProfile.objects.filter(email=data.get("email")).exists():
                        return Response({'detail': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
            
            password = serializer.validated_data['password']
            try:
                validate_password(password)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                user = get_user_model().objects.create(**serializer.validated_data)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(
                    user=user,
                    email = data.get('email', None)
                )

            return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
            new_password = request.data.get('password')
            try:
                validate_password(new_password)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.check_password(new_password):
                return Response({'detail': 'New password must be different from the previous password.'}, status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(new_password)
            request.user.save()

            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ---------- UserProfileView ---------- #
class UserProfileView(CustomAPIView):
    serializer_class = UserProfileSerializer
    model = UserProfile.objects
    not_allowed_actions = ["post", "put", "delete"]

    def get(self, request):
        try:
            user = request.user
            queryset = UserProfile.objects.get(user=user)
            serializer = self.serializer_class(queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            user = request.user
            print(user)
            data = request.data
            if data.get("email", None):
                if is_valid_email(data.get("email")):
                    if user.userProfile.email == data.get("email", None):
                        data.pop("email")
                    elif UserProfile.objects.filter(email=data.get("email")).exists():
                        return Response({'detail': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserProfileSerializer(data=data, instance=user.userProfile, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
