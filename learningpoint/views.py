from learningpoint.models import Newusers
from django.contrib import messages
from django.contrib.messages.api import success
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import hashlib
from django.contrib.messages.api import success
from django.shortcuts import redirect, render

def index(request):    
    return render(request, 'index.html')

# def userreg(request):
#     if request.method=='POST':
#         Username=request.POST['username']
#         Email= request.POST['Email']
#         password = request.POST['password']
#         Newusers(Username=Username,Email=Email,password=password).save()
#         messages.success(request, 'The New User  '+request.POST['username']+' is Saved Successfully...!')
#         return render(request, 'registration.html')
#     else:
#        return render(request, 'registration.html')

def userreg(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNumber') and request.POST.get('expert') and request.POST.get('email') and request.POST.get('password'):
            saveRecord = Newusers()

            t_email = request.POST.get('Email')

            saveRecord.firstName = request.POST.get('firstName')
            saveRecord.lastName = request.POST.get('lastName')
            saveRecord.phoneNumber = request.POST.get('phoneNumber')
            saveRecord.expert = request.POST.get('expert')
            saveRecord.point = '100'
            saveRecord.email = t_email
            saveRecord.username = t_email.split('@')[0]
            saveRecord.password = make_password(request.POST.get('password'))

            if saveRecord.isExists():
                messages.error(request, t_email +
                               " email address already registered!")
                return render(request, 'registration.html', context)
            else:
                saveRecord.save()
                messages.success(
                    request, "New user " + t_email.split('@')[0] + ", registration details saved successfully...! Please Log in now.")
                return render(request, 'registration.html', context)

    else:
        return render(request, 'registration.html', context)

  
  



def loginpage(request):
    context = {}
    if request.method == 'POST':
        try:
            UserDetails = Newusers.objects.get(Email=request.POST.get(
                'Email'), password=request.POST.get('password'))
            request.session['Email'] = UserDetails.Email       
            return render(request, 'home.html', context)       
        except Newusers.DoesNotExist as e:
            messages.success(request, 'Username / Password Invalid...!')
    return render(request, 'login.html', context)

def logout(request):
    try:
        del request.session['Email']
    except:
        return render(request, 'index.html')
    return render(request, 'index.html')
def home(request):
    return render(request,'home.html')
def term(request):
    return render(request, 'term.html')
def privacy(request):
    return render(request, 'privacy.html')
def notes(request):
    return render(request, 'mynotes.html')
def upload(request):
    return render(request, 'upload.html')
def mylibrary(request):
    return render(request, 'mylibrary.html')
def lstore(request):
    return render(request, 'store.html') 
def profile(request):
    return render(request, 'profile.html') 
        







           