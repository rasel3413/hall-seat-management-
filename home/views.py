from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreationForm,profFrom
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import *
from django.db.models import Q,Count


# Create your views here.
from .decorators import unauthenticated_user, allowed_users


def home(request):
    complaints = Complain.objects.all()
    cnt= Complain.objects.filter(is_solved=False)
    nws=News.objects.all()
    

    return render(request, 'base.html',{'complaints': complaints ,'cnt':cnt,'nws':nws})



@login_required(login_url="/home/login")
@allowed_users(allowed_role=['admin'])
def signup_view(request):
    taken_rooms = UserProfile.objects.filter(Room_No__isnull=False).values_list('Room_No__roomNo', 'Room_No__seat')
    available_rooms = RoomNumber.objects.exclude(roomNo__in=[room[0] for room in taken_rooms], seat__in=[room[1] for room in taken_rooms])

    
    if request.method == 'POST':
        form = CreationForm(request.POST)
        trop=profFrom(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
           
            group = Group.objects.get(name='helper')
            user.groups.add(group)
            profile = trop.save(commit=False)
            profile.user = user
            profile.save()
           
            login(request, user)
            return render(request, 'base.html')
        else:
            messages.error(request, 'error')

    else:

        form = CreationForm()
        trop=profFrom()

    return render(request, 'signup.html', {'form': form,'trop':trop,'Rooms':available_rooms})


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)

            return  redirect('/home')
        else:
            messages.error(request,'user name or password is incorrect')

    else:
        form=AuthenticationForm()

    return  render(request,'login.html',{'form':form})





def logut_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/home/login')


@login_required(login_url="/home/login")
@allowed_users(allowed_role=['helper'])
def user_prof(request):

    name = request.user.userprofile.name
    room = request.user.userprofile.Room_No
    phone = request.user.userprofile.Phone
    email = request.user.userprofile.Email
    pic = request.user.userprofile.profile_pic.url
    reg=request.user.userprofile.ID_NO
    batch=request.user.userprofile.Batch


    con = {'name': name, 'room': room, 'phone': phone, 'email': email, 'pic': pic,'reg':reg,'batch':batch}

    return render(request, 'user profile.html', con)



class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mydata'] = []
        return context

    def post(self, request, *args, **kwargs):
        query = request.POST.get('query')
        rquery = request.POST.get('room_query')

        if rquery:
            mydata = UserProfile.objects.filter(Room_No__roomNo__icontains=rquery)
      

        elif query:
            mydata = UserProfile.objects.filter(Q(ID_NO=query) | Q(Batch=query))
        else:
            mydata = UserProfile.objects.all()
        context = {'mydata': mydata}
        return render(request, 'search.html', context)



class ComplainCreateView(CreateView):
    model = Complain
    fields = ['complaint']
    success_url = reverse_lazy('index')
    template_name = 'complain_form.html'

    def form_valid(self, form):
        # Get the logged in user's profile
        user_profile = UserProfile.objects.get(user=self.request.user)

        # Populate the name and registration_no fields in the form
        form.instance.name = user_profile.name
        form.instance.registration_no = user_profile.ID_NO
        form.instance.room_no=user_profile.Room_No

        return super().form_valid(form)

    from django.shortcuts import redirect

class ComplaintSolveView(View):
    
    def get(self, request, *args, **kwargs):
        complaint = get_object_or_404(Complain, pk=kwargs['pk'])
        complaint.is_solved = True
        complaint.save()
        return redirect('/home')
class ComplaintListView(ListView):
    model = Complain
    template_name = 'report.html'
    context_object_name = 'complaints'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        selected_month = self.request.GET.get('month')
        if selected_month:
            queryset = queryset.filter(created_at__month=selected_month)
        return queryset
@login_required
def delete_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    user = user_profile.user
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('search')



class NewsCreateView(CreateView):
    model = News
    fields = ['news']
    template_name = 'create_news.html'
    success_url = reverse_lazy('index')

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'base.html'
    success_url = reverse_lazy('index')