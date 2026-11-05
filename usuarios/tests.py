from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import PagoEntrega, PagoRepartidor, SeguimientoGeolocalizacion, TipoPago


class UsuariosPagesTests(TestCase):
	def test_operational_pages_extend_shared_layout(self):
		paths = [
			reverse("usuarios:login"),
			reverse("usuarios:registro"),
			reverse("usuarios:pagos_entrega"),
			reverse("usuarios:pagos_repartidor"),
			reverse("usuarios:seguimientos"),
		]

		for path in paths:
			with self.subTest(path=path):
				response = self.client.get(path)
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, 'class="site-header"')
				self.assertContains(response, 'class="site-sidebar"')
				self.assertContains(response, 'class="site-footer"')

	def test_list_gets_do_not_create_sample_records(self):
		self.client.get(reverse("usuarios:pagos_repartidor"))
		self.client.get(reverse("usuarios:seguimientos"))

		self.assertEqual(PagoRepartidor.objects.count(), 0)
		self.assertEqual(SeguimientoGeolocalizacion.objects.count(), 0)

	def test_detail_pages_use_shared_layout(self):
		pago = PagoRepartidor.objects.create(
			id_repartidor=3,
			monto_total_generado="100.00",
			comision_plataforma="10.00",
			monto_neto="90.00",
		)
		seguimiento = SeguimientoGeolocalizacion.objects.create(
			id_repartidor=3,
			latitud="4.711000",
			longitud="-74.072100",
			velocidad=20,
		)
		paths = [
			reverse("usuarios:detalle_pago_repartidor", args=[pago.pk]),
			reverse("usuarios:detalle_seguimiento", args=[seguimiento.pk]),
		]

		for path in paths:
			with self.subTest(path=path):
				response = self.client.get(path)
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, 'class="site-header"')

	def test_payment_forms_create_records(self):
		response = self.client.post(
			reverse("usuarios:pagos_entrega"),
			{
				"btn_tipo_pago": "1",
				"efectivo": "100.00",
				"transferencia": "",
			},
		)
		self.assertRedirects(response, reverse("usuarios:pagos_entrega"))
		tipo_pago = TipoPago.objects.get()

		response = self.client.post(
			reverse("usuarios:pagos_entrega"),
			{
				"btn_pago_entrega": "1",
				"tipo_de_pago": tipo_pago.pk,
				"valor_total": "80.00",
				"metodo_pago": "EFECTIVO",
				"evidencia_url": "",
				"fecha_de_pago": timezone.localtime().strftime("%Y-%m-%dT%H:%M"),
				"estado": "COMPLETADO",
			},
		)
		self.assertRedirects(response, reverse("usuarios:pagos_entrega"))
		self.assertEqual(PagoEntrega.objects.count(), 1)

	def test_repartidor_and_tracking_forms_create_records(self):
		response = self.client.post(
			reverse("usuarios:pagos_repartidor"),
			{
				"id_repartidor": "9",
				"monto_total_generado": "250.00",
				"comision_plataforma": "25.00",
				"monto_neto": "225.00",
				"estado": "pendiente",
			},
		)
		self.assertRedirects(response, reverse("usuarios:pagos_repartidor"))
		self.assertEqual(PagoRepartidor.objects.count(), 1)

		response = self.client.post(
			reverse("usuarios:seguimientos"),
			{
				"id_repartidor": "9",
				"latitud": "4.711000",
				"longitud": "-74.072100",
				"velocidad": "25",
			},
		)
		self.assertRedirects(response, reverse("usuarios:seguimientos"))
		self.assertEqual(SeguimientoGeolocalizacion.objects.count(), 1)

	def test_delete_views_require_post(self):
		pago = PagoRepartidor.objects.create(
			id_repartidor=3,
			monto_total_generado="100.00",
			comision_plataforma="10.00",
			monto_neto="90.00",
		)
		seguimiento = SeguimientoGeolocalizacion.objects.create(
			id_repartidor=3,
			latitud="4.711000",
			longitud="-74.072100",
			velocidad=20,
		)

		pago_delete = reverse("usuarios:eliminar_pago_repartidor", args=[pago.pk])
		seguimiento_delete = reverse(
			"usuarios:eliminar_seguimiento",
			args=[seguimiento.pk],
		)
		self.assertEqual(self.client.get(pago_delete).status_code, 405)
		self.assertEqual(self.client.get(seguimiento_delete).status_code, 405)
		self.assertTrue(PagoRepartidor.objects.filter(pk=pago.pk).exists())
		self.assertTrue(
			SeguimientoGeolocalizacion.objects.filter(pk=seguimiento.pk).exists()
		)

		self.assertRedirects(
			self.client.post(pago_delete),
			reverse("usuarios:pagos_repartidor"),
		)
		self.assertRedirects(
			self.client.post(seguimiento_delete),
			reverse("usuarios:seguimientos"),
		)
