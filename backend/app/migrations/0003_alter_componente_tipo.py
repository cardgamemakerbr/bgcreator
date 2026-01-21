# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_componente_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componente',
            name='tipo',
            field=models.CharField(choices=[('TATICO', 'Tático'), ('SORTE', 'Sorte'), ('LUDICO', 'Lúdico'), ('HABILIDADE', 'Habilidade'), ('GERENCIAMENTO', 'Gerenciamento'), ('NEUTRO', 'Neutro')], default='TATICO', max_length=15),
        ),
    ]