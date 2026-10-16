from django.db import models


class Pagamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        APROVADO = "aprovado", "Aprovado"
        RECUSADO = "recusado", "Recusado"
        CANCELADO = "cancelado", "Cancelado"
        ESTORNADO = "estornado", "Estornado"

    solicitacao = models.ForeignKey(
        "solicitacao.Solicitacao",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    preference_id = models.CharField(max_length=100, blank=True)
    # id do mercado pago
    mp_payment_id = models.CharField(
        max_length=50, unique=True, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDENTE
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Pagamento #{self.pk} | pedido {self.solicitacao_id} | {self.status}"