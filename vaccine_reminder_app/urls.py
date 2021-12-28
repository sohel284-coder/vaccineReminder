from django.urls import path
from vaccine_reminder_app.views import *


urlpatterns = [
    
    path('', home, name='home'),
    path('vaccine-registration-status', vaccine_regsitration_status, name='vaccine_regsitration_status'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('vaccine/<int:id>', vaccine_details, name='vaccine_details'),
    path('api/registration', VaccineReminderRegistrationAPIView.as_view(), ),
    path('api/vaccine-schedule', VaccineScheduleAPIView.as_view()),
   

]