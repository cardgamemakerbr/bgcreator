# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componente',
            name='tipo',
            field=models.CharField(choices=[('TATICO', 'Tático'), ('SORTE', 'Sorte'), ('LUDICO', 'Lúdico'), ('HABILIDADE', 'Habilidade')], default='TATICO', max_length=15),
        ),
    ]