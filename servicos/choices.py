from django.db.models import TextChoices

class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_VALVULA_MOTOR = 'TVM', 'Trocar valvula de motor'
    TROCAR_OLEO_MOTOR = 'TO', 'Trocar de óleo'
    BALANCEAMENTO = 'BAL', 'Balanceamento'
    ALINHAMENTO = 'ALI', 'Alinhamento'