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
from .forms import *
from django.db.models import Q,Count


# Create your views here.
from .decorators import unauthenticated_user, allowed_users


def home(request):
    complaints = Complain.objects.all()
    cnt= Complain.objects.filter(is_solved=False)
    nws=News.objects.all()
    evnt=Events.objects.all()
    notice=Notice.objects.all()
    

    return render(request, 'base.html',{'complaints': complaints ,'cnt':cnt,'nws':nws,'evnt':evnt,'notice':notice})



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
        taken_rooms = UserProfile.objects.filter(Room_No__isnull=False).values_list('Room_No__roomNo', 'Room_No__seat')
        
        available_rooms = RoomNumber.objects.exclude(roomNo__in=[room[0] for room in taken_rooms], seat__in=[room[1] for room in taken_rooms])

        context['available_rooms'] = available_rooms
        mydata = UserProfile.objects.all()
        context['mydata'] = mydata
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
        taken_rooms = UserProfile.objects.filter(Room_No__isnull=False).values_list('Room_No__roomNo', 'Room_No__seat')
        available_rooms = RoomNumber.objects.exclude(roomNo__in=[room[0] for room in taken_rooms], seat__in=[room[1] for room in taken_rooms])


        context = {'mydata': mydata,'available_rooms':available_rooms }
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


class EventsCreateView(CreateView):
    model = Events
    fields = ['events']
    template_name = 'create_events.html'
    success_url = reverse_lazy('index')

class EventsDeleteView(DeleteView):
    model = Events
    template_name = 'base.html'
    success_url = reverse_lazy('index')


class NoticeCreateView(CreateView):
    model = Notice
    fields = ['notice']
    template_name = 'create_notice.html'
    success_url = reverse_lazy('index')

class NoticeDeleteView(DeleteView):
    model = Notice
    template_name = 'base.html'
    success_url = reverse_lazy('index')
class PaymentPageView(TemplateView):
    template_name = 'payment.html'

def show_complaints(request):
    complaints = Complain.objects.filter(is_solved=False)
    context = {
        'complaints': complaints
    }
    return render(request, 'show_Unsolved_complain.html', context)


class MarkAsSolvedView(UpdateView):
    model = Complain
    fields = []
    success_url = reverse_lazy('show_complaints')

    def form_valid(self, form):
        # set is_solved to True when the form is submitted
        self.object = form.save(commit=False)
        self.object.is_solved = True
        self.object.save()
        return redirect(self.success_url)
def update_room(request, id):
    user_profile = UserProfile.objects.get(id=id)
    room_id = request.POST.get('room')
    if room_id:
        room = RoomNumber.objects.get(id=room_id)
        user_profile.Room_No = room
        user_profile.save()
    return redirect('search')


def update_room(request, pk):
    user = UserProfile.objects.get(pk=pk)
    new_room_id = request.POST.get('room_number')
    new_room = RoomNumber.objects.get(pk=new_room_id)
    user.Room_No = new_room
    user.save()
    return redirect('search')