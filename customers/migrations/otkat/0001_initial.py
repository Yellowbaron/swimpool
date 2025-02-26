# Generated by Django 3.0.1 on 2019-12-23 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Couch',
            fields=[
                ('couchID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('custID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('address', models.TextField(blank=True, null=True)),
                ('doctorCert', models.CharField(max_length=255, verbose_name='Врач')),
                ('certExpiration', models.DateField(verbose_name='Срок справки')),
                ('category', models.CharField(choices=[('H', 'Оздоровительное плавание'), ('D', 'Группы инвалидов'), ('L', 'Обучение плаванию'), ('S', 'Группы спортивного плавания'), ('M', 'Группы от предприятий'), ('G', 'Группы по программам поддержки Правительства')], default=None, max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schID', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField(verbose_name='Время и дата')),
                ('end', models.DateTimeField(verbose_name='Время и дата')),
                ('counter', models.IntegerField(verbose_name='Количество')),
                ('category', models.CharField(choices=[('H', 'Оздоровительное плавание'), ('D', 'Группы инвалидов'), ('L', 'Обучение плаванию'), ('S', 'Группы спортивного плавания'), ('M', 'Группы от предприятий'), ('G', 'Группы по программам поддержки Правительства')], default=None, max_length=1, null=True)),
                ('duty', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='customers.Couch')),
            ],
        ),
    ]
