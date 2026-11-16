from django.core.exceptions import ValidationError


class PasswordRobustaValidator:
    def validate(self, password, user=None):
        if password is None or len(password) <= 8:
            raise ValidationError("La contraseña tiene que tener mas de 8 caracteres.")
        tiene_letra = any(c.isalpha() for c in password)
        tiene_numero = any(c.isdigit() for c in password)
        tiene_especial = any(not c.isalnum() for c in password)
        if not tiene_letra or not tiene_numero:
            raise ValidationError("Tiene que tener letras y numeros.")
        if not tiene_especial:
            raise ValidationError("Tiene que tener al menos un caracter especial.")

    def get_help_text(self):
        return "Mas de 8 caracteres, con letras, numeros y un caracter especial."
