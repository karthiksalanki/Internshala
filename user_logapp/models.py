from collections.abc import Iterable
from django.contrib.auth.models import User
from django.db import models

from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CompanyProfile(models.Model):
    Name = models.CharField(max_length=500)
    Location = models.CharField(max_length=500,null = True, blank = True)
    CompanyLogo = models.ImageField(upload_to='static/Company/')
    Industry = models.CharField(max_length=500,null = True, blank = True)
    No_of_Emps = models.CharField(max_length=250,null = True, blank = True)
    Hiring_since = models.DateField(auto_now_add=True)
    Opportunities_posted = models.CharField(max_length=250,null = True, blank = True)
    Candidates_hired = models.CharField(max_length=250,null = True, blank = True)
    About = models.TextField()
    
    class Meta:
        verbose_name = 'CompanyProfile'
        verbose_name_plural = 'CompanyProfile' 

    def __str__(self):
        return  self.Name 

class Corejobinfo(models.Model):
    WFH = "wfm"
    In_Office = "office"
    work_mode =[(WFH,"work from home"),(In_Office,"InOffice")]
    Role = models.CharField(max_length=500)
    Company_name = models.CharField(max_length=500)
    Location = models.CharField(max_length=500)
    Work_mode = models.CharField(max_length=250,choices = work_mode,default = "InOffice")
    Skills = models.CharField(max_length=500) #ArrayField(models.CharField(max_length=250), blank=True, null=True)
    Salary = models.PositiveIntegerField(null = True, blank = True)
    date_of_post = models.DateField(auto_now_add=True)
    Responsibilities = models.TextField(null = True, blank = True)
    Eligibility = models.TextField(null = True, blank = True)
    Perks =models.TextField(null = True, blank = True)
    No_of_openings = models.PositiveIntegerField(null = True, blank = True)
    CompanyProfile = models.ForeignKey(CompanyProfile,on_delete=models.PROTECT, null = True, blank = True)
    Count = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True

# For Jobs
class Jobs(Corejobinfo):
    Experience = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Jobs'
        verbose_name_plural = 'Jobs'
        
    # def save(self,*args, **kwargs):
    #     self.Company_name=self.CompanyProfile.Name
    #     return super().save(self,*args,**kwargs)
    
    def __str__(self):
     	return self.Role
  

# For Internships   
class Internships(Corejobinfo):
    Duration = models.CharField(max_length=250,null = True, blank = True) 
       
    class Meta:
        verbose_name = 'Internships'
        verbose_name_plural = 'Internships'
        
    # def save(self,*args, **kwargs):
    #     self.Company_name=self.CompanyProfile.Name
    #     return super().save(self,*args,**kwargs)
            
    def __str__(self):
       return self.Role

class Applications(models.Model):
    first_name = models.CharField(max_length=500,null = True, blank = True)
    last_name = models.CharField(max_length=100,null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    contact= models.CharField(max_length=250,null = True, blank = True)
    address = models.CharField(max_length=250,null = True, blank = True)
    applicant_skills = models.CharField(null = True, blank = True,max_length=200)   #ArrayField(models.CharField(max_length=250), blank=True, null=True)
    relocation = models.CharField(max_length=250,null = True, blank = True)
    
    class Meta:
        abstract = True

class JobApplications(Applications):
    job = models.ForeignKey(Jobs,on_delete=models.DO_NOTHING)
    resume = models.FileField(upload_to='Resumes/jobs/',null = True, blank = True)
        
    class Meta:
        verbose_name = 'JobApplications'
        verbose_name_plural = 'JobApplications'
        
        # def __str__(self):
        #     return  self.first_name
    
class InternApplications(Applications):
    internship = models.ForeignKey(Internships,on_delete=models.DO_NOTHING)
    resume = models.FileField(upload_to='Resumes/internship/',null = True, blank = True)
    
    class Meta:
        verbose_name = 'InternshipApplications'
        verbose_name_plural = 'InternshipApplications' 

    def __str__(self):
        return  self.first_name 
    
    
class myApplications(models.Model):
    applied_at = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    job = models.ForeignKey(Jobs, on_delete=models.DO_NOTHING, null = True, blank = True)
    internship = models.ForeignKey(Internships, on_delete=models.DO_NOTHING, null = True, blank = True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    #job_type = models.CharField(max_length=50, null=True, blank=True)
      
    class Meta:
        verbose_name = 'MyApplications'
        verbose_name_plural = 'MyApplications'
        

    
    # def __str__(self):
    #     return self.job,self.internship
    
class Savedapplication(models.Model):
    job = models.ForeignKey(Jobs,on_delete=models.DO_NOTHING,null = True, blank = True)
    internship = models.ForeignKey(Internships, on_delete=models.DO_NOTHING,null = True, blank = True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = 'Savedapplication'
        verbose_name_plural = 'Savedapplication'
        
    def __str__(self):
        return self.user.username
    
    
class Experience(models.Model):
    organization = models.CharField(max_length=250,null=True,blank=True)
    location = models.CharField(max_length=250,null=True,blank=True)
    start_date = models.DateField(auto_now=False,null=True,blank=True)
    end_date = models.DateField(auto_now=False,null = True, blank = True)
    description = models.TextField(null=True,blank=True)
    
    class Meta:
        abstract = True
        
class JobExperience(Experience):
    designation = models.CharField(max_length=50,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    
    class Meta:
        verbose_name = 'JobExperience'
        verbose_name_plural = 'JobExperience'
    
    def __str__(self):
        return self.user.username

class InterenshipExperience(Experience):
    designation = models.CharField(max_length=50,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    
    class Meta:
        verbose_name = 'InterenshipExperience'
        verbose_name_plural = 'InterenshipExperience'
    
    def __str__(self):
        return self.user.username
    
class Course(Experience):
    cource_name = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Cource'
        verbose_name_plural = 'Cource'
    
    def __str__(self):
        return self.user.username

class Projects(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    start_date = models.DateField(auto_now=False,null=True,blank=True)
    end_date = models.DateField(auto_now=False,null = True, blank = True)
    description = models.TextField(null=True,blank=True)
    link =  models.URLField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    

# class Eduacation(models.Model):
#     college = models.CharField(max_length=150)
#     stream = models.CharField(50,blank=True,null=True)
#     start_date = models.DateField(auto_now=True)
#     end_date = models.DateField(auto_now=True,null = True, blank = True)
#     description = models.TextField()

class Profile(models.Model):
    phone = models.CharField(max_length=250,null=True,blank=True)
    present_location = models.CharField(max_length=250,null=True,blank=True)
    permanent_location = models.CharField(max_length=250,null=True,blank=True)
    education =models.TextField(null=True,blank=True)
    job_experience = models.ForeignKey(JobExperience,on_delete=models.DO_NOTHING,null=True,blank=True)
    internship_experience = models.ForeignKey(InterenshipExperience,on_delete=models.DO_NOTHING,null=True,blank=True)
    courses = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True)
    projects = models.ForeignKey(Projects,on_delete=models.DO_NOTHING,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    skills = models.TextField(null=True,blank=True)