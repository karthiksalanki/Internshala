from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from django.template import loader
from .forms import Login
from rest_framework import status,permissions,authentication
from rest_framework.response import Response



# Create your views here.

from django import template

register = template.Library()

#Home page
def index(request):
    try:
        msg = "Welcome To Intershala"
        return render(request,'index.html',{ 'text': msg,'images':'img'})
    except Exception as e:
        messages.info(request,'Something went wronge')
        return render(request, 'index.html')

#Not used
def base(request):
    return render(request,'base.html')

#To Register
def register(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            Password1 = request.POST['Password1']
            Password2 = request.POST['Password2']
            phone = request.POST['phone']
            if Password1 == Password2:
                if User.objects.filter(username = username).exists():
                    messages.info(request,'username already exists')
                    return redirect('/register')
                elif User.objects.filter(email = email).exists():
                    messages.info(request,'Email already exists')
                    return redirect('/login')
                else:
                    user = User.objects.create_user(username=username,email=email,password=Password1,first_name=first_name,last_name=last_name)
                    Profile.objects.create(phone=phone,user_id=user.id)
                    user.save()
                    return redirect('/login')
            else:
                messages.info(request,'Password doesnot matching')
                return redirect('/register')
        else:
            return render(request,'register.html')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# To login
def login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            Password = request.POST.get('password')
            print(request,username,Password)
            user = authenticate(request,username=username,password=Password)
            print(user) 
            if user is not None:
                messages.info(request,'login sucssfully')
                auth.login(request,user)
                print('login sucssfully')
                #return render(request,'index.html') #{'myjobs' :data}
                return index(request)
            else:
                messages.info(request,'user not found')
                print("logout")
                return render(request,'login.html',{'msg':"mentioned username or password is not matching."})
        else:
            return render(request,'login.html')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# To logout  
def logout(request):
    auth.logout(request)
    return redirect('/')

# Send email rest request
def send_email_reset(request):
    try:
        if request.method == 'GET':
            return render(request,'send_email_reset.html')
        else:
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            if user.email == email:
                uid = urlsafe_base64_encode(force_bytes(request.user.pk))
                #token = default_token_generator.make_token(user.username)
                token, created = Token.objects.get_or_create(user=user)
                reset_link = f"http://127.0.0.1:8000/forgotpassword/{user.username}/{token}/"
                print(user)
                subject = 'Password Reset'
                message = f"Click the link below to reset your password:\n{reset_link}"
                from_email = 'karthiksalanki1999@example.com'
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list,fail_silently=False)
                return render(request,'password_reset_done.html')
            else:
                msg = "Email does not exists,please provide valid email"
                return render(request,'send_email_reset.html',{ 'text': msg })
    except Exception as e:
        messages.info(request,'Email does not exists')
        return JsonResponse('send_email_reset.html',{'error': 'An error occurred: ' + str(e)}, status=500)


#Change password
def changepassword(request):
    try:
        username = request.POST.get('username')
        new_password = request.POST.get('newpassword')
        retype_password = request.POST.get('retypepassword')
        if new_password == retype_password:
            userdata = User.objects.get(id=request.user.id)
            userdata.set_password(new_password)
            userdata.save()
            return redirect('/')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)       
    
    
#Forgot password
def reset_password(request,user=0,token=0):
    try:
        if request.method == 'GET':
            return render(request,'reset_password.html')
        if request.method == 'POST':
            user=Token.objects.get(key=token)
            username = request.POST.get('username')
            new_password = request.POST.get('newpassword')
            retype_password = request.POST.get('retypepassword')
            if new_password == retype_password:
                userdata = User.objects.get(id=user.user_id)
                userdata.set_password(new_password)
                userdata.save()
                return redirect('/')
            else:
                return Response({'msg':'Password mismatch'})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# Joblist

# def joblist(request):
#     jobs_data = Jobs.objects.all().order_by('-id')
#     jobapplied = myApplications.objects.filter(user=request.user)       #extra
#     data=jobapplied.last()
#     print(jobs_data,jobapplied,data)
#     return render(request,'jobs.html',{'myjobs' : jobs_data,'applied':jobapplied,'last':data})

def joblist(request):
    try:
        jobs_data = Jobs.objects.all().order_by('-id')
        jobapplied = myApplications.objects.filter(user=request.user)       #extra
        data=[]
        for j in jobapplied:
            if j.job is not None:
                print(j.job.id)
                data=data+[j.job.id]
        print(jobs_data,jobapplied,data)
        return render(request,'jobs.html',{'myjobs' : jobs_data,'applied':data})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# Internshiplist
def internshiplist(request):
    try:
        internships_data = Internships.objects.all().order_by('-id')
        internshipapplied = myApplications.objects.filter(user=request.user)       #extra
        data=[]
        for j in internshipapplied:
            if j.internship is not None:
                print(j.internship.id)
                data=data+[j.internship.id]
        print(internships_data)
        return render(request,'internships.html',{'data': internships_data,'applied':data})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

#not used
def test(request):
    obj = myApplications.objects.get(id=17)
    return render(request,'index.html')

# Apply for post  
def applynow(request,id,jobtype):
    try:
        if request.method == 'GET':
            if jobtype=="job":
                data = Jobs.objects.get(id=id)
            else:
                data = Internships.objects.get(id=id)
            return render(request,'apply_now.html',{'data':data})    
        else:
            data={'applicant_skills' : request.POST.get('skills'),
            'first_name' : request.POST.get('fname'),
            'last_name' : request.POST.get('lname'),
            'email' : request.POST.get('email'),
            'contact' : request.POST.get('number'),
            'address' : request.POST.get('address'),
            'mode_of_work' : request.POST.getlist('checkbox'), 
            'resume':request.FILES.get('resume')}

            if jobtype == "job":
                obj = Jobs.objects.get(id = id)
                check_already_applied = JobApplications.objects.filter(user=request.user,job=id)
                if check_already_applied is None:
                    jobapplication=JobApplications.objects.create(job=obj,**data)
                    obj.Count=obj.Count+1
                    obj.save()
                    myApplications.objects.create(job_id=obj.id,user=request.user)
                    sendmail(jobapplication.email,jobapplication.first_name,obj.Role,obj.Company_name)
                return redirect('jobs')
            else:
                obj = Internships.objects.get(id = id)
                check_already_applied = JobApplications.objects.filter(user=request.user,job=id)
                if check_already_applied is None:
                    internapplication=myApplications.objects.create(internship_id=obj.id,user=request.user)
                    obj2 = InternApplications.objects.create(internship=obj,**data)
                    obj.Count=obj.Count+1
                    obj.save()
                    sendmail(obj2.email,obj2.first_name,obj.Role,obj.Company_name)
                return redirect('internships')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# my-applications list
def my_applications(request):
    try:
        msg = "Your have not applied for any jobs or internships"
        applications = myApplications.objects.all().filter(user_id=request.user).order_by('-id')
        if applications.count()>=1:
            return render(request,'my_applications.html',{'myapplications' : applications,})
        else:
            return render(request,'my_applications.html',{'myapplications' : applications,'msg':msg})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# sending mail afterapply
def sendmail(email,fname,role,company):
    try:
        subject = f'Your Application For {role} at {company}'
        #link="http://127.0.0.1:8000/my-applications/"      To know more about the position
        message = f"Dear {fname}, Thank you for your interest in a career at {company}. We have received your application for the {role}.What happens now? We will review your application and will contact you if there is a good match. \n Sincerely, \n The {company} Hiring Team"
        from_email = 'karthiksalanki1999@example.com'
        send_mail(subject, message, from_email, [email],fail_silently=False)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)


# Detailview
def internshihppostview(request,id):
    try:
        postdata = Internships.objects.get(id = id)
        applicationdata = myApplications.objects.filter(user=request.user,internship_id = id).first()
        print(id,postdata,applicationdata)
        if applicationdata is not None:
            internship_applied="Already Applied"
        else:
            internship_applied="Apply Now"
        saved_data = Savedapplication.objects.filter(internship_id=postdata.id).filter(user_id=request.user)
        if saved_data.count()>0:
            return render(request,'view.html',{'data':postdata,'msg':"internship saved",'check_applied_or_not':internship_applied})
        else:    
            return render(request,'view.html',{'data':postdata,'check_applied_or_not':internship_applied})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# Detailview
def jobpostview(request,id):
        postdata = Jobs.objects.get(id = id)
        applicationdata = myApplications.objects.filter(user=request.user,job_id = id).first()
        print(id,postdata,applicationdata)
        if applicationdata is not None:
            job_applied="Already Applied"
        else:
            job_applied="Apply Now"
        saved_data = Savedapplication.objects.filter(job_id=postdata.id).filter(user_id=request.user)
        if saved_data.count()>0:
            return render(request,'view.html',{'data':postdata,'msg':"job saved",'check_applied_or_not':job_applied})
        else:
            return render(request,'view.html',{'data':postdata,'check_applied_or_not':job_applied})

    
# To Save 
def postSave(request,jobtype,id):
    try:        
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
                jobdata = Jobs.objects.get(id = id)
                test = Savedapplication.objects.filter(job_id=jobdata.id,user_id=request.user)
                obj=Savedapplication.objects.create(job=jobdata,user=request.user )
                return jobpostview(request,id)      #render(request,'view.html',{'data':jobdata})
            else:
                internshipdata=Internships.objects.get(id = id)
                Savedapplication.objects.create(internship=internshipdata,user=request.user)
                return internshihppostview(request,id)      #render(request,'view.html',{'data':internshipdata})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

#unsave
def unsave(request,jobtype,id):
    if jobtype=="job":
        jobdata = Savedapplication.objects.get(job_id=id,user_id=request.user.id)
        jobdata.delete()
        return redirect('saved')
    else:
        internshipdata = Savedapplication.objects.get(internship_id=id,user_id=request.user.id)
        internshipdata.delete()
        return redirect('saved')
        

# saved application list
def saved_application(request):
    try:
        saveddata=Savedapplication.objects.all().filter(user_id=request.user).order_by('-id')
        if saveddata.count() == 0:
            msg = "No Jobs or Internships Saved"
            return render(request,'saved.html',{'msg':msg})
        return render(request,'saved.html',{'data':saveddata})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

#profile
def profileform(request):
    try:
        if request.method  == 'GET':
            print(request.user.id)
            profiledata = Profile.objects.get(user_id = request.user.id) 
            jobdata = JobExperience.objects.filter(user_id = request.user)
            internshipdata = InterenshipExperience.objects.filter(user_id=request.user)
            coursedata = Course.objects.filter(user_id=request.user)
            project = Projects.objects.filter(user_id=request.user)         
            return render(request,'profile_form.html',{'data':profiledata,'jobdata':jobdata,'internshipdata':internshipdata,'coursedata':coursedata,'projects':project})
        elif request.method == 'POST':
            # profiledata = Profile.objects.get(user = request.user)
            # jobdata = JobExperience.objects.filter(user_id = request.user)
            # internshipdata = InterenshipExperience.objects.filter(user_id=request.user)
            # coursedata = Course.objects.filter(user_id=request.user)
            # project = Projects.objects.filter(user_id=request.user)           
            education = request.POST.get('education')
            skills = request.POST.get('skills')
            profiledata = Profile.objects.get(user_id = request.user.id)
            if education:
                profiledata.education=education
            if skills:
                profiledata.skills=skills 
            profiledata.save()
            return redirect('profileform')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)
 
#To Edit Basicdata   
def subprofileform(request,experiencetype):
    try:
        if request.method == 'GET':
            if experiencetype =="projects":
                return render(request,'projects_form.html',{'data':experiencetype})
            return render(request,'sub_profile_form.html',{'data':experiencetype})
        elif request.method == 'POST':
            start_date = request.POST.get('startdate')
            end_date = request.POST.get('enddate')
            working = request.POST.get('working')
            cource_name = request.POST.get('designation')
            designation = request.POST.get('designation')
            data = {
                    'organization' : request.POST.get('organization'),
                    'location' : request.POST.get('location'),
                    'start_date' : start_date,
                    'description':request.POST.get('description'),
                }
            #else:
                # data = {
                #     'organization' : request.POST.get('organization'),
                #     'location' : request.POST.get('location'),
                #     #'start_date' : end_date,
                #     # 'end_date' : start_date,
                #     'description':request.POST.get('description'),
                # } 
            if experiencetype == 'jobexperience':
                if working:
                    experiencedata = JobExperience.objects.create(**data,designation=designation,user_id=request.user.id)
                else:
                    experiencedata = JobExperience.objects.create(**data,end_date=end_date,designation=designation,user_id=request.user)
                return redirect('profileform')
            if experiencetype == 'internshipexperience':
                if working:
                    experiencedata = InterenshipExperience.objects.create(**data,designation=designation,user_id=request.user.id)
                else:
                    experiencedata = InterenshipExperience.objects.create(**data,end_date=end_date,designation=designation,user_id=request.user.id)
                return redirect('profileform')
            elif experiencetype == 'courses':
                if working:
                    experiencedata = Course.objects.create(**data,cource_name=cource_name,user_id=request.user.id)
                else:
                    experiencedata = Course.objects.create(**data,end_date=end_date,cource_name=cource_name,user_id=request.user.id)
            else:
                data = {                   
                    'title':request.POST.get('title'),
                    'start_date':request.POST.get('startdate'),
                    'end_date':request.POST.get('enddate'),
                    'description':request.POST.get('description'),
                    'link':request.POST.get('link'),
                }
                Projects.objects.create(**data,user_id=request.user.id)
            return redirect('profileform')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)
        
#To Delete The Experience
def todelete(request,experiencetype,id):
    try:
        if experiencetype == 'jobexperience':
            print(experiencetype,id)
            jobdata = JobExperience.objects.get(id=id)
            jobdata.delete()
        elif experiencetype == 'internshipexperience':
            internshipdata = InterenshipExperience.objects.get(id=id)
            internshipdata.delete()
        elif experiencetype == 'courses':
            coursedata = Course.objects.get(id=id)
            coursedata.delete()
        elif experiencetype == 'education':
            educationdata = Profile.objects.get(id=id)
            educationdata.education = None
            educationdata.save()
        elif experiencetype == 'skills':
            educationdata = Profile.objects.get(id=id)
            educationdata.skills = None
            educationdata.save()
        elif experiencetype == 'projects':
            projectsdata = Projects.objects.get(id=id)
            projectsdata.delete()
        return profileform(request)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

# To Edit Profile
def editprofile(request):
    try:
        if request.method == 'GET':
            data=User.objects.get(username=request.user)
            profile_data = Profile.objects.get(user_id = request.user.id)
            return render(request,'basic_profile_form.html',{'data':data,'profile':profile_data})
        else:
            username=request.POST.get('username')
            first_name=request.POST.get('firstname')
            last_name=request.POST.get('lastname')
            email=request.POST.get('email')
            password=request.POST.get('password')
            confirm_password=request.POST.get('confirm_password')
            phone=request.POST.get('phone')
            permanent_location=request.POST.get('permanentlocation')
            present_location=request.POST.get('presentlocation')
            
            if password == confirm_password:
                print(request.user.username)
                userdata = User.objects.get(username = request.user)
                profiledata= Profile.objects.get(user_id = request.user.id)     #.update(phone = phone,permanent_location =permanent_location,present_location = present_location)
                userdata.username = username
                userdata.first_name = first_name
                userdata.last_name = last_name
                userdata.email = email
                userdata.set_password(password)
                userdata.save()
                profiledata.phone = phone
                profiledata.permanent_location = permanent_location
                profiledata.present_location = present_location
                profiledata.save()
                return redirect('login')
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)
        

# Add Project To Profile      
# def addprojects(request):
#     try:
#         if request.method == 'GET':
#             print("############################################")
#             return render(request,'projects_form.html')
#         else:
#             data = {
#                 'title':request.POST.get('title'),
#                 'start_date':request.POST.get('startdate'),
#                 'end_date':request.POST.get('enddate'),
#                 'description':request.POST.get('description'),
#                 'link':request.POST.get('link'),
#                 }
#             Projects.objects.create(**data,user_id=request.user)
#             return redirect('profileform')
#     except Exception as e:
#         return Response(str(e))