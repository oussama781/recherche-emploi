from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login,logout
# Create your views here.
def index(request):
    d={'nbar': 'index'}
    return render(request,'index.html',d)

def admin_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except Exception as e:
            print(e)
            error="yes"

    d={"error":error,'nbar': 'admin_login'}
    return render(request,'admin_login.html',d)

def recruiter_signup(request):
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        comp=request.POST['company']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            try:
                i=request.FILES['image']
                Recruitor.objects.create(user=user,mobile=con,image=i,company=comp,gender=gen,type="recruiter",status="pending")
            except:
                Recruitor.objects.create(user=user,mobile=con,company=comp,gender=gen,type="recruiter",status="pending")
            error="no"
        except Exception as e:
            print("Error: ",e)
            error="yes"
    d={'error':error}
    return render(request,'recruiter_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        try:
            student.user.save()
            student.save()

            error="no"
        except Exception as e:
            print(e)
            error="yes"
        try:
            i=request.FILES['image']
            student.image=i
            student.save()
        except Exception as e:
            print(e)
            pass
    d={'student':student,'error':error,'nbar':'user_home'}
    return render(request,'user_home.html',d)


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruitor.objects.get(user=user)
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con
        recruiter.gender=gen
        try:
            recruiter.user.save()
            recruiter.save()

            error="no"
        except Exception as e:
            print(e)
            error="yes"
        try:
            i=request.FILES['image']
            recruiter.image=i
            recruiter.save()
        except Exception as e:
            print(e)
            pass
    d={'recruiter':recruiter,'error':error,'nbar':'recruiter_home'}
    return render(request,'recruiter_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    rcount=Recruitor.objects.all().count()
    scount = StudentUser.objects.all().count()
    prcount = Recruitor.objects.filter(status="pending").count()
    arcount = Recruitor.objects.filter(status="Accept").count()
    rrcount = Recruitor.objects.filter(status="Reject").count()
    jcount = Job.objects.all().count()
    mcount = Contact.objects.all().count()
    d = {'rcount':rcount,'scount':scount,'nbar': 'home','prcount':prcount,'arcount':arcount,'rrcount':rrcount,'jcount':jcount,'mcount':mcount}
    return render(request,'admin_home.html',d)



def recruiter_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1=Recruitor.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request,user)
                    error="no"
                else:
                    error="not"
            except Exception as e:
                print(e)
                error="yes"
        else:
            error="yes"

    d={"error":error,'nbar': 'recruiter_login'}

    return render(request,'recruiter_login.html',d)

def user_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except Exception as e:
                print(e)
                error="yes"
        else:
            error="yes"

    d={"error":error,'nbar':"user_login"}
    return render(request,'user_login.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def user_signup(request):
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']

        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p,)
            try:
                i=request.FILES['image']
                StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student")
            except Exception as e:
                StudentUser.objects.create(user=user,mobile=con,gender=gen,type="student")
            error="no"
        except Exception as e:
            print(e)
            error="yes"
    d={'error':error}

    return render(request,'user_signup.html',d)



def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    data = StudentUser.objects.all()
    d={'data':data,'nbar': 'views_users'}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')



def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    data = Recruitor.objects.filter(status="pending")
    d={'data':data,'nbar':'recruiter_pending'}
    return render(request,'recruiter_pending.html',d)


def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = Recruitor.objects.get(id=pid)
    error=""
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    data = Recruitor.objects.filter(status="Accept")
    d={'data':data,'nbar':'recruiter_accepted'}
    return render(request,'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruitor.objects.filter(status="Reject")
    d={'data':data,'nbar':'recruiter_rejected'}
    return render(request,'recruiter_rejected.html',d)

def all_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    data = Recruitor.objects.all()
    d={'data':data,'nbar':'all_recruiters'}
    return render(request,'all_recruiters.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('all_recruiters')

def delete_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    job = Job.objects.get(id=pid)
    job.delete()
    return redirect('job_list')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error,'nbar':'change_passwordadmin'}
    return render(request,'change_passwordadmin.html',d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error,'nbar':'change_passworduser'}
    return render(request,'change_passworduser.html',d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error,'nbar':'change_passwordrecruiter'}
    return render(request,'change_passwordrecruiter.html',d)

from datetime import date
def add_job(request):
    error=""
    if request.method=="POST":
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        l=request.FILES['logo']
        sal=request.POST['salary']
        loc=request.POST['location']
        exp=request.POST['experience']
        skills=request.POST['skills']
        des=request.POST['description']
        user = request.user
        recruiter = Recruitor.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,image=l,salary=sal,location=loc,experience=exp,skills=skills,description=des,creationdate=date.today())
            error="no"
        except Exception as e:
            print(e)
            error="yes"
    d={'error':error,'nbar':'add_job'}
    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruitor.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    print(job)
    d={'job':job,'nbar':'job_list'}
    return render(request,'job_list.html',d)

def admin_joblist(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('Logout')
    job = Job.objects.all()
    print(job)
    d={'job':job,'nbar': 'admin_joblist'}
    return render(request,'admin_joblist.html',d)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']

        sal=request.POST['salary']
        loc=request.POST['location']
        exp=request.POST['experience']
        skills=request.POST['skills']
        des=request.POST['description']

        job.title =jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error="no"
        except Exception as e:
            print(e)
            error="yes"
        if sd:
            try:
                job.start_date =sd
                job.save()
            except:
                pass
        else:
            pass

        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass

        try:
            l=request.FILES['logo']
            job.image=l
            job.save()
        except:
            pass

    d={'error':error,'job':job}
    return render(request,'edit_jobdetail.html',d)

def edit_jobdetail_admin(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']

        sal=request.POST['salary']
        loc=request.POST['location']
        exp=request.POST['experience']
        skills=request.POST['skills']
        des=request.POST['description']

        job.title =jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error="no"
        except Exception as e:
            print(e)
            error="yes"
        if sd:
            try:
                job.start_date =sd
                job.save()
            except:
                pass
        else:
            pass

        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass

        try:
            l=request.FILES['logo']
            job.image=l
            job.save()
        except:
            pass

    d={'error':error,'job':job}
    return render(request,'edit_jobdetail_admin.html',d)


def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        l=request.FILES['logo']
        if l:
            try:
                job.image=l
                job.save()
                error="no"
            except:
                error="yes"
        else:
            error="no"

    d={'error':error,'job':job}
    return render(request,'change_companylogo.html',d)


def latest_jobs(request):
    data=Job.objects.all().order_by('-start_date')
    d={'data':data,'nbar': 'latest_jobs'}
    return render(request,'latest_jobs.html',d)

def user_latestjobs(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li':li,'nbar':'user_latestjobs'}
    return render(request,'user_latestjobs.html',d)


def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    d={'job':job}
    return render(request,'job_detail.html',d)


def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login',{'nbar': 'home'})
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date>date1:
        error="notopen"
    else:
        if request.method=="POST":
            r=request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
            error="done"

    d={'error':error}
    return render(request,'applyforjob.html',d)


def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
        if not user.is_staff:
            return
    data=Apply.objects.all()

    d={'data':data,'nbar':'applied_candidatelist'}
    return render(request,'applied_candidatelist.html',d)


def contact(request):
    error=""
    if request.method=="POST":
        e=request.POST['email']
        sub=request.POST['subject']
        msg=request.POST['message']
        try:
            Contact.objects.create(email=e,subject=sub,message=msg)
            error="no"
        except Exception as e:
            print("Error: ",e)
            error="yes"
    c = {'error':error,'nbar': 'contact' }
    return render(request,'contact.html',c)


def messages(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    messages = Contact.objects.all()
    d={'messages':messages,'nbar':'messages'}
    return render(request,'messages.html',d)
