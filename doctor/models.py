from django.db import models
from account.models import User


class Doctor(models.Model):
    DEPARTMENT_CHOICES = [
        ('CL', 'Cardiologist'),
        ('DL', 'Dermatologists'),
        ('EMC', 'Emergency Medicine Specialists'),
        ('IL', 'Immunologists'),
        ('AL', 'Anesthesiologists'),
        ('CRS', 'Colon and Rectal Surgeons'),
    ]

    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, default='CL')
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
        return "{} ({})".format(self.user.first_name, self.department)
