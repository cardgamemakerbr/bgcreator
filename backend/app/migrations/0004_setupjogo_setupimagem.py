# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_componente_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetupJogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('ordem', models.IntegerField(default=1)),
                ('jogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.jogo')),
            ],
            options={
                'ordering': ['ordem'],
            },
        ),
        migrations.CreateModel(
            name='SetupImagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='setup/')),
                ('setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.setupjogo')),
            ],
        ),
    ]