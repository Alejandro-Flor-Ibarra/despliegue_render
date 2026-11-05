from django.db import models


class Resultado(models.Model):
    operacion = models.CharField("operación", max_length=100)
    resultado = models.FloatField("resultado")
    fecha = models.DateTimeField("fecha", auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "resultado de cálculo"
        verbose_name_plural = "resultados de cálculo"

    def __str__(self):
        return f"{self.operacion} = {self.resultado}"