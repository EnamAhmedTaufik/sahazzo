from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('LoginDonator/', views.LoginDonator),
    path('LoginOrganizor/', views.LoginOrganizor),
    path('LoginVolunteer/', views.LoginVolunteer),
    path('LoginAdmin/', views.LoginAdmin),
    path('SignupDonator/', views.SignupDonator),
    path('SignupOrganizor/', views.SignupOrganizor),
    path('SignupVolunteer/', views.SignupVolunteer),
    path('donator_profile/', views.donator_profile),
    path('organizor_profile/', views.organizor_profile),
    path('volunteer_profile/', views.volunteer_profile),
    path('admin_profile/', views.admin_profile),
    path('create_event/', views.create_event),
    path('event_details_o/', views.event_details_o),
    path('event_details_d/', views.event_details_d),
    path('event_details_v/', views.event_details_v),
    path('donateHistory/', views.donateHistory),
    path('voluntaryHistory/', views.voluntaryHistory),
    path('packages/', views.packages),
    path('manageEvents/', views.manageEvents),
    path('shopPayment/', views.shopPayment),
    path('collectFund/', views.collectFund),
    path('donatorDatabase/', views.donatorDatabase),
    path('organizorDatabase/', views.organizorDatabase),
    path('volunteerDatabase/', views.volunteerDatabase),
    path('updatePerson/<str:id>', views.updatePerson),
    path('deletePerson/<str:id>', views.deletePerson),
    path('updateEvent/<str:id>', views.updateEvent),
    path('deleteEvent/<str:id>', views.deleteEvent),
    path('paymentConfirm/<str:id>', views.paymentConfirm),
    path('collectFundConfirm/<str:id>', views.collectFundConfirm),
    
    
]
