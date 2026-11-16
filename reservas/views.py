import logging

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reservas.models import Reserva, Usuario
from reservas.permissions import EsAdmin, EsDuenioOAdmin
from reservas.serializers import (
    PerfilSerializer,
    RegistroSerializer,
    ReservaSerializer,
    UsuarioAdminSerializer,
)

logger = logging.getLogger("seguridad")


class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        login = str(request.data.get("username", "")).strip()
        password = str(request.data.get("password", ""))
        user = Usuario.objects.filter(username=login).first()
        if user is None:
            user = Usuario.objects.filter(email=login).first()

        if user is None or not user.is_active or not user.check_password(password):
            logger.warning(
                "login fallido usuario=%s accion=login recurso=auth resultado=fallido",
                login,
            )
            return Response(
                {"detail": "Usuario o contraseña incorrectos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "rol": user.rol,
                "username": user.username,
                "id": user.id,
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Falta el refresh."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({"detail": "Refresh invalido."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(PerfilSerializer(request.user).data)

    def put(self, request):
        serializer = PerfilSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, EsDuenioOAdmin]

    def get_queryset(self):
        if self.request.user.rol == "admin":
            return Reserva.objects.all()
        return Reserva.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioAdminSerializer
    permission_classes = [EsAdmin]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Usuario.objects.all().order_by("username")

    def partial_update(self, request, *args, **kwargs):
        usuario = self.get_object()
        if usuario.id == request.user.id and request.data.get("is_active") is False:
            return Response(
                {"detail": "No podes desactivarte a vos mismo."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        respuesta = super().partial_update(request, *args, **kwargs)
        if respuesta.status_code < 400:
            logger.info(
                "cambio admin usuario=%s accion=patch recurso=usuario:%s resultado=ok campos=%s",
                request.user.username,
                usuario.id,
                ",".join(sorted(request.data.keys())),
            )
        return respuesta
