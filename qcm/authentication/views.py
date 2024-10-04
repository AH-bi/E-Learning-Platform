from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app1.models import Category,Subcategory,Domain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.utils.safestring import mark_safe

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from .tokens import account_activation_token

# Create your views here.


def activate(request,uidb64,token):
    user=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
    if user is not None and  account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Thank you for your email confirmation, Now you can Login you account ")
        return redirect('home')
    else:
        messages.error(request,"Activation link is invalid ")
    return redirect('home')




def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def about(request):
    return render(request,"about.html")


def home(request):  
    if request.user.is_authenticated:
        if request.session.get('score_user') is not None:
            del request.session['score_user']
        if request.session.get('score_computer') is not None:
            del request.session['score_computer'] 
        if request.session.get('que') is not None:
            del request.session['que'] 
        if request.session.get('round') is not None:
            del request.session['round']
        domains = Domain.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        for category in categories:
            if not Subcategory.objects.filter(category=category).exists():
                categories = categories.exclude(id=category.id)
        context = {
            'domains': domains,
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request,'index.html',context)
    return render(request,'index.html')



def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please try some other username ")    
            return redirect("signup")

        if User.objects.filter(email=email):
            messages.error(request,"Email already registred")    
            return redirect("signup")
        if(len(username)>10):
            messages.error(request,"Username must be under 10 characteres")    
            return redirect("signup")
        if(pass1!=pass2):
            messages.error(request,"Passwords didn't match ")    
            return redirect("signup")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric  ")    
            return redirect("signup")


        
        myuser = User.objects.create_user(username, email, pass1)

        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active = False
        myuser.save()
        activate_email(request,myuser,myuser.email)
        #messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        return redirect("home") 
    return render(request,"signup.html")


def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pass1']
        user=authenticate(request,username=username,password=password)
        if user is not None:
  
            login(request,user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect("home")
        else:
            messages.error(request, "Bad Credentials!!")
            error_message = "Bad Credentials!!"
            return render(request, "login.html", {'error_message': error_message} )
    return render(request, "login.html" )






def signout(request):
    logout(request)
    messages.success(request,"logout Successfully")
    return redirect("home")



class Configuration(LoginRequiredMixin,View):
    
    def get(self,request):
        diff=['Easy','Medium','Hard']
        opp=['Computer','Friend']
        ctx = {
            'difficulty': diff,
            'timer': 10,
            'opponent': opp,
                }
        return render(request, 'configure_quizz.html', ctx)

    def post(self,request):
        if request.method=='POST':
            request.session['difficulty']=request.POST.get('difficulty')
            request.session['timer']=request.POST.get('timer')
            request.session['opponent']=request.POST.get('opponent')
            request.session['total_round']=request.POST.get('round')

        print(request.session['total_round'])
        return redirect("home")

def error_404_view(request,exception):
        return render(request, '404.html', status=404)





class ProfileEdit(View):
    template_name = 'edit_profile.html'
    def get(self,request):
        user=request.user
        return render(request,ProfileEdit.template_name,{'user':user})





    def post(self, request):
        # the login user 
        user = request.user

        username = request.POST.get('username')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get('email')
        
        if user.first_name == first_name or user.last_name == last_name or user.email == email and user.username == username :
            error='No changes made'        
            return render (request,ProfileEdit.template_name,{'error':error})
        
        if first_name != None and last_name != None and email != None and username !=None :  

            if(first_name != user.first_name):
                user.first_name=first_name
            if(last_name != user.last_name):
                user.last_name=last_name



            if(username != user.username):
                    if(len(username)>10):
                        error="Username must be under 10 characteres"   
                        return render (request,ProfileEdit.template_name,{'error':error})
                    if not username.isalnum():
                        error="Username must be Alpha-Numeric"   
                        return render (request,ProfileEdit.template_name,{'error':error})
                    user.username=username
            user.save()
        else :
            
            pass
            
        return redirect('profile')
     
        """if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please try some other username ")    
            return redirect("signup")

        if User.objects.filter(email=email):
            messages.error(request,"Email already registred")    
            return redirect("signup")
        if(len(username)>10):
            messages.error(request,"Username must be under 10 characteres")    
            return redirect("signup")
        if(pass1!=pass2):
            messages.error(request,"Passwords didn't match ")    
            return redirect("signup")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric  ")    
            return redirect("signup")
"""
        
        