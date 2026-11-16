from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from reservas.models import Reserva, Usuario


class ApiTests(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="Admin123!",
            rol="admin",
        )
        self.juan = Usuario.objects.create_user(
            username="juan",
            email="juan@test.com",
            password="Usuario123!",
            rol="usuario",
        )
        self.ana = Usuario.objects.create_user(
            username="ana",
            email="ana@test.com",
            password="Usuario123!",
            rol="usuario",
        )
        cuando = timezone.localtime() + timedelta(days=3)
        self.reserva = Reserva.objects.create(
            usuario=self.juan,
            fecha=cuando.date(),
            hora_inicio=cuando.time().replace(minute=0, second=0, microsecond=0),
            hora_fin=(cuando + timedelta(hours=1)).time().replace(second=0, microsecond=0),
            motivo="clase",
        )

    def _reserva(self, hora_inicio, hora_fin, dias=4):
        cuando = timezone.localtime() + timedelta(days=dias)
        return {
            "fecha": str(cuando.date()),
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "motivo": "practica",
        }

    def test_password_debil(self):
        resp = self.client.post(
            "/api/auth/register/",
            {
                "username": "nuevo",
                "email": "nuevo@test.com",
                "password": "12345678",
                "first_name": "A",
                "last_name": "B",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_login_y_sin_token(self):
        mal = self.client.post(
            "/api/auth/login/",
            {"username": "juan", "password": "no-es-esta"},
            format="json",
        )
        self.assertEqual(mal.status_code, 401)

        ok = self.client.post(
            "/api/auth/login/",
            {"username": "juan", "password": "Usuario123!"},
            format="json",
        )
        self.assertEqual(ok.status_code, 200)
        self.assertIn("access", ok.data)

        sin = self.client.get("/api/reservas/")
        self.assertEqual(sin.status_code, 401)

    def test_no_ve_reserva_ajena(self):
        self.client.force_authenticate(self.ana)
        resp = self.client.get(f"/api/reservas/{self.reserva.id}/")
        self.assertEqual(resp.status_code, 404)

        lista = self.client.get("/api/reservas/")
        ids = [item["id"] for item in lista.data]
        self.assertNotIn(self.reserva.id, ids)

    def test_usuario_no_administra(self):
        self.client.force_authenticate(self.juan)
        resp = self.client.get("/api/usuarios/")
        self.assertEqual(resp.status_code, 403)

    def test_solape_y_hora_fin(self):
        self.client.force_authenticate(self.ana)
        mal_hora = self.client.post(
            "/api/reservas/",
            self._reserva("15:00", "14:00"),
            format="json",
        )
        self.assertEqual(mal_hora.status_code, 400)

        self.client.force_authenticate(self.juan)
        primera = self.client.post(
            "/api/reservas/",
            self._reserva("18:00", "19:00", dias=5),
            format="json",
        )
        self.assertEqual(primera.status_code, 201)

        self.client.force_authenticate(self.ana)
        solape = self.client.post(
            "/api/reservas/",
            self._reserva("18:30", "19:30", dias=5),
            format="json",
        )
        self.assertEqual(solape.status_code, 400)

    def test_log_sin_password(self):
        self.client.post(
            "/api/auth/login/",
            {"username": "juan", "password": "clave-mala-XYZ!"},
            format="json",
        )
        from django.conf import settings

        texto = (settings.BASE_DIR / "logs" / "seguridad.log").read_text()
        self.assertNotIn("clave-mala-XYZ!", texto)
        self.assertIn("login fallido", texto)
