# Generated manually

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_setupjogo_setupimagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioJogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('comentario', models.TextField()),
                ('avaliacao', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('jogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.jogo')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]