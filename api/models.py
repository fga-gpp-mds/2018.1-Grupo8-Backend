from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
UF_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)

EDUCATION_CHOICES = (
    ('EFC', 'Ensino Fundamental Completo'),
    ('EFI', 'Ensino Fundamental Incompleto'),
    ('EMC', 'Ensino Médio Completo'),
    ('EMI', 'Ensino Médio Incompleto'),
    ('ESC', 'Ensino Superior Completo'),
    ('ESI', 'Ensino Superior Incompleto'),
    ('PG', 'Pós-Graduação'),
    ('ME', 'Mestrado'),
    ('DO', 'Doutorado'),
    ('PD', 'Pós-Doutorado')
)


class CustomUser(User):
    def save(self, **kwargs):  # pylint: disable=arguments-differ
        super(CustomUser, self).save(**kwargs)
        if (SocialInformation.objects.filter(owner=self).
            count() == 0):
            social = SocialInformation(owner=self)
            social.save()


class SocialInformation(models.Model):

    owner = models.OneToOneField(
        CustomUser,
        related_name='social_information',
        on_delete=models.CASCADE
    )
    federal_unit = models.CharField(max_length=150, choices=UF_CHOICES, default='AC')
    city = models.CharField(max_length=150, blank=True)
    income = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    education = models.CharField(
        max_length=150, choices=EDUCATION_CHOICES, default='EFC'
    )
    job = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(default=datetime.date.today)
