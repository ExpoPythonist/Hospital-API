from django.contrib import admin
from .models import Doctor
from patient.models import Appointment


# Register your models here.

class DoctorAppointment(admin.TabularInline):
    model = Appointment


# hospital-admin.site.register()

class doctorAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'department', 'address', 'mobile', 'user']
    inlines = [DoctorAppointment]


admin.site.register(Doctor, doctorAdmin)
