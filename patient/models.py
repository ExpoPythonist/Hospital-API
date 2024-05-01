from django.db import models
from account.models import User
from doctor.models import Doctor


class Patient(models.Model):
    age = models.DecimalField(max_digits=4, decimal_places=1)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.username


class History(models.Model):
    DEPARTMENT_CHOICES = [
        ('CL', 'Cardiologist'),
        ("DL", 'Dermatologist'),
        ("EMC", 'Emergency Medicine Specialist'),
        ("IL", 'Immunologist'),
        ("AL", 'Anesthesiologist'),
        ("CRS", 'Colon and Rectal Surgeon')
    ]

    admit_date = models.DateField(verbose_name="Admit Date", auto_now=False, auto_now_add=True)
    symptoms = models.TextField()
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, default="CL")
    release_date = models.DateField(verbose_name="Release Date", auto_now=False, auto_now_add=False, null=True,
                                    blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.get_name


class Appointment(models.Model):
    appointment_date = models.DateField(verbose_name="Appointment date", auto_now=False, auto_now_add=False)
    appointment_time = models.TimeField(verbose_name="Appointement time", auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)
    # related_name fix reverse relationship field name with patient_history model
    patient_history = models.ForeignKey(History, related_name='patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='doctor_appointments', null=True, on_delete=models.SET_NULL)

    @property
    def patient_name(self):
        self.patient_history.patient.get_name

    def __str__(self):
        return self.patient_history.patient.get_name + '-' + self.doctor.get_name


class Cost(models.Model):
    room_charge = models.PositiveIntegerField(verbose_name="Room charge", null=False)
    medicine_cost = models.PositiveIntegerField(verbose_name="Medicine cost", null=False)
    doctor_fee = models.PositiveIntegerField(verbose_name="Doctor Fee", null=False)
    other_charge = models.PositiveIntegerField(verbose_name="Other charges", null=False)
    patient_details = models.OneToOneField(History, related_name='costs', on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return "{} tk".format(self.room_charge + self.medicine_cost + self.doctor_fee + self.other_charge)

    def __str__(self):
        return self.patient_details.patient.get_name + '-' + str(self.patient_details.admit_date)
