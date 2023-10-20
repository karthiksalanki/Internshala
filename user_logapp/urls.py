from django.urls import path,include
from .import views
from user_log import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index, name ="index"),
    path('base/',views.test,name = "base"),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name="logout"),
    #path('forgotpassword/<str:user>/<slug:token>/',views.reset_password,name ="reset_password"),
    path('saved/',views.saved_application,name="saved"),
    #path('send_email_reset',views.send_email_reset,name = "send_email_reset"),
    path('password_reset/',views.reset_password,name ="reset_password"),
    path('forgotpassword/',views.send_email_reset,name = "send_email_reset"),
    path('forgotpassword/<str:user>/<slug:token>/',views.reset_password,name ="reset_password"),       #using token
    path('changepassword/',views.changepassword,name ="changepassword"),        #change password
    

    path('internview/<int:id>/',views.internshihppostview, name="internpostview"),
    path('jobview/<int:id>/',views.jobpostview, name="jobview"),
    path('apply-now/<str:jobtype>/<int:id>/',views.applynow, name="apply_now"),
    #path('apply-now/<str:jobtype>/<int:id>/',views.ApplyNow.as_view(), name="apply_now"),
    path('<str:jobtype>/<int:id>/save/',views.postSave, name="PostSave"),
    path('<str:jobtype>/<int:id>/unsave/',views.unsave,name="unsave"),
    #path('internview/<int:id>/save/',views.internSave, name="internview"),        #internsave
    #path('jobview/<int:id>/save/',views.jobSave, name="jobview"),       #jobsave
    path('jobs/',views.joblist, name="jobs"),
    path('internships/',views.internshiplist,name="internships"),
    #path('internships/',views.InternshipList.as_view(),name="internships"),
    path('my-applications/',views.my_applications,name="my_applications"),
    
    #Profile
    path('profile/',views.profileform, name="profileform"),     #profile
    path('profile/edit/',views.editprofile, name="editprofile"),     #editprofile
    path('profile/<str:experiencetype>/',views.subprofileform, name="subprofileform"),           #toadd job experience
    path('profile/<str:experiencetype>/<int:id>/',views.todelete, name="todelete"),
    #path('profile/<str:experiencetype>/',views.addprojects, name="addprojects"),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



