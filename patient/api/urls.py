from .views import (RegistrationView,
                    CustomAuthToken,
                    PatientProfileView,
                    PatientHistoryView,
                    AppointmentViewPatient)
from django.urls import path

app_name = 'patient'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api_patient_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_patient_login'),
    path('profile/', PatientProfileView.as_view(), name='api_patient_profile'),
    path('history/', PatientHistoryView.as_view(), name='api_patient_history'),
    path('appointment/', AppointmentViewPatient.as_view(), name='api_patient_appointment'),

]
