import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserUpdateSerializer
from .models import User

logger = logging.getLogger(__name__)


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer


class GoogleAuthView(APIView):
    """
    Exchange a Google OAuth2 access token for SOIE JWT tokens.
    No authentication required — this IS the login endpoint.
    """
    permission_classes = [AllowAny]           # ← CRITICAL FIX
    authentication_classes = []               # ← skip JWT check entirely

    def post(self, request):
        import requests as req

        access_token = request.data.get("access_token")
        if not access_token:
            return Response(
                {"status": 400, "message": "Google access token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify token with Google's userinfo endpoint
        try:
            google_resp = req.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
        except req.exceptions.RequestException:
            return Response(
                {"status": 503, "message": "Could not reach Google. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if google_resp.status_code != 200:
            return Response(
                {"status": 401, "message": "Invalid Google token. Please sign in with Google again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        google_data = google_resp.json()
        email = google_data.get("email")

        if not email:
            return Response(
                {"status": 400, "message": "Google did not provide an email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": google_data.get("given_name", ""),
                "last_name":  google_data.get("family_name", ""),
                "is_active":  True,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()
            try:
                from apps.accounts.tasks import send_welcome_email
                send_welcome_email.delay(str(user.id))
            except Exception as e:
                logger.warning(f"Could not queue welcome email: {e}")

        refresh = RefreshToken.for_user(user)
        return Response({
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
            "user":    UserSerializer(user).data,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"status": 400, "message": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": 200, "message": "Logged out successfully."})
        except Exception:
            return Response(
                {"status": 400, "message": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )