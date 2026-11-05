from django.db import models


class PagoRepartidor(models.Model):
	ESTADO_CHOICES = [
		("pendiente", "Pendiente"),
		("pagado", "Pagado"),
		("fallido", "Fallido"),
	]

	id_repartidor = models.PositiveIntegerField()
	monto_total_generado = models.DecimalField(max_digits=12, decimal_places=2)
	comision_plataforma = models.DecimalField(max_digits=12, decimal_places=2)
	monto_neto = models.DecimalField(max_digits=12, decimal_places=2)
	fecha_pago = models.DateTimeField(auto_now_add=True)
	estado = models.CharField(
		max_length=20,
		choices=ESTADO_CHOICES,
		default="pendiente",
	)

	def __str__(self):
		return f"Pago #{self.pk} del repartidor {self.id_repartidor}"


class SeguimientoGeolocalizacion(models.Model):
	id_repartidor = models.PositiveIntegerField()
	latitud = models.DecimalField(max_digits=9, decimal_places=6)
	longitud = models.DecimalField(max_digits=9, decimal_places=6)
	timestamp = models.DateTimeField(auto_now_add=True)
	velocidad = models.IntegerField()

	def __str__(self):
		return f"Seguimiento #{self.pk} del repartidor {self.id_repartidor}"


class TipoPago(models.Model):
	efectivo = models.DecimalField(
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
	)
	transferencia = models.DecimalField(
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
	)

	def __str__(self):
		return f"Tipo de pago #{self.pk}"


class PagoEntrega(models.Model):
	METODO_CHOICES = [
		("EFECTIVO", "Efectivo"),
		("TRANSFERENCIA", "Transferencia"),
		("OTRO", "Otro"),
	]
	ESTADO_CHOICES = [
		("PENDIENTE", "Pendiente"),
		("COMPLETADO", "Completado"),
		("CANCELADO", "Cancelado"),
	]

	tipo_de_pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE)
	valor_total = models.DecimalField(max_digits=12, decimal_places=2)
	metodo_pago = models.CharField(max_length=50, choices=METODO_CHOICES)
	evidencia_url = models.URLField(max_length=255, null=True, blank=True)
	fecha_de_pago = models.DateTimeField()
	estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)

	def __str__(self):
		return f"Pago de entrega #{self.pk} - {self.estado}"
