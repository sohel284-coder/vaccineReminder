from django import forms
from django.contrib.auth.models import User

from accounts.models import HealthComplexUser



class HealthComplexUserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, )
    repeat_password = forms.CharField(max_length=32, )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("The email is already in use")
        except User.DoesNotExist:
            return email

    def clean(self):
        super(HealthComplexUserRegistrationForm, self).clean()
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('repeat_password')
        if not password == re_password:
            raise forms.ValidationError('Password must match')

    def create(self, validated_data):
        #create auth user
        user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=validated_data['password'])
        # create a health complex user
        health_complex_user = HealthComplexUser.objects.create(user=user)
        return health_complex_user
    