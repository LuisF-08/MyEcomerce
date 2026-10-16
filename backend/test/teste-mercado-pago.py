from api.services.pagamento import criar_preferencia

r = criar_preferencia(
    itens=[{"id": 1, "titulo": "Produto teste", "quantidade": 1, "preco": 10.00}],
    external_reference="teste-1",
)
print(r)