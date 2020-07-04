
from django.urls import path,include
from .views import login,tech,register1,logout,edit,displaystd,deletestd,update,update1,attendece,trans,admindashboard,serachbar,testsandmarks,editpersonal,displaystdrate,stdstudentdisplay,adminreg,addtecher1,std1,techdispaly,std1display,searchadmin,displaystd121,messageview,stdvideo,index,videoview1

urlpatterns = [
    path('register1', register1, name='register1'),
    path('register12', edit, name='register12'),
    path('accounts/login/tech', tech, name='tech'),
    path('accounts/logout',logout,name='logout'),
    path('displaystd',displaystd,name='displaystd'),
    path('delete/<int:id>',deletestd,name='delete'),
    path('update1/<int:id>/',update1,name='update1'),
    path('update/<int:id>/', update, name='update'),
    path('trans12',trans,name="trans"),
    path('admindashboard',admindashboard,name='admindashboard'),
    path('attendece',attendece,name='attendece'),
    path('ss',serachbar,name="ss"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login',login,name='login'),
    path('testsandmarks',testsandmarks,name='testsandmarks'),
    path('editpersonal/<int:id>/',editpersonal,name='editpersonal'),
    path('displaystdrate',displaystdrate,name='displaystdrate'),
    path('stdstudentdisplay',stdstudentdisplay,name='stdstudentdisplay'),
    path('adminreg',adminreg,name='adminreg'),
    path('addtecher1',addtecher1,name='addtecher1'),
    path('std1',std1,name='std1'),
    path('techdispaly',techdispaly,name='techdispaly'),
    path('std1display',std1display,name='std1display'),
    path('searchadmin',searchadmin,name='searchadmin'),
    path('displaystd121',displaystd121,name='displaystd121'),
    path('messageview',messageview,name='messageview'),
    path('stdvideo/',stdvideo,name='stdvideo'),
    path('index/',index,name='index'),
    path('videoview1',videoview1,name='videoview1')



]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
