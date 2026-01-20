from rest_framework import serializers
from .models import Jogo, Mecanica, Tema, Componente, CondicoesVitoria, CondicoesDerrota, EstruturaJogo, CondicoesEspeciais, Glossario

class MecanicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecanica
        fields = '__all__'

class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = '__all__'

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'

class CondicoesVitoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicoesVitoria
        fields = '__all__'

class CondicoesDerrotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicoesDerrota
        fields = '__all__'

class CondicoesEspeciaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicoesEspeciais
        fields = '__all__'

class EstruturaJogoSerializer(serializers.ModelSerializer):
    condicoes_especiais = CondicoesEspeciaisSerializer(source='condicoesespeciais_set', many=True, read_only=True)
    
    class Meta:
        model = EstruturaJogo
        fields = '__all__'

class GlossarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossario
        fields = '__all__'

class JogoSerializer(serializers.ModelSerializer):
    mecanicas = MecanicaSerializer(many=True, read_only=True)
    temas = TemaSerializer(many=True, read_only=True)
    componentes = ComponenteSerializer(many=True, read_only=True)
    condicoes_vitoria = CondicoesVitoriaSerializer(source='condicoesvitoria_set', many=True, read_only=True)
    condicoes_derrota = CondicoesDerrotaSerializer(source='condicoesderrota_set', many=True, read_only=True)
    estruturas = EstruturaJogoSerializer(source='estruturajogo_set', many=True, read_only=True)
    glossario = GlossarioSerializer(source='glossario_set', many=True, read_only=True)
    
    class Meta:
        model = Jogo
        fields = '__all__'

class JogoCreateSerializer(serializers.ModelSerializer):
    mecanicas_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    temas_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    componentes_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    
    class Meta:
        model = Jogo
        fields = ['nome', 'subtitulo', 'descricao_curta', 'capa', 'jogadores_min', 
                 'jogadores_max', 'tempo_min', 'tempo_max', 'idade_recomendada',
                 'mecanicas_ids', 'temas_ids', 'componentes_ids']
    
    def create(self, validated_data):
        mecanicas_ids = validated_data.pop('mecanicas_ids', [])
        temas_ids = validated_data.pop('temas_ids', [])
        componentes_ids = validated_data.pop('componentes_ids', [])
        
        jogo = Jogo.objects.create(**validated_data)
        
        if mecanicas_ids:
            jogo.mecanicas.set(mecanicas_ids)
        if temas_ids:
            jogo.temas.set(temas_ids)
        if componentes_ids:
            jogo.componentes.set(componentes_ids)
            
        return jogo