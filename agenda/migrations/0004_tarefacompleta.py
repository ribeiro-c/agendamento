from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_update_whatsappenvio'),
    ]

    operations = [
        migrations.CreateModel(
            name='TarefaCompleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concluida', models.BooleanField(default=False)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.aluno')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.agendaevento')),
            ],
            options={
                'unique_together': {('aluno', 'evento')},
            },
        ),
    ]
