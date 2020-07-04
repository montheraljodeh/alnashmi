from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse, reverse_lazy

from . import models
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.files.storage import  FileSystemStorage



from django.db.models import Count, Sum


ss=0
def  stdcount(request,id):
    dd=models.student.objects.filter(techer=id)

    return len(dd)

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username, password=password)


        if user is not None:
            try:
                request.session['user_id'] = user.id

                user1=models.Addtecher.objects.get(id=user.id)
                auth.login(request,user)
                users = models.message.objects.raw('SELECT * FROM ennashmi_message WHERE date1=%s AND t2=%s',
                                                   [date.today(), user.username])

                list1 = []
                for i in users:
                    list1.append(i)

                return render(request, 'ENnashmi/TeachersAPI/mainpagetecher.html',{'user':user1,'countofstd':stdcount(request,user.id),'message1':len(list1) })

            except models.Addtecher.DoesNotExist:
                try:
                    request.session['user_id'] = user.id

                    user=models.student.objects.get(id=user.id)
                    user1=models.atdence.objects.filter(sdtid=user)
                    user2=models.rateandexam.objects.filter(stduentid=user).aggregate(Sum('points'))
                    print(user2)
                    user3=models.rateandexam.objects.filter(stduentid=user).aggregate(Sum('behavior'))
                    print(user3)
                    user4=models.rateandexam.objects.filter(stduentid=user).aggregate(Sum('pagenumber'))

                    for i in user1:
                        if i.stuts=='tt':
                            i.stuts='حاضر'
                        else:
                            i.stuts='غايب'
                    return render(request,'ENnashmi/stdAPI/STDAPI.html',{'user1':user1,'user2':user2,'user3':user3,'user4':user4})
                except models.student.DoesNotExist:
                    try:
                        request.session['user_id'] = user.id


                        user3=models.addadmin.objects.get(id=user.id)
                        auth.login(request,user)
                        user2 = models.Addtecher.objects.all()
                        print(len(user2))
                        user3 = models.student.objects.all()
                        print(len(user3))

                        return  render(request,'ENnashmi/ADMINAPI/admindashboard.html',{'user2':len(user2),'user3':len(user3)})
                    except models.addadmin.DoesNotExist:
                        return HttpResponse('خطا')
        else:
            return redirect('login')


    else:
        return render(request,'ENnashmi/login.html',{})


@login_required()
def tech(request):
    a=request.session.get('user_id')
    user1=models.message.objects.all()
    user2=models.Addtecher.objects.get(id=a)
    dd=stdcount(request,a)
    user=User.objects.get(id=a)
    users = models.message.objects.raw('SELECT * FROM ennashmi_message WHERE date1=%s AND t2=%s',
                                       [date.today(), user.username])

    list1 = []
    for i in users:
        list1.append(i)

    print("sss",dd)
    return render(request,'ENnashmi/TeachersAPI/mainpagetecher.html',{'new':user1,'user':user2,'countofstd':dd,'message1':len(list1)})

@login_required()
def adminpage(request):

    std=models.student.objects.all()
    tech=models.Addtecher.objects.all()
    return render(request,'ENnashmi/ADMINAPI/mainpageadmin.html',{'std':len(std),'tech':len(tech)})

def adminreg(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']

        #username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phonenumber = request.POST['phonenumber']
        if(password1==password2):
            all=User.objects.all()
            for i in all:
                if i.username==email:
                    messages.error(request,email+"يوجد ادمن مكرر بهذا الاسم الرجاء تغيير البريد الالكتروني")
                    return render(request, 'ENnashmi/ADMINAPI/Add.html', {})
                else:
                    pass
            user = User.objects.create_user(username=email,email=email, password=password1, first_name=first_name)

            user.save();
            user1 = models.addadmin(user=user, stuts='admin', phonenumber=phonenumber, id=user.id)

            user1.save();
            messages.success(request, "تمت اضافة الادمن بنجاح بنجاح")
            return render(request,'ENnashmi/ADMINAPI/Add.html',{})
        else:
            messages.error(request,"<h1>خطا في تاكيد كلمة سر الرجاء ادخال كلمة سر بشكل صحيح</h1>")

    else:
        return render(request,'ENnashmi/ADMINAPI/Add.html',{})
@login_required()
def addtecher1(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']

       # username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phonenumber = request.POST['phonenumber']

        if password1==password2:
            all=User.objects.all()
            for i in all:
                if i.username==email:
                    messages.error(request,"يوجد تكرار في البريد الالكتروني الرجاء تفيير البريد الالكتروني")
                    return render(request,'ENnashmi/ADMINAPI/AddTech.html',{})
                else:
                    pass
            if (phonenumber[0]=='+' or phonenumber[0]=='0') and phonenumber[1:].isdigit()==True:


                user = User.objects.create_user(username=email,email=email, password=password1, first_name=first_name)

                user.save();

                user1 = models.Addtecher(user=user, stuts='techer', phonenumber=phonenumber, id=user.id)

                user1.save();
                messages.success(request,'تم اضافة المعلم في نجاح')
                return render(request, 'ENnashmi/ADMINAPI/AddTech.html', {})
            else:
                messages.success(request, 'الرجاء كتابة رقم الهاتف بشكل صحيح مبدتئا اما بصفر او +')

                return render(request,'ENnashmi/ADMINAPI/AddTech.html',{})


        else:
            messages.error(request,'خطا في كلمة سر')
            return render(request, 'ENnashmi/ADMINAPI/AddTech.html', {})
    else:
        return render(request,'ENnashmi/ADMINAPI/AddTech.html',{})
@login_required()
def std1(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']

        #dsec = request.POST['dsec']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phonenumber = request.POST['phonenumber']
        grade=request.POST['grade']
        date=request.POST['date']

        addte=request.POST.get('addte')
        print('theid'+addte)
        if password1==password2:


            all=User.objects.all()
            for i in all:
                if i.username ==email:
                    messages.error(request,'يوجد ايميل مكرر الرجاء تفغيير العنوان البريدي')
                    user = models.Addtecher.objects.all()
                    return render(request, 'ENnashmi/ADMINAPI/AddStd.html', {'new': user})

                else:
                        pass
            all1=models.student.objects.all()


            for i in range(0,len(phonenumber)):

                if(phonenumber[0]=='+' or phonenumber[0]=='0'):
                    pass
                else:
                    user = models.Addtecher.objects.all()
                    messages.error(request,'الرجاء بداية رقم الهاتف اما بصفر او +')
                    return render(request, 'ENnashmi/ADMINAPI/AddStd.html', {'new': user})
            if phonenumber[1:].isdigit()==False:
                user = models.Addtecher.objects.all()
                messages.error(request,'الرجاء اكتب رقم الهاتف بشكل صحيح ')
                return render(request, 'ENnashmi/ADMINAPI/AddStd.html', {'new': user})




            user = User.objects.create_user(username=email, password=password1, first_name=first_name)

            user.save();
            user2=models.Addtecher.objects.get(id=addte)

            user1 = models.student(id=user.id,user=user, stuts='std', phonenumber=phonenumber, techer=user2,grade=grade,date=date)


            user1.save();
            messages.success(request,'تمت اضافة الطالب بنجاح')
            user = models.Addtecher.objects.all()
            return render(request, 'ENnashmi/ADMINAPI/AddStd.html', {'new': user})
        else:
            messages.error(request, 'الرجاء تكرار كلمة سر')
            user = models.Addtecher.objects.all()
            return render(request, 'ENnashmi/ADMINAPI/AddStd.html', {'new': user})



    else:
        user=models.Addtecher.objects.all()
        return render(request,'ENnashmi/ADMINAPI/AddStd.html',{'new':user})
@login_required()
def techdispaly(request):
    tech=models.Addtecher.objects.all()
    return render(request,'ENnashmi/ADMINAPI/teachersdisplay.html',{'new':tech})
@login_required()
def std1display(request):
    if request.method=='POST':
        TECH = request.POST.get('TECH')
        print(TECH)

        std12=models.student.objects.filter(techer=TECH)
        user = models.Addtecher.objects.all()
        return render (request,'ENnashmi/ADMINAPI/studentsdisplay.html',{'new':std12,'tech':user})
    else:
        user=models.Addtecher.objects.all()
        return render(request,'ENnashmi/ADMINAPI/studentsdisplay.html',{'tech':user})
@login_required()
def searchadmin(request):
    ss1=request.POST.get('ss1')
    print(ss1)
    user = User.objects.filter(username=ss1)

    ss1 = 0
    for i in user:
        print(i)
        ss1 = i.id
        print('the id is ',i.id)
    ss=ss1
    print(ss)

    try:
        user1=models.student.objects.get(id=ss)
        new2=models.atdence.objects.extra(where=["sdtid_id='%s'","stuts='ff'"],params=[ss]).aggregate(Count('stuts'))
        new3=models.rateandexam.objects.filter(stduentid=ss).aggregate(Sum('points'),Sum('pagenumber'),Sum('behavior'))
        return render(request,'ENnashmi/ADMINAPI/searchbarstd.html',{'new':user1,'new2':new2,'new3':new3})
    except models.student.DoesNotExist:

        try:
            print(ss)
            user1 = models.Addtecher.objects.get(id=ss)
            return render(request, 'ENnashmi/ADMINAPI/searchbarteacher.html', {'new': user1})

        except models.Addtecher.DoesNotExist:
            return HttpResponse('لايوجد طالب او معلم بهذا الاسم')



@login_required
def edit(request):
    a=request.session.get('user_id')
    user2=models.Addtecher.objects.get(id=a)

    return render(request, 'ENnashmi/TeachersAPI/addstudent.html', {'new':user2})

@login_required
def register1(request):
    a=request.session.get('user_id')

    if request.method == 'POST':


        first_name = request.POST['first_name']
        email1 = request.POST['email']
        technid=request.POST.get('technid')
        print(email1)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phonenumber=request.POST['phonenumber']
        grade=request.POST['grade']
        date=request.POST['date']

        if password1==password2:
            if (phonenumber[0]=='+' or phonenumber[0]=='0') and phonenumber[1:].isdigit()==True:





                user2 = models.Addtecher.objects.get(id=a)

                user = User.objects.create_user(username=email1, password=password1, email=email1,first_name=first_name)
                user.save();

                user1=models.student(user=user,stuts='std',phonenumber=phonenumber,id=user.id,techer=user2,date=date,grade=grade)

                user1.save();
                messages.success(request,"تمت اضافة طالب بنجاح")
                return redirect('register12')



            else:
                messages.error(request, 'خطا في الرقم الرجاء كتابة الرقم بشكل صحيح مبدتئا بصفر او اشارة +')


        else:
            messages.error(request,"خطا في كلمة سر الرجاء اعادة كتاب كلمة سر مرة ثانية")

    else:

        return render(request, 'ENnashmi/TeachersAPI/addstudent.html', {})

    return render(request, 'ENnashmi/TeachersAPI/addstudent.html', {})

def logout(request):
    auth.logout(request)
    return redirect('login')
@login_required
def register12(request,id):
    user3 = models.Addtecher.objects.get(id=id)

    return render(request, 'ENnashmi/TeachersAPI/addstudent.html', {'new':user3})

@login_required
def displaystd(request):
    a=request.session.get('user_id')
    print(a)
    if request.method=='POST':


        dateof=request.POST.get('date1')
        techerof=request.POST.get('mo12')
        print(dateof)
        print(date.today())
        print(techerof)

        users = models.atdence.objects.raw('SELECT * FROM ennashmi_atdence WHERE date=%s AND techerid_id=%s AND stuts=%s',
                                         [dateof, a,'ff'])


        list1 = []
        for p in users:
            list1.append(p)
        for i in list1:
            if(i.stuts=='tt'):
                i.stuts='حاضر'
            elif(i.stuts=='ff'):

                i.stuts='غايب'
        print(users)
            #print(i.stduentid.user.first_name)


        return render(request,'ENnashmi/TeachersAPI/studentdisplayforteacher.html',{'users':list1,'new1':a,'new2':dateof})
    else:
        return render(request, 'ENnashmi/TeachersAPI/studentdisplayforteacher.html', {})
@login_required()
def testsandmarks(request):
    a=request.session.get('user_id')
    if request.method=='POST':
        stdid=request.POST.getlist('stdid[]')
        surah=request.POST.getlist('surah[]')
        pagenumber=request.POST.getlist('pagenumber[]')
        behv = request.POST.getlist('behv[]')
        points = request.POST.getlist('points[]')
        date1=request.POST.get('date1')

        print(stdid)
        print(surah)
        print(pagenumber)
        print(behv)
        print(points)
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        for i in range(0,len(stdid)):
            list1.append(int(stdid[i]))
            list2.append(str(surah[i]))
            list3.append(int(pagenumber[i]))
            list4.append(int(behv[i]))
            list5.append(int(points[i]))
        for i in range(0,len(list1)):
            tech=models.Addtecher.objects.get(id=a)
            user=models.student.objects.get(id=list1[i])
            new=models.rateandexam(Surah=list2[i],pagenumber=list3[i],date=date1,behavior=list4[i],points=list5[i],stduentid=user,techerid=tech)
            new.save()
        return redirect('/accounts/login/tech')



    else:

        new=models.atdence.objects.raw('SELECT * FROM ennashmi_atdence WHERE date=%s AND techerid_id=%s',[date.today(),a])
        list1=[]
        for p in new:
            list1.append(p)
        return render(request,'ENnashmi/TeachersAPI/testsandmarks.html',{'new':new,'new2':a})
@login_required
def deletestd(request,id):


    #print(ss)
    #ff=ss
    new=models.student(id=id)


    u1 = models.atdence(id=id)
    u1.delete()
    u2 = models.rateandexam(id=id)
    u2.delete()
    new.delete()
    u = User.objects.get(id=id)
    u.delete()


    return HttpResponse('تم حذف الطالب')

@login_required
def update(request,id):
    if request.method=='POST':

        new=models.student.objects.get(id=id)
        new.phonenumber=request.POST['phonenumber']
        print(new.phonenumber)
        new1=User.objects.get(id=id)
        new1.first_name = request.POST['first_name']
        new1.email = request.POST['email']
        new1.username=request.POST['email']
        new1.save()

        new.save()
        return redirect('/accounts/login/tech')
    else:

        return render(request,'ENnashmi/TeachersAPI/Editthepersonalinformationstd.html',{})
    return render(request, 'ENnashmi/TeachersAPI/Editthepersonalinformationstd.html', {})
@login_required
def update1(request,id):
    new=models.student.objects.get(id=id)
    return render(request,'ENnashmi/TeachersAPI/Editthepersonalinformationstd.html',{'new':new})

@login_required
def trans(request):
    if request.method=='POST':



        user2=User.objects.all()
        name=0

        for ss in user2:
            if(str(ss) == request.POST['t2']):
                name=ss.id


                print('techer',ss.id)
            else:
                pass
        user3=models.student.objects.all()
        for i in user3:

            if(i.user.username==request.POST['s1']):

                    user3=models.Addtecher.objects.get(id=name)
             #b = Blog.objects.get(name='Beatles Blog', tagline='All the latest Beatles news.')
                    print(user3)

                    i=models.student.objects.get(id=i.id)
                    i1=models.atdence.objects.filter(sdtid=i.id).update(techerid=user3)
                    i2=models.rateandexam.objects.filter(stduentid=i.id).update(techerid=user3)



                    i.techer=user3

                    i.save()
                   
                    print(i.id)
            else:
                pass
        ss=request.POST.get('reson')
        print(ss)
        user=models.message(std1=request.POST['s1'],t2=request.POST['t2'],reson=request.POST['reson'],date1=date.today())
        user.save()
        messages.success(request,'تم نقل طالب بنجاح')
        a = request.session.get('user_id')
        print('tt', a)

        user2 = models.student.objects.filter(techer=a)
        user3 = models.Addtecher.objects.all()
        return render(request, 'ENnashmi/TeachersAPI/transferstudenttootherteacher.html',
                      {'new': user2, 'new1': user3, 'new3': a})
    else:
        a = request.session.get('user_id')
        print('tt', a)

        user2 = models.student.objects.filter(techer=a)
        user3 = models.Addtecher.objects.all()

        return render(request, 'ENnashmi/TeachersAPI/transferstudenttootherteacher.html',
                      {'new': user2, 'new1': user3, 'new3': a})






@login_required
def admindashboard(request):
    user2=models.Addtecher.objects.all()
    print(len(user2))
    user3=models.student.objects.all()
    print(len(user3))

    return render(request,'ENnashmi/ADMINAPI/admindashboard.html',{'user2':len(user2),'user3':len(user3)})


@login_required
def attendece(request):
    a=request.session.get('user_id')

    if request.method=='POST':
        ss=request.POST.getlist('ss[]')
        ss1 = request.POST.getlist('ss1[]')
        ss2=request.POST.get('date1')
        user1=models.atdence.objects.filter(date=ss2)
        print(len(user1))
        print(ss2)
        print(ss)
        print(ss1)
        list1=[]
        list2=[]
        print(date.today())
        if len(user1)==0:

            for i in ss1:
                list1.append(int(i))
            for i in ss:
                list2.append(str(i))
            print(list1)
            print(list2)
            for i in range(0,len(list1)):
                user1=models.student.objects.get(id=list1[i])
                user2=models.Addtecher.objects.get(id=a)
                user=models.atdence(date=ss2,techerid=user2,stuts=list2[i],sdtid=user1)
                user.save()
            new = models.atdence.objects.raw('SELECT * FROM ennashmi_atdence WHERE date=%s AND techerid_id=%s AND stuts=%s',
                                         [ss2, a,'tt'])
            list1 = []
            for p in new:
                list1.append(p)
            return render(request, 'ENnashmi/TeachersAPI/testsandmarks.html', {'new': new, 'new2': a,'date1':ss2})
        else:
            return render(request, 'ENnashmi/TeachersAPI/attendence.html', {'message':'لقد اخذت تاريخ هذا بلفعل'})



    else:


        ss=models.student.objects.filter(techer=a)

        return render(request,'ENnashmi/TeachersAPI/attendence.html',{'new':ss,'new1':id})


@login_required
def serachbar(request):
    a=request.session.get('user_id')
    ss=request.POST.get('ss1')
    print(ss)

    print(ss)
    name=5
    new1=models.student.objects.raw('SELECT * FROM ennashmi_student s,auth_user u WHERE s.techer_id=%s  AND s.id=u.id  AND u.username=%s',[a,str(ss)])
    print(new1)
    list1=[]
    for i in new1:
        list1.append(i)
    if len(list1)!=0:

        from django.db.models import Count,Sum


        new2=models.atdence.objects.extra(where=["sdtid_id='%s'","stuts='ff'"],params=[list1[0].id]).aggregate(Count('stuts'))
        print(new2)
        print(list1[0].id)

        q = models.rateandexam.objects.filter(stduentid=list1[0].id).aggregate(Sum('pagenumber'),Sum('points'),Sum('behavior'))
        list2=[]
        for i in q.values():
            list2.append(i)

        print(list2)
        return render(request,'ENnashmi/TeachersAPI/Editthepersonalinformationstdsearch.html',{'new':list1,'new2':new2,'new3':list2})
    else:
        return HttpResponse('لا يوجد طالب بهذا الاسم')


def editpersonal(request,id):


    return render(request,'ENnashmi/TeachersAPI/Editthepersonalinformation.html',{})
@login_required
def displaystdrate(request):
    a=request.session.get('user_id')
    if request.method=='POST':



        dateof=request.POST.get('date1')
        techerof=request.POST.get('mo12')
        print(dateof)
        print(date.today())
        print(techerof)
        users = models.rateandexam.objects.raw('SELECT * FROM ennashmi_rateandexam WHERE date=%s AND techerid_id=%s',
                                         [dateof, a])
        list1 = []
        for p in users:
            list1.append(p)
        for i in list1:
            i.id
            #print(i.stduentid.user.first_name)
        if len(list1)==0:

            return render(request, 'ENnashmi/TeachersAPI/studentdisplayforteacher1.html', {'date1':dateof,'ss':'لا يوجد طلاب مقيمين في هذا تاريخ'})
        else:


            return render(request,'ENnashmi/TeachersAPI/studentdisplayforteacher1.html',{'users':list1,'new1':a,'date1':dateof})
    else:
        return render(request, 'ENnashmi/TeachersAPI/studentdisplayforteacher1.html', {})

@login_required()
def stdstudentdisplay(request,id):


    return render(request,'ENnashmi/stdAPI/STDAPI.html',{})

@login_required()
def displaystd121(request):
    a=request.session.get('user_id')
    user2 = models.student.objects.filter(techer=a)


    return render(request,'ENnashmi/TeachersAPI/displaystd121.html',{'new':user2,'new3':a})

@login_required()
def messageview(request):

    a=request.session.get('user_id')
    user=User.objects.get(id=a)

    users = models.message.objects.raw('SELECT * FROM ennashmi_message WHERE date1=%s AND t2=%s',
                                           [date.today(), user.username])

    list1=[]
    for i in users:
        list1.append(i)

    for i in list1:
        user=User.objects.get(username=i.std1)
        i.std1=user.first_name

    print(len(list1))

    return render(request,'ENnashmi/TeachersAPI/displaystd1211.html',{'new':list1})
def videoview(request):


    return render(request,'ENnashmi/V.html',{})


def uploadvideoview(request):


    return render(request,'ENnashmi/upload.html',{})

def stdvideo(request):
    if request.method=='POST':
        a=request.session.get('user_id')
        b=models.student.filter(id=a)
        myfile=request.POST['myfile']
        print(myfile)

        videofile=models.videostd(techer=b.id,stdname=a,date=date.today(),videoname='video',myfile=myfile)
        videofile.save()
        return HttpResponse('تم ارسال الفيديو')

    else:

        return render(request,'ENnashmi/stdAPI/video.html',{})


from .functions import handle_uploaded_file   # functions.py
from .forms import StudentForm  # forms.py

'''
def index(request):
    student = StudentForm()

    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)

        if student.is_valid():

            handle_uploaded_file(request.FILES['file'])
            model_instance = student.save(commit=False)
            model_instance.save()
            student = StudentForm()

            return redirect("/")

    else:
        student = StudentForm()
        return render(request, "ENnashmi/stdAPI/index.html", {'form': student})
ndex(request):
    if request.method=='POST':
        print('monther')
        ss = models.student.objects.get(id=request.session.get('user_id'))
        handle_uploaded_file(request.FILES['file'],request.session.get('user_id'),date.today())

        user1=models.StudentForm(date=date.today(),stuentid=request.session.get('user_id'),Addtecher=ss.techer,file=handle_uploaded_file(request.FILES['file'],request.session.get('user_id'),date.today()))
        user1.save()
        return HttpResponse('file upload')
    else:
        return render(request, "ENnashmi/stdAPI/video.html", {})'''


def index(request):
    if request.method=='POST':
        uploadfile=request.FILES['doc']



        if '.mp4' in uploadfile.name or '.3gp' in uploadfile.name or '.wmv' in uploadfile.name:

            name = request.session.get('user_id')
            std = models.student.objects.get(id=name)
            uploadfile1 = uploadfile.name.split('.')
            uploadfile1[0] =str(name)+str(date.today())
            q = models.StudentForm1.objects.filter(stduentid=name).aggregate(Count('stduentid_id'))
            print(q)

            ss = uploadfile1[0]+str(q.values()) + '.' + uploadfile1[1]
            new=models.StudentForm1(Addtecher=std.techer,stduentid=std,date=date.today(),file=ss)

            fs=FileSystemStorage()
            new.save()
            fs.save(ss,uploadfile)
        else:
            return HttpResponse('يجب تحميل فيديو فقط هذه صيغ فيديو')
    return render(request,'ENnashmi/stdAPI/video.html',{})


@login_required()
def videoview1(request):
    a=request.session.get('user_id')
    studetnview=models.StudentForm1.objects.filter(Addtecher=a)


    return render(request,'ENnashmi/TeachersAPI/video1.html',{'new':studetnview})
