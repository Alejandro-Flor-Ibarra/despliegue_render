from django.db import models


class Resultado(models.Model):
    operacion = models.CharField(max_length=100)
    resultado = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.operacion} = {self.resultado}"