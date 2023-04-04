from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='index'),
    path('signup',views.signup_view,name='signup'),
    path('login',views.login_view,name='login'),
    path('logut',views.logut_view,name='logut'),

    # path('complaint/<int:pk>/solve/', views.ComplaintSolveView.as_view(), name='complaint_solve'),
  
    path('profile',views.user_prof,name='profile'),
    path('search',views.SearchView.as_view(),name='search'),
    path('make_complain', views.ComplainCreateView.as_view(), name='complain'),
    path('report', views.ComplaintListView.as_view(), name='complaint_list'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),


    path('complain', views.show_complaints, name='show_complaints'),
   
    path('complain/mark_as_solved/<int:pk>/', views.MarkAsSolvedView.as_view(), name='mark_as_solved'),

 
    
    path('create_news/', views.NewsCreateView.as_view(), name='create_news'),
    path('create_events/', views.EventsCreateView.as_view(), name='create_events'),
    
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='delete_news'),
    path('events/<int:pk>/delete/', views.EventsDeleteView.as_view(), name='delete_events'),
    path('create_notice/', views.NoticeCreateView.as_view(), name='create_notice'),
    path('notice/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='delete_notice'),
    path('payment', views.PaymentPageView.as_view(), name='payment'),

    
   path('update-room/<int:pk>/', views.update_room, name='update_room'),

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)