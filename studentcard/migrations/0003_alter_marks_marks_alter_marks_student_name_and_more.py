# Generated by Django 5.0.6 on 2024-06-19 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentcard', '0002_subject_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='marks',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='marks',
            name='student_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='StudentName', to='studentcard.student'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='subject_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjectName', to='studentcard.subject'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dept', to='studentcard.department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='stu_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentId', to='studentcard.student_id'),
        ),
        migrations.AlterField(
            model_name='student_id',
            name='student_id',
            field=models.CharField(default=None, max_length=20),
        ),
    ]