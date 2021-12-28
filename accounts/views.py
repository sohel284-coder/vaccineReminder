from datetime import date
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

from accounts.forms import HealthComplexUserRegistrationForm
from .serializers import UserSerializer, RegisterSerializer

from knox.views import LoginView as KnoxLoginView


def login_page(request, ):
    if request.method == 'POST':
        username = request.POST['email']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Credentials are not valid')
    return render(request, 'account/login.html', )

def logout_view(request):
    logout(request)
    return redirect('home')



def health_complex_user_registration(request):
    form = HealthComplexUserRegistrationForm
    if request.method == 'POST':
        form = HealthComplexUserRegistrationForm(request.POST)
        if form.is_valid():
            health_complex_user = form.create(form.cleaned_data)
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            return HttpResponseRedirect(reverse('admin:index'))
            # return HttpResponseRedirect('successfully registerd for health complex user but you have no permission to change vaccine status of vaccine user.Please wait for permission') 
        else:
            errors = form.errors
            return render(request, 'account/health_complex_user_registration.html', {'form': form, 'errors': errors})
            
    return render(request, 'account/health_complex_user_registration.html', {'form': form, })




    
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


#Login api

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
       
        serializer = AuthTokenSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True, ):
            user = serializer.validated_data['user']
            login(request, user)
        # return super(LoginAPI, self).post(request, format=None)
            print(serializer.data)
            print(AuthTokenSerializer(user).data)
            return Response({
                "user": user,
                "token": AuthToken.objects.create(user)[1]
            })


