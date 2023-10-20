from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display =  ['__all__']
    

admin.site.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ['Role','Company_name','Location','Work_mode','Skills','Experience','Salary','date_of_post']

admin.site.register(Internships)
class InternshipsAdmin(admin.ModelAdmin):
    list_display =  ['__all__']
       
admin.site.register(JobApplications)
class JobApplicationsAdmin(admin.ModelAdmin):
    list_display =  ['__all__']
    
admin.site.register(InternApplications)
class InternApplicationsAdmin(admin.ModelAdmin):
    list_display =  ['__all__']
    
#admin.site.register(myApplications)
# class myApplicationsAdmin(admin.ModelAdmin):
#     list_display =  ['__all__']
    
#admin.site.register(Savedapplication)
# class SavedapplicationAdmin(admin.ModelAdmin):
#     list_display =  ['__all__']