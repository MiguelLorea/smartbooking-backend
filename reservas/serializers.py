from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from reservas.models import Reserva, Usuario


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "password", "first_name", "last_name"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, datos):
        password = datos.pop("password")
        user = Usuario(**datos)
        user.rol = Usuario.USUARIO
        user.set_password(password)
        user.save()
        return user


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "first_name", "last_name", "rol"]
        read_only_fields = ["id", "username", "rol"]


class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "motivo",
            "usuario",
            "usuario_nombre",
            "creada",
        ]
        read_only_fields = ["usuario", "creada"]

    def validate(self, datos):
        fecha = datos.get("fecha", getattr(self.instance, "fecha", None))
        inicio = datos.get("hora_inicio", getattr(self.instance, "hora_inicio", None))
        fin = datos.get("hora_fin", getattr(self.instance, "hora_fin", None))

        if inicio >= fin:
            raise serializers.ValidationError(
                {"hora_fin": ["La hora de fin tiene que ser posterior a la de inicio."]}
            )

        cuando = datetime.combine(fecha, inicio)
        cuando = timezone.make_aware(cuando, timezone.get_current_timezone())
        if cuando < timezone.now():
            raise serializers.ValidationError(
                {"fecha": ["No se puede reservar en una fecha u horario pasado."]}
            )

        otras = Reserva.objects.filter(fecha=fecha)
        if self.instance is not None and self.instance.pk:
            otras = otras.exclude(pk=self.instance.pk)
        for otra in otras:
            if inicio < otra.hora_fin and fin > otra.hora_inicio:
                raise serializers.ValidationError(
                    {"hora_inicio": ["Ya hay una reserva en esa franja horaria."]}
                )
        return datos


class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "first_name", "last_name", "rol", "is_active"]
        read_only_fields = ["id", "username", "email", "first_name", "last_name"]
