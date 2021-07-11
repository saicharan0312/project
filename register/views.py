from django.shortcuts import render
from django.contrib import messages
from .forms import IndividualForm, CorporateForm, editprofileform
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from .models import Individual, Corporate, vote
from .models import User
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import IndividualForm, CorporateForm, event_creation, editform, eventform,EventRegister,Eventcool
from django.db.models import Count

def event_register(request):
    if request.method == "POST":
        if request.user.is_corporate:
            form= Eventcool(request.POST)
            if(form.is_valid()):
                form.save()
        else:
            form =EventRegister(request.POST)
            if(form.is_valid()):
                form.save()
        return redirect('accounts:Index')

    if request.user.is_corporate:
        form = Eventcool()
    else:
        form = EventRegister()

    return render(request,'register/event_register.html',{'form':form})




def index(requests):
    event_o = event_creation.objects.filter(user__username=requests.user)
    eventobj = event_creation.objects.exclude(user__username__contains=requests.user)

    if(requests.method=='GET'):
        if 'title' in requests.GET:
            event_o=event_o.order_by('event_name')
            eventobj = eventobj.order_by('event_name')

        if 'pub_date' in requests.GET:
            pass
            #event_o = event_o.order_by('event_name')
            #eventobj = eventobj.order_by('event_name')
        if 'num_votes' in requests.GET:
            event_o =event_o.annotate(Count('vote')).order_by('-vote__count')

        if 'search' in requests.GET:
            search=requests.GET['search']
            event_o=event_o.filter(event_name__icontains=search)




    paginator = Paginator(event_o, 5)
    page = requests.GET.get(' page')
    event_o = paginator.get_page(page)

    if requests.method == 'POST':
        print(requests.path)
        id = requests.POST['id']
        o = event_creation.objects.get(id=id)
        if not o.user_can_vote(requests.user):
            messages.error(requests, 'Already voted!')
            return render(requests, 'register/index1.html', {'myself': event_o, 'others': eventobj})
        new_vote = vote(user=requests.user, event=o)
        new_vote.save()
        o.numv = o.numv + 1
        o.save()

    else:
        pass


    return render(requests, 'register/index1.html', {'myself': event_o, 'others': eventobj})


@login_required
def detail(request, id):
    obj = get_object_or_404(event_creation, id=id)
    return render(request, 'register/detail.html', {'obj': obj})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'register/password_changeform.html', {'form': form})


@login_required
def edit_event(request, id):
    print(id)
    obj = get_object_or_404(event_creation, id=id)
    print(obj)
    if request.user != obj.user:
        return redirect('/')

    if request.method == 'POST':
        form = editform(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details updated!!', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('accounts:Index')

    else:
        form = editform(instance=obj)
    return render(request, 'register/edit_event_form.html', {'form': form})


@login_required
def event(request):
    print(request.user.username)
    form = eventform()
    if request.method == 'POST' and request.user.is_authenticated:
        print(request.POST)

        u = eventform(request.POST)
        # __mail(request.POST['event_name'])
        if u.is_valid():
            o = request.user
            c = u.save(commit=False)
            c.user = o
            c.save()
        messages.success(request, 'Details updated!!', extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('accounts:Index')
    return render(request, 'register/event_form.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = editprofileform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'register/index1.html', {})
    else:
        form = editprofileform(instance=request.user)
        args = {'form': form}
        return render(request, 'register/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == "POST":
        print(request.POST)
        form = PasswordChangeForm(user=request.user, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            print("cool")
            print(request.user)
            update_session_auth_hash(request, form.user)
            return render(request, 'register/index1.html', {})
            # render(request,'register/edit_profile.html',{})
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'register/change_password.html', args)


class Thanks(TemplateView):
    template_name = "register/thanks.html"


class index1(TemplateView):
    template_name = 'register/index1.html'


def Register(request):
    context = {}
    l = len(request.POST)
    print(l)
    u = 0
    if request.method == 'POST' and 'gender' not in request.POST:
        if l == 10:
            print(request.POST)
            print(request.FILES)
            u = IndividualForm(request.POST, request.FILES)
            print(u.is_valid())
            print(u.errors)
            context['errors'] = u.errors
            if u.is_valid():
                username = u.cleaned_data['user_name']
                pass_word = u.cleaned_data['pass_word']
                enc_password = make_password(pass_word)
                user = User(username=username, password=enc_password)
                user.is_individual = True
                user.is_corporate = False
                user.save()
                print(user)
                use = User.objects.get(username=username)
                c = u.save(commit=False)
                c.user = use
                c.save()
                messages.success(request, 'Thanks for registring {}'.format(username))
                return redirect('accounts:Login')
        else:
            print('*********COOL***********')
            print(request.POST)
            u = CorporateForm(request.POST)
            if u.is_valid():
                username = u.cleaned_data['company_name']
                pass_word = u.cleaned_data['pass_word']
                enc_password = make_password(pass_word)
                user = User(username=username, password=enc_password)
                user.is_individual = False
                user.is_corporate = True
                user.save()
                print(user)
                use = User.objects.get(username=username)
                c = u.save(commit=False)
                c.user = use
                c.save()
                messages.success(request, 'Thanks for registring {}'.format(username))
                return redirect('accounts:Login')

    else:
        print(request.POST)
        context['gender'] = 1
        print(request.POST.get('gender'), type(request.POST.get('gender')))
        if (request.POST.get('gender') == 'male'):
            context['gender'] = 1
        elif request.POST.get('gender') == 'female':
            context['gender'] = 0

        print('hello', context['gender'])

        if context.get('gender') == 1:
            form = IndividualForm()
            context['form'] = form
        elif context.get('gender') == 0:
            form = CorporateForm()
            context['form'] = form
        print(context)

    if 'errors' in context:
        context['form'] = IndividualForm
        context['gender'] = 1
        print(context)
    return render(request, 'register/register_form.html', context)


class Login(View):
    def post(self, requests, *args, **kwargs):
        print(requests.user)
        print(requests.method)
        print(requests.POST)
        l = len(requests.POST)
        if requests.method == 'POST' and 'gender' not in requests.POST:
            if l == 3:
                username = requests.POST.get('username')
                password = requests.POST.get('password')
                print(username)
                print(password)
                user = authenticate(requests, username=username, password=password)
                print(user)

                if user is not None:
                    print("sdkjakj")
                    u = User.objects.get(username=username)

                    # if u.is_individual == True and u.is_corporate == False:
                    print("cool!")
                    login(requests, user)
                    return redirect('accounts:Index')
                else:
                    print("fasjk")
                    messages.error(requests, 'Bad request')
                    return redirect('accounts:Login')
            else:
                print("else ...man! ")
                username = requests.POST.get('username')
                password = requests.POST.get('password')
                cin = requests.POST.get('cin')
                print(username)
                print(password)
                user = authenticate(requests, username=username, password=password)
                print(user)
                if user is not None:
                    u = Corporate.objects.get(company_name=username)
                    if u.CIN == cin:
                        login(requests, user)
                    else:
                        messages.error(requests, 'Bad request')
                        return redirect('accounts:Login')

                    return redirect('accounts:Index')
                else:
                    messages.error(requests, 'Bad request')
                    return redirect('accounts:Login')

        else:
            context = {}
            if (requests.POST.get('gender') == 'male'):
                context['gender'] = 1
            elif requests.POST.get('gender') == 'female':
                context['gender'] = 0

            context['form'] = None
            if context.get('gender') == 1:
                form = IndividualForm()
                context['form'] = form
            elif context.get('gender') == 0:
                form = CorporateForm()
                context['form'] = form
        return render(requests, 'register/login_form.html', context)

    def get(self, requests, *args, **kwargs):
        return render(requests, 'register/login_form.html', {'gender': 1})


class Logout(View):
    def get(self, requests, *args, **kwargs):
        logout(requests)
        return redirect('accounts:Index')

    '''


    def post(self, request, *args, **kwargs):
        context={}
        if request.method=='POST' and 'gender' not in request.POST:
            l=len(request.POST)
            if l == 4:
                u = IndividualForm(request.POST,request.FILES)
                print(u.is_valid())
                if u.is_valid():
                    username = u.cleaned_data['user_name']
                    pass_word = u.cleaned_data['pass_word']
                    enc_password=make_password(pass_word)
                    user = User(username=username, password=enc_password)
                    user.is_individual = True
                    user.is_corporate = False
                    user.save()
                    print(user)
                    use = User.objects.get(username=username)
                    c=u.save(commit=False)
                    c.user = use
                    c.save()
                    messages.success(request, 'Thanks for registring {}'.format(username))
                    return redirect('accounts:Login')
            else:
                u = CorporateForm(request.POST)
                if u.is_valid():
                    username = u.cleaned_data['user_name']
                    pass_word = u.cleaned_data['pass_word']
                    enc_password = make_password(pass_word)
                    user = User(username=username, password=enc_password)
                    user.is_corporate = True
                    user.save()
                    c = u.save(commit=False)
                    use = User.objects.get(username=username)
                    c.user = use
                    c.save()
                    messages.success(request, 'Thanks for registring {}'.format(username))
                    messages.success(request, 'Thanks for registring {}'.format(username))
                    return redirect('accounts:Login')

        else:
            if (request.POST.get('gender') == 'male'):
                context['gender'] = 1
            elif request.POST.get('gender') == 'female':
                context['gender'] = 0

            context['form'] = None
            if context.get('gender') == 1:
                form = IndividualForm()
                context['form'] = form
            elif context.get('gender') == 0:
                form = CorporateForm()
                context['form'] = form
        return render(request, 'register/register_form.html', context)




    def get(self,request,*args,**kwargs):
        context={}
        return render(request, 'register/register_form.html', context)



    









===========================================================
          context = {}
    l=len(request.POST)
    print(l)
    if request.method=='POST' and 'gender' not in request.POST:
        if l<=5:
            print(request.POST)
            u = IndividualForm(request.POST)
            print(u.is_valid())
            print(u.errors)
            if u.is_valid():
                user_id=u.cleaned_data['user']
                username = u.cleaned_data['user_name']
                pass_word = u.cleaned_data['pass_word']
                status =u.cleaned_data['status']
                print(u.cleaned_data)
                user = User.objects.create_user(username=username, password=password)
                new_individual =User.objects.create_user(username='pop',password='popsagar')
                new_individual =u.save()
                print("helo", new_individual,username,pass_word,status)
                #print(user)
                messages.success(request, 'Thanks for registring {}'.format(username))
                return redirect('accounts:log')
                #return HttpResponseRedirect(reverse('accounts:log'))
        else:
            print('*********COOL***********')

            print(request.POST)
            u = CorporateForm(request.POST)
            if u.is_valid():
                username = u.cleaned_data['cname']
                #phone = u.cleaned_data['']
                status = u.cleaned_data['service']
                print(u.cleaned_data)
                new_individual = u.save()
                print("helo", new_individual, username, status)
                # print(user)
                messages.success(request, 'Thanks for registring {}'.format(username))
                return redirect('accounts:log')

    '''
