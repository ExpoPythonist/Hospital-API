# Generated by Django 3.0.3 on 2024-04-30 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.DecimalField(decimal_places=1, max_digits=4)),
                ('address', models.TextField()),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admit_date', models.DateField(auto_now_add=True, verbose_name='Admit Date')),
                ('symptoms', models.TextField()),
                ('department', models.CharField(choices=[('CL', 'Cardiologist'), ('DL', 'Dermatologist'), ('EMC', 'Emergency Medicine Specialist'), ('IL', 'Immunologist'), ('AL', 'Anesthesiologist'), ('CRS', 'Colon and Rectal Surgeon')], default='CL', max_length=3)),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Release Date')),
                ('assigned_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_charge', models.PositiveIntegerField(verbose_name='Room charge')),
                ('medicine_cost', models.PositiveIntegerField(verbose_name='Medicine cost')),
                ('doctor_fee', models.PositiveIntegerField(verbose_name='Doctor Fee')),
                ('other_charge', models.PositiveIntegerField(verbose_name='Other charges')),
                ('patient_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='patient.History')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(verbose_name='Appointment date')),
                ('appointment_time', models.TimeField(verbose_name='Appointement time')),
                ('status', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_appointments', to='doctor.Doctor')),
                ('patient_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointments', to='patient.History')),
            ],
        ),
    ]