from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_delete


class Cumpleañero(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    dia_cumpleaños = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(31)])
    mes_cumpleaños = models.PositiveIntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])
    foto = models.ImageField(upload_to='media/cumpleañeros/', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        verbose_name = 'Cumpleañero'
        verbose_name_plural = 'Cumpleañeros'
        db_table = 'cumples'
        ordering = ['mes_cumpleaños', 'dia_cumpleaños']


@receiver(pre_save, sender=Cumpleañero)
def validate_cumpleaños(sender, instance, **kwargs):
    if not (1 <= instance.dia_cumpleaños <= 31 and 1 <= instance.mes_cumpleaños <= 12):
        raise ValidationError("El día y el mes deben ser válidos.")

@receiver(pre_delete, sender=Cumpleañero)
def delete_cumpleañero_image(sender, instance, **kwargs):
    # Elimina la imagen asociada al objeto Cumpleañero al eliminar el objeto
    if instance.foto:
        instance.foto.delete(save=False)