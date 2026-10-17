from decimal import Decimal
from django.db import transaction
from api.services.pagamento import consultar_pagamento
from pagamento.models import Pagamento
from solicitacao.models import Solicitacao, StatusSolicitacao


class PagamentoInvalido(Exception):
    pass


#  status do Mercado Pago -> status do nosso model
STATUS_MP = {
    "approved": Pagamento.Status.APROVADO,
    "pending": Pagamento.Status.PENDENTE,
    "in_process": Pagamento.Status.PENDENTE,
    "authorized": Pagamento.Status.PENDENTE,
    "rejected": Pagamento.Status.RECUSADO,
    "cancelled": Pagamento.Status.CANCELADO,
    "refunded": Pagamento.Status.ESTORNADO,
    "charged_back": Pagamento.Status.ESTORNADO,
}


@transaction.atomic
def conciliar_pagamento(payment_id):
    dados = consultar_pagamento(payment_id)

    # external_reference foi o id da Solicitacao que manda ao criar o link
    try:
        solicitacao = Solicitacao.objects.select_for_update().get(
            pk=dados.get("external_reference")
        )
    except (Solicitacao.DoesNotExist, ValueError, TypeError):
        raise PagamentoInvalido("Pedido não encontrado para este pagamento.")

    # Defesa extra: o valor pago tem que ser o valor exato do pedido
    # O Python pode gerar imprecisões bizarras. É por isso que passamos a string
    # lida perfeitamente e com 100% de precisão quando recebe uma string que representa o número
    if Decimal(str(dados["transaction_amount"])) != solicitacao.total:
        raise PagamentoInvalido("Valor pago não bate com o valor do pedido.")

    novo_status = STATUS_MP.get(dados["status"], Pagamento.Status.PENDENTE)

    # Reaproveita o registro: 
    # ou já tem este payment_id, ou é a tentativa
    # pendente mais recente deste pedido 
    pagamento = (
        Pagamento.objects.select_for_update().filter(mp_payment_id=str(payment_id)).first()
        or 
        Pagamento.objects.select_for_update().filter(solicitacao=solicitacao, mp_payment_id__isnull=True)
        .order_by("-criado_em")
        .first()
        or
        Pagamento(solicitacao=solicitacao, valor=solicitacao.total)
    )
    pagamento.mp_payment_id = str(payment_id)
    pagamento.status = novo_status
    pagamento.save()

    # Só libera o pedido se estava aguardando e foi aprovado
    if (
        novo_status == Pagamento.Status.APROVADO
        and solicitacao.status == StatusSolicitacao.AGUARDANDO_PAGAMENTO
    ):
        solicitacao.status = StatusSolicitacao.NOVO
        solicitacao.save(update_fields=["status"])

    return pagamento