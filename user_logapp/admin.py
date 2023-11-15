from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CompanyProfile)
class CompanyProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CompanyProfile
    list_display = ['Name','Location','CompanyLogo','Industry','No_of_Emps','Hiring_since','Opportunities_posted','Candidates_hired']

@admin.register(Jobs)
class JobsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['Role','Company_name','Location','Work_mode','Skills','Experience','Salary','date_of_post']

@admin.register(Internships)
class InternshipsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display =  ['Role','Company_name','Location','Duration','Work_mode','Skills','Salary','date_of_post']
       
@admin.register(JobApplications)
class JobApplicationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display =  ['first_name','last_name','email','contact','address','applicant_skills','mode_of_work','job']
    
@admin.register(InternApplications)
class InternApplicationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display =  ['first_name','last_name','email','contact','address','applicant_skills','mode_of_work','internship']
    
#@admin.register(myApplications)
# class myApplicationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display =  ['__all__']
    
#@admin.register(Savedapplication)
# class SavedapplicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display =  ['__all__']