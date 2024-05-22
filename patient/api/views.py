from .serializers import (PatientRegistrationSerializer,
                          PatientProfileSerializer,
                          PatientHistorySerializer,
                          AppointmentPatientSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from patient.models import Patient, History, Appointment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """custom Permission class for Patient"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='patient').exists())


class CustomAuthToken(ObtainAuthToken):
    """This class returns custom Authentication token only for patient"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='patient').exists()
        if not user.status:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif not account_approval:
            return Response(
                {
                    'message': "You are not authorized to login as a patient"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    """"API endpoint for Patient Registration"""

    permission_classes = []

    def post(self, request, format=None):
        registration_serializer = PatientRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = PatientProfileSerializer(data=request.data.get('profile_data'))

        check_registration = registration_serializer.is_valid()
        check_profile = profile_serializer.is_valid()

        if check_registration and check_profile:
            patient = registration_serializer.save()
            profile_serializer.save(user=patient)
            return Response({'user_data': registration_serializer.data,
                             'profile_data': profile_serializer.data
                             }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileView(APIView):
    """
    API endpoint for Patient profile view/update -- Only accessible by patients
    """
    permission_classes = [IsPatient]

    def get(self, request, format=None):
        profile = Patient.objects.get(user=request.user)

        # Serialize user data and profile data separately
        user_serializer = PatientRegistrationSerializer(request.user)
        profile_serializer = PatientProfileSerializer(profile)

        return Response({
            'user_data': user_serializer.data,
            'profile_data': profile_serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        profile = Patient.objects.get(user=request.user)
        profile_serializer = PatientProfileSerializer(instance=profile, data=request.data.get('profile_data'),
                                                      partial=True)

        if profile_serializer.is_valid():
            # Save the updated profile data
            profile_serializer.save()
            return Response({
                'profile_data': profile_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientHistoryView(APIView):
    """"API endpoint for Patient history and costs view Only accessible by patients"""
    permission_classes = [IsPatient]

def get(self, request, format=None):
        """
        Retrieve patient history and costs.
        """
        user = request.user
        patient = get_object_or_404(Patient, user=user)
        patient_history = History.objects.filter(patient=patient)
        patient_history_serializer = PatientHistorySerializer(patient_history, many=True)
        return Response(patient_history_serializer.data, status=HTTP_200_OK)


class AppointmentViewPatient(APIView):
    """
    API endpoint for getting appointment details and creating appointments.
    """
    permission_classes = [IsPatient]

    def get(self, request, pk=None, format=None):
        """
        Get appointments details for the current patient.
        """
        try:
            user_patient = Patient.objects.get(user=request.user)
            history = History.objects.filter(patient=user_patient).latest('admit_date')
            appointment = Appointment.objects.filter(status=True, patient_history=history)
            history_serializer = AppointmentPatientSerializer(appointment, many=True)
            return Response(history_serializer.data, status=status.HTTP_200_OK)
        except (Patient.DoesNotExist, History.DoesNotExist):
            return Response({"error": "Patient or History not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        """
        Create a new appointment for the current patient.
        """
        try:
            user_patient = Patient.objects.get(user=request.user)
            history = History.objects.filter(patient=user_patient).latest('admit_date')
            serializer = AppointmentPatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient_history=history)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (Patient.DoesNotExist, History.DoesNotExist):
            return Response({"error": "Patient or History not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None, format=None):
        """
        Delete an appointment for the current patient.
        """
        try:
            user_patient = Patient.objects.get(user=request.user)
            history = History.objects.filter(patient=user_patient).latest('admit_date')
            appointment = Appointment.objects.get(pk=pk, patient_history=history)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Patient.DoesNotExist, History.DoesNotExist, Appointment.DoesNotExist):
            return Response({"error": "Patient, History, or Appointment not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
