from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs["username"] = attrs.get("username", None).lower() if attrs.get("username", None) else None
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["id"] = self.user.id

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer