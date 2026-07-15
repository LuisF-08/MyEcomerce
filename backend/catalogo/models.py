from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField( upload_to="categorias/",
    blank=True,
    null=True)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)    
    
    def __str__(self):
        return self.nome    
    
class Produto(models.Model):

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0) 
    categoria = models.ForeignKey("Categoria",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="produtos")
    imagem_1 = models.ImageField( upload_to="loja/produtos/",
    blank=True,
    null=True,
    )
    variacoes = models.JSONField(
    default=list,
    blank=True
    )
    imagem_2 = models.ImageField( upload_to="loja/produtos/",
    blank=True,
    null=True,
    )
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    