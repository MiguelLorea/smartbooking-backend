from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from reservas.views import (
    LoginView,
    LogoutView,
    PerfilView,
    RegistroView,
    ReservaViewSet,
    UsuarioViewSet,
)

router = DefaultRouter()
router.register("reservas", ReservaViewSet, basename="reservas")
router.register("usuarios", UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path("auth/register/", RegistroView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("perfil/", PerfilView.as_view()),
    path("", include(router.urls)),
]
