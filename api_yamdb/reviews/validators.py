from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValueError(f'Год выпуска не может быть больше {current_year}.')
    if value < 0:
        raise ValueError('Год выпуска не может быть отрицательным.')