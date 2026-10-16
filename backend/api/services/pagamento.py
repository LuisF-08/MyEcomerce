import mercadopago
from django.conf import settings


class ErroMercadoPago(Exception):
    pass


def _sdk():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


def criar_preferencia(*, itens, external_reference):
    """
    itens: lista de dicts {"id", "titulo", "quantidade", "preco"}
    external_reference: id da sua Solicitacao (liga o pagamento ao pedido)
    Retorna: {"preference_id": ..., "init_point": ...}
    """
    base = settings.FRONTEND_URL
    corpo = {
        "items": [
            {
                "id": str(i["id"]),
                "title": i["titulo"],
                "quantity": int(i["quantidade"]),
                "unit_price": float(i["preco"]),
                "currency_id": "BRL",
            }
            for i in itens
        ],
        "external_reference": str(external_reference),
        "back_urls": {
            "success": f"{base}/pagamento/retorno",
            "failure": f"{base}/pagamento/retorno",
            "pending": f"{base}/pagamento/retorno",
        },
        "auto_return": "approved",
    }

    resposta = _sdk().preference().create(corpo)
    if resposta["status"] not in (200, 201):
        raise ErroMercadoPago(resposta.get("response"))

    dados = resposta["response"]
    return {"preference_id": dados["id"], "init_point": dados["init_point"]}


def consultar_pagamento(payment_id):
    # Pergunta ao Mercado Pago o estado real de um pagamento
    resposta = _sdk().payment().get(payment_id)
    if resposta["status"] != 200:
        raise ErroMercadoPago(resposta.get("response"))
    return resposta["response"]