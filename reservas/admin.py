from django.contrib import admin

from reservas.models import Reserva, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "rol", "is_active")
    list_filter = ("rol", "is_active")


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "hora_inicio", "hora_fin", "motivo")
    list_filter = ("fecha",)
