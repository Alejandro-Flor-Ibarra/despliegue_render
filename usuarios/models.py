from django.db import models


class PagoRepartidor(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("fallido", "Fallido"),
    ]

    id_repartidor = models.PositiveIntegerField("ID del repartidor")
    monto_total_generado = models.DecimalField(
        "monto total generado", max_digits=12, decimal_places=2
    )
    comision_plataforma = models.DecimalField(
        "comisión de la plataforma", max_digits=12, decimal_places=2
    )
    monto_neto = models.DecimalField("monto neto", max_digits=12, decimal_places=2)
    fecha_pago = models.DateTimeField("fecha de pago", auto_now_add=True)
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=ESTADO_CHOICES,
        default="pendiente",
    )

    class Meta:
        verbose_name = "pago a repartidor"
        verbose_name_plural = "pagos a repartidores"

    def __str__(self):
        return f"Pago #{self.pk} del repartidor {self.id_repartidor}"


class SeguimientoGeolocalizacion(models.Model):
    id_repartidor = models.PositiveIntegerField("ID del repartidor")
    latitud = models.DecimalField("latitud", max_digits=9, decimal_places=6)
    longitud = models.DecimalField("longitud", max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField("fecha y hora", auto_now_add=True)
    velocidad = models.IntegerField("velocidad")

    class Meta:
        verbose_name = "seguimiento de geolocalización"
        verbose_name_plural = "seguimientos de geolocalización"

    def __str__(self):
        return f"Seguimiento #{self.pk} del repartidor {self.id_repartidor}"




class PagoEntrega(models.Model):
    METODO_CHOICES = [
        ("EFECTIVO", "Efectivo"),
        ("TRANSFERENCIA", "Transferencia"),
    ]
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("COMPLETADO", "Completado"),
        ("CANCELADO", "Cancelado"),
    ]

    valor_total = models.DecimalField(
        "valor recibido", max_digits=12, decimal_places=2
    )
    metodo_pago = models.CharField(
        "método de pago", max_length=50, choices=METODO_CHOICES
    )
    evidencia_url = models.URLField(
        "URL de la evidencia", max_length=255, null=True, blank=True
    )
    fecha_de_pago = models.DateTimeField("fecha de pago")
    estado = models.CharField("estado", max_length=50, choices=ESTADO_CHOICES)

    class Meta:
        verbose_name = "pago de entrega"
        verbose_name_plural = "pagos de entrega"

    def __str__(self):
        return f"Pago de entrega #{self.pk} - {self.estado}"