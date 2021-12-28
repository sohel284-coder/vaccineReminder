from django.contrib import admin

from vaccine_reminder_app.models import Vaccination, VaccineName, VaccineReminderRegistration, VaccineSchedule


class VaccineScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ('first_dose_vaccine_date', 'second_dose_vaccine_date', 'third_dose_vaccine_date', 'fourth_dose_vaccine_date', )
    

admin.site.register(VaccineReminderRegistration)
admin.site.register(Vaccination)
admin.site.register(VaccineName)
admin.site.register(VaccineSchedule, VaccineScheduleAdmin)
