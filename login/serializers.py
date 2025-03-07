from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from login.models import User , Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','company', 'role']

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("not valid user")

        refresh = RefreshToken.for_user(user)

        return{
            'access': str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data

        }          
    
class ProfileSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source = 'user.email', read_only = True)
    user_company = serializers.CharField(source = 'user.company.name' , read_only = True)
    user_role = serializers.CharField(source = "role.name", read_only = True)

    class Meta:
        model = Profile
        fields = ["user_email", "user_company", "user_role", "created_at", "modified_at"]
