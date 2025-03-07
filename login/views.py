from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import LoginSerializer , ProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch logged-in user's profile."""
        user = request.user

        # ✅ Ensure the user has a profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        # ✅ Serialize profile correctly
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)