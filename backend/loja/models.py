from django.db import models

class DiasTrabalho(models.TextChoices):
    SEGUNDA_A_SEXTA = 'S', 'segunda à sexta'
    SEGUNDA_A_SABADO = 'SS', 'segunda à sábado'
    

class Loja(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to="loja/logos",
    null=True,
    blank=True)
    banner_1 = models.ImageField( upload_to="loja/banner/",
    blank=True,
    null=True,
    )
    banner_2 = models.ImageField( upload_to="loja/banner/",
    blank=True,
    null=True,
    )
    banner_3 = models.ImageField( upload_to="loja/banner/",
    blank=True,
    null=True,
    )
    banner_4 = models.ImageField( upload_to="loja/banner/",
    blank=True,
    null=True,
    )
    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    pix = models.CharField(
    max_length=120,
    blank=True
    )
    cpf = models.CharField(max_length=14)
    cnpj = models.CharField(
        max_length=18,
        blank=True
    )
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    referencia = models.CharField(
    max_length=200,
    blank=True
    )
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cor_primaria = models.CharField(max_length=7)
    cor_secundaria = models.CharField(max_length=7)
    mensagem_whatsapp = models.TextField(
    default="Olá! Gostaria de fazer um pedido."
    )
    horario_funcionamento = models.TimeField()
    horario_fechamento = models.TimeField()
    dias_funcionamento = models.CharField(
    max_length=2,
    choices=DiasTrabalho.choices,
    default=DiasTrabalho.SEGUNDA_A_SEXTA,
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
    unique=True
    )

    def __str__(self):
        return f"{self.nome} - {self.descricao}"