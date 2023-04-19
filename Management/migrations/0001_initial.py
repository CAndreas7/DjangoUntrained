# Generated by Django 4.1.7 on 2023-04-19 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.IntegerField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=40)),
                ('courseDescription', models.CharField(max_length=140)),
                ('courseDepartment', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Supervisor'), (2, 'Instructor'), (3, 'TA')])),
            ],
        ),
        migrations.CreateModel(
            name='UsersToCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.user')),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('sectionID', models.IntegerField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=8)),
                ('startTime', models.CharField(max_length=7)),
                ('endTime', models.CharField(max_length=7)),
                ('capacity', models.IntegerField()),
                ('TA', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Management.user')),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.course')),
            ],
        ),
    ]
