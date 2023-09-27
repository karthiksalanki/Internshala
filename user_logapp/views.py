from django.shortcuts import render,redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from django.template import loader
from .forms import Login
# Create your views here.

#Home page
def index(request):
    msg = "Welcome To Intershala"
    return render(request,'index.html',{ 'text': msg })
#Not used
def base(request):
    return render(request,'base.html')

#To Register
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        Password1 = request.POST['Password1']
        Password2 = request.POST['Password2']
        if Password1 == Password2:
            if User.objects.filter(username = username).exists():
                messages.info(request,'username already exists')
                return redirect('/register')
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email already exists')
                return redirect('/login')
            else:
                user = User.objects.create_user(username=username,email=email,password=Password1,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('/login')
        
        else:
            messages.info(request,'Password doesnot matching')
            return redirect('/register')
    
    else:
        return render(request,'register.html')

# To login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        Password = request.POST.get('password')
        print(request,username,Password)
        user = authenticate(request, username = username,password=Password)
        print(user) 
        if user is not None:
            print("login")
            messages.info(request,'login sucssfully')
            auth.login(request,user)
            print('login sucssfully')
            #return render(request,'index.html') #{'myjobs' :data}
            return index(request)
        else:
            messages.info(request,'user not found')
            print("logout")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

# To logout  
def logout(request):
    auth.logout(request)
    return redirect('/')

# Send email rest request
def send_email_reset(request):
    if request.method == 'GET':
        return render(request,'send_email_reset.html')
    else:
        try:
            email = request.POST.get('email')
            if request.user.email == email:
                token = default_token_generator.make_token(request.user)
                uid = urlsafe_base64_encode(force_bytes(request.user.pk))
                reset_link = f"http://127.0.0.1:8000/forgotpassword/{request.user}/{token}/"
                print(request.user.email)
                subject = 'Password Reset'
                message = f"Click the link below to reset your password:\n{reset_link}"
                from_email = 'karthiksalanki1999@example.com'
                recipient_list = [request.user.email]
                send_mail(subject, message, from_email, recipient_list,fail_silently=False)
                return render(request,'password_reset_done.html')
            else:
                msg = "Email does not exists,please provide valid email"
                return render(request,'send_email_reset.html',{ 'text': msg })
        except Exception as e:
            print(str(e))
            messages.info(request,'Email does not exists')
            return render(request, 'send_email_reset.html')

#Change password
def reset_password(request,user,token):
    print(request)
    if request.method == 'GET':
        return render(request,'reset_password.html')
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            new_passowrd = request.POST.get('newpassword')
            retype_password = request.POST.get('retypepassword')
            if new_passowrd == retype_password:
                user = User.objects.get(username = username)
                print(user,new_passowrd)
                user.password = new_passowrd
                user.save()
                return redirect('/')
    except Exception as e:
        return str(e)

# Joblist
def joblist(request):
    jobs_data = Jobs.objects.all()
    print(jobs_data)
    return render(request,'jobs.html',{'myjobs' : jobs_data})

# Internshiplist
def internshiplist(request):
    internships_data = Internships.objects.all()
    print(internships_data)
    return render(request,'internships.html',{'data': internships_data})

#not used
def test(request):
    obj = myApplications.objects.get(id=17)
    print(obj.internship.Role,obj.internship.Duration,obj.job,obj.internship)
    #print(obj.Role,obj.Skills)
    return render(request,'index.html')

# Apply for post  
def applynow(request,id,jobtype):
    if request.method == 'GET':
        return render(request,'apply_now.html')    
    else:
        print(request.POST.getlist('skills'),request.POST.get('fname'),request.POST.get('lname'),request.POST.get('email'),request.POST.get('number'),request.POST.get('address'),request.FILES.get('resume') )
        data={'applicant_skills' : request.POST.get('skills'),
        'first_name' : request.POST.get('fname'),
        'last_name' : request.POST.get('lname'),
        'email' : request.POST.get('email'),
        'contact' : request.POST.get('number'),
        'address' : request.POST.get('address'), 
        'resume':request.FILES.get('resume')}

        if jobtype == "job":
            obj = Jobs.objects.get(id = id)
            jobapplication=JobApplications.objects.create(job=obj,**data)
            myApplications.objects.create(job_id=obj.id,user=request.user)
            sendmail(jobapplication.email,jobapplication.first_name,obj.Role,obj.Company_name)
            return redirect('jobs')
        else:
            print(data)
            obj = Internships.objects.get(id = id)
            print(obj.Location)
            internapplication=myApplications.objects.create(internship_id=obj.id,user=request.user)
            obj2 = InternApplications.objects.create(internship=obj,**data)
            sendmail(obj2.email,obj2.first_name,obj.Role,obj.Company_name)
            return redirect('internships')

# my-applications list
def my_applications(request):
    applications = myApplications.objects.all()
    print(applications)
    return render(request,'my_applications.html',{'myapplications' : applications})

# sending mail afterapply
def sendmail(email,fname,role,company):
    subject = f'Your Application For {role} at {company}'
    #link="http://127.0.0.1:8000/my-applications/"      To know more about the position
    message = f"Dear {fname}, Thank you for your interest in a career at Kwalee. We have received your application for the Junior Software Engineer - Backend position.What happens now? We will review your application and will contact you if there is a good match. \n Sincerely, \n The Kwalee Talent Acquisition Team"
    from_email = 'karthiksalanki1999@example.com'
    send_mail(subject, message, from_email, [email],fail_silently=False)

# Detailview
def Internshihppostview(request,id):
    postdata = Internships.objects.get(id = id)
    return render(request,'view.html',{'data':postdata})

# Detailview
def Jobpostview(request,id):
    postdata = Jobs.objects.get(id = id)
    return render(request,'view.html',{'data':postdata})

# Save 
def PostSave(request,jobtype,id):
    print(jobtype,id)
    jobdata = Jobs.objects.get(id = id)
    internshipdata=Internships.objects.get(id = id)
    # data={'Role':jobdata.Role,
    #       'Company_name':jobdata.Company_name,
    #       'Location':jobdata.Location,
    #       'Work_mode':jobdata.Work_mode,
    #       'Skills':jobdata.Skills,
    #       'Experience':jobdata.Experience,
    #       'Salary':jobdata.Salary,
    #       'date_of_post':jobdata.date_of_post,
    #       'Responsibilities':jobdata.Responsibilities,
    #       'Eligibility':jobdata.Eligibility,
    #       'Perks':jobdata.Perks,
    #       'No_of_openings':jobdata.No_of_openings,
    #       'CompanyProfile':jobdata.CompanyProfile,
    #       'Count':jobdata.Count}
    if jobtype == "job":
        obj=Savedapplication.objects.create(job=jobdata,user=request.user )
        #Savedapplication.objects.create(**data,Experience=jobdata.Experience)
        return render(request,'view.html',{'data':jobdata})
    else:
        Savedapplication.objects.create(internship=internshipdata,user=request.user)
        return render(request,'view.html',{'data':internshipdata})
        
# saved application list
def saved_application(request):
    saveddata=Savedapplication.objects.all()
    return render(request,'saved.html',{'data':saveddata})