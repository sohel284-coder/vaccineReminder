from collections import namedtuple
import logging
import datetime
from re import U
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from sms import send_sms
from twilio.rest import Client
from googlevoice import Voice
from googlevoice.util import input

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from vaccineReminder.settings import EMAIL_HOST_USER, ACCOUNT_SID, AUTH_TOKEN
from vaccine_reminder_app.models import Vaccination, VaccineName, VaccineReminderRegistration, VaccineSchedule
from vaccine_reminder_app.serializers import VaccineReminderRegistrationSerializer, VaccineScheduleSerializer


def home(request):
    vaccination = Vaccination.objects.get(id=1)
    vaccines = VaccineName.objects.filter()


    return render(request, 'home.html', {
        'vaccination':vaccination,
        'vaccines':vaccines,
    })

@login_required(login_url='/account/login')
def vaccine_regsitration_status(request, ):            
    vaccine_schedules = VaccineSchedule.objects.filter(vaccine_user__email=request.user.email)

    return render(request, 'vaccine_registration_status.html', {'vaccine_schedules':vaccine_schedules})


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
    def send_vaccine_registration_email(self, reg_info, password):
        html_message = render_to_string('email/registration_email.html', {
            'reg_info':reg_info,
            'password':password,
        })
        recipient_list = [reg_info.email]
        subject = "Vaccine Registration"
        send_mail(subject, None, EMAIL_HOST_USER, recipient_list, html_message=html_message, fail_silently=False,)
    def send_vaccine_registration_sms(self, reg_info, password):
        phone_number = f'+88{reg_info.phone}'
        account_sid = ACCOUNT_SID
        auth_token =  AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f'Your vaccine registration is successfully from Mohsin Vaccine Reminder service.your login credential username:{reg_info.email} and passord:{password}',
            from_='+14156882382',
            to=phone_number, 
        )
        print(message)
            

    def get(self, request, format=None):
        objs = VaccineReminderRegistration.objects.all()
        return Response(VaccineReminderRegistrationSerializer(objs, many=True).data)


    def post(self, request, format=None):
        dict={
            'success':'',
            'invalid_email':"",
        }
        serializer = VaccineReminderRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True, ):
            validated_data = serializer.validated_data

            try:
                reg_user = VaccineReminderRegistration.objects.get(email=validated_data['email'])
                if reg_user:
                    dict['invalid_email'] = 'Email is already used'
                    return Response(dict, status=status.HTTP_208_ALREADY_REPORTED)
            except:        
                try:
                    user = User(username=validated_data['email'], email=validated_data['email'])
                    password = User.objects.make_random_password(length=6)
                    user.set_password(password)
                    user.save()
                except:
                    logging.exception('faild to user create')

                reg_info = serializer.save()
                
                try:
                    self.send_vaccine_registration_email(reg_info, password)
                except:
                    logging.exception("Failed to send email after Registration")
                try:
                    self.send_vaccine_registration_sms(reg_info, password)
                except:
                    logging.exception('faild to send sms after registration')             
                
                dict['success'] = "Registration successfully completed"
                return Response(dict, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



class VaccineScheduleAPIView(APIView):
    def send_vaccine_reminder_sms(self, vaccine_schedules):
        for vacs in vaccine_schedules:
            print(vacs)
            vaccine_user_phone = vacs.vaccine_user.phone
            vaccine_name = vacs.vaccine_name.name 

        vaccine_user_phone = f'+88{vaccine_user_phone}'
        
        account_sid = ACCOUNT_SID
        auth_token =  AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f'Your children is eligible for {vaccine_name}.Please vaccinated your children as soon as possible',
            from_='+14156882382',
            to=vaccine_user_phone, 
        )
        print(message)
    def send_vaccine_reminder_email(self, vaccine_schedules):
        recipient_list = []
        for vacs in vaccine_schedules:
            print(vacs)
            recipient_list.append(vacs.vaccine_user.email)
            vaccine_name = vacs.vaccine_name.name
        html_message = render_to_string('email/reminder_email.html', {'vaccine_name':vaccine_name})
        subject = "Vaccine Reminder"
        send_mail(subject, None, EMAIL_HOST_USER, recipient_list, html_message=html_message, fail_silently=False, )

        

    def get(self, request, format=None):
        today = datetime.date.today()
        vaccine_schedules = VaccineSchedule.objects.filter(first_dose_vaccine_date=today, first_dose_completed=False) or VaccineSchedule.objects.filter(second_dose_vaccine_date=today, second_dose_completed=False) or VaccineSchedule.objects.filter(third_dose_vaccine_date=today, third_dose_completed=False) or VaccineSchedule.objects.filter(fourth_dose_vaccine_date=today, fourth_dose_completed=False)
        try:
            self.send_vaccine_reminder_sms(vaccine_schedules)
        except:
            pass
        try:
            self.send_vaccine_reminder_email(vaccine_schedules)
        except:
            logging.exception('faild to send vaccine reminder email')             
                  
        return Response(VaccineScheduleSerializer(vaccine_schedules, many=True).data)


    



