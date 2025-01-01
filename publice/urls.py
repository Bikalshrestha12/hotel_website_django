from django.urls import path
from . views import *

urlpatterns = [
    path('check_booking/' , check_booking),
    path('', home, name='home'),
    path('hotel_list/', hotel_list, name="hotel_list"),
    path('hotel_detail/<uid>/' , hotel_detail, name="hotel_detail"),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('contact/',contact,name="contact"),
    path('contactsend/', contactsend, name="contactsend"),
    path('about/', about, name="about"),
    path('feature/', feature, name="feature"),
    path('blog/', blog, name="blog"),
    path('logout/', logout, name='logout'),
]