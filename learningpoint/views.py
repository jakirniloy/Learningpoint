from learningpoint.models import Newusers
from learningpoint.models import Userpost
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
    context = {
        
    }
    if request.method == 'POST':
        if request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNumber') and request.POST.get('expert') and request.POST.get('Email') and request.POST.get('password'):
            saveRecord = Newusers()

            t_email = request.POST.get('Email')

            saveRecord.firstName = request.POST.get('firstName')
            saveRecord.lastName = request.POST.get('lastName')
            saveRecord.phoneNumber = request.POST.get('phoneNumber')
            saveRecord.expert = request.POST.get('expert')
            saveRecord.point = '100'
            saveRecord.Email = t_email
            saveRecord.Username = t_email.split('@')[0]
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
    context = {
        
    }
    if request.method == 'POST':
        try:
            userDetail = Newusers.objects.get(Email=request.POST.get('Email'))
            if check_password(request.POST.get('password'), (userDetail.password)):
                request.session['Email'] = userDetail.Email
                return render(request, 'home.html', context)
            else:
                messages.success(
                    request, 'Password incorrect...!')
        except Newusers       .DoesNotExist as e:
            messages.success(
                request, 'No user found of this email....!')

    return render(request, 'login.html', context) 




# def loginpage(request):
#     context = {}
#     if request.method == 'POST':
#         try:
#             UserDetails = Newusers.objects.get(Email=request.POST.get(
#                 'Email'), password=request.POST.get('password'))
#             request.session['Email'] = UserDetails.Email       
#             return render(request, 'home.html', context)       
#         except Newusers.DoesNotExist as e:
#             messages.success(request, 'Username / Password Invalid...!')
#     return render(request, 'login.html', context)

def logout(request):
    try:
        del request.session['Email']
    except:
        return render(request, 'index.html')
    return render(request, 'index.html')

#........home
def home(request):
    
     if request.method == 'POST':
        if request.POST.get('questionTitle') and request.POST.get('qustionDescription') :
            saveQuestion = Userpost()

            users = Newusers.objects.raw(
                'SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])

            for user in users:

                saveQuestion.publisherId = user.id
                saveQuestion.publisherName = user.firstName + " " + user.lastName
                saveQuestion.title = request.POST.get('questionTitle')
                saveQuestion.description = request.POST.get(
                    'qustionDescription')
                
                

                if int(user.point) >= 10:
                    user.point = str(int(user.point) - 10)

                    user.save()

                    saveQuestion.save()
                    messages.success(
                        request, "Your question has been submitted!")
                    return render(request, 'home.html', {'users': users})
                else:
                    messages.success(
                        request, "You don't have enough point! Please buy points.")
                    return render(request, 'home.html', {'users': users})
     else:
        try:
            users = Newusers.objects.raw(
                'SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])
            return render(request, 'home.html', {'users': users})
        except:
            messages.success(request, 'You need to login first')
            return redirect('login')
#endhome
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
    users = Newusers.objects.raw('SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])
    return render(request, 'profile.html', {'users': users})

def blog(request):
   
        user = Newusers.objects.get(Email=request.session['Email'])
        questions = Userpost.objects.raw(
            'SELECT * FROM users_post  WHERE PUBLISHERID =  %s ORDER BY id DESC', [user.id])
        users = Newusers.objects.raw(
            'SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])
        return render(request, 'blog.html', {'questions': questions,'users': users})

  
    


def edit_profile(request):
    if request.method == 'POST':
        users = Newusers.objects.raw(
            'SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])
        if request.POST.get('editFirstName') and request.POST.get('editLastName') and request.POST.get('editPhoneNumber') and request.POST.get('editEmail') and request.POST.get('editUsername') and request.POST.get('editExpert'):

            updateRecord = Newusers()

            updateRecord.id = users[0].id
            updateRecord.firstName = request.POST.get('editFirstName')
            updateRecord.lastName = request.POST.get('editLastName')
            updateRecord.phoneNumber = request.POST.get('editPhoneNumber')
            updateRecord.Email = request.POST.get('editEmail')
            updateRecord.Username = request.POST.get('editUsername')
            updateRecord.expert = request.POST.get('editExpert')
            updateRecord.password = users[0].password
            updateRecord.point = users[0].point

            if len(request.FILES) != 0:
                updateRecord.image = request.FILES['editPhoto']

            updateRecord.save()
            messages.success(
                request, "User details updated successfully...!")

            return redirect('edit-profile')

    else:
        try:
            users = Newusers.objects.raw(
                'SELECT * FROM learningpoint_newusers WHERE EMAIL = %s', [request.session['Email']])
            return render(request, 'edit-profile.html', {'users': users})
        except:
            messages.success(request, 'You need to login first')
            return redirect('loginpage')
   






           