from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.index, name ="index"),
    path('base/',views.test,name = "base"),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name="logout"),
    path('forgotpassword/<str:user>/<slug:token>/',views.reset_password,name ="reset_password"),
    path('saved/',views.saved_application,name="saved"),
    path('send_email_reset',views.send_email_reset,name = "send_email_reset"),
    
    path('internview/<int:id>/',views.Internshihppostview, name="internpostview"),
    path('jobview/<int:id>/',views.Jobpostview, name="jobview"),
    path('apply-now/<str:jobtype>/<int:id>/',views.applynow, name="apply_now"),
    path('<str:jobtype>/<int:id>/save/',views.PostSave, name="PostSave"),
    #path('internview/<int:id>/save/',views.internSave, name="internview"),        #internsave
    #path('jobview/<int:id>/save/',views.jobSave, name="jobview"),       #jobsave
    path('jobs/',views.joblist, name="jobs"),
    path('internships/',views.internshiplist,name="internships"),
    path('my-applications/',views.my_applications,name="my_applications"),
    
    #Saved
    
    
    

]


