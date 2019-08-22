from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm, EditForm, RatingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from .models import Student, Teacher, Search_Code, Rating, Role
import random, string
import datetime
from django.utils import timezone
from datetime import date


# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return redirect('/login')



def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request, "Authenticated Successfully.")
                    return redirect("/")

                    return 
                else:
                    messages.error(request, "Disabled Account.")
                    return redirect('/login')
            else:
                messages.error(request, "Invalid login.")
                return redirect('/login')
    else:
        form = LoginForm()
        r_form = RegistrationForm()
    return render(request, 'registration/login_register.html',{'form':form,'r_form':r_form})


def user_registration(request):
    if request.method=='POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            u_role = request.POST['role']
            print(u_role)
            if u_role =='student':
                Student.objects.create(u = new_user)
                Role.objects.create(u = new_user, my_role = 'student')
            else:
                Teacher.objects.create(u = new_user)
                Role.objects.create(u=new_user, my_role='teacher')


            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('registration/activate_account.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'account/register_done.html',{'new_user':new_user})
        else:
            r_form = RegistrationForm()
            form = LoginForm()
            return render(request,'registration/login_register.html',{'r_form':r_form,'form':form})
    r_form = RegistrationForm()
    form = LoginForm()
    return render(request, 'registration/login_register.html',{'r_form':r_form,'form':form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required
def student_dashboard(request):
    role = 'Student'
    ratings = Rating.objects.filter(u = request.user, active = True)
    sc = Search_Code.objects.filter(u__id = request.user.id).order_by('-created')[0]
    rc = Rating.objects.filter(u__id = request.user.id).order_by('-created')[0]
    attnt = 0
    prfrm = 0
    punct = 0
    coop = 0
    count = 0
    print('Ratings: ',ratings)
    for r in ratings:
        if r.attention:
            attnt += r.attention
            prfrm += r.performance
            punct += r.punctuality
            coop += r.cooperation
            count +=1
    if count>0:
        attnt = attnt/ count 
        prfrm = prfrm/ count
        punct = punct/ count
        coop = coop / count

    

    return render(request, 'newbase.html',{'role':role, 'attnt':attnt,'prfrm':prfrm,'punct':punct,'coop':coop,
    'ratings':ratings,'sc':sc,'rc':rc})



@login_required
def teacher_dashboard(request):
    cd = None
    rating = False
    role = 'Teacher'
    tchr = Teacher.objects.filter(u__id=request.user.id)
    if tchr != []:
        print('Teacher:',tchr)
        if tchr[0].search_count == None:
            search_count = 0 
        else:
            search_count = tchr[0].search_count
    rating_profiles = request.user.given_rating.filter(active=True)


    return render(request,'teacher_profile.html',{'role':role,'search_count':search_count,'cd':cd,'rating':rating,
     'rating_profiles':rating_profiles}) 


@login_required
def dashboard(request):
    cd = None
    if request.user.is_superuser:
        return redirect('admin/')
    
    elif request.user.roly.my_role =='student':
        return redirect('student_dashboard/')
    else:
        return redirect('teacher_dashboard/')

    
        



@login_required
def edit(request):
    if request.method=='POST':
        user_form = EditForm(instance = request.user, data = request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,"Changes saved successfully.")
            return redirect('/edit')
        else:
            messages.error(request,"Please enter correct values.")
            user_form = EditForm(instance = request.user)
    user_form = EditForm(instance = request.user)
    return render(request, 'new_edit.html',{'user_form':user_form})


@login_required
def create_code(request):
    random_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
    r = False
    if request.GET.get('rating') =='Yes':
        r = True
    srch_code = Search_Code.objects.create(u= request.user, code = random_code)
    messages.success(request,"Search code generated.")

    return redirect('/')

@login_required
def rating_code(request):
    random_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
    rating_code = Rating.objects.create(u = request.user, code=random_code)
    return redirect('/')


@login_required
def search(request):
    return render(request,'search.html')


@login_required
def search_student(request):
    if request.user.roly.my_role =='teacher':
        role = 'Student'
        
        s = request.GET.get('code')
        rtng = False
        rate_code = Rating.objects.filter(code = s)
        print(rate_code)
        print('Length: ',len(rate_code))
        if len(rate_code)>0:
            rc = ''
            rtng = True
            print('Rating',rtng)
            r = get_object_or_404(Rating, code = s, active=True)
            if not r.u.is_active:
                return HttpResponse("That student is banned.")
            if r.teacher:
                return HttpResponse("Ask the student for new rating code.")
            stdnt = r.u
            name = r.u.get_full_name()
            rgstrd = r.u.date_joined
            attnt = 0
            prfrm = 0
            punct = 0
            coop = 0
            count = 0
            ratings = Rating.objects.filter(u = r.u, active = True)
            for r in ratings:
                if r.attention:
                    attnt += r.attention
                    prfrm += r.performance
                    punct += r.punctuality
                    coop += r.cooperation
                    count +=1
            if count>0:
                attnt = attnt/ count 
                prfrm = prfrm/ count
                punct = punct/ count
                coop = coop / count
        else:

            sc = get_object_or_404(Search_Code, code = s)
            now = timezone.now()
            diff = now - sc.created
            seconds = diff.seconds
            hours = seconds/60/60
            print("hours:", hours)
            if hours > 240.0:
                return HttpResponse("The code has been expired.")
        
            ratings = Rating.objects.filter(u = sc.u, active = True)
            stdnt = sc.u
            name = sc.u.get_full_name()
            rgstrd = sc.u.date_joined
            rc = Rating.objects.filter(u__id = stdnt.id).order_by('-created')[0]
            attnt = 0
            prfrm = 0
            punct = 0
            coop = 0
            count = 0
            print('Ratings: ',ratings)
            for r in ratings:
                if r.attention:
                    attnt += r.attention
                    prfrm += r.performance
                    punct += r.punctuality
                    coop += r.cooperation
                    count +=1
            if count>0:
                attnt = attnt/ count 
                prfrm = prfrm/ count
                punct = punct/ count
                coop = coop / count
            t = Teacher.objects.get(u = request.user)
            s_count = t.search_count
            if s_count ==None:
                s_count = 0
            s_count +=1
            t.search_count = s_count
            t.save()
            sc.accessed_by = request.user
            sc.accessed_date = timezone.now()
            sc.save()

        return render(request,'account/student_profile.html',{'role':role, 'attnt':attnt,'prfrm':prfrm,'punct':punct,'coop':coop,
    'ratings':ratings,'rc':rc,'name':name,'rgstrd':rgstrd,'rtng':rtng,'stdnt':stdnt,'s':s})


@login_required
def ssearch_student(request):
    sc = 0
    std = 0
    ratings = []
    if request.user.roly.my_role =='teacher':
        s = request.GET.get('code')
        print(request.GET)
        
        sc = get_object_or_404(Search_Code, code=s)
        
        now = timezone.now()
        diff = now - sc.created
        seconds = diff.seconds
        hours = seconds/60/60
        print("Hours:", hours)
        if hours > 240.0:
            messages.error(request,'Code has been expired')
            return redirect('teacher_dashboard')
        

        
                                                                                                 
        #sc = Search_Code.objects.get(code=s)
        print('Code User: ',sc.u)
        std = sc.u
        t = Teacher.objects.get(u = request.user)
        s_count = t.search_count
        if s_count ==None:
            s_count = 0
        s_count +=1
        t.search_count = s_count
        t.save()

        student = Student.objects.get(u = sc.u)
        ca_count = student.code_count
        print("CA count", ca_count)
        if ca_count == None:
            ca_count = 0
        ca_count +=1
        student.code_count = ca_count
        student.save()
        sc.accessed_by.add(request.user)

        ratings = Rating.objects.filter(u = sc.u, active=True).order_by('-created')[:5]
        
    return render(request,'account/student_profile.html',{'sc':sc,'std':std,'ratings':ratings})



@login_required
def student_rating(request):
    if request.user.roly.my_role == 'teacher':
        r = request.GET.get('ratings')
        print(r)
        custId = request.GET.get('custId')
        code = request.GET.get('code')
        attnt = int(request.GET.get('attnt'))
        prfrm = int(request.GET.get('prfrm'))
        punct = int(request.GET.get('punct'))
        coop = int(request.GET.get('coop'))
        rating = attnt + prfrm + punct + coop
        rating = rating/4

        print('CustId: ',custId,'attnt: ',attnt,'prfrm: ',prfrm,'punct: ',punct,'coop: ',coop)
        u = get_object_or_404(User, username = custId)
        dt = str(date.today())
        rt = get_object_or_404(Rating,u = u, code=code)
        if rt.teacher:
            return redirect('teacher_dashboard')
        if rt.teacher == request.u:
            return HttpResponse("You cannot use this rating code once again.")
        rt.teacher = request.user
        rt.rating = rating
        rt.attention = attnt
        rt.performance = prfrm
        rt.punctuality = punct
        rt.cooperation = coop
        rt.rated = dt
        rt.active = False
        rt.save()
        t = Teacher.objects.get(u = request.user)
        r_count = t.rating_count
        if r_count ==None:
            r_count = 0
        r_count +=1
        t.rating_count = r_count
        t.save()
        return redirect('teacher_dashboard')



