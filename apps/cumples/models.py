from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def clean(self):
        # Validar la cantidad de días en función del mes seleccionado
        max_dias = 31  # Por defecto, 31 días
        if self.mes_cumpleaños == 4 or self.mes_cumpleaños == 6 or self.mes_cumpleaños == 9 or self.mes_cumpleaños == 11:
            max_dias = 30  # Meses con 30 días
        elif self.mes_cumpleaños == 2:
            max_dias = 29  # Febrero (asumiendo 29 días por defecto)

        if self.dia_cumpleaños < 1 or self.dia_cumpleaños > max_dias:
            raise ValidationError("El día seleccionado no es válido para el mes.")

@receiver(pre_save, sender=Cumpleañero)
def validate_cumpleaños(sender, instance, **kwargs):
    if not (1 <= instance.dia_cumpleaños <= 31 and 1 <= instance.mes_cumpleaños <= 12):
        raise ValidationError("El día y el mes deben ser válidos.")

@receiver(pre_delete, sender=Cumpleañero)
def delete_cumpleañero_image(sender, instance, **kwargs):
    # Elimina la imagen asociada al objeto Cumpleañero al eliminar el objeto
    if instance.foto:
        instance.foto.delete(save=False)
