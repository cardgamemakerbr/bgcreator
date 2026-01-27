from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Mecanica(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome

class Tema(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome

class Componente(models.Model):
    TIPOS_CHOICES = [
        ('TATICO', 'Tático'),
        ('SORTE', 'Sorte'),
        ('LUDICO', 'Lúdico'),
        ('HABILIDADE', 'Habilidade'),
        ('GERENCIAMENTO', 'Gerenciamento'),
        ('NEUTRO', 'Neutro')
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=15, choices=TIPOS_CHOICES, default='TATICO')
    
    def __str__(self):
        return self.nome

class Jogo(models.Model):
    IDADES_CHOICES = [
        (2, '2+'), (4, '4+'), (6, '6+'), (8, '8+'), (10, '10+'),
        (11, '11+'), (12, '12+'), (14, '14+'), (16, '16+'), (18, '18+')
    ]
    
    TEMPOS_CHOICES = [
        (5, '5 min'), (10, '10 min'), (15, '15 min'), (20, '20 min'),
        (25, '25 min'), (30, '30 min'), (35, '35 min'), (40, '40 min'),
        (45, '45 min'), (50, '50 min'), (60, '60 min'), (80, '80 min'),
        (100, '100 min'), (120, '120 min'), (140, '140 min'), (180, '180 min'),
        (200, '200 min'), (240, '240 min'), (300, '300 min'), (360, '360 min')
    ]
    
    nome = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True)
    descricao_curta = models.TextField()
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    
    jogadores_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    jogadores_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    tempo_min = models.IntegerField(choices=TEMPOS_CHOICES)
    tempo_max = models.IntegerField(choices=TEMPOS_CHOICES)
    idade_recomendada = models.IntegerField(choices=IDADES_CHOICES)
    peso = models.FloatField(default=0.1, editable=False)
    
    mecanicas = models.ManyToManyField(Mecanica, blank=True)
    temas = models.ManyToManyField(Tema, blank=True)
    componentes = models.ManyToManyField(Componente, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calcular_peso(self):
        peso = 0.1
        
        # Peso por tempo (0.1 a cada 30min, máx 1.0)
        tempo_medio = (self.tempo_min + self.tempo_max) / 2
        peso_tempo = min((tempo_medio // 30) * 0.1, 1.0)
        peso += peso_tempo
        
        # Peso por mecânicas (0.1 cada, máx 1.0)
        peso_mecanicas = min(self.mecanicas.count() * 0.1, 1.0)
        peso += peso_mecanicas
        
        # Peso por componentes (0.1 cada, máx 1.0)
        peso_componentes = min(self.componentes.count() * 0.1, 1.0)
        peso += peso_componentes
        
        # Peso por condições de vitória (0.1 cada, máx 0.3)
        peso_vitorias = min(self.condicoesvitoria_set.count() * 0.1, 0.3)
        peso += peso_vitorias
        
        # Peso por condições de derrota (0.1 cada, máx 0.3)
        peso_derrotas = min(self.condicoesderrota_set.count() * 0.1, 0.3)
        peso += peso_derrotas
        
        # Peso por estruturas (0.1 cada, máx 1.0)
        peso_estruturas = min(self.estruturajogo_set.count() * 0.1, 1.0)
        peso += peso_estruturas
        
        # Peso por condições especiais (0.1 cada, máx 0.5)
        total_especiais = sum(e.condicoesespeciais_set.count() for e in self.estruturajogo_set.all())
        peso_especiais = min(total_especiais * 0.1, 0.5)
        peso += peso_especiais
        
        return round(peso, 1)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.peso = self.calcular_peso()
        super().save(update_fields=['peso'])
    
    def __str__(self):
        return self.nome

class CondicoesVitoria(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    descricao = models.TextField()
    
    def __str__(self):
        return f"{self.jogo.nome} - Vitória"

class CondicoesDerrota(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    descricao = models.TextField()
    
    def __str__(self):
        return f"{self.jogo.nome} - Derrota"

class SetupJogo(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ordem = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['ordem']
    
    def __str__(self):
        return f"{self.jogo.nome} - Setup: {self.nome}"

class SetupImagem(models.Model):
    setup = models.ForeignKey(SetupJogo, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='setup/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.setup.nome} - {self.descricao}"

class EstruturaJogo(models.Model):
    TIPOS_CHOICES = [
        ('FASE', 'Fase'),
        ('ACAO', 'Ação'),
        ('RODADA', 'Rodada')
    ]
    
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES)
    ordem = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['ordem']
    
    def __str__(self):
        return f"{self.jogo.nome} - {self.nome}"

class CondicoesEspeciais(models.Model):
    estrutura = models.ForeignKey(EstruturaJogo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    
    def __str__(self):
        return f"{self.estrutura.nome} - {self.nome}"

class Glossario(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    palavra = models.CharField(max_length=100)
    definicao = models.TextField()
    imagem = models.ImageField(upload_to='glossario/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.jogo.nome} - {self.palavra}"

class ComentarioJogo(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    comentario = models.TextField()
    avaliacao = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.jogo.nome} - {self.usuario} ({self.avaliacao}★)"