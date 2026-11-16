from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ADMIN = "admin"
    USUARIO = "usuario"
    ROLES = (
        (ADMIN, "Administrador"),
        (USUARIO, "Usuario"),
    )

    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default=USUARIO)

    def __str__(self):
        return self.username


class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora_inicio"]

    def __str__(self):
        return f"{self.fecha} {self.hora_inicio}-{self.hora_fin}"
