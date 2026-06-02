import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    def validate(self, password, user=None):
        erros = []

        if not re.search(f'[A-Z]', password):
            erros.append(_("A senha deve conter letras maiúsculas."))
        
        if not re.search(r'[a-z]', password):
            erros.append(_("A senha deve conter letras minúsculas."))

        if not re.search(r'\d', password):
            erros.append(_("A senha deve conter pelo menos um número."))
    
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            erros.append(_("A senha deve conter pelo menos um caractere especial."))

        if erros:
            raise ValidationError(erros)

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos 8 caracteres, incluindo letras "
            "maiúsculas, minúsculas, números e caracteres especiais."
        )