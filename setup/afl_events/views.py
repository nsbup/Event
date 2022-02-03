from ast import Pass
from email import header
from django.http import HttpResponse

from django.shortcuts import render
from afl_events.models import Admin
import json
from afl_events.forms import RegisterForm,EventAddForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from afl_events.models import Event
from django.utils.translation import gettext as _
from django.core import serializers
from django.http import JsonResponse
from django.views import View

# Create your views here.
def index(request):

    return render(request,'registration.html')
#BACKEND -> For User Registration
def test(request):
    return render(request,'admin_login.html',{})

    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        re_password = request.POST.get('repassword')

        if(password == re_password):
            user = User(name=name,email=email,gender=gender,password=password)
            user.save()
            request.session['uname'] = name
            return render(request,'admin_login.html',{})
        else:
            data = {'status':"Password and Re-entered password must be same"}
            return render(request,'registration.html',context=data)
    else:
        return HttpResponse("Something went wrong!!!!!")
#BACKEND -> For User Login
def login_user(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = User.objects.get(name=name)

            if user.password == password:
                request.session['uname'] = name
                return user_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'registration.html',context=data)

        except Exception as e:
            data = {'status':"User does not exists! You have to register first."}
            return render(request,'registration.html',context=data)
    else:
        return HttpResponse("Something went wrong!!!!!")

       
#User Logout
def user_logout(request):
    if 'uname' in request.session:
        del request.session['uname']

    if 'book_status' in request.session:
        del request.session['book_status']

    return render(request,'registration.html')
#User Event Page
def user_event(request):
    if 'uname' in request.session:
        event = Event.objects.all()
        data = {'event':event}
        return render(request,'user_event.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'registration.html',context=data)
def testcodensb(request):
    user = User.objects.all()
    print("user-----")
    print(user)
    for i in user:
        print(i.__dict__)

    # Put the logging info within your django view

    return render(request,'registration.html')

#BACKEND -> For Admin Login
def login_admin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(name=name)

            if user.password == password:
                request.session['aname'] = name
                # return HttpResponse('ffaf')
                return admin_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'admin_login.html',context=data)

        except Exception as e:
            data = {'status':"Invalid Username"}
            return render(request,'admin_login.html',context=data)
    else:
        return HttpResponse("Something went wrong faffsffa!!!!!")


#BACKEND -> For Admin Login
def login_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(name=name)

            if user.password == password:
                request.session['aname'] = name
                # return HttpResponse('ffaf')
                return admin_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'admin_login.html',context=data)

        except Exception as e:
            data = {'status':"Invalid Username"}
            return render(request,'admin_login.html',context=data)
    else:
        return HttpResponse("Something went wrong faffsffa!!!!!")


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    # Redirect to a success page.


def register_view(request):
    print("innnn--register_view")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("innnn--saveedd")
            return redirect('login')
        else:
            print("valid error!!!!!")
            return render(request,'register.html',{'form':form})      

    else:
        form = RegisterForm()
        print("render--registration")
        return render(request,'register.html',{'form':form})  
        # return render(request, "home.html")
  
def login_view(request):
    return render(request,'login.html')

#User Home Page
# @login_required(redirect_field_name='/afl/login')
def user_home(request):
    return render(request,'home.html',context={})
@login_required(redirect_field_name='/afl/login')
def dashboard(request):
    evnt = Event.objects.all()
    addevntform = EventAddForm()

    context ={}
    headers = {
                'id' : _("Event ID"),
                'name' : _("Event Name"),
                'date' :_("Event Date"),
                'time' :_("Event Time"),
                'duration' :_("Event Duration (hrs)"),
                'payment': _('Pay Amount')
                
            }
    context['headers'] = headers        
    context['addevntform'] = addevntform        
    context['evnt'] = evnt  
    return render(request,'dashboard.html',context)    
def addevent(request):
    print("add event___")
    Pass

def addEvent(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = EventAddForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)    

class PayAmount(View):
    pass    