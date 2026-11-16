from datetime import date, time, timedelta

from django.core.management.base import BaseCommand

from reservas.models import Reserva, Usuario


class Command(BaseCommand):
    help = "Crea el admin y un usuario de prueba"

    def handle(self, *args, **options):
        admin, creado = Usuario.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@smartbooking.local",
                "rol": Usuario.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Admin",
                "last_name": "Demo",
            },
        )
        if creado:
            admin.set_password("Admin123!")
            admin.save()

        usuario, creado = Usuario.objects.get_or_create(
            username="usuario",
            defaults={
                "email": "usuario@smartbooking.local",
                "rol": Usuario.USUARIO,
                "first_name": "Juan",
                "last_name": "Perez",
            },
        )
        if creado:
            usuario.set_password("Usuario123!")
            usuario.save()

        if not Reserva.objects.filter(usuario=usuario).exists():
            dia = date.today() + timedelta(days=2)
            Reserva.objects.create(
                usuario=usuario,
                fecha=dia,
                hora_inicio=time(10, 0),
                hora_fin=time(11, 0),
                motivo="reunion de prueba",
            )

        self.stdout.write("usuarios de prueba listos")
