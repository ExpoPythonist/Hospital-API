from django.contrib import admin
from .models import Patient, History, Appointment, Cost

# Register your models here.

# admin.site.register(Patient)
# admin.site.register(History)
admin.site.register(Appointment)
admin.site.register(Cost)


class PatientCost(admin.TabularInline):
    model = Cost


class PatientAppointment(admin.TabularInline):
    model = Appointment


class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assigned_doctor', 'admit_date', 'department', 'release_date')
    inlines = [PatientAppointment, PatientCost]


admin.site.register(History, PatientHistoryAdmin)


class PatientHistoryInline(admin.StackedInline):
    model = History


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'address', 'mobile')
    inlines = [PatientHistoryInline]


admin.site.register(Patient, PatientAdmin)
