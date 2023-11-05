from django.db import models



class Cumpleañero (models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='cumpleañeros/', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    class Meta:
        verbose_name = 'Cumpleañero'
        verbose_name_plural = 'Cumpleañeros'
        db_table = 'cumples'
        ordering = ['fecha_nacimiento']

