import logging
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from vaccineReminder.settings import EMAIL_HOST_USER
from vaccine_reminder_app.models import Vaccination, VaccineName, VaccineReminderRegistration
from vaccine_reminder_app.serializers import VaccineReminderRegistrationSerializer


def home(request):
    vaccination = Vaccination.objects.get(id=1)
    vaccines = VaccineName.objects.filter()

    return render(request, 'home.html', {
        'vaccination':vaccination,
        'vaccines':vaccines,
    })

def contact(request, ):
    vaccines = VaccineName.objects.filter()
    return render(request, 'contact.html', {
        'vaccines':vaccines,

    }) 
    
def about(request, ):
    vaccines = VaccineName.objects.filter()
    return render(request, 'about.html', {
        'vaccines':vaccines,

    })    

def vaccine_details(request, id):
    vaccination = Vaccination.objects.get(id=1)
    vaccines = VaccineName.objects.filter()
    vaccine = VaccineName.objects.get(id=id)
    return render(request, 'vaccine_details.html', {
        'vaccine':vaccine,
        'vaccination':vaccination,
        'vaccines':vaccines,
    })    


def enforce_csrf(self, request):
    return  # To not perform the csrf check previously happening

class VaccineReminderRegistrationAPIView(APIView):
    def send_vaccine_reminder_email(self, reg_info):
        html_message = render_to_string('email/registration_email.html', {
            'reg_info':reg_info,
        })
        recipient_list = [reg_info.email]
        subject = "Vaccine Registration"
        send_mail(subject, None, EMAIL_HOST_USER, recipient_list, html_message=html_message, fail_silently=False,)

    def get(self, request, format=None):
        objs = VaccineReminderRegistration.objects.all()
        return Response(VaccineReminderRegistrationSerializer(objs, many=True).data)


    def post(self, request, format=None):
        serializer = VaccineReminderRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            reg_info = serializer.save()
            try:
                self.send_vaccine_reminder_email(reg_info)
            except:
                logging.exception("Failed to send email after Registration")    

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


# class VaccineReminderRegistrationListCreateAPIView(ListCreateAPIView):
#     permission_class = (permissions.AllowAny, )
#     serializer_class = VaccineReminderRegistrationSerializer
#     queryset = VaccineReminderRegistration.objects.filter()
    




