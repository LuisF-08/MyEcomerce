from django.db import models
from catalogo.models import Produto

class StatusSolicitacao(models.TextChoices):
    NOVO = "NOV", "Novo"
    VISTO = "VIS", "Visto"
    CONCLUIDO = "CON", "Concluído"
    CANCELADO = "CAN", "Cancelado"


class Solicitacao(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    cep = models.CharField(max_length=9, blank=True)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    referencia = models.CharField(
        max_length=200,
        blank=True
    )
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    observacao = models.TextField(
        blank=True
    )
    # Campo 'produtos' removido por redundância
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    mensagem = models.TextField(blank=True) # Ajustado para aceitar em branco (pode ser gerado via API)
    status = models.CharField(
        max_length=3,
        choices=StatusSolicitacao.choices,
        default=StatusSolicitacao.NOVO
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"] # Ordena da solicitação mais recente para a mais antiga

    def __str__(self):
        return f"{self.nome} - {self.get_status_display()}"
    
    
class ItemSolicitacao(models.Model):
    solicitacao = models.ForeignKey(
        "Solicitacao",
        on_delete=models.CASCADE,
        related_name="itens"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="itens_solicitados"
    )
    produto_nome = models.CharField(max_length=120)
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    variacao = models.CharField(
    max_length=20,
    blank=True
)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"] 

    def __str__(self):
        return f"{self.produto_nome} ({self.quantidade})"